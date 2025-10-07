const int beach_bridge = 1310;
const int final_water_bridge = 1313;
const int warning_water_bridge = 1314;

const int aura_damage_unit = 1241;

// FLAG
const int barricade_a_flag = 600; // FLAG A
const int barricade_d_flag = 601; // FLAG B
const int waterfall_flag = 602; // FLAG C
const int smoke_flag = 1152; // FLAG C


void bridge_stats(){
    xsEffectAmount(cSetAttribute, beach_bridge, cUnitSizeX, 0, 0);
    xsEffectAmount(cSetAttribute, beach_bridge, cUnitSizeY, 0, 0);
    xsEffectAmount(cSetAttribute, beach_bridge, cUnitSizeZ, 0, 0);
    xsEffectAmount(cSetAttribute, beach_bridge, cDyingGraphic, 5507, 0);
    xsEffectAmount(cSetAttribute, beach_bridge, cDeadUnitId, -1, 0);
    xsEffectAmount(cSetAttribute, beach_bridge, cFoundationTerrain, 2, 0);
    xsEffectAmount(cSetAttribute, beach_bridge, cStandingGraphic, 0, 0);

    xsEffectAmount(cSetAttribute, final_water_bridge, cUnitSizeX, 0, 0);
    xsEffectAmount(cSetAttribute, final_water_bridge, cUnitSizeY, 0, 0);
    xsEffectAmount(cSetAttribute, final_water_bridge, cUnitSizeZ, 0, 0);
    xsEffectAmount(cSetAttribute, final_water_bridge, cDyingGraphic, 5507, 0);
    xsEffectAmount(cSetAttribute, final_water_bridge, cDeadUnitId, -1, 0);
    xsEffectAmount(cSetAttribute, final_water_bridge, cFoundationTerrain, 1, 0);
    xsEffectAmount(cSetAttribute, final_water_bridge, cStandingGraphic, 0, 0);

    xsEffectAmount(cSetAttribute, warning_water_bridge, cUnitSizeX, 0, 0);
    xsEffectAmount(cSetAttribute, warning_water_bridge, cUnitSizeY, 0, 0);
    xsEffectAmount(cSetAttribute, warning_water_bridge, cUnitSizeZ, 0, 0);
    xsEffectAmount(cSetAttribute, warning_water_bridge, cDyingGraphic, 5507, 0);
    xsEffectAmount(cSetAttribute, warning_water_bridge, cDeadUnitId, -1, 0);
    xsEffectAmount(cSetAttribute, warning_water_bridge, cFoundationTerrain, 15, 0);
    xsEffectAmount(cSetAttribute, warning_water_bridge, cStandingGraphic, 0, 0);
}

