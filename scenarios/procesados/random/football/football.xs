
const int unit_id = 74;
const int stringer_tatsk = 157;
const int player1 = 1;

void train_damage_task(){
    xsTaskAmount(cTaskAttrTaskType , stringer_tatsk);
    xsTaskAmount(cTaskAttrWorkValue1, 10);
    xsTaskAmount(cTaskAttrWorkValue2, 1);
    xsTaskAmount(cTaskAttrWorkRange, 0);
    xsTaskAmount(cTaskAttrSearchWaitTime, 9);    
    xsTaskAmount(cTaskAttrOwnerType, 0);
    xsModifyObjectTasks(unit_id, player1, 1);
    xsEffectAmount(cSetAttribute, unit_id, cCombatAbility, 128, player1);
    
}