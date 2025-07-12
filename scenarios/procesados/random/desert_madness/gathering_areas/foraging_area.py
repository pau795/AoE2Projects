from itertools import pairwise

from AoE2ScenarioParser.datasets.other import OtherInfo
from AoE2ScenarioParser.datasets.players import PlayerId
from AoE2ScenarioParser.datasets.trigger_lists import ObjectAttribute, Operation, DamageClass, AttackStance
from AoE2ScenarioParser.objects.managers.trigger_manager import TriggerManager
from AoE2ScenarioParser.scenarios.aoe2_de_scenario import AoE2DEScenario
from AoE2ScenarioParser.scenarios.support.data_triggers import DataTriggers


def filter_pass(index, tiles, offset):
    for tile in tiles:
        if tile <= index < tile + offset:
            return False
    return True


class ForagingArea:

    def __init__(self, scenario: AoE2DEScenario, trigger_data: DataTriggers):
        self.trigger_manager: TriggerManager = scenario.trigger_manager
        self.trigger_data = trigger_data
        self.foraging_area = self.trigger_data.areas['foraging_area'][0]
        self.foraging_pass = self.trigger_data.areas['foraging_pass']
        self.foraging_units = self.trigger_data.areas['foraging_units']

        self.foraging_sound_tile = self.trigger_data.tiles['foraging_sound'][0]
        self.fire_tiles = self.trigger_data.tiles['foraging_fire']

        self.init_attributes()
        self.explosions()

    def init_attributes(self):
        init_attributes = self.trigger_manager.add_trigger('Foraging Area Initial Attributes')

        init_attributes.new_effect.modify_attribute(
            object_list_unit_id=OtherInfo.FRUIT_BUSH.ID,
            source_player=PlayerId.GAIA,
            object_attributes=ObjectAttribute.DEAD_UNIT_ID,
            operation=Operation.SET,
            quantity=OtherInfo.FRUIT_BUSH.ID
        )

        for units_area in self.foraging_units:
            init_attributes.new_effect.change_object_stance(
                source_player=PlayerId.EIGHT,
                area_x1=units_area.x1,
                area_y1=units_area.y1,
                area_x2=units_area.x2,
                area_y2=units_area.y2,
                attack_stance=AttackStance.NO_ATTACK_STANCE
            )

            init_attributes.new_effect.disable_unit_targeting(
                source_player=PlayerId.EIGHT,
                area_x1=units_area.x1,
                area_y1=units_area.y1,
                area_x2=units_area.x2,
                area_y2=units_area.y2
            )

    def explosions(self):
        burn_tiles = [0, 30, 60, 90, 120, 150, 180]
        empty_distance = 15
        fire_path = self.trigger_manager.add_trigger('Foraging Area Initial Fire')
        for i, tile1 in enumerate(self.fire_tiles):
            if filter_pass(i, burn_tiles, empty_distance):
                fire_path.new_effect.create_object(
                    object_list_unit_id=OtherInfo.IMPALED_CORPSE.ID,
                    source_player=PlayerId.GAIA,
                    location_x=tile1.x,
                    location_y=tile1.y
                )

        fire_chain = []
        for i, tile1 in enumerate(self.fire_tiles):
            fire_control = self.trigger_manager.add_trigger(f'Foraging Area Fire Control {i}', enabled=False)
            fire_control.new_condition.timer(timer=2)
            for p in burn_tiles:
                remove_tile = self.fire_tiles[(p + empty_distance + i) % len(self.fire_tiles)]
                fire_control.new_effect.remove_object(
                    object_list_unit_id=OtherInfo.IMPALED_CORPSE.ID,
                    source_player=PlayerId.GAIA,
                    area_x1=remove_tile.x,
                    area_y1=remove_tile.y,
                    area_x2=remove_tile.x,
                    area_y2=remove_tile.y
                )

                create_tile = self.fire_tiles[(p + i) % len(self.fire_tiles)]
                fire_control.new_effect.create_object(
                    object_list_unit_id=OtherInfo.IMPALED_CORPSE.ID,
                    source_player=PlayerId.GAIA,
                    location_x=create_tile.x,
                    location_y=create_tile.y,
                )
            for player in [PlayerId.ONE, PlayerId.TWO, PlayerId.THREE, PlayerId.FOUR, PlayerId.FIVE, PlayerId.SIX,
                           PlayerId.SEVEN, PlayerId.EIGHT]:
                fire_control.new_effect.play_sound(
                    source_player=player,
                    location_x=self.foraging_sound_tile.x,
                    location_y=self.foraging_sound_tile.y,
                    sound_name='PLAY_CLANK_KATANA'
                )
            fire_burns = self.trigger_manager.add_trigger(f'Foraging Burn {i}', enabled=True, looping=True)
            fire_burns.new_condition.objects_in_area(
                object_list=OtherInfo.IMPALED_CORPSE.ID,
                source_player=PlayerId.GAIA,
                area_x1=tile1.x,
                area_y1=tile1.y,
                area_x2=tile1.x,
                area_y2=tile1.y,
                quantity=1
            )
            for player in [PlayerId.ONE, PlayerId.TWO, PlayerId.THREE, PlayerId.FOUR, PlayerId.FIVE, PlayerId.SIX,
                           PlayerId.SEVEN, PlayerId.EIGHT]:
                fire_burns.new_effect.kill_object(
                    source_player=player,
                    area_x1=tile1.x,
                    area_y1=tile1.y,
                    area_x2=tile1.x,
                    area_y2=tile1.y
                )
            fire_chain.append(fire_control)
        pairs = pairwise(fire_chain)
        for pair in pairs:
            pair[0].new_effect.activate_trigger(trigger_id=pair[1].trigger_id)
        fire_chain[-1].new_effect.activate_trigger(trigger_id=fire_chain[0].trigger_id)
        fire_chain[0].enabled = True
