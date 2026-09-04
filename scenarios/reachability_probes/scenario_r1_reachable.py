"""
R1: Standard Open Map Skirmish - FULLY REACHABLE Scenario

Map: Arabia (open, standard resources)
Civilization: Player: Britons | AI: Franks
Starting Resources: Standard (200F, 200W, 100G, 200S)
Map Resources: 8 sheep, 2 boar, 4 deer, 7 gold piles, 5 stone piles, standard wood lines
Victory Condition: Conquest (destroy all enemy buildings/units)
AI Difficulty: Moderate

Graph Structure:
s0[Start: TC + 3 Vills + Scout]
  -> n1[Dark Age Economy: gather food/wood]
    -> n2[Feudal Age: build military buildings]
      -> n3a[Archers path] -> n4[Castle Age mass] -> V[Conquest]
      -> n3b[Scouts path]  -> n4[Castle Age mass] -> V[Conquest]
      -> n3c[M@A rush]     -> n4[Castle Age mass] -> V[Conquest]
    (At any ni: enemy raid -> n_recovery -> rebuild -> ni+1)

WHY REACHABLE:
- Standard Arabia provides sufficient resources across all four types
- Multiple gathering sites available
- Open map ensures player can always expand to new resource locations
- Multiple military paths (archers, cavalry, infantry) provide strategic redundancy
- Even after enemy raids, player retains TC production capability
- At every node in the graph, at least one edge leads toward V
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
# PLAYER BASE: Britons - Standard Dark Age Start
# ============================================================
player_base_x, player_base_y = quarter, quarter

# Town Center
player_tc = unit_manager.add_unit(PlayerId.ONE, unit_const=BuildingInfo.TOWN_CENTER.ID,
                                   x=player_base_x, y=player_base_y)

# Starting villagers (standard 3)
for i in range(3):
    unit_manager.add_unit(PlayerId.ONE, unit_const=UnitInfo.VILLAGER_MALE.ID,
                          x=player_base_x + 3 + i, y=player_base_y)

# Scout cavalry
scout = unit_manager.add_unit(PlayerId.ONE, unit_const=UnitInfo.SCOUT_CAVALRY.ID,
                              x=player_base_x + 6, y=player_base_y + 3)

# ============================================================
# FULL STANDARD RESOURCES - Enables multiple victory paths
# ============================================================

# 8 Sheep (close to TC, 100F each = 800F)
for i in range(8):
    unit_manager.add_unit(PlayerId.GAIA, unit_const=UnitInfo.SHEEP.ID,
                          x=player_base_x + 6 + i % 4, y=player_base_y - 3 + i // 4)

# 2 Boar (nearby, 340F each = 680F)
unit_manager.add_unit(PlayerId.GAIA, unit_const=UnitInfo.WILD_BOAR.ID,
                      x=player_base_x + 15, y=player_base_y + 8)
unit_manager.add_unit(PlayerId.GAIA, unit_const=UnitInfo.WILD_BOAR.ID,
                      x=player_base_x + 18, y=player_base_y + 12)

# 4 Deer (medium distance, 140F each = 560F)
for i in range(4):
    unit_manager.add_unit(PlayerId.GAIA, unit_const=UnitInfo.DEER.ID,
                          x=player_base_x + 22 + i, y=player_base_y - 5)

# 6 Forage bushes (125F each = 750F)
for i in range(6):
    unit_manager.add_unit(PlayerId.GAIA, unit_const=OtherInfo.FORAGE_BUSH.ID,
                          x=player_base_x - 8 + i, y=player_base_y + 4)

# 7 Gold piles (800G each = 5600G total - PLENTY for gold units)
gold_positions = [
    (player_base_x + 12, player_base_y + 20),
    (player_base_x + 25, player_base_y + 10),
    (player_base_x - 10, player_base_y + 25),
    (center, center + 15),
    (center - 15, center),
    (center + 10, quarter),
    (quarter, center + 10),
]
for gx, gy in gold_positions:
    for i in range(5):  # 5 tiles per pile
        unit_manager.add_unit(PlayerId.GAIA, unit_const=OtherInfo.GOLD_MINE.ID,
                              x=gx + i % 3, y=gy + i // 3)

# 5 Stone piles (350S each = 1750S - enough for castles/TCs)
stone_positions = [
    (player_base_x - 12, player_base_y + 15),
    (player_base_x + 30, player_base_y + 25),
    (center - 20, center + 10),
    (center + 15, quarter + 10),
    (quarter + 10, center - 10),
]
for sx, sy in stone_positions:
    for i in range(4):
        unit_manager.add_unit(PlayerId.GAIA, unit_const=OtherInfo.STONE_MINE.ID,
                              x=sx + i % 2, y=sy + i // 2)

# Standard wood lines (ABUNDANT - open map style with tree clusters)
# Main woodline near player
for x in range(20):
    for y in range(10):
        unit_manager.add_unit(PlayerId.GAIA, unit_const=OtherInfo.TREE_OAK.ID,
                              x=player_base_x + 20 + x, y=player_base_y - 15 + y)

# Secondary woodline
for x in range(15):
    for y in range(8):
        unit_manager.add_unit(PlayerId.GAIA, unit_const=OtherInfo.TREE_OAK.ID,
                              x=player_base_x - 15 + x, y=player_base_y + 30 + y)

# Forward woodline (for expansion)
for x in range(12):
    for y in range(6):
        unit_manager.add_unit(PlayerId.GAIA, unit_const=OtherInfo.TREE_OAK.ID,
                              x=center - 5 + x, y=center - 20 + y)

# ============================================================
# ENEMY BASE: Franks - Mirror start (fair matchup)
# ============================================================
enemy_base_x, enemy_base_y = three_quarter, three_quarter

# Enemy TC
enemy_tc = unit_manager.add_unit(PlayerId.TWO, unit_const=BuildingInfo.TOWN_CENTER.ID,
                                  x=enemy_base_x, y=enemy_base_y)

# Enemy villagers (standard 3)
for i in range(3):
    unit_manager.add_unit(PlayerId.TWO, unit_const=UnitInfo.VILLAGER_MALE.ID,
                          x=enemy_base_x + 3 + i, y=enemy_base_y)

# Enemy scout
unit_manager.add_unit(PlayerId.TWO, unit_const=UnitInfo.SCOUT_CAVALRY.ID,
                      x=enemy_base_x + 6, y=enemy_base_y + 3)

# Enemy resources (mirrored)
# Sheep
for i in range(8):
    unit_manager.add_unit(PlayerId.GAIA, unit_const=UnitInfo.SHEEP.ID,
                          x=enemy_base_x + 6 + i % 4, y=enemy_base_y - 3 + i // 4)

# Boar
unit_manager.add_unit(PlayerId.GAIA, unit_const=UnitInfo.WILD_BOAR.ID,
                      x=enemy_base_x - 15, y=enemy_base_y - 8)
unit_manager.add_unit(PlayerId.GAIA, unit_const=UnitInfo.WILD_BOAR.ID,
                      x=enemy_base_x - 18, y=enemy_base_y - 12)

# Gold
for pile in range(4):
    for i in range(5):
        unit_manager.add_unit(PlayerId.GAIA, unit_const=OtherInfo.GOLD_MINE.ID,
                              x=enemy_base_x - 15 + pile * 8, y=enemy_base_y + 15 + i)

# Stone
for pile in range(3):
    for i in range(4):
        unit_manager.add_unit(PlayerId.GAIA, unit_const=OtherInfo.STONE_MINE.ID,
                              x=enemy_base_x + 15 + pile * 6, y=enemy_base_y - 15 + i)

# Enemy woodline
for x in range(18):
    for y in range(8):
        unit_manager.add_unit(PlayerId.GAIA, unit_const=OtherInfo.TREE_OAK.ID,
                              x=enemy_base_x - 25 + x, y=enemy_base_y + 20 + y)

# Berries
for i in range(6):
    unit_manager.add_unit(PlayerId.GAIA, unit_const=OtherInfo.FORAGE_BUSH.ID,
                          x=enemy_base_x + 8 + i, y=enemy_base_y - 6)

# ============================================================
# TRIGGERS: Reachability demonstration
# ============================================================

# Setup
t = trigger_manager.add_trigger("[Setup] R1 Standard Skirmish - REACHABLE")
t.new_condition.timer(timer=1)
t.new_effect.display_instructions(
    source_player=PlayerId.ONE,
    display_time=20,
    message="<GREEN>R1: STANDARD OPEN MAP SKIRMISH\n\n<AQUA>FULLY REACHABLE SCENARIO\n\nYou are the Britons vs Franks on Arabia.\nStandard resources: 8 sheep, 2 boar, 7 gold piles, 5 stone piles.\n\nMultiple paths to victory exist.\nRecovery is always possible."
)

# Objectives
t = trigger_manager.add_trigger("[Objectives] Display")
t.new_condition.timer(timer=5)
t.new_effect.display_instructions(
    source_player=PlayerId.ONE,
    display_time=12,
    message="<AQUA>OBJECTIVES:\n- Build your economy\n- Train an army\n- Destroy the enemy Town Center and military\n\n<GREEN>VICTORY PATHS:\n- n3a: Archer rush -> Castle Age -> V\n- n3b: Scout rush -> Castle Age -> V\n- n3c: Men-at-Arms -> Castle Age -> V"
)

# State Analysis: s0
t = trigger_manager.add_trigger("[Analysis] State s0 - Initial")
t.new_condition.timer(timer=10)
t.new_effect.display_instructions(
    source_player=PlayerId.ONE,
    display_time=12,
    message="<GREEN>[GRAPH STATE s0]\n\nResources: 200F / 200W / 100G / 200S\nMap resources: ABUNDANT\n- Gold: 5600G available (multiple piles)\n- Stone: 1750S available\n- Wood: Unlimited (multiple forests)\n- Food: ~2800F (sheep, boar, deer, berries)\n\nAll four resource types accessible.\nMultiple paths to V exist."
)

# Path Analysis: Feudal options
t = trigger_manager.add_trigger("[Analysis] Feudal Age Reached")
t.new_condition.timer(timer=600)  # ~10 min
t.new_effect.display_instructions(
    source_player=PlayerId.ONE,
    display_time=12,
    message="<GREEN>[GRAPH STATE n2 - Feudal Age]\n\nMilitary options now available:\n\n-> n3a: Archers (Britons bonus: +1 range)\n-> n3b: Scouts (mobility, map control)\n-> n3c: Men-at-Arms (early pressure)\n\nEach path leads toward V.\nPath redundancy ensures reachability."
)

# Recovery demonstration
t = trigger_manager.add_trigger("[Analysis] Recovery Paths")
t.new_condition.timer(timer=900)  # 15 min
t.new_effect.display_instructions(
    source_player=PlayerId.ONE,
    display_time=12,
    message="<GREEN>[RECOVERY ANALYSIS]\n\nEven after setbacks:\n- Lost villagers? TC can produce more.\n- Lost military? Resources allow rebuilding.\n- Lost forward base? Fall back, re-expand.\n\nAs long as TC + villagers exist,\nrecovery paths lead back toward V.\n\nNO DEAD ENDS in this graph."
)

# Gold sustainability
t = trigger_manager.add_trigger("[Analysis] Gold Sustainability")
t.new_condition.timer(timer=1200)  # 20 min
t.new_effect.display_instructions(
    source_player=PlayerId.ONE,
    display_time=10,
    message="<GREEN>[RESOURCE SUSTAINABILITY]\n\n7 gold piles = 5600G total.\nMarket available for selling excess resources.\nTrade available if game extends.\nRelics provide infinite gold.\n\nNO resource dead end possible.\nGold units always available."
)

# Map control analysis
t = trigger_manager.add_trigger("[Analysis] Map Control")
t.new_condition.timer(timer=1500)  # 25 min
t.new_effect.display_instructions(
    source_player=PlayerId.ONE,
    display_time=10,
    message="<GREEN>[POSITIONAL ANALYSIS]\n\nOpen Arabia map:\n- No impassable barriers\n- Multiple attack angles\n- Forward positions available\n- Flanking routes exist\n\nNO positional traps.\nEnemy base is always reachable."
)

# Timing analysis
t = trigger_manager.add_trigger("[Analysis] Fair Timing")
t.new_condition.timer(timer=1800)  # 30 min
t.new_effect.display_instructions(
    source_player=PlayerId.ONE,
    display_time=10,
    message="<GREEN>[TIMING ANALYSIS]\n\nBoth players start Dark Age.\nFair economic start.\nNo overwhelming military advantage.\n\nPlayer has time to develop.\nNO timing collapse.\nVictory achievable through skill."
)

# Victory
t = trigger_manager.add_trigger("[Victory] Conquest")
t.new_condition.own_fewer_objects(
    quantity=1,
    source_player=PlayerId.TWO,
    object_list=BuildingInfo.TOWN_CENTER.ID
)
t.new_effect.display_instructions(
    source_player=PlayerId.ONE,
    display_time=12,
    message="<GREEN>VICTORY!\n\n[GRAPH STATE V - Victory]\n\nYou successfully traversed the state graph\nfrom s0 to V.\n\nThis demonstrates FULL REACHABILITY:\n- Multiple paths existed\n- Recovery was possible at every state\n- No dead ends encountered\n- Resources, tech, position, timing all favorable"
)
t.new_effect.declare_victory(source_player=PlayerId.ONE, enabled=1)

# Defeat (still possible but not forced)
t = trigger_manager.add_trigger("[Defeat] TC Lost")
t.new_condition.own_fewer_objects(
    quantity=1,
    source_player=PlayerId.ONE,
    object_list=BuildingInfo.TOWN_CENTER.ID
)
t.new_condition.own_fewer_objects(
    quantity=1,
    source_player=PlayerId.ONE,
    object_list=UnitInfo.VILLAGER_MALE.ID
)
t.new_effect.display_instructions(
    source_player=PlayerId.ONE,
    display_time=10,
    message="<RED>DEFEAT\n\nYou lost, but victory WAS achievable.\nThis was not an unreachable scenario.\n\nThe graph allowed paths to V.\nYou were outplayed, not trapped."
)
t.new_effect.declare_victory(source_player=PlayerId.TWO, enabled=1)

# Save scenario
output_path = "r1_standard_reachable.aoe2scenario"
scenario.write_to_file(output_path)
print(f"Created: {output_path}")
print("Reachability: FULL (at every state, path to V exists)")
print("Recovery: ALWAYS POSSIBLE (TC + villagers = rebuild)")