void aura_damage(){
    xsEffectAmount(cSetAttribute, aura_damage_unit, cCombatAbility, 32, 0);
    xsEffectAmount(cSetAttribute, aura_damage_unit, cMovementSpeed, 0, 0);
    xsEffectAmount(cSetAttribute, aura_damage_unit, cStandingGraphic, 9420, 0);
    xsEffectAmount(cSetAttribute, aura_damage_unit, cWalkingGraphic, 0, 0);
    xsEffectAmount(cSetAttribute, aura_damage_unit, cAttackGraphic, 0, 0);
    xsEffectAmount(cSetAttribute, aura_damage_unit, cDyingGraphic, 0, 0);
    xsEffectAmount(cSetAttribute, aura_damage_unit, cDeadUnitId, 0, 0);
    xsEffectAmount(cSetAttribute, aura_damage_unit, cHitpoints, 20000, 0);
    xsEffectAmount(cSetAttribute, aura_damage_unit, cInvulnerabilityLevel, -20000, 0);
    xsEffectAmount(cSetAttribute, aura_damage_unit, cInteractionMode, 0, 0);
    xsEffectAmount(cSetAttribute, aura_damage_unit, cLineOfSight, 20, 0);
    xsEffectAmount(cSetAttribute, aura_damage_unit, cSearchRadius, 0, 0);
    xsEffectAmount(cSetAttribute, aura_damage_unit, cUnitSizeX, 0, 0);
    xsEffectAmount(cSetAttribute, aura_damage_unit, cUnitSizeY, 0, 0);
    xsEffectAmount(cSetAttribute, aura_damage_unit, cUnitSizeZ, 0, 0);
    xsEffectAmount(cSetAttribute, aura_damage_unit, cBlastAttackLevel, 0, 0);
    xsTaskAmount(cTaskAttrWorkValue1, -999999);
    xsTaskAmount(cTaskAttrWorkValue2, 1);
    xsTaskAmount(cTaskAttrWorkRange, 2);
    xsTaskAmount(cTaskAttrSearchWaitTime, 109);
    xsTaskAmount(cTaskAttrCombatLevelFlag, 0);
    xsTaskAmount(cTaskAttrOwnerType, 0);

    xsTask(aura_damage_unit, cTaskTypeAura, cArcherClass, 0);
    xsTask(aura_damage_unit, cTaskTypeAura, cArtifactClass, 0);
    xsTask(aura_damage_unit, cTaskTypeAura, cTradeBoatClass, 0);
    xsTask(aura_damage_unit, cTaskTypeAura, cBuildingClass, 0);
    xsTask(aura_damage_unit, cTaskTypeAura, cVillagerClass, 0);
    xsTask(aura_damage_unit, cTaskTypeAura, cInfantryClass, 0);
    xsTask(aura_damage_unit, cTaskTypeAura, cForageBushClass, 0);
    xsTask(aura_damage_unit, cTaskTypeAura, cStoneMineClass, 0);
    xsTask(aura_damage_unit, cTaskTypeAura, cPreyAnimalClass, 0);
    xsTask(aura_damage_unit, cTaskTypeAura, cPredatorAnimalClass, 0);
    xsTask(aura_damage_unit, cTaskTypeAura, cMiscellaneousClass, 0);
    xsTask(aura_damage_unit, cTaskTypeAura, cCavalryClass, 0);
    xsTask(aura_damage_unit, cTaskTypeAura, cSiegeWeaponClass, 0);
    xsTask(aura_damage_unit, cTaskTypeAura, cTerrainClass, 0);
    xsTask(aura_damage_unit, cTaskTypeAura, cTreeClass, 0);
    xsTask(aura_damage_unit, cTaskTypeAura, cTreeStumpClass, 0);
    xsTask(aura_damage_unit, cTaskTypeAura, cHealerClass, 0);
    xsTask(aura_damage_unit, cTaskTypeAura, cMonkClass, 0);
    xsTask(aura_damage_unit, cTaskTypeAura, cTradeCartClass, 0);
    xsTask(aura_damage_unit, cTaskTypeAura, cTransportShipClass, 0);
    xsTask(aura_damage_unit, cTaskTypeAura, cFishingBoatClass, 0);
    xsTask(aura_damage_unit, cTaskTypeAura, cWarshipClass, 0);
    xsTask(aura_damage_unit, cTaskTypeAura, cConquistadorClass, 0);
    xsTask(aura_damage_unit, cTaskTypeAura, cWarElephantClass, 0);
    xsTask(aura_damage_unit, cTaskTypeAura, cHeroClass, 0);
    xsTask(aura_damage_unit, cTaskTypeAura, cElephantArcherClass, 0);
    xsTask(aura_damage_unit, cTaskTypeAura, cWallClass, 0);
    xsTask(aura_damage_unit, cTaskTypeAura, cPhalanxClass, 0);
    xsTask(aura_damage_unit, cTaskTypeAura, cDomesticAnimalClass, 0);
    xsTask(aura_damage_unit, cTaskTypeAura, cFlagClass, 0);
    xsTask(aura_damage_unit, cTaskTypeAura, cDeepSeaFishClass, 0);
    xsTask(aura_damage_unit, cTaskTypeAura, cGoldMine, 0);
    xsTask(aura_damage_unit, cTaskTypeAura, cShoreFish, 0);
    xsTask(aura_damage_unit, cTaskTypeAura, cPetardClass, 0);
    xsTask(aura_damage_unit, cTaskTypeAura, cCavalryArcherClass, 0);
    xsTask(aura_damage_unit, cTaskTypeAura, cDoppelgangerClass, 0);
    xsTask(aura_damage_unit, cTaskTypeAura, cBirdClass, 0);
    xsTask(aura_damage_unit, cTaskTypeAura, cGateClass, 0);
    xsTask(aura_damage_unit, cTaskTypeAura, cSalvagePileClass, 0);
    xsTask(aura_damage_unit, cTaskTypeAura, cResourcePileClass, 0);
    xsTask(aura_damage_unit, cTaskTypeAura, cMonkWithRelicClass, 0);
    xsTask(aura_damage_unit, cTaskTypeAura, cHandCannoneerClass, 0);
    xsTask(aura_damage_unit, cTaskTypeAura, cTwoHandedSwordsmanClass, 0);
    xsTask(aura_damage_unit, cTaskTypeAura, cPikemanClass, 0);
    xsTask(aura_damage_unit, cTaskTypeAura, cScoutCavalryClass, 0);
    xsTask(aura_damage_unit, cTaskTypeAura, cOreMineClass, 0);
    xsTask(aura_damage_unit, cTaskTypeAura, cFarmClass, 0);
    xsTask(aura_damage_unit, cTaskTypeAura, cSpearmanClass, 0);
    xsTask(aura_damage_unit, cTaskTypeAura, cPackedUnitClass, 0);
    xsTask(aura_damage_unit, cTaskTypeAura, cTowerClass, 0);
    xsTask(aura_damage_unit, cTaskTypeAura, cBoardingShipClass, 0);
    xsTask(aura_damage_unit, cTaskTypeAura, cUnpackedSiegeUnitClass, 0);
    xsTask(aura_damage_unit, cTaskTypeAura, cScorpionClass, 0);
    xsTask(aura_damage_unit, cTaskTypeAura, cRaiderClass, 0);
    xsTask(aura_damage_unit, cTaskTypeAura, cCavalryRaiderClass, 0);
    xsTask(aura_damage_unit, cTaskTypeAura, cLivestockClass, 0);
    xsTask(aura_damage_unit, cTaskTypeAura, cKingClass, 0);
    xsTask(aura_damage_unit, cTaskTypeAura, cMiscBuildingClass, 0);
    xsTask(aura_damage_unit, cTaskTypeAura, cControlledAnimalClass, 0);
    xsTask(aura_damage_unit, cTaskTypeAura, cGoldFishClass, 0);
    xsTask(aura_damage_unit, cTaskTypeAura, cLandMineClass, 0);
}

