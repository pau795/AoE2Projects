const int snow_leopard = 1241;



void unit_stats(int unit_id = 0, int player = 0){
    xsEffectAmount(cSetAttribute, unit_id, cHitpoints, 20000, player);
    xsEffectAmount(cSetAttribute, unit_id, cInvulnerabilityLevel, -20000, player);
    xsEffectAmount(cSetAttribute, unit_id, cUnitSizeZ, 0, player);    
    xsEffectAmount(cSetAttribute, unit_id, cStandingGraphic, 5314, player);
    xsEffectAmount(cSetAttribute, unit_id, cWalkingGraphic, 5314, player);
    xsEffectAmount(cSetAttribute, unit_id, cAttackGraphic, 5314, player);
    xsEffectAmount(cSetAttribute, unit_id, cMovementSpeed, 5, player);
    xsEffectAmount(cSetAttribute, unit_id, cTerrainTable, 0, player);
    xsEffectAmount(cSetAttribute, unit_id, cFogFlag, 1, player);
    xsEffectAmount(cSetAttribute, unit_id, cDeadUnitId, -1, player);
    xsEffectAmount(cSetAttribute, unit_id, cCombatAbility, 32, player);
    
    xsTaskAmount(cTaskAttrWorkValue1, 3);
    xsTaskAmount(cTaskAttrWorkValue2, 1);
    xsTaskAmount(cTaskAttrWorkRange, 2);
    xsTaskAmount(cTaskAttrSearchWaitTime, 5);
    xsTaskAmount(cTaskAttrCombatLevelFlag, 7);
    xsTaskAmount(cTaskAttrOwnerType, 0);

    xsTask(unit_id, cTaskTypeAura, cArcherClass, 0);
    xsTask(unit_id, cTaskTypeAura, cArtifactClass, 0);
    xsTask(unit_id, cTaskTypeAura, cTradeBoatClass, 0);
    xsTask(unit_id, cTaskTypeAura, cVillagerClass, 0);
    xsTask(unit_id, cTaskTypeAura, cInfantryClass, 0);
    xsTask(unit_id, cTaskTypeAura, cMiscellaneousClass, 0);
    xsTask(unit_id, cTaskTypeAura, cCavalryClass, 0);
    xsTask(unit_id, cTaskTypeAura, cSiegeWeaponClass, 0);
    xsTask(unit_id, cTaskTypeAura, cHealerClass, 0);
    xsTask(unit_id, cTaskTypeAura, cMonkClass, 0);
    xsTask(unit_id, cTaskTypeAura, cTradeCartClass, 0);
    xsTask(unit_id, cTaskTypeAura, cTransportShipClass, 0);
    xsTask(unit_id, cTaskTypeAura, cFishingBoatClass, 0);
    xsTask(unit_id, cTaskTypeAura, cWarshipClass, 0);
    xsTask(unit_id, cTaskTypeAura, cConquistadorClass, 0);
    xsTask(unit_id, cTaskTypeAura, cWarElephantClass, 0);
    xsTask(unit_id, cTaskTypeAura, cHeroClass, 0);
    xsTask(unit_id, cTaskTypeAura, cElephantArcherClass, 0);
    xsTask(unit_id, cTaskTypeAura, cPhalanxClass, 0);
    xsTask(unit_id, cTaskTypeAura, cDomesticAnimalClass, 0);
    xsTask(unit_id, cTaskTypeAura, cPetardClass, 0);
    xsTask(unit_id, cTaskTypeAura, cCavalryArcherClass, 0);
    xsTask(unit_id, cTaskTypeAura, cDoppelgangerClass, 0);
    xsTask(unit_id, cTaskTypeAura, cBirdClass, 0);
    xsTask(unit_id, cTaskTypeAura, cGateClass, 0);
    xsTask(unit_id, cTaskTypeAura, cSalvagePileClass, 0);
    xsTask(unit_id, cTaskTypeAura, cResourcePileClass, 0);
    xsTask(unit_id, cTaskTypeAura, cMonkWithRelicClass, 0);
    xsTask(unit_id, cTaskTypeAura, cHandCannoneerClass, 0);
    xsTask(unit_id, cTaskTypeAura, cTwoHandedSwordsmanClass, 0);
    xsTask(unit_id, cTaskTypeAura, cPikemanClass, 0);
    xsTask(unit_id, cTaskTypeAura, cScoutCavalryClass, 0);
    xsTask(unit_id, cTaskTypeAura, cSpearmanClass, 0);
    xsTask(unit_id, cTaskTypeAura, cPackedUnitClass, 0);
    xsTask(unit_id, cTaskTypeAura, cBoardingShipClass, 0);
    xsTask(unit_id, cTaskTypeAura, cUnpackedSiegeUnitClass, 0);
    xsTask(unit_id, cTaskTypeAura, cScorpionClass, 0);
    xsTask(unit_id, cTaskTypeAura, cRaiderClass, 0);
    xsTask(unit_id, cTaskTypeAura, cCavalryRaiderClass, 0);
    xsTask(unit_id, cTaskTypeAura, cLivestockClass, 0);
    xsTask(unit_id, cTaskTypeAura, cKingClass, 0);
    xsTask(unit_id, cTaskTypeAura, cControlledAnimalClass, 0);
}



void main(){    
    unit_stats(snow_leopard, 0);
}