const int mobile_city_wall_unit =  448;
const int mobile_fortified_palisade_wall_unit  = 546;
const int mobile_sea_wall_unit = 441;

const int sea_wall = 788;
const int city_wall = 370;
const int fortified_palisade_wall = 119;

const int horse_a = 814;

void wall_stats(){
    
    xsEffectAmount(cSetAttribute, 814, cHitpoints, 20000, 3);
    xsEffectAmount(cSetAttribute, 814, cInvulnerabilityLevel, -20000, 3);
    xsEffectAmount(cSetAttribute, 814, cInteractionMode, 0, 3);
    xsEffectAmount(cSetAttribute, 814, cStandingGraphic, 0, 3);
    xsEffectAmount(cSetAttribute, 814, cWalkingGraphic, 0, 3);    

    xsEffectAmount(cSetAttribute, city_wall, cTerrainTable, 0, 3);
    xsEffectAmount(cSetAttribute, city_wall, cHitpoints, 20000, 3);
    xsEffectAmount(cSetAttribute, city_wall, cInvulnerabilityLevel, -20000, 3);
    xsEffectAmount(cSetAttribute, city_wall, cFoundationTerrain, -1, 3);
    xsEffectAmount(cSetAttribute, city_wall, cTrainTime, 0, 3);

    xsEffectAmount(cSetAttribute, fortified_palisade_wall, cTerrainTable, 0, 3);    
    xsEffectAmount(cSetAttribute, fortified_palisade_wall, cHitpoints, 20000, 3);
    xsEffectAmount(cSetAttribute, fortified_palisade_wall, cInvulnerabilityLevel, -20000, 3);
    xsEffectAmount(cSetAttribute, fortified_palisade_wall, cFoundationTerrain, -1, 3);
    xsEffectAmount(cSetAttribute, fortified_palisade_wall, cTrainTime, 0, 3);
    
    xsEffectAmount(cSetAttribute, sea_wall, cTerrainTable, 0, 3);
    xsEffectAmount(cSetAttribute, sea_wall, cHitpoints, 20000, 3);
    xsEffectAmount(cSetAttribute, sea_wall, cInvulnerabilityLevel, -20000, 3);
    xsEffectAmount(cSetAttribute, sea_wall, cFoundationTerrain, -1, 3);
    xsEffectAmount(cSetAttribute, sea_wall, cTrainTime, 0, 3);

    xsEffectAmount(cSetAttribute, mobile_city_wall_unit, cTerrainTable, 0, 3);
    xsEffectAmount(cSetAttribute, mobile_city_wall_unit, cUnitSizeX, 0, 3);
    xsEffectAmount(cSetAttribute, mobile_city_wall_unit, cUnitSizeY, 0, 3);
    xsEffectAmount(cSetAttribute, mobile_city_wall_unit, cUnitSizeZ, 0, 3);
    xsEffectAmount(cSetAttribute, mobile_city_wall_unit, cMovementSpeed, 2, 3);
    xsEffectAmount(cSetAttribute, mobile_city_wall_unit, cShownAttack, 0, 3);
    xsEffectAmount(cSetAttribute, mobile_city_wall_unit, cShownMeleeArmor, 0, 3);
    xsEffectAmount(cSetAttribute, mobile_city_wall_unit, cShownPierceArmor, 0, 3);
    xsEffectAmount(cSetAttribute, mobile_city_wall_unit, cIconId, 32, 3);
    xsEffectAmount(cSetAttribute, mobile_city_wall_unit, cNameId, 5754, 3);    
    xsEffectAmount(cSetAttribute, mobile_city_wall_unit, cHitpoints, 20000, 3);
    xsEffectAmount(cSetAttribute, mobile_city_wall_unit, cInvulnerabilityLevel, -20000, 3);
    xsEffectAmount(cSetAttribute, mobile_city_wall_unit, cStandingGraphic, 621, 3);
    xsEffectAmount(cSetAttribute, mobile_city_wall_unit, cWalkingGraphic, 621, 3);

    xsEffectAmount(cSetAttribute, mobile_city_wall_unit, cTerrainTable, 0, 3);
    xsEffectAmount(cSetAttribute, mobile_city_wall_unit, cUnitSizeX, 0, 3);
    xsEffectAmount(cSetAttribute, mobile_city_wall_unit, cUnitSizeY, 0, 3);
    xsEffectAmount(cSetAttribute, mobile_city_wall_unit, cUnitSizeZ, 0, 3);
    xsEffectAmount(cSetAttribute, mobile_city_wall_unit, cMovementSpeed, 0.5, 3);
    xsEffectAmount(cSetAttribute, mobile_city_wall_unit, cShownAttack, 0, 3);
    xsEffectAmount(cSetAttribute, mobile_city_wall_unit, cShownMeleeArmor, 0, 3);
    xsEffectAmount(cSetAttribute, mobile_city_wall_unit, cShownPierceArmor, 0, 3);
    xsEffectAmount(cSetAttribute, mobile_city_wall_unit, cIconId, 32, 3);
    xsEffectAmount(cSetAttribute, mobile_city_wall_unit, cNameId, 5754, 3);    
    xsEffectAmount(cSetAttribute, mobile_city_wall_unit, cHitpoints, 20000, 3);
    xsEffectAmount(cSetAttribute, mobile_city_wall_unit, cInvulnerabilityLevel, -20000, 3);
    xsEffectAmount(cSetAttribute, mobile_city_wall_unit, cStandingGraphic, 621, 3);
    xsEffectAmount(cSetAttribute, mobile_city_wall_unit, cStanding2Graphic, 621, 3);
    xsEffectAmount(cSetAttribute, mobile_city_wall_unit, cWalkingGraphic, 621, 3);

    xsEffectAmount(cSetAttribute, mobile_fortified_palisade_wall_unit, cTerrainTable, 0, 3);
    xsEffectAmount(cSetAttribute, mobile_fortified_palisade_wall_unit, cUnitSizeX, 0, 3);
    xsEffectAmount(cSetAttribute, mobile_fortified_palisade_wall_unit, cUnitSizeY, 0, 3);
    xsEffectAmount(cSetAttribute, mobile_fortified_palisade_wall_unit, cUnitSizeZ, 0, 3);
    xsEffectAmount(cSetAttribute, mobile_fortified_palisade_wall_unit, cMovementSpeed, 0.5, 3);
    xsEffectAmount(cSetAttribute, mobile_fortified_palisade_wall_unit, cShownAttack, 0, 3);
    xsEffectAmount(cSetAttribute, mobile_fortified_palisade_wall_unit, cShownMeleeArmor, 0, 3);
    xsEffectAmount(cSetAttribute, mobile_fortified_palisade_wall_unit, cShownPierceArmor, 0, 3);
    xsEffectAmount(cSetAttribute, mobile_fortified_palisade_wall_unit, cIconId, 30, 32);
    xsEffectAmount(cSetAttribute, mobile_fortified_palisade_wall_unit, cNameId, 5205, 3);    
    xsEffectAmount(cSetAttribute, mobile_fortified_palisade_wall_unit, cHitpoints, 20000, 3);
    xsEffectAmount(cSetAttribute, mobile_fortified_palisade_wall_unit, cInvulnerabilityLevel, -20000, 3);
    xsEffectAmount(cSetAttribute, mobile_fortified_palisade_wall_unit, cStandingGraphic, 606, 3);
    xsEffectAmount(cSetAttribute, mobile_fortified_palisade_wall_unit, cStanding2Graphic, 606, 3);
    xsEffectAmount(cSetAttribute, mobile_fortified_palisade_wall_unit, cWalkingGraphic, 606, 3);

    xsEffectAmount(cSetAttribute, mobile_sea_wall_unit, cTerrainTable, 0, 3);
    xsEffectAmount(cSetAttribute, mobile_sea_wall_unit, cUnitSizeX, 0, 3);
    xsEffectAmount(cSetAttribute, mobile_sea_wall_unit, cUnitSizeY, 0, 3);
    xsEffectAmount(cSetAttribute, mobile_sea_wall_unit, cUnitSizeZ, 0, 3);
    xsEffectAmount(cSetAttribute, mobile_sea_wall_unit, cMovementSpeed, 0.5, 3);
    xsEffectAmount(cSetAttribute, mobile_sea_wall_unit, cShownAttack, 0, 3);
    xsEffectAmount(cSetAttribute, mobile_sea_wall_unit, cShownMeleeArmor, 0, 3);
    xsEffectAmount(cSetAttribute, mobile_sea_wall_unit, cShownPierceArmor, 0, 3);
    xsEffectAmount(cSetAttribute, mobile_sea_wall_unit, cIconId, 0.5, 92);
    xsEffectAmount(cSetAttribute, mobile_sea_wall_unit, cNameId, 0.5, 5707);      
    xsEffectAmount(cSetAttribute, mobile_sea_wall_unit, cHitpoints, 20000, 3);
    xsEffectAmount(cSetAttribute, mobile_sea_wall_unit, cInvulnerabilityLevel, -20000, 3);
    xsEffectAmount(cSetAttribute, mobile_sea_wall_unit, cStandingGraphic, 6594, 3);
    xsEffectAmount(cSetAttribute, mobile_sea_wall_unit, cStanding2Graphic, 6594, 3);
    xsEffectAmount(cSetAttribute, mobile_sea_wall_unit, cWalkingGraphic, 6594, 3);

}
