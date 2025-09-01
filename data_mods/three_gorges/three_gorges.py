from AoE2ScenarioParser.datasets.terrains import TerrainId
from AoE2ScenarioParser.datasets.trigger_lists import TerrainRestrictions
from genieutils.datfile import DatFile
from genieutils.terrainrestriction import TerrainRestriction

from multimedia_generator import constants


def create_terrain_restriction(new_terrain_restriction: TerrainRestriction,
                               template_terrain_restriction: TerrainRestriction,
                               template_terrain_for_dirt: int):
    for i, (dmg, terrain_graphic) in enumerate(zip(template_terrain_restriction.passable_buildable_dmg_multiplier, template_terrain_restriction.terrain_pass_graphics)):
        new_terrain_restriction.passable_buildable_dmg_multiplier[i] = dmg
        new_terrain_restriction.terrain_pass_graphics[i].exit_tile_sprite_id = terrain_graphic.exit_tile_sprite_id
        new_terrain_restriction.terrain_pass_graphics[i].enter_tile_sprite_id = terrain_graphic.enter_tile_sprite_id
        new_terrain_restriction.terrain_pass_graphics[i].walk_tile_sprite_id = terrain_graphic.walk_tile_sprite_id
        new_terrain_restriction.terrain_pass_graphics[i].walk_sprite_rate = terrain_graphic.walk_sprite_rate

    x = 84
    new_terrain_restriction.passable_buildable_dmg_multiplier[x] = template_terrain_restriction.passable_buildable_dmg_multiplier[template_terrain_for_dirt]
    new_terrain_restriction.terrain_pass_graphics[x].exit_tile_sprite_id = template_terrain_restriction.terrain_pass_graphics[template_terrain_for_dirt].exit_tile_sprite_id
    new_terrain_restriction.terrain_pass_graphics[x].enter_tile_sprite_id = template_terrain_restriction.terrain_pass_graphics[template_terrain_for_dirt].enter_tile_sprite_id
    new_terrain_restriction.terrain_pass_graphics[x].walk_tile_sprite_id = template_terrain_restriction.terrain_pass_graphics[template_terrain_for_dirt].walk_tile_sprite_id
    new_terrain_restriction.terrain_pass_graphics[x].walk_sprite_rate = template_terrain_restriction.terrain_pass_graphics[template_terrain_for_dirt].walk_sprite_rate


if __name__ == "__main__":
    dat = DatFile.parse(constants.AOE_DAT_FILE_PATH)
    tr_land = dat.terrain_restrictions[TerrainRestrictions.ALL_EXCEPT_WATER]
    tr_land_beach = dat.terrain_restrictions[TerrainRestrictions.LAND_AND_BEACH]
    tr_water = dat.terrain_restrictions[TerrainRestrictions.WATER_MEDIUM_TRAIL]

    tr_land_no_dirt = dat.terrain_restrictions[40]
    tr_land_beach_no_dirt = dat.terrain_restrictions[41]
    tr_water_and_dirt = dat.terrain_restrictions[42]
    create_terrain_restriction(tr_land_no_dirt, tr_land, TerrainId.WATER_MEDIUM)
    create_terrain_restriction(tr_land_beach_no_dirt, tr_land_beach, TerrainId.WATER_MEDIUM)
    create_terrain_restriction(tr_water_and_dirt, tr_water, TerrainId.WATER_MEDIUM)

    mod_land = dat.terrain_block.terrains[84]
    mod_land.name_1 = "Floodable Land"
    mod_land.name_2 = "g_ds2"
    mod_land.is_water = 64
    mod_land.hide_in_editor = 0

    dat.save("output/empires2_x2_p1.dat")
