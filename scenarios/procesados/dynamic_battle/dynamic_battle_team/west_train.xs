const int teutonic_knight = 25;
const int elite_teutonic_knight = 554;
const int outpost = 598;
const int movement_damage_task = 152;
const int aura_task = 155;
const int player = 7;
const int infantry_class = 906;
const float train_header_speed = 1.0;
const float train_wagon_extra_speed = 0.05;
const float speed_buff = 1.7;
const int speed_buff_range = 10;
const int train_roll_range = 1;

const int standing_graphic_attribute = 71;
const int walking_graphic_attribute = 75;
const int attacking_graphic_attribute = 70;
const int dying_graphic_attribute = 73;
const int icon_id_attribute = 25;

const int train_standing_graphic = 12328;
const int train_walking_graphic = 12330;
const int train_attacking_graphic = 12326;
const int train_dying_graphic = 12327;
const int smoke_graphic = 5462;
const int train_name = 5561;
const int train_icon = 370;
const int train_hp = 20000;
const int train_damage = 1000;
const int train_damage_shown = 200;

const int maxByte = 256;
const int cPierce = 3;
const int cMelee = 4;


void train_damage_task(){
    xsTaskAmount(0, train_damage);
    xsTaskAmount(1, 1);
    xsTaskAmount(2, train_roll_range);
    xsTaskAmount(4, 0);
    xsTaskAmount(5, 2);
    xsTaskAmount(6, 5);
    xsTask(teutonic_knight, movement_damage_task, -1, player);
    xsTask(elite_teutonic_knight, movement_damage_task, -1, player);  
}

void unit_stats(int unit_id = 25){
    xsEffectAmount(cSetAttribute, unit_id, cHitpoints, train_hp, player); 
    xsEffectAmount(cSetAttribute, unit_id, cAttack, cMelee * maxByte + train_damage_shown, player); 
    xsEffectAmount(cMulAttribute, unit_id, cAttack, cMelee * maxByte + train_damage_shown, player); 
    xsEffectAmount(cAddAttribute, unit_id, cAttack, cMelee * maxByte + train_damage_shown, player); 
    xsEffectAmount(cAddAttribute, unit_id, cAttack, cMelee * maxByte + train_damage_shown, player); 
    xsEffectAmount(cAddAttribute, unit_id, cAttack, cMelee * maxByte + train_damage_shown, player); 

    xsEffectAmount(cSetAttribute, unit_id, cArmor, cMelee * maxByte + train_damage_shown, player); 
    xsEffectAmount(cAddAttribute, unit_id, cArmor, cMelee * maxByte + train_damage_shown, player); 
    xsEffectAmount(cAddAttribute, unit_id, cArmor, cMelee * maxByte + train_damage_shown, player); 
    xsEffectAmount(cAddAttribute, unit_id, cArmor, cMelee * maxByte + train_damage_shown, player); 
    xsEffectAmount(cAddAttribute, unit_id, cArmor, cMelee * maxByte + train_damage_shown, player); 
    
    xsEffectAmount(cSetAttribute, unit_id, cArmor, cPierce * maxByte + train_damage_shown, player); 
    xsEffectAmount(cAddAttribute, unit_id, cArmor, cPierce * maxByte + train_damage_shown, player); 
    xsEffectAmount(cAddAttribute, unit_id, cArmor, cPierce * maxByte + train_damage_shown, player); 
    xsEffectAmount(cAddAttribute, unit_id, cArmor, cPierce * maxByte + train_damage_shown, player); 
    xsEffectAmount(cAddAttribute, unit_id, cArmor, cPierce * maxByte + train_damage_shown, player); 

    xsEffectAmount(cSetAttribute, unit_id, cMovementSpeed, train_header_speed, player);    
    xsEffectAmount(cSetAttribute, unit_id, cUnitSizeX, 0.2, player);
    xsEffectAmount(cSetAttribute, unit_id, cUnitSizeY, 0.2, player);
    xsEffectAmount(cSetAttribute, unit_id, cUnitSizeZ, 0.0, player);
    xsEffectAmount(cSetAttribute, unit_id, cBlastWidth, train_roll_range, player);

    xsEffectAmount(cSetAttribute, unit_id, standing_graphic_attribute, train_standing_graphic, player);
    xsEffectAmount(cSetAttribute, unit_id, walking_graphic_attribute, train_walking_graphic, player);
    xsEffectAmount(cSetAttribute, unit_id, attacking_graphic_attribute, train_attacking_graphic, player);
    xsEffectAmount(cSetAttribute, unit_id, dying_graphic_attribute, train_dying_graphic, player);
    xsEffectAmount(cSetAttribute, unit_id, icon_id_attribute, train_icon, player);
    xsEffectAmount(cSetAttribute, unit_id, cNameId, train_name, player);
    xsEffectAmount(cSetAttribute, unit_id, cShownAttack, train_damage, player);
    xsEffectAmount(cSetAttribute, unit_id, cShownMeleeArmor, train_damage, player);
    xsEffectAmount(cSetAttribute, unit_id, cShownPierceArmor, train_damage, player);    
    xsEffectAmount(cSetAttribute, unit_id, cRegenerationRate, train_hp, player); 

}

