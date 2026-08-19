from AoE2ScenarioParser.datasets.buildings import BuildingInfo
from AoE2ScenarioParser.datasets.players import PlayerId
from AoE2ScenarioParser.datasets.units import UnitInfo
from scenarios.procesados.clash_royale.cr_constants import ClashRoyaleSounds, ClashRoyaleUnits, ClashRoyaleVariables


class ClashRoyaleBridges:
    BRIDGES = {
        ClashRoyaleUnits.SPEAR_GOBLINS: {
            "bridge": BuildingInfo.BRIDGE_A_TOP.ID,
            "cost": 2,
            "sound": ClashRoyaleSounds.SPEAR_GOBLINS_SPAWN,
            "direct": False,
            "variable": {
                PlayerId.ONE: ClashRoyaleVariables.SPEAR_GOBLINS_P1,
                PlayerId.TWO: ClashRoyaleVariables.SPEAR_GOBLINS_P2,
            },
            "units": {
                UnitInfo.SKIRMISHER.ID: 3
            }
        },
        ClashRoyaleUnits.GOBLINS: {
            "bridge": BuildingInfo.BRIDGE_A_BOTTOM.ID,
            "cost": 2,
            "sound": ClashRoyaleSounds.GOBLINS_SPAWN,
            "direct": False,
            "variable": {
                PlayerId.ONE: ClashRoyaleVariables.GOBLINS_P1,
                PlayerId.TWO: ClashRoyaleVariables.GOBLINS_P2,
            },
            "units": {
                UnitInfo.SPEARMAN.ID: 4
            }
        },
        ClashRoyaleUnits.KNIGHT: {
            "bridge": BuildingInfo.BRIDGE_A_MIDDLE.ID,
            "cost": 3,
            "sound": ClashRoyaleSounds.KNIGHT_SPAWN,
            "direct": True,
            "variable": {
                PlayerId.ONE: ClashRoyaleVariables.KNIGHT_P1,
                PlayerId.TWO: ClashRoyaleVariables.KNIGHT_P2,
            },
            "units": {
                UnitInfo.SERJEANT.ID: 1
            }
        },
        ClashRoyaleUnits.ARCHERS: {
            "bridge": BuildingInfo.BRIDGE_A_CRACKED.ID,
            "cost": 3,
            "sound": ClashRoyaleSounds.ARCHERS_SPAWN,
            "direct": False,
            "variable": {
                PlayerId.ONE: ClashRoyaleVariables.ARCHERS_P1,
                PlayerId.TWO: ClashRoyaleVariables.ARCHERS_P2,
            },
            "units": {
                UnitInfo.ARCHER.ID: 2
            }
        },
        ClashRoyaleUnits.PRINCE: {
            "bridge": BuildingInfo.BRIDGE_A_BROKEN_TOP.ID,
            "cost": 5,
            "sound": ClashRoyaleSounds.PRINCE_SPAWN,
            "direct": True,
            "variable": {
                PlayerId.ONE: ClashRoyaleVariables.PRINCE_P1,
                PlayerId.TWO: ClashRoyaleVariables.PRINCE_P2,
            },
            "units": {
                UnitInfo.COUSTILLIER.ID: 1
            }
        },
        ClashRoyaleUnits.MINI_PEKKA: {
            "bridge": BuildingInfo.BRIDGE_A_BROKEN_BOTTOM.ID,
            "cost": 4,
            "sound": ClashRoyaleSounds.MINI_PEKKA_SPAWN,
            "direct": True,
            "variable": {
                PlayerId.ONE: ClashRoyaleVariables.MINI_PEKKA_P1,
                PlayerId.TWO: ClashRoyaleVariables.MINI_PEKKA_P2,
            },
            "units": {
                UnitInfo.TEUTONIC_KNIGHT.ID: 1
            }
        },
        ClashRoyaleUnits.MUSKETEER: {
            "bridge": BuildingInfo.BRIDGE_B_TOP.ID,
            "cost": 4,
            "sound": ClashRoyaleSounds.MUSKETEER_SPAWN,
            "direct": True,
            "variable": {
                PlayerId.ONE: ClashRoyaleVariables.MUSKETEER_P1,
                PlayerId.TWO: ClashRoyaleVariables.MUSKETEER_P2,
            },
            "units": {
                UnitInfo.JANISSARY.ID: 1
            }
        },
        ClashRoyaleUnits.SKELETONS: {
            "bridge": BuildingInfo.BRIDGE_B_BOTTOM.ID,
            "cost": 1,
            "sound": ClashRoyaleSounds.SKELETONS_SPAWN,
            "direct": False,
            "variable": {
                PlayerId.ONE: ClashRoyaleVariables.SKELETONS_P1,
                PlayerId.TWO: ClashRoyaleVariables.SKELETONS_P2,
            },
            "units": {
                UnitInfo.KARAMBIT_WARRIOR.ID: 3
            }
        },
        ClashRoyaleUnits.GOLEM: {
            "bridge": BuildingInfo.BRIDGE_B_MIDDLE.ID,
            "cost": 8,
            "sound": ClashRoyaleSounds.GOLEM_SPAWN,
            "direct": True,
            "variable": {
                PlayerId.ONE: ClashRoyaleVariables.GOLEM_P1,
                PlayerId.TWO: ClashRoyaleVariables.GOLEM_P2,
            },
            "units": {
                UnitInfo.ELITE_WAR_ELEPHANT.ID: 1
            }
        },
        ClashRoyaleUnits.DARK_PRINCE: {
            "bridge": BuildingInfo.BRIDGE_B_CRACKED.ID,
            "cost": 4,
            "sound": ClashRoyaleSounds.DARK_PRINCE_SPAWN,
            "direct": False,
            "variable": {
                PlayerId.ONE: ClashRoyaleVariables.DARK_PRINCE_P1,
                PlayerId.TWO: ClashRoyaleVariables.DARK_PRINCE_P2,
            },
            "units": {
                UnitInfo.CATAPHRACT.ID: 1
            }
        },
        ClashRoyaleUnits.WIZARD: {
            "bridge": BuildingInfo.BRIDGE_B_BROKEN_TOP.ID,
            "cost": 5,
            "sound": ClashRoyaleSounds.WIZARD_SPAWN,
            "direct": True,
            "variable": {
                PlayerId.ONE: ClashRoyaleVariables.WIZARD_P1,
                PlayerId.TWO: ClashRoyaleVariables.WIZARD_P2,
            },
            "units": {
                UnitInfo.GRENADIER.ID: 1
            }
        },
        ClashRoyaleUnits.PRINCESS: {
            "bridge": BuildingInfo.BRIDGE_B_BROKEN_BOTTOM.ID,
            "cost": 3,
            "sound": ClashRoyaleSounds.PRINCESS_SPAWN,
            "direct": True,
            "variable": {
                PlayerId.ONE: ClashRoyaleVariables.PRINCESS_P1,
                PlayerId.TWO: ClashRoyaleVariables.PRINCESS_P2,
            },
            "units": {
                UnitInfo.AMAZON_ARCHER.ID: 1
            }
        },
        ClashRoyaleUnits.BARBARIANS: {
            "bridge": BuildingInfo.BRIDGE_C_TOP.ID,
            "cost": 5,
            "sound": ClashRoyaleSounds.BARBARIANS_SPAWN,
            "direct": False,
            "variable": {
                PlayerId.ONE: ClashRoyaleVariables.BARBARIANS_P1,
                PlayerId.TWO: ClashRoyaleVariables.BARBARIANS_P2,
            },
            "units": {
                UnitInfo.LONG_SWORDSMAN.ID: 5
            }
        },
        ClashRoyaleUnits.BATTLE_RAM: {
            "bridge": BuildingInfo.BRIDGE_C_BOTTOM.ID,
            "cost": 4,
            "sound": ClashRoyaleSounds.BATTLE_RAM_SPAWN,
            "direct": True,
            "variable": {
                PlayerId.ONE: ClashRoyaleVariables.BATTLE_RAM_P1,
                PlayerId.TWO: ClashRoyaleVariables.BATTLE_RAM_P2,
            },
            "units": {
                UnitInfo.BATTERING_RAM.ID: 1
            }
        },
        ClashRoyaleUnits.WITCH: {
            "bridge": BuildingInfo.BRIDGE_C_MIDDLE.ID,
            "cost": 5,
            "sound": ClashRoyaleSounds.WITCH_SPAWN,
            "direct": True,
            "variable": {
                PlayerId.ONE: ClashRoyaleVariables.WITCH_P1,
                PlayerId.TWO: ClashRoyaleVariables.WITCH_P2,
            },
            "units": {
                UnitInfo.GBETO.ID: 1
            }
        },
        ClashRoyaleUnits.DART_GOBLIN: {
            "bridge": BuildingInfo.BRIDGE_C_CRACKED.ID,
            "cost": 3,
            "sound": ClashRoyaleSounds.DART_GOBLIN_SPAWN,
            "direct": True,
            "variable": {
                PlayerId.ONE: ClashRoyaleVariables.DART_GOBLIN_P1,
                PlayerId.TWO: ClashRoyaleVariables.DART_GOBLIN_P2,
            },
            "units": {
                UnitInfo.PLUMED_ARCHER.ID: 1
            }
        },
        ClashRoyaleUnits.FIRE_SPIRIT: {
            "bridge": BuildingInfo.BRIDGE_C_BROKEN_TOP.ID,
            "cost": 1,
            "sound": ClashRoyaleSounds.FIRE_SPIRIT_SPAWN,
            "direct": True,
            "variable": {
                PlayerId.ONE: ClashRoyaleVariables.FIRE_SPIRIT_P1,
                PlayerId.TWO: ClashRoyaleVariables.FIRE_SPIRIT_P2,
            },
            "units": {
                UnitInfo.DEMOLITION_RAFT.ID: 1
            }
        },
        ClashRoyaleUnits.WALLBREAKERS: {
            "bridge": BuildingInfo.BRIDGE_C_BROKEN_BOTTOM.ID,
            "cost": 2,
            "sound": ClashRoyaleSounds.WALLBREAKERS_SPAWN,
            "direct": False,
            "variable": {
                PlayerId.ONE: ClashRoyaleVariables.WALLBREAKERS_P1,
                PlayerId.TWO: ClashRoyaleVariables.WALLBREAKERS_P2,
            },
            "units": {
                UnitInfo.PETARD.ID: 2
            }
        },
        ClashRoyaleUnits.HOG_RIDER: {
            "bridge": BuildingInfo.BRIDGE_D_TOP.ID,
            "cost": 4,
            "sound": ClashRoyaleSounds.HOG_RIDER_SPAWN,
            "direct": True,
            "variable": {
                PlayerId.ONE: ClashRoyaleVariables.HOG_RIDER_P1,
                PlayerId.TWO: ClashRoyaleVariables.HOG_RIDER_P2,
            },
            "units": {
                UnitInfo.TARKAN.ID: 1
            }
        },
        ClashRoyaleUnits.MAGIC_ARCHER: {
            "bridge": BuildingInfo.BRIDGE_D_BOTTOM.ID,
            "cost": 4,
            "sound": ClashRoyaleSounds.MAGIC_ARCHER_SPAWN,
            "direct": True,
            "variable": {
                PlayerId.ONE: ClashRoyaleVariables.MAGIC_ARCHER_P1,
                PlayerId.TWO: ClashRoyaleVariables.MAGIC_ARCHER_P2,
            },
            "units": {
                UnitInfo.COMPOSITE_BOWMAN.ID: 1
            }
        },
        ClashRoyaleUnits.ELITE_BARBARIANS: {
            "bridge": BuildingInfo.BRIDGE_D_MIDDLE.ID,
            "cost": 6,
            "sound": ClashRoyaleSounds.ELITE_BARBARIANS_SPAWN,
            "direct": False,
            "variable": {
                PlayerId.ONE: ClashRoyaleVariables.ELITE_BARBARIANS_P1,
                PlayerId.TWO: ClashRoyaleVariables.ELITE_BARBARIANS_P2,
            },
            "units": {
                UnitInfo.CHAMPION.ID: 2
            }
        },
        ClashRoyaleUnits.ICE_WIZARD: {
            "bridge": BuildingInfo.BRIDGE_D_CRACKED.ID,
            "cost": 3,
            "sound": ClashRoyaleSounds.ICE_WIZARD_SPAWN,
            "direct": True,
            "variable": {
                PlayerId.ONE: ClashRoyaleVariables.ICE_WIZARD_P1,
                PlayerId.TWO: ClashRoyaleVariables.ICE_WIZARD_P2,
            },
            "units": {
                UnitInfo.GUECHA_WARRIOR.ID: 1
            }
        },
        ClashRoyaleUnits.SKELETON_ARMY: {
            "bridge": BuildingInfo.BRIDGE_D_BROKEN_TOP.ID,
            "cost": 3,
            "sound": ClashRoyaleSounds.SKELETON_ARMY_SPAWN,
            "direct": True,
            "variable": {
                PlayerId.ONE: ClashRoyaleVariables.SKELETON_ARMY_P1,
                PlayerId.TWO: ClashRoyaleVariables.SKELETON_ARMY_P2,
            },
            "units": {
                UnitInfo.KARAMBIT_WARRIOR.ID: 15
            }
        },
        ClashRoyaleUnits.ROYAL_HOGS: {
            "bridge": BuildingInfo.BRIDGE_D_BROKEN_BOTTOM.ID,
            "cost": 5,
            "sound": ClashRoyaleSounds.ROYAL_HOGS_SPAWN,
            "direct": False,
            "variable": {
                PlayerId.ONE: ClashRoyaleVariables.ROYAL_HOGS_P1,
                PlayerId.TWO: ClashRoyaleVariables.ROYAL_HOGS_P2,
            },
            "units": {
                UnitInfo.WOAD_RAIDER.ID: 4
            }
        },
        ClashRoyaleUnits.GOBLIN_HUT: {
            "bridge": BuildingInfo.YURT_B.ID,
            "cost": 4,
            "sound": ClashRoyaleSounds.GOBLIN_HUT_SPAWN,
            "direct": True,
            "variable": {
                PlayerId.ONE: ClashRoyaleVariables.GOBLIN_HUT_P1,
                PlayerId.TWO: ClashRoyaleVariables.GOBLIN_HUT_P2,
            },
            "units": {}
        },
        ClashRoyaleUnits.BOMB_TOWER: {
            "bridge": BuildingInfo.BOMBARD_TOWER.ID,
            "cost": 5,
            "sound": ClashRoyaleSounds.BOMB_TOWER_SPAWN,
            "direct": True,
            "variable": {
                PlayerId.ONE: ClashRoyaleVariables.BOMB_TOWER_P1,
                PlayerId.TWO: ClashRoyaleVariables.BOMB_TOWER_P2,
            },
            "units": {}
        },
        ClashRoyaleUnits.INFERNO_TOWER: {
            "bridge": BuildingInfo.SEA_TOWER.ID,
            "cost": 5,
            "sound": ClashRoyaleSounds.INFERNO_TOWER_SPAWN,
            "direct": True,
            "variable": {
                PlayerId.ONE: ClashRoyaleVariables.INFERNO_TOWER_P1,
                PlayerId.TWO: ClashRoyaleVariables.INFERNO_TOWER_P2,
            },
            "units": {}
        },
        ClashRoyaleUnits.XBOW: {
            "bridge": BuildingInfo.WATCH_TOWER.ID,
            "cost": 6,
            "sound": ClashRoyaleSounds.XBOW_SPAWN,
            "direct": True,
            "variable": {
                PlayerId.ONE: ClashRoyaleVariables.XBOW_P1,
                PlayerId.TWO: ClashRoyaleVariables.XBOW_P2,
            },
            "units": {}
        },
        ClashRoyaleUnits.MORTAR: {
            "bridge": BuildingInfo.GUARD_TOWER.ID,
            "cost": 4,
            "sound": ClashRoyaleSounds.MORTAR_SPAWN,
            "direct": True,
            "variable": {
                PlayerId.ONE: ClashRoyaleVariables.MORTAR_P1,
                PlayerId.TWO: ClashRoyaleVariables.MORTAR_P2,
            },
            "units": {}
        },
        ClashRoyaleUnits.ARROWS: {
            "bridge": BuildingInfo.WOODEN_BRIDGE_A_TOP.ID,
            "cost": 3,
            "sound": ClashRoyaleSounds.ARROWS_CAST,
            "direct": True,
            "delete_delay": 2,
            "variable": {
                PlayerId.ONE: ClashRoyaleVariables.ARROWS_P1,
                PlayerId.TWO: ClashRoyaleVariables.ARROWS_P2,
            },
            "units": {
                UnitInfo.MANGUDAI.ID: 1
            }
        },
        ClashRoyaleUnits.THE_LOG: {
            "bridge": BuildingInfo.WOODEN_BRIDGE_A_BOTTOM.ID,
            "cost": 2,
            "sound": ClashRoyaleSounds.THE_LOG_CAST,
            "direct": True,
            "delete_delay": 3,
            "variable": {
                PlayerId.ONE: ClashRoyaleVariables.THE_LOG_P1,
                PlayerId.TWO: ClashRoyaleVariables.THE_LOG_P2,
            },
            "units": {
                UnitInfo.CAVALRY_ARCHER.ID: 1
            }
        },
        ClashRoyaleUnits.FIREBALL: {
            "bridge": BuildingInfo.WOODEN_BRIDGE_A_MIDDLE.ID,
            "cost": 4,
            "sound": ClashRoyaleSounds.FIREBALL_CAST,
            "direct": True,
            "delete_delay": 2,
            "variable": {
                PlayerId.ONE: ClashRoyaleVariables.FIREBALL_P1,
                PlayerId.TWO: ClashRoyaleVariables.FIREBALL_P2,
            },
            "units": {
                UnitInfo.CAMEL_ARCHER.ID: 1
            }
        },
        ClashRoyaleUnits.POISON: {
            "bridge": BuildingInfo.WOODEN_BRIDGE_B_TOP.ID,
            "cost": 4,
            "sound": ClashRoyaleSounds.POISON_CAST,
            "direct": True,
            "delete_delay": 10,
            "variable": {
                PlayerId.ONE: ClashRoyaleVariables.POISON_P1,
                PlayerId.TWO: ClashRoyaleVariables.POISON_P2,
            },
            "units": {}
        },
        ClashRoyaleUnits.FREEZE: {
            "bridge": BuildingInfo.WOODEN_BRIDGE_B_BOTTOM.ID,
            "cost": 4,
            "sound": ClashRoyaleSounds.FREEZE_CAST,
            "direct": True,
            "delete_delay": 5,
            "variable": {
                PlayerId.ONE: ClashRoyaleVariables.FREEZE_P1,
                PlayerId.TWO: ClashRoyaleVariables.FREEZE_P2,
            },
            "units": {}
        },
        ClashRoyaleUnits.RAGE: {
            "bridge": BuildingInfo.WOODEN_BRIDGE_B_MIDDLE.ID,
            "cost": 2,
            "sound": ClashRoyaleSounds.RAGE_CAST,
            "direct": True,
            "delete_delay": 7,
            "variable": {
                PlayerId.ONE: ClashRoyaleVariables.RAGE_P1,
                PlayerId.TWO: ClashRoyaleVariables.RAGE_P2,
            },
            "units": {}
        },
    }

    unit_reference = {
        UnitInfo.SKIRMISHER.ID,  # Spear Goblins
        UnitInfo.SPEARMAN.ID,  # Goblins
        UnitInfo.SERJEANT.ID,  # Knight
        UnitInfo.ARCHER.ID,  # Archers
        UnitInfo.COUSTILLIER.ID,  # Prince
        UnitInfo.TEUTONIC_KNIGHT.ID,  # Mini PEKKA
        UnitInfo.JANISSARY.ID,  # Musketeer
        UnitInfo.KARAMBIT_WARRIOR.ID,  # Skeletons
        UnitInfo.ELITE_WAR_ELEPHANT.ID,  # Golem
        UnitInfo.WAR_ELEPHANT.ID,  # Golemite
        UnitInfo.CATAPHRACT.ID,  # Dark Prince
        UnitInfo.GRENADIER.ID,  # Wizard
        UnitInfo.AMAZON_ARCHER.ID,  # Princess
        UnitInfo.LONG_SWORDSMAN.ID,  # Barbarians
        UnitInfo.BATTERING_RAM.ID,  # Battle Ram
        UnitInfo.GBETO.ID,  # Witch
        UnitInfo.PLUMED_ARCHER.ID,  # Dart Goblin
        UnitInfo.DEMOLITION_RAFT.ID,  # Fire Spirit
        UnitInfo.PETARD.ID,  # Wallbreakers
        UnitInfo.TARKAN.ID,  # Hog Rider
        UnitInfo.COMPOSITE_BOWMAN.ID,  # Magic Archer
        UnitInfo.CHAMPION.ID,  # Elite Barbarians
        UnitInfo.GUECHA_WARRIOR.ID,  # Ice Wizard
        UnitInfo.ELITE_KARAMBIT_WARRIOR.ID,  # Skeleton Army
        UnitInfo.ELITE_SKIRMISHER.ID,  # Goblin Gang
        BuildingInfo.YURT_B.ID,  # Goblin Hut
        BuildingInfo.BOMBARD_TOWER.ID,  # Bomb Tower
        BuildingInfo.SEA_TOWER.ID,  # Inferno Tower
        BuildingInfo.WATCH_TOWER.ID,  # X-Bow
        BuildingInfo.GUARD_TOWER.ID,  # Mortar
        BuildingInfo.WOODEN_BRIDGE_A_TOP.ID,  # Arrows
        BuildingInfo.WOODEN_BRIDGE_A_BOTTOM.ID,  # The Log
        BuildingInfo.WOODEN_BRIDGE_A_MIDDLE.ID,  # Fireball
        BuildingInfo.WOODEN_BRIDGE_B_TOP.ID,  # Poison
        BuildingInfo.WOODEN_BRIDGE_B_BOTTOM.ID,  # Freeze
        BuildingInfo.WOODEN_BRIDGE_B_MIDDLE.ID,  # Rage
    }
