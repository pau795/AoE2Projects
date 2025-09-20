const int beach_bridge = 1310;
const int shallow_water_bridge = 1313;
const int azure_water_bridge = 1314;


void bridge_stats(){
    xsEffectAmount(cSetAttribute, beach_bridge, cUnitSizeX, 0, 0);
    xsEffectAmount(cSetAttribute, beach_bridge, cUnitSizeY, 0, 0);
    xsEffectAmount(cSetAttribute, beach_bridge, cUnitSizeZ, 0, 0);
    xsEffectAmount(cSetAttribute, beach_bridge, cDyingGraphic, 5507, 0);
    xsEffectAmount(cSetAttribute, beach_bridge, cDeadUnitId, -1, 0);
    xsEffectAmount(cSetAttribute, beach_bridge, cFoundationTerrain, 2, 0);
    xsEffectAmount(cSetAttribute, beach_bridge, cStandingGraphic, 0, 0);

    xsEffectAmount(cSetAttribute, shallow_water_bridge, cUnitSizeX, 0, 0);
    xsEffectAmount(cSetAttribute, shallow_water_bridge, cUnitSizeY, 0, 0);
    xsEffectAmount(cSetAttribute, shallow_water_bridge, cUnitSizeZ, 0, 0);
    xsEffectAmount(cSetAttribute, shallow_water_bridge, cDyingGraphic, 5507, 0);
    xsEffectAmount(cSetAttribute, shallow_water_bridge, cDeadUnitId, -1, 0);
    xsEffectAmount(cSetAttribute, shallow_water_bridge, cFoundationTerrain, 1, 0);
    xsEffectAmount(cSetAttribute, shallow_water_bridge, cStandingGraphic, 0, 0);

    xsEffectAmount(cSetAttribute, azure_water_bridge, cUnitSizeX, 0, 0);
    xsEffectAmount(cSetAttribute, azure_water_bridge, cUnitSizeY, 0, 0);
    xsEffectAmount(cSetAttribute, azure_water_bridge, cUnitSizeZ, 0, 0);
    xsEffectAmount(cSetAttribute, azure_water_bridge, cDyingGraphic, 5507, 0);
    xsEffectAmount(cSetAttribute, azure_water_bridge, cDeadUnitId, -1, 0);
    xsEffectAmount(cSetAttribute, azure_water_bridge, cFoundationTerrain, 15, 0);
    xsEffectAmount(cSetAttribute, azure_water_bridge, cStandingGraphic, 0, 0);
}


void buildings_on_land_and_beach(){
    xsEffectAmount(cSetAttribute, cBuildingClass, cTerrainTable, 10);
    xsEffectAmount(cSetAttribute, cWallClass, cTerrainTable, 10);
    xsEffectAmount(cSetAttribute, cTowerClass, cTerrainTable, 10);
    xsEffectAmount(cSetAttribute, cFarmClass, cTerrainTable, 10);
    xsEffectAmount(cSetAttribute, cGateClass, cTerrainTable, 10);
    xsEffectAmount(cSetAttribute, cBuildingClass, cTerrainTable, 10);
    //FISH TRAP
    xsEffectAmount(cSetAttribute, 199, cTerrainTable, 13);
    
    //DOCKS
    xsEffectAmount(cSetAttribute, 45, cTerrainTable, 6);
    xsEffectAmount(cSetAttribute, 47, cTerrainTable, 6);
    xsEffectAmount(cSetAttribute, 51, cTerrainTable, 6);
    xsEffectAmount(cSetAttribute, 113, cTerrainTable, 6);
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
}

void buildings_on_land_no_beach(){
    xsEffectAmount(cSetAttribute, cBuildingClass, cTerrainTable, 7);
    xsEffectAmount(cSetAttribute, cWallClass, cTerrainTable, 7);
    xsEffectAmount(cSetAttribute, cTowerClass, cTerrainTable, 7);
    xsEffectAmount(cSetAttribute, cFarmClass, cTerrainTable, 7);
    xsEffectAmount(cSetAttribute, cGateClass, cTerrainTable, 7);
    xsEffectAmount(cSetAttribute, cBuildingClass, cTerrainTable, 7);
    
    //FISH TRAP
    xsEffectAmount(cSetAttribute, 199, cTerrainTable, 13);

    //DOCKS
    xsEffectAmount(cSetAttribute, 45, cTerrainTable, 6);
    xsEffectAmount(cSetAttribute, 47, cTerrainTable, 6);
    xsEffectAmount(cSetAttribute, 51, cTerrainTable, 6);
    xsEffectAmount(cSetAttribute, 113, cTerrainTable, 6);
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
}