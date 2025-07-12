import re
from AoE2ScenarioParser.datasets.units import UnitInfo
from AoE2ScenarioParser.objects.managers.trigger_manager import TriggerManager
from scenarios.lib.random_probability import EqualRandomProbability


class NomadStart:

    def __init__(self, trigger_manager, trigger_data, player_id_list):
        self.trigger_manager: TriggerManager = trigger_manager
        self.trigger_data = trigger_data
        self.player_id_list = player_id_list
        if self.check_villager_collisions():
            self.nomad_start()
        else:
            raise Exception("Villager Collisions")

    def nomad_start(self):
        try:
            for player_id in self.player_id_list:
                villager_regex = fr'vill\d+_p{player_id.value}'
                for key, villager_spots in self.trigger_data.tiles.items():
                    villager_triggers = []
                    if not re.match(villager_regex, key):
                        continue
                    villager_number = int(re.findall(r'\d+', key)[0])
                    for i, spot in enumerate(villager_spots):
                        create_villager_trigger = self.trigger_manager.add_trigger(f"Nomad Start Villager {villager_number} Spot{i} P{player_id.value}", enabled=False)
                        create_villager_trigger.new_effect.create_object(
                            source_player=player_id,
                            object_list_unit_id=UnitInfo.VILLAGER_MALE.ID,
                            location_x=spot.x,
                            location_y=spot.y,
                        )
                        villager_triggers.append(create_villager_trigger)
                    villager_probability = EqualRandomProbability(self.trigger_manager, villager_triggers, f'Ramdom Villager {villager_number} P{player_id.value}')
                    villager_probability.enable_probability_trigger.enabled = True

        except Exception as e:
            print(f"Nomad Start Error: {e}")
            raise e

    def check_villager_collisions(self) -> bool:
        tile_dict = {}
        for key, villager_spots in self.trigger_data.tiles.items():
            for i, tile in enumerate(villager_spots):
                if tile not in tile_dict:
                    tile_dict[tile] = []
                tile_dict[tile].append((key, i))
        for tile, villagers in tile_dict.items():
            if len(villagers) > 1:
                raise Exception(f"Villager Collision: {tile} {villagers}")
        return True
