from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable

from typing_extensions import Self

from AoE2ScenarioParser.datasets.trigger_lists import ObjectAttribute, Operation
from AoE2ScenarioParser.scenarios.aoe2_de_scenario import AoE2DEScenario

from scenarios.lib.xs.unit_tasks import UnitTask, XsConstant, format_xs_value


_XsAttributeValue = int | XsConstant
_XsQuantity = int | float | XsConstant


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
        self._xs_attribute_list: list[
            tuple[_XsAttributeValue, int | XsConstant, _XsQuantity, _XsAttributeValue | None]
        ] = []
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

    def modify_attribute_xs(
            self,
            attribute: _XsAttributeValue,
            operation: int | XsConstant,
            quantity: _XsQuantity,
            armor_attack_class: _XsAttributeValue | None = None,
    ) -> Self:
        """Queue an ``xsEffectAmount`` modification.

        Attack and armor amounts are emitted in chunks of at most 255. Their
        multiply and divide operations are unsupported because ``cMulAttribute``
        does not work reliably for damage classes.
        """

        self._ensure_not_created()
        self._xs_attribute_list.append((attribute, operation, quantity, armor_attack_class))
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

        if self._xs_attribute_list or self._task_operations:
            function_name = self._xs_function_name()
            self._scenario.xs_manager.add_script(xs_string=self._render_xs_function(function_name))
            self._modify_unit_trigger.new_effect.script_call(message=f"{function_name}();")

        self._created = True
        return self

    def _render_xs_function(self, function_name: str) -> str:
        unit_id = format_xs_value(self._unit_id)
        source_player = format_xs_value(self._source_player)
        body_lines: list[str] = []

        for attribute, operation, quantity, armor_attack_class in self._xs_attribute_list:
            xs_operations = self._format_xs_attribute_operation(
                attribute,
                operation,
                quantity,
                armor_attack_class,
            )
            for effect, xs_quantity in xs_operations:
                body_lines.append(
                    f"xsEffectAmount({effect}, {unit_id}, {format_xs_value(attribute)}, "
                    f"{xs_quantity}, {source_player});"
                )

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

    @staticmethod
    def _format_xs_attribute_operation(
            attribute: _XsAttributeValue,
            operation: int | XsConstant,
            quantity: _XsQuantity,
            armor_attack_class: _XsAttributeValue | None,
    ) -> list[tuple[str, str]]:
        is_attack_or_armor = attribute in (ObjectAttribute.ATTACK, ObjectAttribute.ARMOR)
        if isinstance(attribute, XsConstant):
            is_attack_or_armor = attribute.name in {"cAttack", "cArmor"}

        operation_name = operation.name if isinstance(operation, XsConstant) else None
        if operation in (0, Operation.SET) or operation_name == "cSetAttribute":
            effect = "cSetAttribute"
            normalized_operation = Operation.SET
        elif operation == Operation.ADD or operation_name == "cAddAttribute":
            effect = "cAddAttribute"
            normalized_operation = Operation.ADD
        elif operation == Operation.SUBTRACT:
            effect = "cAddAttribute"
            normalized_operation = Operation.SUBTRACT
        elif operation == Operation.MULTIPLY or operation_name == "cMulAttribute":
            effect = "cMulAttribute"
            normalized_operation = Operation.MULTIPLY
        elif operation == Operation.DIVIDE:
            effect = "cMulAttribute"
            normalized_operation = Operation.DIVIDE
        else:
            raise ValueError(f"Unsupported modify-attribute operation for XS: {operation!r}")

        if not is_attack_or_armor:
            return [(effect, UnitModifier._format_regular_xs_quantity(normalized_operation, quantity))]
        if armor_attack_class is None:
            raise ValueError("armor_attack_class is required when modifying attack or armor with XS")
        if normalized_operation in (Operation.MULTIPLY, Operation.DIVIDE):
            raise ValueError(
                "XS attack/armor modifications do not support multiply or divide reliably; "
                "use set, add, or subtract"
            )

        return UnitModifier._format_packed_xs_operations(
            normalized_operation,
            quantity,
            armor_attack_class,
        )

    @staticmethod
    def _format_regular_xs_quantity(operation: Operation, quantity: _XsQuantity) -> str:
        if isinstance(quantity, XsConstant):
            quantity_expression = format_xs_value(quantity)
            if operation == Operation.SUBTRACT:
                return f"-({quantity_expression})"
            if operation == Operation.DIVIDE:
                return f"1.0 / ({quantity_expression})"
            return quantity_expression

        if operation == Operation.SUBTRACT:
            quantity = -quantity
        elif operation == Operation.DIVIDE:
            quantity = 1 / quantity
        return format_xs_value(quantity)

    @staticmethod
    def _format_packed_xs_operations(
            operation: Operation,
            quantity: _XsQuantity,
            armor_attack_class: _XsAttributeValue,
    ) -> list[tuple[str, str]]:
        if isinstance(quantity, XsConstant):
            if not isinstance(quantity.value, (int, float)) or isinstance(quantity.value, bool):
                raise ValueError(
                    "XS attack/armor quantity constants need a numeric value so amounts over 255 "
                    "can be split safely"
                )
            numeric_quantity = quantity.value
            if 0 <= numeric_quantity <= 255:
                quantity_expression = format_xs_value(quantity)
                packed_expression = (
                    f"{format_xs_value(armor_attack_class)} * 256 + {quantity_expression}"
                )
                if operation == Operation.SUBTRACT:
                    packed_expression = f"({packed_expression}) * -1"
                effect = "cSetAttribute" if operation == Operation.SET else "cAddAttribute"
                return [(effect, packed_expression)]
            quantity = numeric_quantity

        # Validate finite floats before the chunking loop.
        format_xs_value(quantity)

        if operation == Operation.SUBTRACT:
            quantity = -quantity

        sign = -1 if quantity < 0 else 1
        remaining = abs(quantity)
        chunks: list[int | float] = []
        while remaining > 255:
            chunks.append(255 * sign)
            remaining -= 255
        if remaining or not chunks:
            chunks.append(remaining * sign)

        operations: list[tuple[str, str]] = []
        for chunk_index, chunk in enumerate(chunks):
            effect = (
                "cSetAttribute"
                if operation == Operation.SET and chunk_index == 0
                else "cAddAttribute"
            )
            if isinstance(armor_attack_class, XsConstant):
                packed_expression = (
                    f"{format_xs_value(armor_attack_class)} * 256 + "
                    f"{format_xs_value(abs(chunk))}"
                )
                if chunk < 0:
                    packed_expression = f"({packed_expression}) * -1"
            else:
                packed_quantity = armor_attack_class * 256 + abs(chunk)
                if chunk < 0:
                    packed_quantity *= -1
                packed_expression = format_xs_value(packed_quantity)
            operations.append((effect, packed_expression))
        return operations

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
