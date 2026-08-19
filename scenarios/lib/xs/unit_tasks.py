from __future__ import annotations

import math
from dataclasses import dataclass, field
from enum import IntEnum, IntFlag
from numbers import Real
from typing import ClassVar, Iterable, TypeAlias

from scenarios.lib.xs.xs_constants import XsConstantTaskAttribute, XsConstantTaskType, XsConstant


Number: TypeAlias = int | float
XsValue: TypeAlias = Number | IntEnum | IntFlag | XsConstant


def format_xs_value(value: XsValue) -> str:
    """Convert a supported Python value to a safe XS expression."""

    if isinstance(value, XsConstant):
        return value.name
    if isinstance(value, bool):
        return "1" if value else "0"
    if isinstance(value, (IntEnum, IntFlag)):
        return str(int(value))
    if not isinstance(value, Real):
        raise TypeError(f"Unsupported XS value: {value!r}")
    if isinstance(value, float) and not math.isfinite(value):
        raise ValueError("XS values must be finite")
    return repr(value)


@dataclass(frozen=True, init=False)
class TaskTargets:
    """Object IDs or object classes to which a task applies."""

    uses_object_classes: bool | None
    values: tuple[XsValue, ...]

    def __init__(self, uses_object_classes: bool | None, values: Iterable[XsValue] = ()) -> None:
        normalized_values = tuple(values)
        if uses_object_classes is None and normalized_values:
            raise ValueError("Targetless tasks cannot contain target values")
        if uses_object_classes is not None and not normalized_values:
            raise ValueError("Object ID/class targets cannot be empty")
        for value in normalized_values:
            format_xs_value(value)
        object.__setattr__(self, "uses_object_classes", uses_object_classes)
        object.__setattr__(self, "values", normalized_values)

    @classmethod
    def object_ids(cls, values: Iterable[XsValue]) -> TaskTargets:
        return cls(False, values)

    @classmethod
    def object_classes(cls, values: Iterable[XsValue]) -> TaskTargets:
        return cls(True, values)

    @classmethod
    def none(cls) -> TaskTargets:
        return cls(None)

    @property
    def task_count(self) -> int:
        return max(1, len(self.values))

    def xs_lines_for_target(self, target_offset: int) -> list[str]:
        if self.uses_object_classes is None:
            return [
                f"xsTaskAmount({XsConstantTaskAttribute.OBJECT_ID}, -1);",
                f"xsTaskAmount({XsConstantTaskAttribute.OBJECT_CLASS}, -1);",
            ]

        value = format_xs_value(self.values[target_offset])
        if self.uses_object_classes:
            return [
                f"xsTaskAmount({XsConstantTaskAttribute.OBJECT_ID}, -1);",
                f"xsTaskAmount({XsConstantTaskAttribute.OBJECT_CLASS}, {value});",
            ]
        return [
            f"xsTaskAmount({XsConstantTaskAttribute.OBJECT_ID}, {value});",
            f"xsTaskAmount({XsConstantTaskAttribute.OBJECT_CLASS}, -1);",
        ]


class TargetOwnership(IntEnum):
    ALL = 0
    OWN = 1
    NEUTRAL_AND_ENEMY = 2
    GAIA = 3
    GAIA_OWN_AND_ALLY = 4
    GAIA_NEUTRAL_AND_ENEMY = 5
    ALL_EXCEPT_OWN = 6


class AuraFlags(IntFlag):
    ADD = 0
    MULTIPLY = 1
    CIRCULAR = 2
    VISIBLE_RANGE = 4
    TEMPORARY = 8
    APPLY_ON_ACTIVATION_ONLY = 16
    TRANSLUCENT_RANGE = 32


class StingerFlags(IntFlag):
    ADD = 0
    MULTIPLY = 1
    DO_NOT_STACK = 2


class StingerRecipient(IntEnum):
    ATTACKER = 0
    TARGET = 1


class HPComparisonTarget(IntEnum):
    OWN_HP = 0
    CURRENT_TARGET_HP = 1


class RefundRecipient(IntEnum):
    OWNER = 0
    KILLER = 1


class RefundValueMode(IntEnum):
    FLAT_VALUE = 0
    FRACTION_OF_ASSOCIATED_COST = 1


class HPThresholdMode(IntEnum):
    ABSOLUTE_HP = 0
    CURRENT_HP_MULTIPLIER = 1


class FlyOwnershipMode(IntEnum):
    GAIA_ONLY = 1


class ResourceGenerationMode(IntEnum):
    PASSIVE = 2


class LootMode(IntEnum):
    GAIN_ATTRIBUTES = 1


@dataclass(frozen=True, kw_only=True)
class UnitTask:
    """Base model for a task stored in a unit's task array."""

    # Objects or object classes to which this task applies. Use TaskTargets.none()
    # for tasks that do not select a target type.
    affected_objects: TaskTargets = field(default_factory=TaskTargets.none)

    XS_TASK_TYPE: ClassVar[XsConstant]

    def __post_init__(self) -> None:
        if not isinstance(self.affected_objects, TaskTargets):
            raise TypeError("affected_objects must be a TaskTargets instance")
        for _, value in self.task_attributes():
            format_xs_value(value)

    def task_attributes(self) -> tuple[tuple[str, XsValue], ...]:
        raise NotImplementedError

    def xs_setup_lines(self) -> list[str]:
        lines = ["xsResetTaskAmount();"]
        for attribute, value in self.task_attributes():
            lines.append(f"xsTaskAmount({attribute}, {format_xs_value(value)});")
        lines.append(f"xsTaskAmount({XsConstantTaskAttribute.TASK_TYPE}, {self.XS_TASK_TYPE});")
        return lines


