from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable

from typing_extensions import Self

from AoE2ScenarioParser.datasets.trigger_lists import ObjectAttribute
from AoE2ScenarioParser.scenarios.aoe2_de_scenario import AoE2DEScenario

from scenarios.lib.xs.unit_tasks import UnitTask, format_xs_value


@dataclass(frozen=True)
class _AddTask:
    task: UnitTask
    insertion_index: int | None


@dataclass(frozen=True)
class _EditTask:
    task: UnitTask
    task_indices: tuple[int, ...]


@dataclass(frozen=True)
class _RemoveTasks:
    task_indices: tuple[int, ...]


_TaskOperation = _AddTask | _EditTask | _RemoveTasks


class UnitModifier:
    def __init__(self, scenario: AoE2DEScenario, unit_id: int, source_player: int):
        self._scenario = scenario
        self._unit_id = unit_id
        self._source_player = source_player
        self._modify_unit_trigger = scenario.trigger_manager.add_trigger(f"P{source_player} Modify Unit {unit_id}")
        self._attribute_list: list[tuple[int, int, int | float, int | None]] = []
        self._task_operations: list[_TaskOperation] = []
        self._created = False

    def modify_attribute(
            self,
            attribute: int,
            operation: int,
            quantity: int | float,
            armor_attack_class: int | None = None,
    ) -> Self:
        self._ensure_not_created()
        self._attribute_list.append((attribute, operation, quantity, armor_attack_class))
        return self

    def add_task(self, task: UnitTask, insertion_index: int | None = None) -> Self:
        """Queue a task insertion, appending to the task array when no index is supplied."""

        self._ensure_not_created()
        self._validate_task(task)
        if insertion_index is not None:
            self._validate_index(insertion_index)
        self._task_operations.append(_AddTask(task, insertion_index))
        return self

    def edit_task(self, task: UnitTask, task_indices: int | Iterable[int]) -> Self:
        """Queue replacement of one existing task entry per affected task target."""

        self._ensure_not_created()
        self._validate_task(task)
        normalized_indices = self._normalize_indices(task_indices)
        if len(normalized_indices) != task.affected_objects.task_count:
            raise ValueError(
                "edit_task requires exactly one task index per affected object/class "
                f"({task.affected_objects.task_count} expected, {len(normalized_indices)} received)"
            )
        self._task_operations.append(_EditTask(task, normalized_indices))
        return self

    def remove_task(self, task_index: int) -> Self:
        """Queue removal of a single task-array entry by its zero-based index."""

        return self.remove_tasks([task_index])

    def remove_tasks(self, task_indices: Iterable[int]) -> Self:
        """Queue removals in descending order so earlier indices do not shift."""

        self._ensure_not_created()
        normalized_indices = self._normalize_indices(task_indices)
        if len(set(normalized_indices)) != len(normalized_indices):
            raise ValueError("Task indices to remove must be unique")

        if self._task_operations and isinstance(self._task_operations[-1], _RemoveTasks):
            previous_indices = self._task_operations[-1].task_indices
            combined_indices = previous_indices + normalized_indices
            if len(set(combined_indices)) != len(combined_indices):
                raise ValueError("Task indices to remove must be unique")
            self._task_operations[-1] = _RemoveTasks(tuple(sorted(combined_indices, reverse=True)))
        else:
            self._task_operations.append(_RemoveTasks(tuple(sorted(normalized_indices, reverse=True))))
        return self

    def create_triggers(self) -> Self:
        """Create modify-attribute effects and the XS task script call."""

        if self._created:
            return self

        for object_attribute, operation, quantity, attack_armor_class in self._attribute_list:
            is_attack_or_armor = object_attribute in [ObjectAttribute.ATTACK, ObjectAttribute.ARMOR]
            self._modify_unit_trigger.new_effect.modify_attribute(
                object_list_unit_id=self._unit_id,
                source_player=self._source_player,
                object_attributes=object_attribute,
                operation=operation,
                quantity=None if is_attack_or_armor else quantity,
                armour_attack_quantity=quantity if is_attack_or_armor else None,
                armour_attack_class=attack_armor_class
            )

        if self._task_operations:
            function_name = self._xs_function_name()
            self._scenario.xs_manager.add_script(xs_string=self._render_xs_function(function_name))
            self._modify_unit_trigger.new_effect.script_call(message=f"{function_name}();")

        self._created = True
        return self

    def _render_xs_function(self, function_name: str) -> str:
        unit_id = format_xs_value(self._unit_id)
        source_player = format_xs_value(self._source_player)
        body_lines: list[str] = []

        for operation in self._task_operations:
            if isinstance(operation, _RemoveTasks):
                for task_index in operation.task_indices:
                    body_lines.append(
                        f"xsModifyObjectTasks({unit_id}, {source_player}, {-task_index - 1});"
                    )
                continue

            body_lines.extend(operation.task.xs_setup_lines())
            for target_offset in range(operation.task.affected_objects.task_count):
                body_lines.extend(operation.task.affected_objects.xs_lines_for_target(target_offset))

                if isinstance(operation, _AddTask):
                    if operation.insertion_index is None:
                        index_expression = f"xsGetObjectTaskCount({unit_id}, {source_player})"
                    else:
                        index_expression = str(operation.insertion_index + target_offset)
                    edit_argument = ""
                else:
                    index_expression = str(operation.task_indices[target_offset])
                    edit_argument = ", true"

                body_lines.append(
                    f"xsModifyObjectTasks({unit_id}, {source_player}, {index_expression}{edit_argument});"
                )

        indented_body = "\n".join(f"    {line}" for line in body_lines)
        return f"void {function_name}() {{\n{indented_body}\n}}"

    def _xs_function_name(self) -> str:
        trigger_id = self._modify_unit_trigger.trigger_id
        return f"unit_modifier_tasks_{trigger_id}"

    def _ensure_not_created(self) -> None:
        if self._created:
            raise RuntimeError("UnitModifier cannot be changed after create_triggers()")

    @staticmethod
    def _validate_task(task: UnitTask) -> None:
        if not isinstance(task, UnitTask):
            raise TypeError("task must be an instance of UnitTask")

    @staticmethod
    def _validate_index(task_index: int) -> None:
        if isinstance(task_index, bool) or not isinstance(task_index, int) or task_index < 0:
            raise ValueError("Task indices must be non-negative integers")

    @classmethod
    def _normalize_indices(cls, task_indices: int | Iterable[int]) -> tuple[int, ...]:
        if isinstance(task_indices, int) and not isinstance(task_indices, bool):
            normalized_indices = (task_indices,)
        else:
            try:
                normalized_indices = tuple(task_indices)
            except TypeError as exc:
                raise TypeError("task_indices must be an integer or iterable of integers") from exc

        if not normalized_indices:
            raise ValueError("At least one task index is required")
        for task_index in normalized_indices:
            cls._validate_index(task_index)
        return normalized_indices