void flag_stats(){
    xsEffectAmount(cSetAttribute, barricade_a_flag, cUnitSizeX, 1, 0);
    xsEffectAmount(cSetAttribute, barricade_a_flag, cUnitSizeY, 1, 0);
    xsEffectAmount(cSetAttribute, barricade_a_flag, cUnitSizeZ, 1, 0);
    xsEffectAmount(cSetAttribute, barricade_a_flag, cStandingGraphic, 10373, 0);
    xsEffectAmount(cSetAttribute, barricade_a_flag, cDyingGraphic, 4394, 0);    

    xsEffectAmount(cSetAttribute, barricade_d_flag, cUnitSizeX, 1, 0);
    xsEffectAmount(cSetAttribute, barricade_d_flag, cUnitSizeY, 1, 0);
    xsEffectAmount(cSetAttribute, barricade_d_flag, cUnitSizeZ, 1, 0);
    xsEffectAmount(cSetAttribute, barricade_d_flag, cStandingGraphic, 10376, 0);
    xsEffectAmount(cSetAttribute, barricade_d_flag, cDyingGraphic, 4397, 0);    
    
    xsEffectAmount(cSetAttribute, waterfall_flag, cStandingGraphic, 7569, 0);

    xsEffectAmount(cSetAttribute, smoke_flag, cHitpoints, 15, 0);
    xsEffectAmount(cSetAttribute, smoke_flag, cStandingGraphic, 12185, 0);
    xsEffectAmount(cSetAttribute, smoke_flag, cDeadUnitId, smoke_flag, 0);
}