@dataclass(frozen=True, kw_only=True)
class GarrisonTask(UnitTask):
    """Allow the modified unit to garrison into selected objects or classes.

    Args:
        affected_objects: Optional target object IDs or classes. Defaults to no
            target; normally set with ``TaskTargets.object_ids(...)`` or
            ``TaskTargets.object_classes(...)``.
        garrison_range: Optional range at which the unit can enter the target.
            Defaults to -1.
        target_ownership: Optional ownership filter. Use a member of
            ``GarrisonTask.Ownership``. Defaults to -1.
    """

    XS_TASK_TYPE: ClassVar[XsConstant] = XsConstantTaskType.GARRISON
    Ownership: ClassVar[type[TargetOwnership]] = TargetOwnership

    # Range at which the unit can enter the target object.
    garrison_range: XsValue = -1
    # Ownership relationships that are valid targets; see GarrisonTask.Ownership.
    target_ownership: TargetOwnership | int = -1

    def task_attributes(self) -> tuple[tuple[str, XsValue], ...]:
        return (
            (XsConstantTaskAttribute.WORK_RANGE, self.garrison_range),
            (XsConstantTaskAttribute.OWNER_TYPE, self.target_ownership),
        )


@dataclass(frozen=True, kw_only=True)
class FlyTask(UnitTask):
    """Configure autonomous flying/roaming behavior.

    Args:
        affected_objects: Optional and normally left as ``TaskTargets.none()``.
        roaming_speed_multiplier: Optional movement-speed multiplier while
            roaming. Defaults to -1.
        unit_id_to_avoid: Optional unit ID that the roaming unit avoids.
            Defaults to -1.
        minimum_avoidance_distance: Optional distance maintained from the
            avoided unit. Defaults to -1.
        direction_change_pause_seconds: Optional idle time when changing
            direction. Defaults to -1.
        gaia_only: Optional restriction. Use
            ``FlyTask.OwnershipMode.GAIA_ONLY`` to restrict roaming to Gaia.
            Defaults to -1.
        terrain_table: Optional permitted terrain table. -1 uses the unit's
            own terrain table.
        moving_graphic_id: Optional first randomly selected movement graphic.
            Defaults to -1.
        proceeding_graphic_id: Optional second movement graphic. Defaults to -1.
        working_graphic_id: Optional third movement graphic. Defaults to -1.
        maximum_distance_from_start: Optional roaming limit from the starting
            position. Use 0 for no limit. Defaults to -1.
    """

    XS_TASK_TYPE: ClassVar[XsConstant] = XsConstantTaskType.FLY
    OwnershipMode: ClassVar[type[FlyOwnershipMode]] = FlyOwnershipMode

    # Multiplier applied to movement speed while the unit roams.
    roaming_speed_multiplier: XsValue = -1
    # Unit ID that the roaming unit tries to avoid.
    unit_id_to_avoid: XsValue = -1
    # Minimum distance maintained from the avoided unit.
    minimum_avoidance_distance: XsValue = -1
    # Seconds spent idle whenever the unit changes roaming direction.
    direction_change_pause_seconds: XsValue = -1
    # Set to FlyTask.OwnershipMode.GAIA_ONLY to restrict roaming to Gaia units.
    gaia_only: FlyOwnershipMode | int = -1
    # Terrain table allowed for roaming; -1 uses the unit's own terrain table.
    terrain_table: XsValue = -1
    # First graphic randomly used while moving.
    moving_graphic_id: XsValue = -1
    # Second graphic randomly used while moving.
    proceeding_graphic_id: XsValue = -1
    # Third graphic randomly used while moving.
    working_graphic_id: XsValue = -1
    # Maximum distance from the starting point; 0 removes the limit.
    maximum_distance_from_start: XsValue = -1

    def task_attributes(self) -> tuple[tuple[str, XsValue], ...]:
        return (
            (XsConstantTaskAttribute.WORK_VALUE_1, self.roaming_speed_multiplier),
            (XsConstantTaskAttribute.WORK_VALUE_2, self.unit_id_to_avoid),
            (XsConstantTaskAttribute.WORK_RANGE, self.minimum_avoidance_distance),
            (XsConstantTaskAttribute.SEARCH_WAIT_TIME, self.direction_change_pause_seconds),
            (XsConstantTaskAttribute.COMBAT_LEVEL_FLAG, self.gaia_only),
            (XsConstantTaskAttribute.TERRAIN, self.terrain_table),
            (XsConstantTaskAttribute.MOVING_GRAPHIC, self.moving_graphic_id),
            (XsConstantTaskAttribute.PROCEEDING_GRAPHIC, self.proceeding_graphic_id),
            (XsConstantTaskAttribute.WORKING_GRAPHIC, self.working_graphic_id),
            (XsConstantTaskAttribute.CARRY_CHECK, self.maximum_distance_from_start),
        )


