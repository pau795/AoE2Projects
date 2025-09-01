const int vertical_bridge_unit = 7;
const int horizontal_bridge_unit = 6;

const int vertical_chain_fixed_unit = 1049;
const int horizontal_chain_fixed_unit = 1048;

const int vertical_chain_intermediate_unit = 601;
const int horizontal_chain_intermediate_unit = 600;


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
    //BIDGE AB PIECE
    xsEffectAmount(cSetAttribute, 1842, cStandingGraphic, 0, 3);
    xsEffectAmount(cSetAttribute, 1842, cFoundationTerrain, 1, 3);
    //FIXED CHAINS
    xsEffectAmount(cSetAttribute, vertical_chain_fixed_unit, cTerrainTable, 0, 0);
    xsEffectAmount(cSetAttribute, vertical_chain_fixed_unit, cStandingGraphic, 2326, 0);
    xsEffectAmount(cSetAttribute, vertical_chain_fixed_unit, cUnitSizeX, 1, 0);
    xsEffectAmount(cSetAttribute, vertical_chain_fixed_unit, cUnitSizeY, 0.5, 0);
    xsEffectAmount(cSetAttribute, vertical_chain_fixed_unit, cUnitSizeZ, 4, 0);

    xsEffectAmount(cSetAttribute, horizontal_chain_fixed_unit, cTerrainTable, 0, 0);
    xsEffectAmount(cSetAttribute, horizontal_chain_fixed_unit, cStandingGraphic, 2328, 0);
    xsEffectAmount(cSetAttribute, horizontal_chain_fixed_unit, cUnitSizeX, 0.5, 0);
    xsEffectAmount(cSetAttribute, horizontal_chain_fixed_unit, cUnitSizeY, 1, 0);
    xsEffectAmount(cSetAttribute, horizontal_chain_fixed_unit, cUnitSizeZ, 4, 0);

    //INTERMEDIATE CHAINS
    xsEffectAmount(cSetAttribute, vertical_chain_intermediate_unit, cTerrainTable, 0, 0);
    xsEffectAmount(cSetAttribute, vertical_chain_intermediate_unit, cStandingGraphic, 0, 0);
    xsEffectAmount(cSetAttribute, vertical_chain_intermediate_unit, cUnitSizeX, 1, 0);
    xsEffectAmount(cSetAttribute, vertical_chain_intermediate_unit, cUnitSizeY, 0.5, 0);
    xsEffectAmount(cSetAttribute, vertical_chain_intermediate_unit, cUnitSizeZ, 0, 0);

    xsEffectAmount(cSetAttribute, horizontal_chain_intermediate_unit, cTerrainTable, 0, 0);
    xsEffectAmount(cSetAttribute, horizontal_chain_intermediate_unit, cStandingGraphic, 0, 0);
    xsEffectAmount(cSetAttribute, horizontal_chain_intermediate_unit, cUnitSizeX, 0.5, 0);
    xsEffectAmount(cSetAttribute, horizontal_chain_intermediate_unit, cUnitSizeY, 1, 0);
    xsEffectAmount(cSetAttribute, horizontal_chain_intermediate_unit, cUnitSizeZ, 0, 0);

    //MOVING BRIDGE
    xsEffectAmount(cSetAttribute, horizontal_bridge_unit, cTerrainTable, 0, 3);
    xsEffectAmount(cSetAttribute, horizontal_bridge_unit, cInteractionMode, 0, 3);
    xsEffectAmount(cSetAttribute, horizontal_bridge_unit, cUnitSizeX, 0, 3);
    xsEffectAmount(cSetAttribute, horizontal_bridge_unit, cUnitSizeY, 0, 3);
    xsEffectAmount(cSetAttribute, horizontal_bridge_unit, cUnitSizeZ, 0, 3);
    xsEffectAmount(cSetAttribute, horizontal_bridge_unit, cFogFlag, 1, 3);
    xsEffectAmount(cSetAttribute, horizontal_bridge_unit, cMovementSpeed, 0.5, 3);
    xsEffectAmount(cSetAttribute, horizontal_bridge_unit, cOcclusionMode, 0, 3);
    xsEffectAmount(cSetAttribute, horizontal_bridge_unit, cHitpoints, 20000, 3);
    xsEffectAmount(cSetAttribute, horizontal_bridge_unit, cInvulnerabilityLevel, -20000, 3);
    xsEffectAmount(cSetAttribute, horizontal_bridge_unit, cStandingGraphic, 8233, 3);
    xsEffectAmount(cSetAttribute, horizontal_bridge_unit, cWalkingGraphic, 8233, 3);

    xsEffectAmount(cSetAttribute, vertical_bridge_unit, cTerrainTable, 0, 3);
    xsEffectAmount(cSetAttribute, vertical_bridge_unit, cInteractionMode, 0, 3);
    xsEffectAmount(cSetAttribute, vertical_bridge_unit, cUnitSizeX, 0, 3);
    xsEffectAmount(cSetAttribute, vertical_bridge_unit, cUnitSizeY, 0, 3);
    xsEffectAmount(cSetAttribute, vertical_bridge_unit, cUnitSizeZ, 0, 3);
    xsEffectAmount(cSetAttribute, vertical_bridge_unit, cFogFlag, 1, 3);
    xsEffectAmount(cSetAttribute, vertical_bridge_unit, cMovementSpeed, 0.5, 3);
    xsEffectAmount(cSetAttribute, vertical_bridge_unit, cOcclusionMode, 0, 3);
    xsEffectAmount(cSetAttribute, vertical_bridge_unit, cHitpoints, 20000, 3);
    xsEffectAmount(cSetAttribute, vertical_bridge_unit, cInvulnerabilityLevel, -20000, 3);
    xsEffectAmount(cSetAttribute, vertical_bridge_unit, cStandingGraphic, 8227, 3);
    xsEffectAmount(cSetAttribute, vertical_bridge_unit, cWalkingGraphic, 8227, 3);

}