void buildings_on_land_and_beach(){
    xsEffectAmount(cSetAttribute, cBuildingClass, cTerrainTable, 10);
    xsEffectAmount(cSetAttribute, cWallClass, cTerrainTable, 10);
    xsEffectAmount(cSetAttribute, cTowerClass, cTerrainTable, 10);
    xsEffectAmount(cSetAttribute, cFarmClass, cTerrainTable, 10);
    xsEffectAmount(cSetAttribute, cGateClass, cTerrainTable, 10);
    //FISH TRAP
    xsEffectAmount(cSetAttribute, 199, cTerrainTable, 13);
    
    //DOCKS
    xsEffectAmount(cSetAttribute, 45, cTerrainTable, 6);
    xsEffectAmount(cSetAttribute, 47, cTerrainTable, 6);
    xsEffectAmount(cSetAttribute, 51, cTerrainTable, 6);
    xsEffectAmount(cSetAttribute, 133, cTerrainTable, 6);
    xsEffectAmount(cSetAttribute, 805, cTerrainTable, 6);
    xsEffectAmount(cSetAttribute, 806, cTerrainTable, 6);
    xsEffectAmount(cSetAttribute, 807, cTerrainTable, 6);
    xsEffectAmount(cSetAttribute, 808, cTerrainTable, 6);
    xsEffectAmount(cSetAttribute, 2120, cTerrainTable, 6);
    xsEffectAmount(cSetAttribute, 2121, cTerrainTable, 6);
    xsEffectAmount(cSetAttribute, 2122, cTerrainTable, 6);
    xsEffectAmount(cSetAttribute, 2144, cTerrainTable, 6);
    xsEffectAmount(cSetAttribute, 2145, cTerrainTable, 6);
    xsEffectAmount(cSetAttribute, 2146, cTerrainTable, 6);
    xsEffectAmount(cSetAttribute, 2173, cTerrainTable, 6);
    xsEffectAmount(cSetAttribute, 1189, cTerrainTable, 6);
    xsEffectAmount(cSetAttribute, 446, cTerrainTable, 6);
    xsEffectAmount(cSetAttribute, 2141, cTerrainTable, 6);
    xsEffectAmount(cSetAttribute, 2142, cTerrainTable, 6);
    xsEffectAmount(cSetAttribute, 2143, cTerrainTable, 6);
    xsEffectAmount(cSetAttribute, 2172, cTerrainTable, 6);
    xsEffectAmount(cSetAttribute, 2117, cTerrainTable, 6);
    xsEffectAmount(cSetAttribute, 2118, cTerrainTable, 6);
    xsEffectAmount(cSetAttribute, 2119, cTerrainTable, 6);
}