@dataclass(frozen=True, kw_only=True)
class BuildTask(UnitTask):
    """Allow the modified unit to build selected buildings.

    Args:
        affected_objects: Optional building IDs or classes to build. Defaults
            to no target.
        work_rate_multiplier: Optional multiplier applied to Work Rate.
            Defaults to -1.
        build_range: Optional range at which the unit builds. Defaults to -1.
        proceeding_graphic_id: Optional primary building graphic. Defaults to -1.
        working_graphic_id: Optional secondary building graphic. Defaults to -1.
        build_sound_id: Optional sound played while building. Defaults to -1.

    Note:
        Military builders also require the appropriate Traits and Trait Piece
        object attributes to be configured separately.
    """

    XS_TASK_TYPE: ClassVar[XsConstant] = XsConstantTaskType.BUILD

    # Multiplier applied to the builder's Work Rate object attribute.
    work_rate_multiplier: XsValue = -1
    # Range at which the unit can build.
    build_range: XsValue = -1
    # Graphic used while building the primary building.
    proceeding_graphic_id: XsValue = -1
    # Graphic used while building a secondary building.
    working_graphic_id: XsValue = -1
    # Sound ID played while the unit builds.
    build_sound_id: XsValue = -1

    def task_attributes(self) -> tuple[tuple[str, XsValue], ...]:
        return (
            (XsConstantTaskAttribute.WORK_VALUE_1, self.work_rate_multiplier),
            (XsConstantTaskAttribute.WORK_RANGE, self.build_range),
            (XsConstantTaskAttribute.PROCEEDING_GRAPHIC, self.proceeding_graphic_id),
            (XsConstantTaskAttribute.WORKING_GRAPHIC, self.working_graphic_id),
            (XsConstantTaskAttribute.DEPOSIT_SOUND, self.build_sound_id),
        )


@dataclass(frozen=True, kw_only=True)
class ConvertTask(UnitTask):
    """Allow the modified unit to convert selected objects or classes.

    Args:
        affected_objects: Optional target object IDs or classes. Defaults to no
            target.
        minimum_conversion_seconds: Optional minimum conversion time.
            Defaults to -1.
        maximum_conversion_seconds: Optional maximum conversion time.
            Defaults to -1.
        conversion_range: Optional range; positive values override the object's
            conversion range. Defaults to -1.
        conversion_chance_resource: Optional resource whose value modifies
            conversion chance. Defaults to -1.
        enabling_resource: Optional resource that must be greater than zero to
            enable conversion. Defaults to -1.
    """

    XS_TASK_TYPE: ClassVar[XsConstant] = XsConstantTaskType.CONVERT

    # Minimum time in seconds required for a conversion attempt.
    minimum_conversion_seconds: XsValue = -1
    # Maximum time in seconds required for a conversion attempt.
    maximum_conversion_seconds: XsValue = -1
    # Conversion range; a positive value overrides the object's range attribute.
    conversion_range: XsValue = -1
    # Resource whose current value modifies conversion chance.
    conversion_chance_resource: XsValue = -1
    # Resource that must have a value greater than zero to enable conversion.
    enabling_resource: XsValue = -1

    def task_attributes(self) -> tuple[tuple[str, XsValue], ...]:
        return (
            (XsConstantTaskAttribute.WORK_VALUE_1, self.minimum_conversion_seconds),
            (XsConstantTaskAttribute.WORK_VALUE_2, self.maximum_conversion_seconds),
            (XsConstantTaskAttribute.WORK_RANGE, self.conversion_range),
            (XsConstantTaskAttribute.PRODUCTIVITY_RESOURCE, self.conversion_chance_resource),
            (XsConstantTaskAttribute.UNUSED_RESOURCE, self.enabling_resource),
        )


@dataclass(frozen=True, kw_only=True)
class HealTask(UnitTask):
    """Give the modified unit a healing task.

    Args:
        affected_objects: Optional and normally left as ``TaskTargets.none()``.
        work_rate_multiplier: Optional multiplier applied to Work Rate for
            healing. Defaults to -1.
        healing_graphic_id: Optional graphic used while healing. Defaults to -1.
    """

    XS_TASK_TYPE: ClassVar[XsConstant] = XsConstantTaskType.HEAL

    # Multiplier applied to the healer's Work Rate object attribute.
    work_rate_multiplier: XsValue = -1
    # Graphic used while the unit heals another unit.
    healing_graphic_id: XsValue = -1

    def task_attributes(self) -> tuple[tuple[str, XsValue], ...]:
        return (
            (XsConstantTaskAttribute.WORK_VALUE_1, self.work_rate_multiplier),
            (XsConstantTaskAttribute.PROCEEDING_GRAPHIC, self.healing_graphic_id),
        )


@dataclass(frozen=True, kw_only=True)
class RepairTask(UnitTask):
    """Allow the modified unit to repair selected objects or classes.

    Args:
        affected_objects: Optional repairable object IDs or classes. No target
            means all repairable objects. Defaults to no target.
        work_rate_multiplier: Optional multiplier applied to Work Rate for
            repairing. Defaults to -1.
        proceeding_graphic_id: Optional primary repair graphic. Defaults to -1.
        working_graphic_id: Optional secondary repair graphic. Defaults to -1.
        repair_sound_id: Optional sound played while repairing. Defaults to -1.
    """

    XS_TASK_TYPE: ClassVar[XsConstant] = XsConstantTaskType.REPAIR

    # Multiplier applied to the repairer's Work Rate object attribute.
    work_rate_multiplier: XsValue = -1
    # Graphic used while the unit repairs.
    proceeding_graphic_id: XsValue = -1
    # Secondary repair graphic; the game may not require it.
    working_graphic_id: XsValue = -1
    # Sound ID played while the unit repairs.
    repair_sound_id: XsValue = -1

    def task_attributes(self) -> tuple[tuple[str, XsValue], ...]:
        return (
            (XsConstantTaskAttribute.WORK_VALUE_1, self.work_rate_multiplier),
            (XsConstantTaskAttribute.PROCEEDING_GRAPHIC, self.proceeding_graphic_id),
            (XsConstantTaskAttribute.WORKING_GRAPHIC, self.working_graphic_id),
            (XsConstantTaskAttribute.DEPOSIT_SOUND, self.repair_sound_id),
        )


