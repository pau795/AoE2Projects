const int ryno  = 1139;
const int plague = 1103;
const int horse_a = 814;

const int rino_life_time = 60;
const int plague_life_time = 60;
const int plague_player = 3;
const int maxByte = 256;
const int stringers_task = 157;

void plague_stats(){

    xsEffectAmount(cSetAttribute, horse_a, cStandingGraphic, 0, plague_player);
    xsEffectAmount(cSetAttribute, horse_a, cWalkingGraphic, 0, plague_player);

    xsEffectAmount(cSetAttribute, ryno, cUnitSizeX, 0, 0);
    xsEffectAmount(cSetAttribute, ryno, cUnitSizeY, 0, 0);
    xsEffectAmount(cSetAttribute, ryno, cUnitSizeZ, 0, 0);
    xsEffectAmount(cSetAttribute, ryno, cAmountFirstStorage, 10, 0);
    xsEffectAmount(cSetAttribute, ryno, cHitpoints, rino_life_time, 0);

    xsEffectAmount(cSetAttribute, plague, cUnitSizeX, 0.1, plague_player);
    xsEffectAmount(cSetAttribute, plague, cUnitSizeY, 0.1, plague_player);
    xsEffectAmount(cSetAttribute, plague, cUnitSizeZ, 0, plague_player);
    xsEffectAmount(cSetAttribute, plague, cMaxRange, 0.5, plague_player);
    xsEffectAmount(cSetAttribute, plague, cProjectileUnit, -1, plague_player);
    xsEffectAmount(cSetAttribute, plague, cSecondaryProjectileUnit, -1, plague_player);
    xsEffectAmount(cSetAttribute, plague, cChargeProjectileUnit, -1, plague_player);
    xsEffectAmount(cSetAttribute, plague, cAttackDispersion, 0, plague_player);
    xsEffectAmount(cSetAttribute, plague, cTerrainTable, 0, plague_player);
    xsEffectAmount(cSetAttribute, plague, cAccuracyPercent, 100, plague_player);
    xsEffectAmount(cSetAttribute, plague, cStandingGraphic, 10632, plague_player);
    xsEffectAmount(cSetAttribute, plague, cWalkingGraphic, 10632, plague_player);
    xsEffectAmount(cSetAttribute, plague, cDyingGraphic, 10632, plague_player);
    xsEffectAmount(cSetAttribute, plague, cAttackGraphic, 10632, plague_player);
    xsEffectAmount(cSetAttribute, plague, cAttack2Graphic, 10632, plague_player);
    xsEffectAmount(cSetAttribute, plague, cHitpoints, plague_life_time + rino_life_time, plague_player);
    xsEffectAmount(cSetAttribute, plague, cMovementSpeed, 0.8, plague_player);
    xsEffectAmount(cSetAttribute, plague, cBlastAttackLevel, 2, plague_player);
    xsEffectAmount(cSetAttribute, plague, cAttack, 29 * maxByte + 0 , plague_player);
    xsEffectAmount(cSetAttribute, plague, cAttack, 11 * maxByte + 0 , plague_player);
    xsEffectAmount(cSetAttribute, plague, cAttack, 16 * maxByte + 0 , plague_player);
    xsEffectAmount(cSetAttribute, plague, cAttack, 2 * maxByte + 0 , plague_player);    
    xsEffectAmount(cSetAttribute, plague, cAttack, 3 * maxByte + 0 , plague_player);
    xsEffectAmount(cSetAttribute, plague, cAttack, 34 * maxByte + 0 , plague_player);
    xsEffectAmount(cSetAttribute, plague, cAttack, 4 * maxByte + 3 , plague_player);
    xsEffectAmount(cSetAttribute, plague, cAttackPriority, 1, plague_player);
    xsEffectAmount(cSetAttribute, plague, cAttackReloadTime, 5, plague_player);
    xsEffectAmount(cSetAttribute, plague, cCombatAbility, 1 + 128, plague_player);
    xsEffectAmount(cSetAttribute, plague, cFormationCategory, 1, plague_player);
    xsEffectAmount(cSetAttribute, plague, cLineOfSight, 4, plague_player);
    xsEffectAmount(cSetAttribute, plague, cSearchRadius, 4, plague_player);
    xsEffectAmount(cSetAttribute, plague, cFogFlag, 1, plague_player);
    xsEffectAmount(cSetAttribute, plague, cDeadUnitId, -1, plague_player);
    xsEffectAmount(cSetAttribute, plague, cSelectionEffect, 2, plague_player);
    

    xsTaskAmount(0, -60);
    xsTaskAmount(1, 6);
    xsTaskAmount(2, 1);
    xsTaskAmount(4, 109);
    xsTaskAmount(5, 2);
    xsTaskAmount(6, 0);
    xsTask(plague, stringers_task, 900, plague_player);
    xsTask(plague, stringers_task, 904, plague_player);
    xsTask(plague, stringers_task, 906, plague_player);
    xsTask(plague, stringers_task, 909, plague_player);
    xsTask(plague, stringers_task, 910, plague_player);
    xsTask(plague, stringers_task, 912, plague_player);
    xsTask(plague, stringers_task, 913, plague_player);
    xsTask(plague, stringers_task, 918, plague_player);
    xsTask(plague, stringers_task, 919, plague_player);
    xsTask(plague, stringers_task, 920, plague_player);
    xsTask(plague, stringers_task, 921, plague_player);
    xsTask(plague, stringers_task, 922, plague_player);
    xsTask(plague, stringers_task, 923, plague_player);
    xsTask(plague, stringers_task, 924, plague_player);
    xsTask(plague, stringers_task, 929, plague_player);
    xsTask(plague, stringers_task, 935, plague_player);
    xsTask(plague, stringers_task, 936, plague_player);
    xsTask(plague, stringers_task, 943, plague_player);
    xsTask(plague, stringers_task, 944, plague_player);
    xsTask(plague, stringers_task, 947, plague_player);
    xsTask(plague, stringers_task, 951, plague_player);
    xsTask(plague, stringers_task, 954, plague_player);
    xsTask(plague, stringers_task, 955, plague_player);
    xsTask(plague, stringers_task, 959, plague_player);
}

void main(){
    plague_stats();
}
