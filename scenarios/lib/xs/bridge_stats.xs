const int mobile_vertical_bridge_piece_unit = 7; //Skirmisher
const int mobile_horizontal_bridge_piece_unit = 6; //Elite Skirmisher

const int mobile_vertical_bridge_wall_unit = 93; //Spearman
const int mobile_horizontal_bridge_wall_unit = 358; //Pikeman

const int fixed_vertical_bridge_wall_unit = 1062; //Fence
const int fixed_horizontal_bridge_wall_unit = 72; //Palisade

const int horizontal_sea_gate = 1383;
const int vertical_sea_gate = 1379;


void bridge_stats(){
    //WOODEN BRIDGE
    xsEffectAmount(cSetAttribute, 1309, cFoundationTerrain, -1, 3);
    xsEffectAmount(cSetAttribute, 1310, cFoundationTerrain, -1, 3);
    xsEffectAmount(cSetAttribute, 1311, cFoundationTerrain, -1, 3);
    xsEffectAmount(cSetAttribute, 1312, cFoundationTerrain, -1, 3);
    xsEffectAmount(cSetAttribute, 1313, cFoundationTerrain, -1, 3);
    xsEffectAmount(cSetAttribute, 1314, cFoundationTerrain, -1, 3);

    xsEffectAmount(cSetAttribute, 1309, cOcclusionMode, 0, 3);
    xsEffectAmount(cSetAttribute, 1310, cOcclusionMode, 0, 3);
    xsEffectAmount(cSetAttribute, 1311, cOcclusionMode, 0, 3);
    xsEffectAmount(cSetAttribute, 1312, cOcclusionMode, 0, 3);
    xsEffectAmount(cSetAttribute, 1313, cOcclusionMode, 0, 3);
    xsEffectAmount(cSetAttribute, 1314, cOcclusionMode, 0, 3);

    xsEffectAmount(cSetAttribute, 1309, cLineOfSight, 0, 3);
    xsEffectAmount(cSetAttribute, 1310, cLineOfSight, 0, 3);
    xsEffectAmount(cSetAttribute, 1311, cLineOfSight, 0, 3);
    xsEffectAmount(cSetAttribute, 1312, cLineOfSight, 0, 3);
    xsEffectAmount(cSetAttribute, 1313, cLineOfSight, 0, 3);
    xsEffectAmount(cSetAttribute, 1314, cLineOfSight, 0, 3);


    // BRIDGE WALLS AND GATES
    xsEffectAmount(cSetAttribute, fixed_vertical_bridge_wall_unit, cTerrainTable, 0, 3);
    xsEffectAmount(cSetAttribute, fixed_vertical_bridge_wall_unit, cHitpoints, 20000, 3);
    xsEffectAmount(cSetAttribute, fixed_vertical_bridge_wall_unit, cInvulnerabilityLevel, -20000, 3);
    xsEffectAmount(cSetAttribute, fixed_vertical_bridge_wall_unit, cFoundationTerrain, -1, 3);
    xsEffectAmount(cSetAttribute, fixed_vertical_bridge_wall_unit, cStandingGraphic, 9401, 3);
    xsEffectAmount(cSetAttribute, fixed_vertical_bridge_wall_unit, cTrainTime, 0, 3);
    xsEffectAmount(cSetAttribute, fixed_vertical_bridge_wall_unit, cLineOfSight, 0, 3);

    xsEffectAmount(cSetAttribute, fixed_horizontal_bridge_wall_unit, cTerrainTable, 0, 3);
    xsEffectAmount(cSetAttribute, fixed_horizontal_bridge_wall_unit, cHitpoints, 20000, 3);
    xsEffectAmount(cSetAttribute, fixed_horizontal_bridge_wall_unit, cInvulnerabilityLevel, -20000, 3);
    xsEffectAmount(cSetAttribute, fixed_horizontal_bridge_wall_unit, cFoundationTerrain, -1, 3);
    xsEffectAmount(cSetAttribute, fixed_horizontal_bridge_wall_unit, cStandingGraphic, 9400, 3);
    xsEffectAmount(cSetAttribute, fixed_horizontal_bridge_wall_unit, cTrainTime, 0, 3);
    xsEffectAmount(cSetAttribute, fixed_horizontal_bridge_wall_unit, cLineOfSight, 0, 3);

    xsEffectAmount(cSetAttribute, horizontal_sea_gate, cTerrainTable, 0, 3);
    xsEffectAmount(cSetAttribute, horizontal_sea_gate, cHitpoints, 20000, 3);
    xsEffectAmount(cSetAttribute, horizontal_sea_gate, cInvulnerabilityLevel, -20000, 3);
    xsEffectAmount(cSetAttribute, horizontal_sea_gate, cFoundationTerrain, -1, 3);
    xsEffectAmount(cSetAttribute, horizontal_sea_gate, cTrainTime, 0, 3);
    xsEffectAmount(cSetAttribute, horizontal_sea_gate, cLineOfSight, 0, 3);

    xsEffectAmount(cSetAttribute, vertical_sea_gate, cTerrainTable, 0, 3);
    xsEffectAmount(cSetAttribute, vertical_sea_gate, cHitpoints, 20000, 3);
    xsEffectAmount(cSetAttribute, vertical_sea_gate, cInvulnerabilityLevel, -20000, 3);
    xsEffectAmount(cSetAttribute, vertical_sea_gate, cFoundationTerrain, -1, 3);
    xsEffectAmount(cSetAttribute, vertical_sea_gate, cTrainTime, 0, 3);
    xsEffectAmount(cSetAttribute, vertical_sea_gate, cLineOfSight, 0, 3);

    //ANNEX GATES
    xsEffectAmount(cSetAttribute, 1380, cLineOfSight, 0, 3);
    xsEffectAmount(cSetAttribute, 1381, cLineOfSight, 0, 3);
    xsEffectAmount(cSetAttribute, 1382, cLineOfSight, 0, 3);
    xsEffectAmount(cSetAttribute, 1384, cLineOfSight, 0, 3);
    xsEffectAmount(cSetAttribute, 1385, cLineOfSight, 0, 3);
    xsEffectAmount(cSetAttribute, 1386, cLineOfSight, 0, 3);    



    //MOVING BRIDGE PIECE
    xsEffectAmount(cSetAttribute, mobile_vertical_bridge_piece_unit, cTerrainTable, 0, 3);
    xsEffectAmount(cSetAttribute, mobile_vertical_bridge_piece_unit, cInteractionMode, 0, 3);
    xsEffectAmount(cSetAttribute, mobile_vertical_bridge_piece_unit, cUnitSizeX, 0, 3);
    xsEffectAmount(cSetAttribute, mobile_vertical_bridge_piece_unit, cUnitSizeY, 0, 3);
    xsEffectAmount(cSetAttribute, mobile_vertical_bridge_piece_unit, cUnitSizeZ, 0, 3);
    xsEffectAmount(cSetAttribute, mobile_vertical_bridge_piece_unit, cFogFlag, 1, 3);
    xsEffectAmount(cSetAttribute, mobile_vertical_bridge_piece_unit, cLineOfSight, 0, 3);
    xsEffectAmount(cSetAttribute, mobile_vertical_bridge_piece_unit, cMovementSpeed, 0.5, 3);
    xsEffectAmount(cSetAttribute, mobile_vertical_bridge_piece_unit, cOcclusionMode, 0, 3);
    xsEffectAmount(cSetAttribute, mobile_vertical_bridge_piece_unit, cHitpoints, 20000, 3);
    xsEffectAmount(cSetAttribute, mobile_vertical_bridge_piece_unit, cInvulnerabilityLevel, -20000, 3);
    xsEffectAmount(cSetAttribute, mobile_vertical_bridge_piece_unit, cStandingGraphic, 8227, 3);
    xsEffectAmount(cSetAttribute, mobile_vertical_bridge_piece_unit, cWalkingGraphic, 8227, 3);

    xsEffectAmount(cSetAttribute, mobile_horizontal_bridge_piece_unit, cTerrainTable, 0, 3);
    xsEffectAmount(cSetAttribute, mobile_horizontal_bridge_piece_unit, cInteractionMode, 0, 3);
    xsEffectAmount(cSetAttribute, mobile_horizontal_bridge_piece_unit, cUnitSizeX, 0, 3);
    xsEffectAmount(cSetAttribute, mobile_horizontal_bridge_piece_unit, cUnitSizeY, 0, 3);
    xsEffectAmount(cSetAttribute, mobile_horizontal_bridge_piece_unit, cUnitSizeZ, 0, 3);
    xsEffectAmount(cSetAttribute, mobile_horizontal_bridge_piece_unit, cFogFlag, 1, 3);
    xsEffectAmount(cSetAttribute, mobile_horizontal_bridge_piece_unit, cLineOfSight, 0, 3);
    xsEffectAmount(cSetAttribute, mobile_horizontal_bridge_piece_unit, cMovementSpeed, 0.5, 3);
    xsEffectAmount(cSetAttribute, mobile_horizontal_bridge_piece_unit, cOcclusionMode, 0, 3);
    xsEffectAmount(cSetAttribute, mobile_horizontal_bridge_piece_unit, cHitpoints, 20000, 3);
    xsEffectAmount(cSetAttribute, mobile_horizontal_bridge_piece_unit, cInvulnerabilityLevel, -20000, 3);
    xsEffectAmount(cSetAttribute, mobile_horizontal_bridge_piece_unit, cStandingGraphic, 8233, 3);
    xsEffectAmount(cSetAttribute, mobile_horizontal_bridge_piece_unit, cWalkingGraphic, 8233, 3);

    //MOVING BRIDGE WALL
    xsEffectAmount(cSetAttribute, mobile_vertical_bridge_wall_unit, cTerrainTable, 0, 3);
    xsEffectAmount(cSetAttribute, mobile_vertical_bridge_wall_unit, cInteractionMode, 0, 3);
    xsEffectAmount(cSetAttribute, mobile_vertical_bridge_wall_unit, cUnitSizeX, 0, 3);
    xsEffectAmount(cSetAttribute, mobile_vertical_bridge_wall_unit, cUnitSizeY, 0, 3);
    xsEffectAmount(cSetAttribute, mobile_vertical_bridge_wall_unit, cUnitSizeZ, 0, 3);
    xsEffectAmount(cSetAttribute, mobile_vertical_bridge_wall_unit, cFogFlag, 1, 3);
    xsEffectAmount(cSetAttribute, mobile_vertical_bridge_wall_unit, cLineOfSight, 0, 3);
    xsEffectAmount(cSetAttribute, mobile_vertical_bridge_wall_unit, cMovementSpeed, 0.5, 3);
    xsEffectAmount(cSetAttribute, mobile_vertical_bridge_wall_unit, cOcclusionMode, 0, 3);
    xsEffectAmount(cSetAttribute, mobile_vertical_bridge_wall_unit, cHitpoints, 20000, 3);
    xsEffectAmount(cSetAttribute, mobile_vertical_bridge_wall_unit, cInvulnerabilityLevel, -20000, 3);
    xsEffectAmount(cSetAttribute, mobile_vertical_bridge_wall_unit, cStandingGraphic, 9401, 3);
    xsEffectAmount(cSetAttribute, mobile_vertical_bridge_wall_unit, cWalkingGraphic, 9401, 3);    

    xsEffectAmount(cSetAttribute, mobile_horizontal_bridge_wall_unit, cTerrainTable, 0, 3);
    xsEffectAmount(cSetAttribute, mobile_horizontal_bridge_wall_unit, cInteractionMode, 0, 3);
    xsEffectAmount(cSetAttribute, mobile_horizontal_bridge_wall_unit, cUnitSizeX, 0, 3);
    xsEffectAmount(cSetAttribute, mobile_horizontal_bridge_wall_unit, cUnitSizeY, 0, 3);
    xsEffectAmount(cSetAttribute, mobile_horizontal_bridge_wall_unit, cUnitSizeZ, 0, 3);
    xsEffectAmount(cSetAttribute, mobile_horizontal_bridge_wall_unit, cFogFlag, 1, 3);
    xsEffectAmount(cSetAttribute, mobile_horizontal_bridge_wall_unit, cLineOfSight, 0, 3);
    xsEffectAmount(cSetAttribute, mobile_horizontal_bridge_wall_unit, cMovementSpeed, 0.5, 3);
    xsEffectAmount(cSetAttribute, mobile_horizontal_bridge_wall_unit, cOcclusionMode, 0, 3);
    xsEffectAmount(cSetAttribute, mobile_horizontal_bridge_wall_unit, cHitpoints, 20000, 3);
    xsEffectAmount(cSetAttribute, mobile_horizontal_bridge_wall_unit, cInvulnerabilityLevel, -20000, 3);
    xsEffectAmount(cSetAttribute, mobile_horizontal_bridge_wall_unit, cStandingGraphic, 9400, 3);
    xsEffectAmount(cSetAttribute, mobile_horizontal_bridge_wall_unit, cWalkingGraphic, 9400, 3);

}