@dataclass(frozen=True, kw_only=True)
class PickupUnitTask(UnitTask):
    """Pick up a target object and transform into another unit.

    Args:
        transformed_unit_id: Required unit ID into which the carrier transforms
            after pickup.
        affected_objects: Optional object IDs or classes that may be picked up.
            Defaults to no target. The game currently appears to support relics
            only and may ignore this filter.
    """

    XS_TASK_TYPE: ClassVar[XsConstant] = XsConstantTaskType.PICKUP_UNIT

    # Unit ID into which the carrier transforms after picking up the object.
    transformed_unit_id: XsValue

    def task_attributes(self) -> tuple[tuple[str, XsValue], ...]:
        return ((XsConstantTaskAttribute.WORK_VALUE_1, self.transformed_unit_id),)


@dataclass(frozen=True, kw_only=True)
class DepositUnitTask(UnitTask):
    """Deposit a carried object and transform into another unit.

    Args:
        transformed_unit_id: Required unit ID into which the carrier transforms
            after depositing its carried object.
        affected_objects: Optional destination building IDs or classes.
            Defaults to no target. The game currently appears to support relics
            only.
    """

    XS_TASK_TYPE: ClassVar[XsConstant] = XsConstantTaskType.DEPOSIT_UNIT

    # Unit ID into which the carrier transforms after depositing the object.
    transformed_unit_id: XsValue

    def task_attributes(self) -> tuple[tuple[str, XsValue], ...]:
        return ((XsConstantTaskAttribute.WORK_VALUE_1, self.transformed_unit_id),)


@dataclass(frozen=True, kw_only=True)
class GenerateResourcesTask(UnitTask):
    """Generate a player resource while attacking or idling.

    Args:
        resource_amount: Required base amount granted per activation.
        output_resource: Required resource type to grant.
        productivity_resource: Required resource whose positive current value
            multiplies ``resource_amount``.
        affected_objects: Optional attacked object IDs or classes that activate
            generation. Defaults to no target.
        passive_generation_flag: Optional mode. Use
            ``GenerateResourcesTask.Mode.PASSIVE`` for passive generation on
            units. Buildings generate passively automatically. Defaults to -1.
    """

    XS_TASK_TYPE: ClassVar[XsConstant] = XsConstantTaskType.GENERATE_RESOURCES
    Mode: ClassVar[type[ResourceGenerationMode]] = ResourceGenerationMode

    # Base amount of the output resource granted per activation.
    resource_amount: XsValue
    # Resource type that the task grants.
    output_resource: XsValue
    # Resource whose positive value multiplies resource_amount; required by the task.
    productivity_resource: XsValue
    # Set to GenerateResourcesTask.Mode.PASSIVE for passive generation on units.
    passive_generation_flag: ResourceGenerationMode | int = -1

    def task_attributes(self) -> tuple[tuple[str, XsValue], ...]:
        return (
            (XsConstantTaskAttribute.WORK_VALUE_1, self.resource_amount),
            (XsConstantTaskAttribute.COMBAT_LEVEL_FLAG, self.passive_generation_flag),
            (XsConstantTaskAttribute.PRODUCTIVITY_RESOURCE, self.productivity_resource),
            (XsConstantTaskAttribute.RESOURCE_OUT, self.output_resource),
        )


@dataclass(frozen=True, kw_only=True)
class MovementDamageTask(UnitTask):
    """Damage or heal surrounding units while the modified unit moves.

    Args:
        damage_per_tick: Required HP removed per tick. Use a negative value to
            heal instead; healing can exceed maximum HP.
        tick_interval_seconds: Required time between applications, expressed in
            fractions of a second.
        effect_range: Required range around the moving unit in which the effect
            is applied.
        affected_objects: Optional and normally left as ``TaskTargets.none()``.
    """

    XS_TASK_TYPE: ClassVar[XsConstant] = XsConstantTaskType.MOVEMENT_DAMAGE

    # HP removed per tick; negative values heal and can exceed maximum HP.
    damage_per_tick: XsValue
    # Time in seconds between damage/healing ticks.
    tick_interval_seconds: XsValue
    # Range around the moving unit affected by each tick.
    effect_range: XsValue

    def task_attributes(self) -> tuple[tuple[str, XsValue], ...]:
        return (
            (XsConstantTaskAttribute.WORK_VALUE_1, self.damage_per_tick),
            (XsConstantTaskAttribute.WORK_VALUE_2, self.tick_interval_seconds),
            (XsConstantTaskAttribute.WORK_RANGE, self.effect_range)
        )


