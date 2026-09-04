"""
U4: Tempo/Timing Collapse - UNREACHABLE Scenario

Map: Arabia (open)
Civilization: Player: Turks | AI: Mongols
Scenario Trigger: Player starts Dark Age. AI starts Imperial with
                  30 Mangudai, 5 Trebuchets, 200 pop economy.

Graph Structure:
s0[Player: Dark Age, 3 vills | AI: Imperial, 30 Mangudai + 5 Trebs]
  -> n1[Player builds houses, gathers food]
    -> AI attacks at ~2 min with Mangudai
      -> n2[Player has 0 military units, TC fires arrows]
        -> Mangudai kite TC, Trebs destroy TC from range
          -> n3[TC destroyed, vills killed] -> D[Defeat]
  Alternative: n1 -> n1'[Loom + quick wall]
    -> Trebs break walls in ~30 seconds
      -> n2'[Walls breached] -> n3[TC destroyed] -> D[Defeat]
  Time to first military unit: ~8 min (Feudal Age)
  Time until AI overwhelms: ~3 min
  Gap is structurally unbridgeable -> All paths from s0 lead to D

Unreachability Point: Immediate (s0)
Key Insight: Unreachability through timing - paths exist but are pruned
             by opponent actions before player can traverse them.
"""

import sys
import io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

from AoE2ScenarioParser.scenarios.aoe2_de_scenario import AoE2DEScenario
from AoE2ScenarioParser.datasets.players import PlayerId
from AoE2ScenarioParser.datasets.units import UnitInfo
from AoE2ScenarioParser.datasets.buildings import BuildingInfo
from AoE2ScenarioParser.datasets.other import OtherInfo
from AoE2ScenarioParser.datasets.heroes import HeroInfo
from AoE2ScenarioParser.datasets.terrains import TerrainId

# Create scenario
scenario = AoE2DEScenario.from_default()
unit_manager = scenario.unit_manager
trigger_manager = scenario.trigger_manager
map_manager = scenario.map_manager

map_size = map_manager.map_size
center = map_size // 2
quarter = map_size // 4
three_quarter = (map_size * 3) // 4

# ============================================================
# PLAYER BASE: Turks - Standard DARK AGE start
# This is the weakest possible starting position
# ============================================================
player_base_x, player_base_y = quarter, quarter

# Town Center (only defense)
player_tc = unit_manager.add_unit(PlayerId.ONE, unit_const=BuildingInfo.TOWN_CENTER.ID,
                                   x=player_base_x, y=player_base_y)

# Only 3 villagers (standard Dark Age)
for i in range(3):
    unit_manager.add_unit(PlayerId.ONE, unit_const=UnitInfo.VILLAGER_MALE.ID,
                          x=player_base_x + 3 + i, y=player_base_y)

# Scout cavalry (will die almost instantly to Mangudai)
unit_manager.add_unit(PlayerId.ONE, unit_const=UnitInfo.SCOUT_CAVALRY.ID,
                      x=player_base_x + 6, y=player_base_y)