void outpost_stats(){    
    xsEffectAmount(cSetAttribute, outpost, cUnitSizeX, 0.0, player);
    xsEffectAmount(cSetAttribute, outpost, cUnitSizeY, 0.0, player);
    xsEffectAmount(cSetAttribute, outpost, cUnitSizeZ, 0.0, player);
    xsEffectAmount(cSetAttribute, outpost, standing_graphic_attribute, 0, player);
    xsEffectAmount(cSetAttribute, outpost, walking_graphic_attribute, 0, player);
    xsEffectAmount(cSetAttribute, outpost, attacking_graphic_attribute, 0, player);
    xsEffectAmount(cSetAttribute, outpost, dying_graphic_attribute, 0, player);
    xsEffectAmount(cSetAttribute, outpost, cArmor, cMelee * maxByte + train_damage_shown, player); 
    xsEffectAmount(cAddAttribute, outpost, cArmor, cMelee * maxByte + train_damage_shown, player); 
    xsEffectAmount(cAddAttribute, outpost, cArmor, cMelee * maxByte + train_damage_shown, player); 
    xsEffectAmount(cAddAttribute, outpost, cArmor, cMelee * maxByte + train_damage_shown, player); 
    xsEffectAmount(cAddAttribute, outpost, cArmor, cMelee * maxByte + train_damage_shown, player); 
    
    xsEffectAmount(cSetAttribute, outpost, cArmor, cPierce * maxByte + train_damage_shown, player); 
    xsEffectAmount(cAddAttribute, outpost, cArmor, cPierce * maxByte + train_damage_shown, player); 
    xsEffectAmount(cAddAttribute, outpost, cArmor, cPierce * maxByte + train_damage_shown, player); 
    xsEffectAmount(cAddAttribute, outpost, cArmor, cPierce * maxByte + train_damage_shown, player); 
    xsEffectAmount(cAddAttribute, outpost, cArmor, cPierce * maxByte + train_damage_shown, player); 
    xsEffectAmount(cSetAttribute, outpost, cHitpoints, train_hp, player);
    xsEffectAmount(cSetAttribute, outpost, cRegenerationRate, train_hp, player); 
    xsEffectAmount(cSetAttribute, outpost, cCombatAbility, 2 + 32, player);
    
    xsTaskAmount(0, speed_buff);
    xsTaskAmount(1, 1);
    xsTaskAmount(2, speed_buff_range);
    xsTaskAmount(4, cMovementSpeed);
    xsTaskAmount(5, 4 + 1);
    xsTaskAmount(6, 1);
    xsTask(outpost, aura_task, infantry_class, player);    
}


void main(){
    train_damage_task();
    unit_stats(teutonic_knight);
    xsEffectAmount(cAddAttribute, teutonic_knight, cMovementSpeed, train_wagon_extra_speed, player);    
    unit_stats(elite_teutonic_knight); 
    outpost_stats();
}