@dataclass(frozen=True, kw_only=True)
class LootTask(UnitTask):
    """Gain resources or attributes after kills and conversions.

    Args:
        affected_objects: Optional killed/converted object IDs or classes that
            activate the task. No target affects all eligible objects.
        resource_amount: Optional resources granted per activation. Defaults to -1.
        restricted_player_id: Optional victim-player restriction. 0 accepts all
            players; a positive value accepts only that player. Defaults to -1.
        maximum_trigger_count: Optional per-unit activation cap. Defaults to -1.
        modified_attribute: Optional object attribute changed in attribute-gain
            mode. Defaults to -1.
        gain_attributes_flag: Optional mode. Use
            ``LootTask.Mode.GAIN_ATTRIBUTES`` to gain attributes. Defaults to -1.
        technology_id_resource: Optional resource whose value identifies a
            technology researched on activation. Defaults to -1.
        activation_multiplier_resource_or_technology: Optional positive resource
            ID used as an activation condition and resource multiplier; a
            negative value represents a required technology ID. Defaults to -1.
        output_resource: Optional resource type granted in resource mode.
            Defaults to -1.
        secondary_technology_id_resource: Optional second resource whose value
            identifies a technology researched on activation. Defaults to -1.
        gain_graphic_id: Optional graphic played for an attribute gain.
            Defaults to -1.
        shared_cap_id: Optional ID shared by Loot tasks that use one activation
            cap. Defaults to -1.
        attribute_gain_amount: Optional value added to ``modified_attribute``.
            Defaults to -1.
    """

    XS_TASK_TYPE: ClassVar[XsConstant] = XsConstantTaskType.LOOT
    Mode: ClassVar[type[LootMode]] = LootMode

    # Amount of resources granted when the task activates.
    resource_amount: XsValue = -1
    # 0 applies to all players; a positive ID restricts victims to that player.
    restricted_player_id: XsValue = -1
    # Maximum number of times this unit can activate the task.
    maximum_trigger_count: XsValue = -1
    # Object attribute changed when the task is configured to gain attributes.
    modified_attribute: XsValue = -1
    # Set to LootTask.Mode.GAIN_ATTRIBUTES to modify an attribute instead of resources.
    gain_attributes_flag: LootMode | int = -1
    # Resource whose value identifies a technology to research on activation.
    technology_id_resource: XsValue = -1
    # Positive: activation/multiplier resource. Negative: required technology ID.
    activation_multiplier_resource_or_technology: XsValue = -1
    # Resource type granted by a resource-gain task.
    output_resource: XsValue = -1
    # Second resource whose value identifies a technology to research.
    secondary_technology_id_resource: XsValue = -1
    # Graphic played when an attribute is gained.
    gain_graphic_id: XsValue = -1
    # ID shared by Loot tasks that should count toward the same activation cap.
    shared_cap_id: XsValue = -1
    # Amount added to modified_attribute in attribute-gain mode.
    attribute_gain_amount: XsValue = -1

    def task_attributes(self) -> tuple[tuple[str, XsValue], ...]:
        return (
            (XsConstantTaskAttribute.WORK_VALUE_1, self.resource_amount),
            (XsConstantTaskAttribute.WORK_RANGE, self.restricted_player_id),
            (XsConstantTaskAttribute.WORK_FLAG_2, self.maximum_trigger_count),
            (XsConstantTaskAttribute.SEARCH_WAIT_TIME, self.modified_attribute),
            (XsConstantTaskAttribute.COMBAT_LEVEL_FLAG, self.gain_attributes_flag),
            (XsConstantTaskAttribute.RESOURCE_IN, self.technology_id_resource),
            (XsConstantTaskAttribute.PRODUCTIVITY_RESOURCE, self.activation_multiplier_resource_or_technology),
            (XsConstantTaskAttribute.RESOURCE_OUT, self.output_resource),
            (XsConstantTaskAttribute.UNUSED_RESOURCE, self.secondary_technology_id_resource),
            (XsConstantTaskAttribute.PROCEEDING_GRAPHIC, self.gain_graphic_id),
            (XsConstantTaskAttribute.CARRY_CHECK, self.shared_cap_id),
            (XsConstantTaskAttribute.GATHER_TYPE, self.attribute_gain_amount),
        )