# ============================================================
# PLAYER RESOURCES: Standard (not the problem - TIME is)
# ============================================================
# Sheep
for i in range(6):
    unit_manager.add_unit(PlayerId.GAIA, unit_const=UnitInfo.SHEEP.ID,
                          x=player_base_x + 8 + i % 3, y=player_base_y + i // 3)

# Boar (won't have time to lure)
unit_manager.add_unit(PlayerId.GAIA, unit_const=UnitInfo.WILD_BOAR.ID,
                      x=player_base_x + 15, y=player_base_y + 10)

# Gold
for pile in range(3):
    for i in range(4):
        unit_manager.add_unit(PlayerId.GAIA, unit_const=OtherInfo.GOLD_MINE.ID,
                              x=player_base_x + 10 + pile * 6, y=player_base_y + 15 + i)

# Wood
for x in range(15):
    for y in range(8):
        unit_manager.add_unit(PlayerId.GAIA, unit_const=OtherInfo.TREE_OAK.ID,
                              x=player_base_x + 15 + x, y=player_base_y - 12 + y)

# Berries
for i in range(6):
    unit_manager.add_unit(PlayerId.GAIA, unit_const=OtherInfo.FORAGE_BUSH.ID,
                          x=player_base_x - 8 + i, y=player_base_y + 5)

# ============================================================
# ENEMY: Mongols - IMPERIAL AGE with OVERWHELMING FORCE
# The tempo differential is the trap
# ============================================================
enemy_base_x, enemy_base_y = three_quarter, three_quarter

# Full Imperial infrastructure
unit_manager.add_unit(PlayerId.TWO, unit_const=BuildingInfo.TOWN_CENTER.ID,
                      x=enemy_base_x, y=enemy_base_y)
unit_manager.add_unit(PlayerId.TWO, unit_const=BuildingInfo.CASTLE.ID,
                      x=enemy_base_x + 10, y=enemy_base_y)
unit_manager.add_unit(PlayerId.TWO, unit_const=BuildingInfo.CASTLE.ID,
                      x=enemy_base_x - 8, y=enemy_base_y + 5)
unit_manager.add_unit(PlayerId.TWO, unit_const=BuildingInfo.BLACKSMITH.ID,
                      x=enemy_base_x + 5, y=enemy_base_y + 8)
unit_manager.add_unit(PlayerId.TWO, unit_const=BuildingInfo.UNIVERSITY.ID,
                      x=enemy_base_x - 5, y=enemy_base_y + 8)

# 200 pop economy represented (20 villagers)
for i in range(20):
    unit_manager.add_unit(PlayerId.TWO, unit_const=UnitInfo.VILLAGER_MALE.ID,
                          x=enemy_base_x + 15 + i % 5, y=enemy_base_y + i // 5)

# ============================================================
# THE OVERWHELMING FORCE: 30 Mangudai + 5 Trebuchets
# Positioned ready to attack immediately
# ============================================================

# 30 Mangudai: Fast horse archers that kite everything
# Grouped near player's base for immediate aggression
attack_staging_x = center
attack_staging_y = center

for i in range(30):
    unit_manager.add_unit(PlayerId.TWO, unit_const=UnitInfo.MANGUDAI.ID,
                          x=attack_staging_x + i % 10, y=attack_staging_y + i // 10)

# 5 Trebuchets: Destroy TC from maximum range
# Player cannot stop them without military
for i in range(5):
    unit_manager.add_unit(PlayerId.TWO, unit_const=UnitInfo.TREBUCHET.ID,
                          x=attack_staging_x + i * 4, y=attack_staging_y - 5)

# ============================================================
# TRIGGERS: AI attacks immediately, timing analysis
# ============================================================

# Setup - Timing Analysis
t = trigger_manager.add_trigger("[Setup] U4 Timing Collapse")
t.new_condition.timer(timer=1)
t.new_effect.display_instructions(
    source_player=PlayerId.ONE,
    display_time=20,
    message="<YELLOW>U4: TEMPO/TIMING COLLAPSE\n\n<RED>UNREACHABLE SCENARIO\n\nYou: Dark Age, 3 villagers, 1 scout\nEnemy: Imperial Age, 30 Mangudai, 5 Trebuchets\n\n<RED>TIMING ANALYSIS:\nTime to first military: ~8-10 minutes\nTime until AI destroys you: ~3 minutes\n\nTHE GAP IS STRUCTURALLY UNBRIDGEABLE."
)

# Timing breakdown
t = trigger_manager.add_trigger("[Analysis] Timing Breakdown")
t.new_condition.timer(timer=10)
t.new_effect.display_instructions(
    source_player=PlayerId.ONE,
    display_time=15,
    message="<ORANGE>[TEMPO ANALYSIS]\n\nPLAYER TIMELINE:\n- Houses + gather food: 0-2 min\n- Feudal Age (500F): 8-10 min\n- Barracks + military: 10-12 min\n- Enough units to fight: 15-20 min\n\nENEMY TIMELINE:\n- Attack begins: ~1 minute\n- Mangudai arrive: ~2 minutes\n- Trebs in range: ~2.5 minutes\n- TC destroyed: ~3-4 minutes"
)

# AI Attack Order - 1 minute
t = trigger_manager.add_trigger("[AI] Attack Order - 60 sec")
t.new_condition.timer(timer=60)
t.new_effect.display_instructions(
    source_player=PlayerId.ONE,
    display_time=8,
    message="<RED>THE MONGOL HORDE ADVANCES!\n\n30 Mangudai and 5 Trebuchets move to attack.\nYour military count: 0"
)
# Task Mangudai to attack player base
t.new_effect.task_object(
    object_list_unit_id=UnitInfo.MANGUDAI.ID,
    source_player=PlayerId.TWO,
    location_x=player_base_x,
    location_y=player_base_y
)
# Task Trebuchets
t.new_effect.task_object(
    object_list_unit_id=UnitInfo.TREBUCHET.ID,
    source_player=PlayerId.TWO,
    location_x=player_base_x + 8,
    location_y=player_base_y + 8
)

# 2 minute mark - Mangudai arrive
t = trigger_manager.add_trigger("[Analysis] 2 Min - Mangudai Arrive")
t.new_condition.timer(timer=120)
t.new_effect.display_instructions(
    source_player=PlayerId.ONE,
    display_time=10,
    message="<RED>[TIMING - 2 MINUTES]\n\nMangudai have arrived at your base.\nYour military count: 0\n\nTC fires 5 arrows per volley.\n30 Mangudai: ~1800 HP total.\nMangudai kite TC, taking minimal damage.\nTrebuchets setting up..."
)

# 2.5 minute mark - Trebs in range
t = trigger_manager.add_trigger("[Analysis] 2.5 Min - Trebs in Range")
t.new_condition.timer(timer=150)
t.new_effect.display_instructions(
    source_player=PlayerId.ONE,
    display_time=10,
    message="<RED>[TIMING - 2.5 MINUTES]\n\nTrebuchets in range.\nTrebuchet damage: 200 per shot\nTC HP: 2400\n\n5 Trebuchets = 1000 damage/volley\nTC destroyed in ~3 volleys (~30 seconds)\n\nNo possible intervention."
)

# 3 minute mark - TC critical
t = trigger_manager.add_trigger("[Analysis] 3 Min - TC Critical")
t.new_condition.timer(timer=180)
t.new_effect.display_instructions(
    source_player=PlayerId.ONE,
    display_time=10,
    message="<RED>[TIMING - 3 MINUTES]\n\nTC under heavy bombardment.\nVillagers dying to Mangudai.\n\nTime to Feudal Age: Still ~5 minutes away.\nThe timing gap cannot be closed.\n\nAll paths from s0 are pruned before traversal."
)

# Alternative path analysis - Quick wall
t = trigger_manager.add_trigger("[Analysis] Quick Wall Attempt")
t.new_condition.own_objects(
    quantity=5,
    source_player=PlayerId.ONE,
    object_list=BuildingInfo.PALISADE_WALL.ID
)
t.new_effect.display_instructions(
    source_player=PlayerId.ONE,
    display_time=8,
    message="<ORANGE>[ALTERNATIVE PATH: Quick Wall]\n\nPalisade walls constructed.\n\n<RED>PROBLEM: Trebuchets destroy palisade in ~15 seconds.\nMangudai snipe villagers repairing.\n\nQuick wall path does NOT reach V."
)

# Alternative path analysis - Garrison
t = trigger_manager.add_trigger("[Analysis] Garrison Attempt")
t.new_condition.timer(timer=90)
t.new_effect.display_instructions(
    source_player=PlayerId.ONE,
    display_time=8,
    message="<ORANGE>[ALTERNATIVE PATH: Garrison + Loom]\n\nVillagers garrisoned in TC.\nLoom researched (+15 HP, +1 armor).\n\n<RED>PROBLEM: TC cannot survive:\n- 30 Mangudai kiting\n- 5 Trebuchets bombardment\n- TC destroyed in ~2-3 minutes\n\nGarrison path does NOT reach V."
)

# Critical state - All paths fail
t = trigger_manager.add_trigger("[Critical] All Paths Fail")
t.new_condition.timer(timer=240)
t.new_effect.display_instructions(
    source_player=PlayerId.ONE,
    display_time=20,
    message="<RED>[CRITICAL STATE - TIMING COLLAPSE]\n\nAll paths analyzed:\n\ns0 -> n1 [Eco build]: Pruned at ~3 min (TC destroyed)\ns0 -> n1' [Quick wall]: Pruned at ~2 min (walls breached)\ns0 -> n1'' [Garrison]: Pruned at ~3 min (TC destroyed)\n\nMinimum time to military: ~8 minutes\nMaximum survival time: ~4 minutes\n\n<RED>GAP = 4 MINUTES\nNO SEQUENCE OF ACTIONS CAN BRIDGE THIS GAP\n\nAll paths from s0 lead to D (Defeat)"
)

# Victory (impossible due to timing)
t = trigger_manager.add_trigger("[Victory] Conquest")
t.new_condition.own_fewer_objects(
    quantity=1,
    source_player=PlayerId.TWO,
    object_list=BuildingInfo.TOWN_CENTER.ID
)
t.new_effect.display_instructions(
    source_player=PlayerId.ONE,
    display_time=10,
    message="<GREEN>VICTORY!\n\n(This should be impossible - timing prevents it)"
)
t.new_effect.declare_victory(source_player=PlayerId.ONE, enabled=1)

# Defeat - TC destroyed
t = trigger_manager.add_trigger("[Defeat] TC Destroyed")
t.new_condition.own_fewer_objects(
    quantity=1,
    source_player=PlayerId.ONE,
    object_list=BuildingInfo.TOWN_CENTER.ID
)
t.new_effect.display_instructions(
    source_player=PlayerId.ONE,
    display_time=12,
    message="<RED>DEFEAT\n\n[GRAPH STATE D]\nTC destroyed at approximately 3-4 minutes.\nFirst military unit required ~8 minutes.\n\nTiming collapse made victory impossible from s0.\nPaths to V existed in theory but were pruned\nby opponent actions before you could traverse them."
)
t.new_effect.declare_victory(source_player=PlayerId.TWO, enabled=1)

# Defeat - All villagers dead
t = trigger_manager.add_trigger("[Defeat] Villagers Eliminated")
t.new_condition.own_fewer_objects(
    quantity=1,
    source_player=PlayerId.ONE,
    object_list=UnitInfo.VILLAGER_MALE.ID
)
t.new_condition.own_fewer_objects(
    quantity=1,
    source_player=PlayerId.ONE,
    object_list=UnitInfo.VILLAGER_FEMALE.ID
)
t.new_effect.display_instructions(
    source_player=PlayerId.ONE,
    display_time=10,
    message="<RED>DEFEAT\n\nAll villagers eliminated by Mangudai.\nNo economy, no recovery possible.\n\nTiming collapse: The most game-relevant\ntype of unreachability."
)
t.new_effect.declare_victory(source_player=PlayerId.TWO, enabled=1)

# Save scenario
output_path = "u4_timing_collapse.aoe2scenario"
scenario.write_to_file(output_path)
print(f"Created: {output_path}")
print("Unreachability Type: TIMING_COLLAPSE")
print("Critical State: s0 (immediate - tempo differential unbridgeable)")
