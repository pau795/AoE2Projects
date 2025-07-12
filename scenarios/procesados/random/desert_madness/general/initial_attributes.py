from AoE2ScenarioParser.datasets.buildings import BuildingInfo
from AoE2ScenarioParser.datasets.other import OtherInfo
from AoE2ScenarioParser.datasets.players import PlayerId
from AoE2ScenarioParser.datasets.projectiles import ProjectileInfo
from AoE2ScenarioParser.datasets.trigger_lists import Operation, ObjectAttribute, FogVisibility
from AoE2ScenarioParser.objects.managers.trigger_manager import TriggerManager
from AoE2ScenarioParser.scenarios.aoe2_de_scenario import AoE2DEScenario
from AoE2ScenarioParser.datasets.units import UnitInfo


class InitialAttributes:

    def __init__(self, scenario: AoE2DEScenario):
        self.trigger_manager: TriggerManager = scenario.trigger_manager
        self.gaia_stats()
        self.shop_stats()
        self.initial_villager_stats()
        self.bombard_towers()
        self.flags()
        self.camps()

    def gaia_stats(self):
        gaia_trigger = self.trigger_manager.add_trigger("Gaia Stats")

        # Gaia Rock Formations
        gaia_trigger.new_effect.modify_attribute(
            object_list_unit_id=OtherInfo.ROCK_FORMATION_1.ID,
            source_player=PlayerId.GAIA,
            object_attributes=ObjectAttribute.UNIT_SIZE_Z,
            operation=Operation.SET,
            quantity=2)

        gaia_trigger.new_effect.modify_attribute(
            object_list_unit_id=OtherInfo.ROCK_FORMATION_2.ID,
            source_player=PlayerId.GAIA,
            object_attributes=ObjectAttribute.UNIT_SIZE_Z,
            operation=Operation.SET,
            quantity=5)

        gaia_trigger.new_effect.modify_attribute(
            object_list_unit_id=OtherInfo.HAY_STACK.ID,
            source_player=PlayerId.GAIA,
            object_attributes=ObjectAttribute.UNIT_SIZE_Z,
            operation=Operation.SET,
            quantity=0)

        # Flag used for dead Boars in the hunting area
        gaia_trigger.new_effect.modify_attribute(
            object_list_unit_id=OtherInfo.FLAG_M.ID,
            source_player=PlayerId.GAIA,
            object_attributes=ObjectAttribute.STANDING_GRAPHIC,
            operation=Operation.SET,
            quantity=2454)

    def shop_stats(self):
        graphic_trigger = self.trigger_manager.add_trigger("P8 Graphics")

        # lumberjack carry
        graphic_trigger.new_effect.modify_attribute(
            object_list_unit_id=UnitInfo.SHOTEL_WARRIOR.ID,
            source_player=PlayerId.EIGHT,
            object_attributes=ObjectAttribute.STANDING_GRAPHIC,
            operation=Operation.SET,
            quantity=1603)

        # lumberjack carry icon
        graphic_trigger.new_effect.modify_attribute(
            object_list_unit_id=UnitInfo.SHOTEL_WARRIOR.ID,
            source_player=PlayerId.EIGHT,
            object_attributes=ObjectAttribute.ICON_ID,
            operation=Operation.SET,
            quantity=339)

        # lumberjack work
        graphic_trigger.new_effect.modify_attribute(
            object_list_unit_id=UnitInfo.ELITE_SHOTEL_WARRIOR.ID,
            source_player=PlayerId.EIGHT,
            object_attributes=ObjectAttribute.STANDING_GRAPHIC,
            operation=Operation.SET,
            quantity=1604)

        # lumberjack_work_icon
        (graphic_trigger.new_effect.modify_attribute(
            object_list_unit_id=UnitInfo.ELITE_SHOTEL_WARRIOR.ID,
            source_player=PlayerId.EIGHT,
            object_attributes=ObjectAttribute.ICON_ID,
            operation=Operation.SET,
            quantity=339))

        # gold miner carry
        graphic_trigger.new_effect.modify_attribute(
            object_list_unit_id=UnitInfo.BERSERK.ID,
            source_player=PlayerId.EIGHT,
            object_attributes=ObjectAttribute.STANDING_GRAPHIC,
            operation=Operation.SET,
            quantity=1605)

        # gold miner carry icon
        graphic_trigger.new_effect.modify_attribute(
            object_list_unit_id=UnitInfo.BERSERK.ID,
            source_player=PlayerId.EIGHT,
            object_attributes=ObjectAttribute.ICON_ID,
            operation=Operation.SET,
            quantity=334)

        # gold miner work
        graphic_trigger.new_effect.modify_attribute(
            object_list_unit_id=UnitInfo.ELITE_BERSERK.ID,
            source_player=PlayerId.EIGHT,
            object_attributes=ObjectAttribute.STANDING_GRAPHIC,
            operation=Operation.SET,
            quantity=1606)

        # gold miner work icon
        graphic_trigger.new_effect.modify_attribute(
            object_list_unit_id=UnitInfo.ELITE_BERSERK.ID,
            source_player=PlayerId.EIGHT,
            object_attributes=ObjectAttribute.ICON_ID,
            operation=Operation.SET,
            quantity=334)

        # stone miner carry
        graphic_trigger.new_effect.modify_attribute(
            object_list_unit_id=UnitInfo.OBUCH.ID,
            source_player=PlayerId.EIGHT,
            object_attributes=ObjectAttribute.STANDING_GRAPHIC,
            operation=Operation.SET,
            quantity=1949)

        # stone miner carry icon
        graphic_trigger.new_effect.modify_attribute(
            object_list_unit_id=UnitInfo.OBUCH.ID,
            source_player=PlayerId.EIGHT,
            object_attributes=ObjectAttribute.ICON_ID,
            operation=Operation.SET,
            quantity=336)

        # stone_miner_work
        graphic_trigger.new_effect.modify_attribute(
            object_list_unit_id=UnitInfo.ELITE_OBUCH.ID,
            source_player=PlayerId.EIGHT,
            object_attributes=ObjectAttribute.STANDING_GRAPHIC,
            operation=Operation.SET,
            quantity=1682)
        # stone miner work icon
        graphic_trigger.new_effect.modify_attribute(
            object_list_unit_id=UnitInfo.ELITE_OBUCH.ID,
            source_player=PlayerId.EIGHT,
            object_attributes=ObjectAttribute.ICON_ID,
            operation=Operation.SET,
            quantity=336)

        # forager carry
        graphic_trigger.new_effect.modify_attribute(
            object_list_unit_id=UnitInfo.KAMAYUK.ID,
            source_player=PlayerId.EIGHT,
            object_attributes=ObjectAttribute.STANDING_GRAPHIC,
            operation=Operation.SET,
            quantity=2440)

        # forager carry icon
        graphic_trigger.new_effect.modify_attribute(
            object_list_unit_id=UnitInfo.KAMAYUK.ID,
            source_player=PlayerId.EIGHT,
            object_attributes=ObjectAttribute.ICON_ID,
            operation=Operation.SET,
            quantity=332)

        # forager work
        graphic_trigger.new_effect.modify_attribute(
            object_list_unit_id=UnitInfo.ELITE_KAMAYUK.ID,
            source_player=PlayerId.EIGHT,
            object_attributes=ObjectAttribute.STANDING_GRAPHIC,
            operation=Operation.SET,
            quantity=2449)

        # forager work icon
        graphic_trigger.new_effect.modify_attribute(
            object_list_unit_id=UnitInfo.ELITE_KAMAYUK.ID,
            source_player=PlayerId.EIGHT,
            object_attributes=ObjectAttribute.ICON_ID,
            operation=Operation.SET,
            quantity=332)

        # fisherman carry
        graphic_trigger.new_effect.modify_attribute(
            object_list_unit_id=UnitInfo.KARAMBIT_WARRIOR.ID,
            source_player=PlayerId.EIGHT,
            object_attributes=ObjectAttribute.STANDING_GRAPHIC,
            operation=Operation.SET,
            quantity=3153)

        # fisherman carry icon
        graphic_trigger.new_effect.modify_attribute(
            object_list_unit_id=UnitInfo.KARAMBIT_WARRIOR.ID,
            source_player=PlayerId.EIGHT,
            object_attributes=ObjectAttribute.ICON_ID,
            operation=Operation.SET,
            quantity=332)

        # fisherman work
        graphic_trigger.new_effect.modify_attribute(
            object_list_unit_id=UnitInfo.ELITE_KARAMBIT_WARRIOR.ID,
            source_player=PlayerId.EIGHT,
            object_attributes=ObjectAttribute.STANDING_GRAPHIC,
            operation=Operation.SET,
            quantity=3154)

        # fisherman carry icon
        graphic_trigger.new_effect.modify_attribute(
            object_list_unit_id=UnitInfo.ELITE_KARAMBIT_WARRIOR.ID,
            source_player=PlayerId.EIGHT,
            object_attributes=ObjectAttribute.ICON_ID,
            operation=Operation.SET,
            quantity=332)

        # hunter carry
        graphic_trigger.new_effect.modify_attribute(
            object_list_unit_id=UnitInfo.SERJEANT.ID,
            source_player=PlayerId.EIGHT,
            object_attributes=ObjectAttribute.STANDING_GRAPHIC,
            operation=Operation.SET,
            quantity=1601)
        # hunter carry icon
        graphic_trigger.new_effect.modify_attribute(
            object_list_unit_id=UnitInfo.SERJEANT.ID,
            source_player=PlayerId.EIGHT,
            object_attributes=ObjectAttribute.ICON_ID,
            operation=Operation.SET,
            quantity=332)

        graphic_trigger.new_effect.modify_attribute(
            object_list_unit_id=UnitInfo.ELITE_SERJEANT.ID,
            source_player=PlayerId.EIGHT,
            object_attributes=ObjectAttribute.STANDING_GRAPHIC,
            operation=Operation.SET,
            quantity=1602)

        # fisherman carry icon
        graphic_trigger.new_effect.modify_attribute(
            object_list_unit_id=UnitInfo.ELITE_SERJEANT.ID,
            source_player=PlayerId.EIGHT,
            object_attributes=ObjectAttribute.ICON_ID,
            operation=Operation.SET,
            quantity=332)

        # villager walk
        graphic_trigger.new_effect.modify_attribute(
            object_list_unit_id=UnitInfo.SAMURAI.ID,
            source_player=PlayerId.EIGHT,
            object_attributes=ObjectAttribute.STANDING_GRAPHIC,
            operation=Operation.SET,
            quantity=1288)
        # villager icon
        graphic_trigger.new_effect.modify_attribute(
            object_list_unit_id=UnitInfo.SAMURAI.ID,
            source_player=PlayerId.EIGHT,
            object_attributes=ObjectAttribute.ICON_ID,
            operation=Operation.SET,
            quantity=15)

        # builder walk
        graphic_trigger.new_effect.modify_attribute(
            object_list_unit_id=UnitInfo.JAGUAR_WARRIOR.ID,
            source_player=PlayerId.EIGHT,
            object_attributes=ObjectAttribute.STANDING_GRAPHIC,
            operation=Operation.SET,
            quantity=1598)

        # builder icon
        graphic_trigger.new_effect.modify_attribute(
            object_list_unit_id=UnitInfo.JAGUAR_WARRIOR.ID,
            source_player=PlayerId.EIGHT,
            object_attributes=ObjectAttribute.ICON_ID,
            operation=Operation.SET,
            quantity=330)

    def initial_villager_stats(self):
        villager_stats_trigger = self.trigger_manager.add_trigger("Villager Stats")

        villager_list = [
            UnitInfo.VILLAGER_MALE.ID,
            UnitInfo.VILLAGER_MALE_LUMBERJACK.ID,
            UnitInfo.VILLAGER_MALE_FORAGER.ID,
            UnitInfo.VILLAGER_MALE_FISHERMAN.ID,
            UnitInfo.VILLAGER_MALE_HUNTER.ID,
            UnitInfo.VILLAGER_MALE_SHEPHERD.ID,
            UnitInfo.VILLAGER_MALE_FARMER.ID,
            UnitInfo.VILLAGER_MALE_BUILDER.ID,
            UnitInfo.VILLAGER_MALE_REPAIRER.ID,
            UnitInfo.VILLAGER_MALE_GOLD_MINER.ID,
            UnitInfo.VILLAGER_MALE_STONE_MINER.ID]

        for villager in villager_list:
            villager_stats_trigger.new_effect.modify_attribute(
                object_list_unit_id=villager,
                source_player=PlayerId.ONE,
                object_attributes=ObjectAttribute.UNIT_SIZE_Z,
                operation=Operation.SET,
                quantity=2)
            villager_stats_trigger.new_effect.modify_attribute(
                object_list_unit_id=villager,
                source_player=PlayerId.ONE,
                object_attributes=ObjectAttribute.MOVEMENT_SPEED,
                operation=Operation.SET,
                quantity=135)
            villager_stats_trigger.new_effect.modify_attribute(
                object_list_unit_id=villager,
                source_player=PlayerId.ONE,
                object_attributes=ObjectAttribute.MOVEMENT_SPEED,
                operation=Operation.DIVIDE,
                quantity=100)

            villager_stats_trigger.new_effect.modify_attribute(
                object_list_unit_id=villager,
                source_player=PlayerId.ONE,
                object_attributes=ObjectAttribute.HIT_POINTS,
                operation=Operation.SET,
                quantity=100)

        self.trigger_manager.copy_trigger_per_player(
            trigger_select=villager_stats_trigger.trigger_id,
            from_player=PlayerId.ONE,
            create_copy_for_players=[
                PlayerId.TWO,
                PlayerId.THREE,
                PlayerId.FOUR,
                PlayerId.FIVE,
                PlayerId.SIX,
                PlayerId.SEVEN]
        )

    def bombard_towers(self):
        bombard_tower_stats = self.trigger_manager.add_trigger("P8 Bombard Tower Stats")
        bombard_tower_stats.new_effect.modify_attribute(
            object_list_unit_id=ProjectileInfo.BTW.ID,
            source_player=PlayerId.EIGHT,
            object_attributes=ObjectAttribute.MOVEMENT_SPEED,
            operation=Operation.SET,
            quantity=5)
        bombard_tower_stats.new_effect.modify_attribute(
            object_list_unit_id=ProjectileInfo.BTW.ID,
            source_player=PlayerId.EIGHT,
            object_attributes=ObjectAttribute.FOG_VISIBILITY,
            operation=Operation.SET,
            quantity=FogVisibility.ALWAYS_VISIBLE)
        bombard_tower_stats.new_effect.disable_unit_targeting(
            object_list_unit_id=BuildingInfo.BOMBARD_TOWER.ID,
            source_player=PlayerId.EIGHT
        )

    def flags(self):
        flag_attributes = self.trigger_manager.add_trigger("Flag Attributes")
        players = [PlayerId.ONE, PlayerId.TWO, PlayerId.THREE, PlayerId.FOUR,
                   PlayerId.FIVE, PlayerId.SIX, PlayerId.SEVEN, PlayerId.EIGHT]
        for player in players:
            flag_attributes.new_effect.modify_attribute(
                object_list_unit_id=OtherInfo.FLAG_G.ID,
                source_player=player,
                object_attributes=ObjectAttribute.LINE_OF_SIGHT,
                operation=Operation.SET,
                quantity=0
            )
            flag_attributes.new_effect.modify_attribute(
                object_list_unit_id=OtherInfo.FLAG_B.ID,
                source_player=player,
                object_attributes=ObjectAttribute.LINE_OF_SIGHT,
                operation=Operation.SET,
                quantity=0
            )

    def camps(self):
        camp_attributes = self.trigger_manager.add_trigger("Camps Attributes")
        players = [PlayerId.ONE, PlayerId.TWO, PlayerId.THREE, PlayerId.FOUR,
                   PlayerId.FIVE, PlayerId.SIX, PlayerId.SEVEN, PlayerId.EIGHT]
        for player in players:
            camp_attributes.new_effect.modify_attribute(
                object_list_unit_id=BuildingInfo.LUMBER_CAMP.ID,
                source_player=player,
                object_attributes=ObjectAttribute.LINE_OF_SIGHT,
                operation=Operation.SET,
                quantity=3
            )

            camp_attributes.new_effect.modify_attribute(
                object_list_unit_id=BuildingInfo.MINING_CAMP.ID,
                source_player=player,
                object_attributes=ObjectAttribute.LINE_OF_SIGHT,
                operation=Operation.SET,
                quantity=3
            )

            camp_attributes.new_effect.modify_attribute(
                object_list_unit_id=BuildingInfo.MILL.ID,
                source_player=player,
                object_attributes=ObjectAttribute.LINE_OF_SIGHT,
                operation=Operation.SET,
                quantity=3
            )

            camp_attributes.new_effect.disable_unit_targeting(
                object_list_unit_id=BuildingInfo.LUMBER_CAMP.ID,
                source_player=player
            )

            camp_attributes.new_effect.disable_unit_targeting(
                object_list_unit_id=BuildingInfo.MINING_CAMP.ID,
                source_player=player
            )

            camp_attributes.new_effect.disable_unit_targeting(
                object_list_unit_id=BuildingInfo.MILL.ID,
                source_player=player
            )

            camp_attributes.new_effect.disable_object_deletion(
                object_list_unit_id=BuildingInfo.LUMBER_CAMP.ID,
                source_player=player
            )

            camp_attributes.new_effect.disable_object_deletion(
                object_list_unit_id=BuildingInfo.MINING_CAMP.ID,
                source_player=player
            )

            camp_attributes.new_effect.disable_object_deletion(
                object_list_unit_id=BuildingInfo.MILL.ID,
                source_player=player
            )