@dataclass(frozen=True, kw_only=True)
class AuraTask(UnitTask):
    """Modify attributes of selected nearby objects or classes.

    Args:
        modifier_value: Required value added to or multiplied with the selected
            attribute.
        effect_range: Required aura radius/square range.
        modified_attribute: Required object attribute ID modified by the aura.
        affected_objects: Optional affected object IDs or classes. Defaults to
            no target.
        minimum_units_in_range: Optional eligible-unit count required to
            activate the aura. Defaults to -1.
        flags: Optional behavior bitfield. Combine members of ``AuraTask.Flags``
            to multiply, make the range circular/visible, or configure temporary
            behavior. Defaults to -1.
        target_ownership: Optional ownership filter from ``AuraTask.Ownership``.
            Defaults to -1.
        affected_unit_graphic_id: Optional graphic displayed over affected units.
            Defaults to -1.
        indicator_short_tooltip_id: Optional short-tooltip string ID for the UI
            indicator. Defaults to -1.
        indicator_long_tooltip_id: Optional long-tooltip string ID for the UI
            indicator. Defaults to -1.
        indicator_icon_id: Optional UI indicator icon ID. Defaults to -1.
        activation_resource: Optional resource that must be greater than zero
            for activation. Defaults to -1.

    Note:
        The owning unit also needs the Aura bit in its Combat Ability object
        attribute; temporary auras need the corresponding charge attributes.
    """

    XS_TASK_TYPE: ClassVar[XsConstant] = XsConstantTaskType.AURA
    Flags: ClassVar[type[AuraFlags]] = AuraFlags
    Ownership: ClassVar[type[TargetOwnership]] = TargetOwnership

    # Value added to, or multiplied with, the selected object attribute.
    modifier_value: XsValue
    # Radius or square range covered by the aura.
    effect_range: XsValue
    # Object attribute ID modified on affected units.
    modified_attribute: XsValue
    # Minimum number of eligible units in range before the aura activates.
    minimum_units_in_range: XsValue = -1
    # Aura behavior bitfield; combine members of AuraTask.Flags.
    flags: AuraFlags | int = -1
    # Ownership relationships that the aura can affect; see AuraTask.Ownership.
    target_ownership: TargetOwnership | int = -1
    # Graphic displayed over units receiving the aura.
    affected_unit_graphic_id: XsValue = -1
    # String ID used as the aura indicator's short tooltip.
    indicator_short_tooltip_id: XsValue = -1
    # String ID used as the aura indicator's long tooltip.
    indicator_long_tooltip_id: XsValue = -1
    # UI icon ID used by the aura range indicator.
    indicator_icon_id: XsValue = -1
    # Resource that must be greater than zero for the aura to activate.
    activation_resource: XsValue = -1

    def task_attributes(self) -> tuple[tuple[str, XsValue], ...]:
        return (
            (XsConstantTaskAttribute.WORK_VALUE_1, self.modifier_value),
            (XsConstantTaskAttribute.WORK_VALUE_2, self.minimum_units_in_range),
            (XsConstantTaskAttribute.WORK_RANGE, self.effect_range),
            (XsConstantTaskAttribute.SEARCH_WAIT_TIME, self.modified_attribute),
            (XsConstantTaskAttribute.COMBAT_LEVEL_FLAG, self.flags),
            (XsConstantTaskAttribute.OWNER_TYPE, self.target_ownership),
            (XsConstantTaskAttribute.PROCEEDING_GRAPHIC, self.affected_unit_graphic_id),
            (XsConstantTaskAttribute.GATHERING_SOUND, self.indicator_short_tooltip_id),
            (XsConstantTaskAttribute.DEPOSIT_SOUND, self.indicator_long_tooltip_id),
            (XsConstantTaskAttribute.GATHER_TYPE, self.indicator_icon_id),
            (XsConstantTaskAttribute.ENABLED, self.activation_resource),
        )


@dataclass(frozen=True, kw_only=True)
class AdditionalSpawnTask(UnitTask):
    """Spawn additional units whenever the modified unit is trained.

    Args:
        spawned_unit_id: Required unit ID spawned alongside the trained unit.
        spawn_count: Required base number of additional units to spawn.
        affected_objects: Optional and normally left as ``TaskTargets.none()``.
        enabling_resource: Optional resource that must be greater than zero for
            activation. Defaults to -1.
        bonus_count_resource: Optional resource whose current value is added to
            ``spawn_count``. Defaults to -1.
    """

    XS_TASK_TYPE: ClassVar[XsConstant] = XsConstantTaskType.EXTRA_SPAWN

    # Unit ID spawned alongside the trained unit.
    spawned_unit_id: XsValue
    # Base number of additional units to spawn.
    spawn_count: XsValue
    # Resource that must be greater than zero for the task to activate.
    enabling_resource: XsValue = -1
    # Resource whose value is added to spawn_count.
    bonus_count_resource: XsValue = -1

    def task_attributes(self) -> tuple[tuple[str, XsValue], ...]:
        return (
            (XsConstantTaskAttribute.WORK_VALUE_1, self.spawned_unit_id),
            (XsConstantTaskAttribute.WORK_VALUE_2, self.spawn_count),
            (XsConstantTaskAttribute.RESOURCE_IN, self.enabling_resource),
            (XsConstantTaskAttribute.PRODUCTIVITY_RESOURCE, self.bonus_count_resource),
        )


@dataclass(frozen=True, kw_only=True)
class StingerTask(UnitTask):
    """Temporarily or permanently modify an attacker or attack target.

    Args:
        modifier_value: Required value added to or multiplied with the selected
            attribute.
        effect_duration_seconds: Required duration in seconds. A negative value
            makes the effect permanent.
        modified_attribute: Required object attribute ID modified by the task.
        affected_objects: Optional object IDs or classes eligible for the
            stinger. Defaults to no target.
        recipient: Optional recipient from ``StingerTask.Recipient``: attacker
            or attacked target. Defaults to -1.
        flags: Optional behavior bitfield composed from ``StingerTask.Flags``.
            Defaults to -1.
        target_ownership: Optional ownership filter from
            ``StingerTask.Ownership``. Defaults to -1.
        activation_resource: Optional resource that must be greater than zero
            for activation. Defaults to -1.

    Note:
        The owning unit also needs the Stinger bit in its Combat Ability object
        attribute.
    """

    XS_TASK_TYPE: ClassVar[XsConstant] = XsConstantTaskType.STINGER
    Flags: ClassVar[type[StingerFlags]] = StingerFlags
    Recipient: ClassVar[type[StingerRecipient]] = StingerRecipient
    Ownership: ClassVar[type[TargetOwnership]] = TargetOwnership

    # Value added to, or multiplied with, the selected object attribute.
    modifier_value: XsValue
    # Effect duration in seconds; a negative value makes it permanent.
    effect_duration_seconds: XsValue
    # Object attribute ID modified by the stinger.
    modified_attribute: XsValue
    # Whether the attacker or attacked target receives the effect.
    recipient: StingerRecipient | int = -1
    # Stinger behavior bitfield; combine members of StingerTask.Flags.
    flags: StingerFlags | int = -1
    # Ownership relationships that the stinger can affect.
    target_ownership: TargetOwnership | int = -1
    # Resource that must be greater than zero for the stinger to activate.
    activation_resource: XsValue = -1

    def task_attributes(self) -> tuple[tuple[str, XsValue], ...]:
        return (
            (XsConstantTaskAttribute.WORK_VALUE_1, self.modifier_value),
            (XsConstantTaskAttribute.WORK_VALUE_2, self.effect_duration_seconds),
            (XsConstantTaskAttribute.WORK_RANGE, self.recipient),
            (XsConstantTaskAttribute.SEARCH_WAIT_TIME, self.modified_attribute),
            (XsConstantTaskAttribute.COMBAT_LEVEL_FLAG, self.flags),
            (XsConstantTaskAttribute.OWNER_TYPE, self.target_ownership),
            (XsConstantTaskAttribute.PRODUCTIVITY_RESOURCE, self.activation_resource),
        )


