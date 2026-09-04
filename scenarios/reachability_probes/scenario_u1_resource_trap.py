"""
U1: Resource Starvation Trap - UNREACHABLE Scenario

Graph Structure:
s0[Start: TC + 3 Vills, 200F/200W/0G/0S]
  -> n1[Gather sheep + wood]
    -> n2[Build Barracks, train Militia (no gold for M@A upgrade)]
      -> n3[Attack with 5-6 Militia vs full Byzantine base] -> D[Defeat]
    -> n2'[Try to reach Feudal: need 500F]
      -> n3'[Feudal reached but 200G = ~4 archers total]
        -> n4[All gold depleted. No market. No trade.] -> DEADLOCK
          -> Only Spearmen/Skirmishers possible (no gold units)
          -> Cannot break fortified Byzantine base -> D[Defeat]

Unreachability Point: Node n4 (gold depletion)
Critical State: Total gold = 400G. Byzantines with Cataphracts, walls, towers
               are impervious to any trash + minimal archer composition.
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
# PLAYER BASE: Goths - Enclosed area with CRITICALLY LIMITED resources
# ============================================================
player_base_x, player_base_y = quarter, quarter

# Town Center
unit_manager.add_unit(PlayerId.ONE, unit_const=BuildingInfo.TOWN_CENTER.ID,
                      x=player_base_x, y=player_base_y)

# Starting villagers (only 3)
for i in range(3):
    unit_manager.add_unit(PlayerId.ONE, unit_const=UnitInfo.VILLAGER_MALE.ID,
                          x=player_base_x + 3 + i, y=player_base_y)

# ============================================================
# THE TRAP: EXTREMELY LIMITED RESOURCES
# Total gold on map = 200G (starting 0 + 200 mined)
# No market, no trade, no relics
# ============================================================

# Only 4 sheep (minimal food - ~400F)
for i in range(4):
    unit_manager.add_unit(PlayerId.GAIA, unit_const=UnitInfo.SHEEP.ID,
                          x=player_base_x + 8 + i, y=player_base_y)

# Only 2 small wood patches (~500W each = 1000W total)
for patch in range(2):
    base_x = player_base_x + 12 + patch * 8
    for i in range(8):
        unit_manager.add_unit(PlayerId.GAIA, unit_const=OtherInfo.TREE_OAK.ID,
                              x=base_x + i % 4, y=player_base_y + 8 + i // 4)

# ONLY 200G total (1 small pile) - THIS IS THE CRITICAL CONSTRAINT
for i in range(3):
    unit_manager.add_unit(PlayerId.GAIA, unit_const=OtherInfo.GOLD_MINE.ID,
                          x=player_base_x + 8, y=player_base_y + 15 + i)

# NO STONE - cannot build castles, towers, or additional TCs
# NO FISH - no alternative food source
# NO RELICS - no infinite gold
# MARKET DISABLED via trigger

# ============================================================
# ENCLOSURE: Cliffs form impassable boundary (no expansion)
# ============================================================
wall_radius = 20
for i in range(wall_radius * 2):
    # North wall
    unit_manager.add_unit(PlayerId.GAIA, unit_const=OtherInfo.CLIFF_DEFAULT_2.ID,
                          x=player_base_x - wall_radius + i, y=player_base_y - wall_radius)
    # South wall
    unit_manager.add_unit(PlayerId.GAIA, unit_const=OtherInfo.CLIFF_DEFAULT_2.ID,
                          x=player_base_x - wall_radius + i, y=player_base_y + wall_radius)
    # East wall
    unit_manager.add_unit(PlayerId.GAIA, unit_const=OtherInfo.CLIFF_DEFAULT_2.ID,
                          x=player_base_x + wall_radius, y=player_base_y - wall_radius + i)
    # West wall (gap for enemy to enter - player cannot escape)
    if i < wall_radius - 4 or i > wall_radius + 4:
        unit_manager.add_unit(PlayerId.GAIA, unit_const=OtherInfo.CLIFF_DEFAULT_2.ID,
                              x=player_base_x - wall_radius, y=player_base_y - wall_radius + i)

# ============================================================
# ENEMY BASE: Byzantines - Full resources, heavily fortified
# ============================================================
enemy_base_x, enemy_base_y = three_quarter, three_quarter

# Enemy Town Center
unit_manager.add_unit(PlayerId.TWO, unit_const=BuildingInfo.TOWN_CENTER.ID,
                      x=enemy_base_x, y=enemy_base_y)

# Enemy Castle (requires siege to break - player can't make siege without gold)
unit_manager.add_unit(PlayerId.TWO, unit_const=BuildingInfo.CASTLE.ID,
                      x=enemy_base_x + 10, y=enemy_base_y)

# Stone walls around enemy base
for i in range(20):
    unit_manager.add_unit(PlayerId.TWO, unit_const=BuildingInfo.STONE_WALL.ID,
                          x=enemy_base_x - 10 + i, y=enemy_base_y - 8)
    unit_manager.add_unit(PlayerId.TWO, unit_const=BuildingInfo.STONE_WALL.ID,
                          x=enemy_base_x - 10 + i, y=enemy_base_y + 12)
    unit_manager.add_unit(PlayerId.TWO, unit_const=BuildingInfo.STONE_WALL.ID,
                          x=enemy_base_x - 10, y=enemy_base_y - 8 + i)
    unit_manager.add_unit(PlayerId.TWO, unit_const=BuildingInfo.STONE_WALL.ID,
                          x=enemy_base_x + 10, y=enemy_base_y - 8 + i)

# Enemy-owned gate (AI can exit)
enemy_gate = unit_manager.add_unit(PlayerId.TWO, unit_const=BuildingInfo.GATE_NORTH_TO_SOUTH.ID,
                                   x=enemy_base_x, y=enemy_base_y - 8)

# Guard towers
for i in range(4):
    unit_manager.add_unit(PlayerId.TWO, unit_const=BuildingInfo.GUARD_TOWER.ID,
                          x=enemy_base_x - 8 + i * 5, y=enemy_base_y - 5)

# THE COUNTER COMPOSITION: Cataphracts
# Cataphracts have trample damage and bonus vs infantry - hard counter to trash
for i in range(10):
    unit_manager.add_unit(PlayerId.TWO, unit_const=UnitInfo.CATAPHRACT.ID,
                          x=enemy_base_x + i % 5, y=enemy_base_y + 3 + i // 5)

# Enemy economy (full)
for i in range(15):
    unit_manager.add_unit(PlayerId.TWO, unit_const=UnitInfo.VILLAGER_MALE.ID,
                          x=enemy_base_x - 5 + i % 5, y=enemy_base_y + 6 + i // 5)

# Enemy resources (abundant)
for pile in range(5):
    for i in range(4):
        unit_manager.add_unit(PlayerId.GAIA, unit_const=OtherInfo.GOLD_MINE.ID,
                              x=enemy_base_x + 15 + pile * 3, y=enemy_base_y + i)

# ============================================================
# TRIGGERS
# ============================================================

# Setup - Introduction
t = trigger_manager.add_trigger("[Setup] U1 Resource Starvation Trap")
t.new_condition.timer(timer=1)
t.new_effect.display_instructions(
    source_player=PlayerId.ONE,
    display_time=20,
    message="<YELLOW>U1: RESOURCE STARVATION TRAP\n\n<RED>UNREACHABLE SCENARIO\n\nYou are the Goths, trapped in an enclosed area.\nTotal gold on map: 200G\nNo market access. No trade routes. No relics.\n\nThe Byzantines have Cataphracts and fortifications."
)

# Disable Market building (THE TRAP MECHANISM)
t = trigger_manager.add_trigger("[Trap] Disable Market")
t.new_condition.timer(timer=1)
t.new_effect.kill_object(
    object_list_unit_id=BuildingInfo.MARKET.ID,
    source_player=PlayerId.ONE,
    area_x1=0, area_y1=0, area_x2=map_size, area_y2=map_size
)

# Looping market destruction
t = trigger_manager.add_trigger("[Trap] Market Check Loop")
t.new_condition.timer(timer=10)
t.new_effect.kill_object(
    object_list_unit_id=BuildingInfo.MARKET.ID,
    source_player=PlayerId.ONE,
    area_x1=0, area_y1=0, area_x2=map_size, area_y2=map_size
)
t.new_effect.activate_trigger(trigger_id=2)

# State Analysis: s0
t = trigger_manager.add_trigger("[Analysis] State s0 - Initial")
t.new_condition.timer(timer=5)
t.new_effect.display_instructions(
    source_player=PlayerId.ONE,
    display_time=12,
    message="<ORANGE>[GRAPH STATE s0]\nStarting resources: 200F/200W/0G/0S\nMap resources: 4 sheep, ~1000W, 200G, 0 stone\n\nGold budget: Castle Age costs 200G alone.\nNo gold left for military production."
)

# State Analysis: n1 - Gathering
t = trigger_manager.add_trigger("[Analysis] State n1 - Gathering")
t.new_condition.timer(timer=90)
t.new_effect.display_instructions(
    source_player=PlayerId.ONE,
    display_time=10,
    message="<ORANGE>[GRAPH STATE n1]\nGathering sheep and wood.\nGold pile being mined...\n\nPath options:\n- n2: Militia rush (no gold for upgrades)\n- n2': Feudal advance (costs gold)"
)

# State Analysis: n3 - Gold Warning
t = trigger_manager.add_trigger("[Analysis] State n3 - Gold Depleting")
t.new_condition.timer(timer=180)
t.new_effect.display_instructions(
    source_player=PlayerId.ONE,
    display_time=12,
    message="<RED>[GRAPH STATE n3 APPROACHING]\nGold reserves critically low.\n\nOnce depleted:\n- Only trash units available (Spears, Skirms)\n- Byzantine Cataphracts counter ALL trash\n- Castle requires siege you cannot build"
)

# Critical State: n4 - Gold Depleted (UNREACHABILITY POINT)
t = trigger_manager.add_trigger("[Critical] State n4 - UNREACHABLE")
t.new_condition.timer(timer=300)
t.new_effect.display_instructions(
    source_player=PlayerId.ONE,
    display_time=20,
    message="<RED>[CRITICAL STATE n4 - UNREACHABILITY POINT]\n\nGOLD DEPLETED. NO RECOVERY POSSIBLE.\n\nRecovery mechanisms disabled:\n- Market: DISABLED\n- Trade routes: NONE\n- Relics: NONE\n- Expansion: BLOCKED by cliffs\n\nAll paths from n4 lead to D (Defeat).\nVictory node V is unreachable."
)

# Victory (technically exists but unreachable)
t = trigger_manager.add_trigger("[Victory] Conquest")
t.new_condition.own_fewer_objects(
    quantity=1,
    source_player=PlayerId.TWO,
    object_list=BuildingInfo.TOWN_CENTER.ID
)
t.new_condition.own_fewer_objects(
    quantity=1,
    source_player=PlayerId.TWO,
    object_list=BuildingInfo.CASTLE.ID
)
t.new_effect.display_instructions(
    source_player=PlayerId.ONE,
    display_time=10,
    message="<GREEN>VICTORY!\n\n(This state should be unreachable given constraints)"
)
t.new_effect.declare_victory(source_player=PlayerId.ONE, enabled=1)

# Defeat
t = trigger_manager.add_trigger("[Defeat] Player Eliminated")
t.new_condition.own_fewer_objects(
    quantity=1,
    source_player=PlayerId.ONE,
    object_list=BuildingInfo.TOWN_CENTER.ID
)
t.new_effect.display_instructions(
    source_player=PlayerId.ONE,
    display_time=10,
    message="<RED>DEFEAT\n\n[GRAPH STATE D]\nResource starvation made victory impossible.\nAll paths from n4 (gold depletion) led here."
)
t.new_effect.declare_victory(source_player=PlayerId.TWO, enabled=1)

# Save scenario
output_path = "u1_resource_starvation_trap.aoe2scenario"
scenario.write_to_file(output_path)
print(f"Created: {output_path}")
print("Unreachability Type: RESOURCE_DEAD_END")
print("Critical State: n4 (gold depletion with no recovery mechanism)")