void buildings_on_land_no_beach(){
    xsEffectAmount(cSetAttribute, cBuildingClass, cTerrainTable, 4);
    xsEffectAmount(cSetAttribute, cTowerClass, cTerrainTable, 4);
    xsEffectAmount(cSetAttribute, cFarmClass, cTerrainTable, 4);
    //FISH TRAP
    xsEffectAmount(cSetAttribute, 199, cTerrainTable, 13);

    //DOCKS
    xsEffectAmount(cSetAttribute, 45, cTerrainTable, 6);
    xsEffectAmount(cSetAttribute, 47, cTerrainTable, 6);
    xsEffectAmount(cSetAttribute, 51, cTerrainTable, 6);
    xsEffectAmount(cSetAttribute, 133, cTerrainTable, 6);
    xsEffectAmount(cSetAttribute, 805, cTerrainTable, 6);
    xsEffectAmount(cSetAttribute, 806, cTerrainTable, 6);
    xsEffectAmount(cSetAttribute, 807, cTerrainTable, 6);
    xsEffectAmount(cSetAttribute, 808, cTerrainTable, 6);
    xsEffectAmount(cSetAttribute, 2120, cTerrainTable, 6);
    xsEffectAmount(cSetAttribute, 2121, cTerrainTable, 6);
    xsEffectAmount(cSetAttribute, 2122, cTerrainTable, 6);
    xsEffectAmount(cSetAttribute, 2144, cTerrainTable, 6);
    xsEffectAmount(cSetAttribute, 2145, cTerrainTable, 6);
    xsEffectAmount(cSetAttribute, 2146, cTerrainTable, 6);
    xsEffectAmount(cSetAttribute, 2173, cTerrainTable, 6);
    xsEffectAmount(cSetAttribute, 1189, cTerrainTable, 6);
    xsEffectAmount(cSetAttribute, 446, cTerrainTable, 6);
    xsEffectAmount(cSetAttribute, 2141, cTerrainTable, 6);
    xsEffectAmount(cSetAttribute, 2142, cTerrainTable, 6);
    xsEffectAmount(cSetAttribute, 2143, cTerrainTable, 6);
    xsEffectAmount(cSetAttribute, 2172, cTerrainTable, 6);
    xsEffectAmount(cSetAttribute, 2117, cTerrainTable, 6);
    xsEffectAmount(cSetAttribute, 2118, cTerrainTable, 6);
    xsEffectAmount(cSetAttribute, 2119, cTerrainTable, 6);
}

void units_land_no_beach(){
    xsEffectAmount(cSetAttribute, cArcherClass, cTerrainTable, 40);
	xsEffectAmount(cSetAttribute, cVillagerClass, cTerrainTable, 40);
	xsEffectAmount(cSetAttribute, cInfantryClass, cTerrainTable, 40);
	xsEffectAmount(cSetAttribute, cCavalryClass, cTerrainTable, 40);
	xsEffectAmount(cSetAttribute, cSiegeWeaponClass, cTerrainTable, 40);
	xsEffectAmount(cSetAttribute, cMonkClass, cTerrainTable, 40);
	xsEffectAmount(cSetAttribute, cTradeCartClass, cTerrainTable, 40);
	xsEffectAmount(cSetAttribute, cConquistadorClass, cTerrainTable, 40);
	xsEffectAmount(cSetAttribute, cWarElephantClass, cTerrainTable, 40);
	xsEffectAmount(cSetAttribute, cHeroClass, cTerrainTable, 40);
	xsEffectAmount(cSetAttribute, cElephantArcherClass, cTerrainTable, 40);
	xsEffectAmount(cSetAttribute, cPetardClass, cTerrainTable, 40);
	xsEffectAmount(cSetAttribute, cCavalryArcherClass, cTerrainTable, 40);
	xsEffectAmount(cSetAttribute, cMonkWithRelicClass, cTerrainTable, 40);
	xsEffectAmount(cSetAttribute, cHandCannoneerClass, cTerrainTable, 40);
	xsEffectAmount(cSetAttribute, cScoutCavalryClass, cTerrainTable, 40);
	xsEffectAmount(cSetAttribute, cPackedUnitClass, cTerrainTable, 40);
	xsEffectAmount(cSetAttribute, cUnpackedSiegeUnitClass, cTerrainTable, 40);
	xsEffectAmount(cSetAttribute, cScorpionClass, cTerrainTable, 40);
	xsEffectAmount(cSetAttribute, cLivestockClass, cTerrainTable, 40);
	xsEffectAmount(cSetAttribute, cKingClass, cTerrainTable, 40);
	xsEffectAmount(cSetAttribute, cControlledAnimalClass, cTerrainTable, 40);
}

void main(){
    bridge_stats();
    aura_damage();
    flag_stats();
}