@dataclass(frozen=True, kw_only=True)
class HPTransformationTask(UnitTask):
    """Transform the modified unit when an HP threshold is crossed.

    Args:
        transformed_unit_id: Required destination unit ID.
        hp_threshold: Required threshold. Positive values transform above the
            threshold; negative values transform below their absolute value.
        affected_objects: Optional and normally left as ``TaskTargets.none()``.
        threshold_mode: Optional threshold interpretation from
            ``HPTransformationTask.ThresholdMode``. Defaults to -1.
        activation_resource_or_technology: Optional positive resource ID that
            must have a value greater than zero, or negative required technology
            ID. Defaults to -1.
        threshold_bonus_resource: Optional resource whose value is added to
            ``hp_threshold``. Defaults to -1.
        transformation_graphic_id: Optional graphic played on transformation.
            Defaults to -1.
    """

    XS_TASK_TYPE: ClassVar[XsConstant] = XsConstantTaskType.HP_TRANSFORM
    ThresholdMode: ClassVar[type[HPThresholdMode]] = HPThresholdMode

    # Unit ID into which the current unit transforms.
    transformed_unit_id: XsValue
    # Positive transforms above the threshold; negative transforms below its absolute value.
    hp_threshold: XsValue
    # Absolute-HP or current-HP-multiplier interpretation of hp_threshold.
    threshold_mode: HPThresholdMode | int = -1
    # Positive: required resource. Negative: absolute value is a required technology ID.
    activation_resource_or_technology: XsValue = -1
    # Resource whose current value is added to hp_threshold.
    threshold_bonus_resource: XsValue = -1
    # Graphic played when the transformation occurs.
    transformation_graphic_id: XsValue = -1

    def task_attributes(self) -> tuple[tuple[str, XsValue], ...]:
        return (
            (XsConstantTaskAttribute.WORK_VALUE_1, self.transformed_unit_id),
            (XsConstantTaskAttribute.WORK_VALUE_2, self.hp_threshold),
            (XsConstantTaskAttribute.COMBAT_LEVEL_FLAG, self.threshold_mode),
            (XsConstantTaskAttribute.PRODUCTIVITY_RESOURCE, self.activation_resource_or_technology),
            (XsConstantTaskAttribute.RESOURCE_OUT, self.threshold_bonus_resource),
            (XsConstantTaskAttribute.PROCEEDING_GRAPHIC, self.transformation_graphic_id),
        )


@dataclass(frozen=True, kw_only=True)
class AmphibiousTask(UnitTask):
    """Change speed and graphics while the unit is on selected terrain.

    Args:
        terrain_or_terrain_type: Required activation terrain. Non-negative values
            are terrain IDs; negative values are combinable terrain-type bits.
        affected_objects: Optional and normally left as ``TaskTargets.none()``.
        movement_speed_multiplier: Optional movement-speed multiplier.
            Defaults to -1.
        attack_speed_multiplier: Optional attack-speed multiplier. Defaults to -1.
        walking_graphic_id: Optional walking graphic. Defaults to -1.
        attack_graphic_id: Optional attack graphic. Defaults to -1.
        running_graphic_id: Optional running graphic. Defaults to -1.
        idle_graphic_id: Optional idle graphic. Defaults to -1.
        dying_graphic_id: Optional dying graphic. Defaults to -1.
        undead_graphic_id: Optional undead/corpse graphic. Defaults to -1.
    """

    XS_TASK_TYPE: ClassVar[XsConstant] = XsConstantTaskType.AMPHIBIOUS

    # Non-negative terrain ID, or negative terrain-type bitfield, that activates the task.
    terrain_or_terrain_type: XsValue
    # Movement-speed multiplier used on the selected terrain.
    movement_speed_multiplier: XsValue = -1
    # Attack-speed multiplier used on the selected terrain.
    attack_speed_multiplier: XsValue = -1
    # Walking graphic used on the selected terrain.
    walking_graphic_id: XsValue = -1
    # Attack graphic used on the selected terrain.
    attack_graphic_id: XsValue = -1
    # Running graphic used on the selected terrain.
    running_graphic_id: XsValue = -1
    # Idle graphic used on the selected terrain.
    idle_graphic_id: XsValue = -1
    # Dying graphic used on the selected terrain.
    dying_graphic_id: XsValue = -1
    # Undead/corpse graphic used on the selected terrain.
    undead_graphic_id: XsValue = -1

    def task_attributes(self) -> tuple[tuple[str, XsValue], ...]:
        return (
            (XsConstantTaskAttribute.WORK_VALUE_1, self.movement_speed_multiplier),
            (XsConstantTaskAttribute.WORK_VALUE_2, self.attack_speed_multiplier),
            (XsConstantTaskAttribute.TERRAIN, self.terrain_or_terrain_type),
            (XsConstantTaskAttribute.MOVING_GRAPHIC, self.walking_graphic_id),
            (XsConstantTaskAttribute.PROCEEDING_GRAPHIC, self.attack_graphic_id),
            (XsConstantTaskAttribute.WORKING_GRAPHIC, self.running_graphic_id),
            (XsConstantTaskAttribute.CARRYING_GRAPHIC, self.idle_graphic_id),
            (XsConstantTaskAttribute.GATHERING_SOUND, self.dying_graphic_id),
            (XsConstantTaskAttribute.DEPOSIT_SOUND, self.undead_graphic_id),
        )


