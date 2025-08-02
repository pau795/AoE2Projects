const int ballista_elephant = 1120;
const int ballista_elephant_projectile = 1167;

const int cPierce = 3;
const int maxByte = 256;
const int unit_damage = 200;
const int player = 3;


void unit_stats(int unit_id = 0){
    xsEffectAmount(cSetAttribute, unit_id, cHitpoints, 20000, player);
    xsEffectAmount(cSetAttribute, unit_id, cRegenerationRate, 20000, player);
    xsEffectAmount(cSetAttribute, unit_id, cCombatAbility, 8, player);
    xsEffectAmount(cSetAttribute, unit_id, cMaxRange, 250, player);
    xsEffectAmount(cSetAttribute, unit_id, cMinimumRange, 0, player);
    xsEffectAmount(cSetAttribute, unit_id, cAttackReloadTime, 10, player);
    xsEffectAmount(cSetAttribute, unit_id, cStandingGraphic, 0, player);
    xsEffectAmount(cSetAttribute, unit_id, cWalkingGraphic, 0, player);
    xsEffectAmount(cSetAttribute, unit_id, cAttackGraphic, 0, player);
    xsEffectAmount(cSetAttribute, unit_id, cDyingGraphic, 0, player);
    xsEffectAmount(cSetAttribute, unit_id, cDeadUnitId, 0, player);    

    xsEffectAmount(cSetAttribute, unit_id, cAttack, cPierce * maxByte + unit_damage, player);
    xsEffectAmount(cAddAttribute, unit_id, cAttack, cPierce * maxByte + unit_damage, player);
    xsEffectAmount(cAddAttribute, unit_id, cAttack, cPierce * maxByte + unit_damage, player);
    xsEffectAmount(cAddAttribute, unit_id, cAttack, cPierce * maxByte + unit_damage, player);
    xsEffectAmount(cAddAttribute, unit_id, cAttack, cPierce * maxByte + unit_damage, player);
}

void projectile_stats(int projectile_id = 0){
    xsEffectAmount(cSetAttribute, projectile_id, cEnableSmartProjectile, 2, player);
    xsEffectAmount(cSetAttribute, projectile_id, cBlastAttackLevel, 1, player);
    xsEffectAmount(cSetAttribute, projectile_id, cUnitSizeX, 1, player);
    xsEffectAmount(cSetAttribute, projectile_id, cUnitSizeY, 1, player);
    xsEffectAmount(cSetAttribute, projectile_id, cUnitSizeZ, 100, player);
    xsEffectAmount(cSetAttribute, projectile_id, cEnableSmartProjectile, 2, player);
    xsEffectAmount(cSetAttribute, projectile_id, cMovementSpeed, 2, player);
    xsEffectAmount(cSetAttribute, projectile_id, cStandingGraphic, 0, player);
    xsEffectAmount(cSetAttribute, projectile_id, cWalkingGraphic, 0, player);
}

void main(){
    unit_stats(ballista_elephant);
    projectile_stats(ballista_elephant_projectile);
}