@dataclass(frozen=True, kw_only=True)
class HPDamageModifierTask(UnitTask):
    """Modify an attribute according to missing HP percentage.

    Args:
        modifier_value: Required value added for each missing-HP threshold.
        hp_percentage_threshold: Required missing-HP percentage interval.
        modified_attribute: Required object attribute ID modified by the task.
        affected_objects: Optional and normally left as ``TaskTargets.none()``.
        comparison_target: Optional HP source from
            ``HPDamageModifierTask.ComparisonTarget``. Defaults to -1.
    """

    XS_TASK_TYPE: ClassVar[XsConstant] = XsConstantTaskType.HP_MODIFIER
    ComparisonTarget: ClassVar[type[HPComparisonTarget]] = HPComparisonTarget

    # Attribute value added for each missing-HP threshold reached.
    modifier_value: XsValue
    # Missing-HP percentage interval that activates another modifier increment.
    hp_percentage_threshold: XsValue
    # Object attribute ID modified by the task.
    modified_attribute: XsValue
    # Whether to inspect this unit's HP or its current target's HP.
    comparison_target: HPComparisonTarget | int = -1

    def task_attributes(self) -> tuple[tuple[str, XsValue], ...]:
        return (
            (XsConstantTaskAttribute.WORK_VALUE_1, self.modifier_value),
            (XsConstantTaskAttribute.WORK_VALUE_2, self.hp_percentage_threshold),
            (XsConstantTaskAttribute.WORK_RANGE, self.comparison_target),
            (XsConstantTaskAttribute.SEARCH_WAIT_TIME, self.modified_attribute),
        )


@dataclass(frozen=True, kw_only=True)
class UnitRefundTask(UnitTask):
    """Grant a resource refund when the modified unit dies.

    Args:
        refund_value: Required flat refund or fraction of associated unit cost.
        refunded_resource: Required resource type to grant.
        affected_objects: Optional and normally left as ``TaskTargets.none()``.
        recipient: Optional recipient from ``UnitRefundTask.Recipient``: owner
            or killer. Defaults to -1.
        value_mode: Optional interpretation from ``UnitRefundTask.ValueMode``:
            flat value or fraction of associated cost. Defaults to -1.
        productivity_resource: Optional resource whose current value multiplies
            ``refund_value``. Defaults to -1.
    """

    XS_TASK_TYPE: ClassVar[XsConstant] = XsConstantTaskType.REFUND
    Recipient: ClassVar[type[RefundRecipient]] = RefundRecipient
    ValueMode: ClassVar[type[RefundValueMode]] = RefundValueMode

    # Flat refund or fraction of the unit's associated resource cost.
    refund_value: XsValue
    # Resource type granted when the unit dies.
    refunded_resource: XsValue
    # Player receiving the refund: owner or killer.
    recipient: RefundRecipient | int = -1
    # Whether refund_value is flat or a fraction of associated cost.
    value_mode: RefundValueMode | int = -1
    # Resource whose current value multiplies refund_value.
    productivity_resource: XsValue = -1

    def task_attributes(self) -> tuple[tuple[str, XsValue], ...]:
        return (
            (XsConstantTaskAttribute.WORK_VALUE_1, self.refund_value),
            (XsConstantTaskAttribute.WORK_RANGE, self.recipient),
            (XsConstantTaskAttribute.COMBAT_LEVEL_FLAG, self.value_mode),
            (XsConstantTaskAttribute.PRODUCTIVITY_RESOURCE, self.productivity_resource),
            (XsConstantTaskAttribute.RESOURCE_OUT, self.refunded_resource),
        )


__all__ = [
    "AdditionalSpawnTask",
    "AmphibiousTask",
    "AuraFlags",
    "AuraTask",
    "BuildTask",
    "ConvertTask",
    "DepositUnitTask",
    "FlyTask",
    "FlyOwnershipMode",
    "GarrisonTask",
    "GenerateResourcesTask",
    "HealTask",
    "HPComparisonTarget",
    "HPDamageModifierTask",
    "HPThresholdMode",
    "HPTransformationTask",
    "LootMode",
    "LootTask",
    "MovementDamageTask",
    "PickupUnitTask",
    "RefundRecipient",
    "RefundValueMode",
    "RepairTask",
    "ResourceGenerationMode",
    "StingerFlags",
    "StingerRecipient",
    "StingerTask",
    "TargetOwnership",
    "TaskTargets",
    "UnitRefundTask",
    "UnitTask",
    "XsConstant",
]
