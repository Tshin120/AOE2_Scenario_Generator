"""
U3: Positional Impossibility - UNREACHABLE Scenario

Map: Custom - Player on small island (15x15 tiles). Enemy on mainland.
Civilization: Player: Celts (weak navy) | AI: Vikings (strong navy)
Constraints: Transport Ships DISABLED via scenario trigger

Graph Structure:
s0[Start: Tiny island, no transport capability]
  -> n1[Gather limited resources]
    -> n2[Build Dock]
      -> n3[Fishing Ships (no deep fish) + Galleys]
        -> n4[Naval battle vs Vikings (superior navy civ)] -> D
    -> n2'[Build military on island]
      -> n3'[Army sits on island with no way to reach enemy] -> STALEMATE
        -> Resources deplete -> D
  No Transport Ships -> no edge connecting island to mainland
  Mainland = unreachable subgraph -> Enemy buildings unreachable -> V unreachable

Unreachability Point: Immediate (s0)
Key Insight: This is the purest form of unreachability - topological disconnection.
             Victory node V is literally unreachable regardless of actions.
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
# PAINT WATER EVERYWHERE FIRST
# ============================================================
for x in range(map_size):
    for y in range(map_size):
        tile = map_manager.get_tile(x=x, y=y)
        tile.terrain_id = TerrainId.WATER_DEEP.value

# ============================================================
# PLAYER ISLAND: Tiny (15x15 tiles) - THE PRISON
# ============================================================
island_x, island_y = quarter - 5, center - 7
island_size = 15

# Create island terrain
for x in range(island_size):
    for y in range(island_size):
        tile = map_manager.get_tile(x=island_x + x, y=island_y + y)
        tile.terrain_id = TerrainId.GRASS_1.value

# Beach edges
for x in range(-1, island_size + 1):
    for y in [-1, island_size]:
        if 0 <= island_x + x < map_size and 0 <= island_y + y < map_size:
            tile = map_manager.get_tile(x=island_x + x, y=island_y + y)
            tile.terrain_id = TerrainId.BEACH.value
for y in range(-1, island_size + 1):
    for x in [-1, island_size]:
        if 0 <= island_x + x < map_size and 0 <= island_y + y < map_size:
            tile = map_manager.get_tile(x=island_x + x, y=island_y + y)
            tile.terrain_id = TerrainId.BEACH.value

# Town Center on island
tc_x, tc_y = island_x + 5, island_y + 5
unit_manager.add_unit(PlayerId.ONE, unit_const=BuildingInfo.TOWN_CENTER.ID,
                      x=tc_x, y=tc_y)

# Starting villagers
for i in range(3):
    unit_manager.add_unit(PlayerId.ONE, unit_const=UnitInfo.VILLAGER_MALE.ID,
                          x=tc_x + 3 + i, y=tc_y)

# Celtic Hero
hero = unit_manager.add_unit(PlayerId.ONE, unit_const=HeroInfo.WILLIAM_WALLACE.ID,
                             x=tc_x + 2, y=tc_y + 3)

# ============================================================
# LIMITED ISLAND RESOURCES
# ============================================================
# 3 sheep
for i in range(3):
    unit_manager.add_unit(PlayerId.GAIA, unit_const=UnitInfo.SHEEP.ID,
                          x=tc_x + 5 + i, y=tc_y + 2)

# 1 small wood patch (~300W)
for i in range(5):
    unit_manager.add_unit(PlayerId.GAIA, unit_const=OtherInfo.TREE_OAK.ID,
                          x=island_x + 1 + i, y=island_y + 1)

# 1 gold pile (100G) - minimal
for i in range(2):
    unit_manager.add_unit(PlayerId.GAIA, unit_const=OtherInfo.GOLD_MINE.ID,
                          x=island_x + 10, y=island_y + 10 + i)

# NO STONE
# NO DEEP FISH around island

# Dock (can build ships but NOT transports)
unit_manager.add_unit(PlayerId.ONE, unit_const=BuildingInfo.DOCK.ID,
                      x=island_x + island_size, y=island_y + 5)

# ============================================================
# MAINLAND: Enemy base with full resources - THE GOAL
# ============================================================
mainland_start_x = three_quarter - 15
mainland_width = map_size - mainland_start_x - 3

# Create mainland terrain
for x in range(mainland_width):
    for y in range(map_size - 6):
        if mainland_start_x + x < map_size:
            tile = map_manager.get_tile(x=mainland_start_x + x, y=3 + y)
            tile.terrain_id = TerrainId.GRASS_1.value

# Beach transition on mainland west edge
for y in range(map_size - 6):
    if mainland_start_x - 1 >= 0:
        tile = map_manager.get_tile(x=mainland_start_x - 1, y=3 + y)
        tile.terrain_id = TerrainId.BEACH.value

# Enemy base on mainland
enemy_base_x = mainland_start_x + 12
enemy_base_y = center

# Viking Town Center (THE CONQUEST TARGET - on mainland)
enemy_tc = unit_manager.add_unit(PlayerId.TWO, unit_const=BuildingInfo.TOWN_CENTER.ID,
                                  x=enemy_base_x, y=enemy_base_y)

# Viking Castle
unit_manager.add_unit(PlayerId.TWO, unit_const=BuildingInfo.CASTLE.ID,
                      x=enemy_base_x + 8, y=enemy_base_y)

# Viking Dock (strong navy civ)
unit_manager.add_unit(PlayerId.TWO, unit_const=BuildingInfo.DOCK.ID,
                      x=mainland_start_x, y=enemy_base_y)

# Viking navy - Longboats (unique ship, very strong)
for i in range(5):
    unit_manager.add_unit(PlayerId.TWO, unit_const=UnitInfo.LONGBOAT.ID,
                          x=mainland_start_x - 8, y=enemy_base_y - 12 + i * 5)

# Fire Ships
for i in range(3):
    unit_manager.add_unit(PlayerId.TWO, unit_const=UnitInfo.FIRE_SHIP.ID,
                          x=mainland_start_x - 5, y=enemy_base_y - 8 + i * 5)

# Viking land military on mainland (Berserks)
for i in range(15):
    unit_manager.add_unit(PlayerId.TWO, unit_const=UnitInfo.BERSERK.ID,
                          x=enemy_base_x + i % 5, y=enemy_base_y + 5 + i // 5)

# Villagers
for i in range(10):
    unit_manager.add_unit(PlayerId.TWO, unit_const=UnitInfo.VILLAGER_MALE.ID,
                          x=enemy_base_x + 10 + i % 5, y=enemy_base_y + i // 5)

# Mainland resources (abundant)
for pile in range(4):
    for i in range(5):
        unit_manager.add_unit(PlayerId.GAIA, unit_const=OtherInfo.GOLD_MINE.ID,
                              x=enemy_base_x + 15 + pile * 5, y=enemy_base_y - 10 + i)

for x in range(20):
    for y in range(8):
        if enemy_base_x + 5 + x < map_size:
            unit_manager.add_unit(PlayerId.GAIA, unit_const=OtherInfo.TREE_OAK.ID,
                                  x=enemy_base_x + 5 + x, y=enemy_base_y + 15 + y)

# ============================================================
# TRIGGERS
# ============================================================

# Setup
t = trigger_manager.add_trigger("[Setup] U3 Positional Impossibility")
t.new_condition.timer(timer=1)
t.new_effect.display_instructions(
    source_player=PlayerId.ONE,
    display_time=20,
    message="<YELLOW>U3: POSITIONAL IMPOSSIBILITY\n\n<RED>UNREACHABLE SCENARIO\n\nYou are trapped on a tiny island (15x15 tiles).\nVictory requires conquering the Viking mainland.\n\n<RED>CRITICAL: TRANSPORT SHIPS ARE DISABLED\n\nThere is NO WAY to reach the mainland."
)

# THE TRAP: Disable Transport Ships
t = trigger_manager.add_trigger("[Trap] Disable Transports - Init")
t.new_condition.timer(timer=1)
t.new_effect.kill_object(
    object_list_unit_id=UnitInfo.TRANSPORT_SHIP.ID,
    source_player=PlayerId.ONE,
    area_x1=0, area_y1=0, area_x2=map_size, area_y2=map_size
)

# Continuous transport destruction loop
t = trigger_manager.add_trigger("[Trap] Transport Check Loop")
t.new_condition.timer(timer=5)
t.new_effect.kill_object(
    object_list_unit_id=UnitInfo.TRANSPORT_SHIP.ID,
    source_player=PlayerId.ONE,
    area_x1=0, area_y1=0, area_x2=map_size, area_y2=map_size
)
t.new_effect.display_instructions(
    source_player=PlayerId.ONE,
    display_time=5,
    message="<RED>Transport Ship destroyed! Transports are DISABLED in this scenario."
)
t.new_effect.activate_trigger(trigger_id=2)

# State Analysis: s0 - IMMEDIATELY UNREACHABLE
t = trigger_manager.add_trigger("[Analysis] State s0 - Topological Disconnection")
t.new_condition.timer(timer=5)
t.new_effect.display_instructions(
    source_player=PlayerId.ONE,
    display_time=18,
    message="<RED>[GRAPH STATE s0 - IMMEDIATELY UNREACHABLE]\n\nGraph analysis:\n- Victory node V: Destroy enemy TC on MAINLAND\n- Player states: All on ISLAND\n- Transport Ships: DISABLED\n\nThe graph has TWO DISCONNECTED COMPONENTS:\n1. {Island states} - where player exists\n2. {Mainland states including V} - unreachable\n\n<RED>NO EDGE CONNECTS ISLAND TO MAINLAND\nV is topologically unreachable from s0."
)

# Naval path analysis
t = trigger_manager.add_trigger("[Analysis] Naval Combat Attempt")
t.new_condition.own_objects(
    quantity=3,
    source_player=PlayerId.ONE,
    object_list=UnitInfo.GALLEY.ID
)
t.new_effect.display_instructions(
    source_player=PlayerId.ONE,
    display_time=12,
    message="<ORANGE>[PATH ANALYSIS: Naval Combat]\n\nGalleys built. Can engage enemy ships.\n\n<RED>BUT: Victory condition is CONQUEST.\nConquest requires destroying enemy BUILDINGS.\nBuildings are on LAND.\nGalleys cannot attack buildings on land.\nNo transports to carry land units.\n\nNaval path does NOT reach V."
)

# Resource depletion warning
t = trigger_manager.add_trigger("[Analysis] Island Resources Depleting")
t.new_condition.timer(timer=300)
t.new_effect.display_instructions(
    source_player=PlayerId.ONE,
    display_time=12,
    message="<ORANGE>[STATE: Resource Depletion]\n\nIsland resources:\n- 3 sheep: Likely gathered\n- ~300W trees: Depleting\n- ~100G gold: Depleting\n- 0 stone: None\n\n<RED>Even with INFINITE resources,\npositional constraint makes V unreachable.\nThe problem is TOPOLOGY, not resources."
)

# Land army analysis
t = trigger_manager.add_trigger("[Analysis] Land Army Built")
t.new_condition.own_objects(
    quantity=10,
    source_player=PlayerId.ONE,
    object_list=UnitInfo.MILITIA.ID
)
t.new_effect.display_instructions(
    source_player=PlayerId.ONE,
    display_time=10,
    message="<ORANGE>[PATH: Land Army]\n\nMilitia trained. Army stands ready.\n\n<RED>PROBLEM: Army is on ISLAND.\nEnemy buildings are on MAINLAND.\nNo Transport Ships to cross water.\n\nArmy cannot reach enemy.\nThis path does NOT reach V."
)

# Stalemate detection
t = trigger_manager.add_trigger("[Analysis] Stalemate Condition")
t.new_condition.timer(timer=600)
t.new_effect.display_instructions(
    source_player=PlayerId.ONE,
    display_time=15,
    message="<RED>[STATE: STALEMATE]\n\n10 minutes elapsed.\nPlayer confined to island.\nEnemy confined to mainland.\n\nNeither can reach the other's buildings.\n(Vikings have no reason to attack island)\n\nGame state: Infinite stalemate\nVictory: IMPOSSIBLE\nThis is positional unreachability."
)

# Victory (impossible to reach)
t = trigger_manager.add_trigger("[Victory] Conquest")
t.new_condition.own_fewer_objects(
    quantity=1,
    source_player=PlayerId.TWO,
    object_list=BuildingInfo.TOWN_CENTER.ID
)
t.new_effect.display_instructions(
    source_player=PlayerId.ONE,
    display_time=10,
    message="<GREEN>VICTORY!\n\n(This should be impossible - topology prevents it)"
)
t.new_effect.declare_victory(source_player=PlayerId.ONE, enabled=1)

# Defeat - Hero dies
t = trigger_manager.add_trigger("[Defeat] William Wallace Falls")
t.new_condition.destroy_object(unit_object=hero.reference_id)
t.new_effect.display_instructions(
    source_player=PlayerId.ONE,
    display_time=10,
    message="<RED>DEFEAT\n\n[GRAPH STATE D]\nWilliam Wallace has fallen.\nPositional trap made victory impossible from s0.\n\nThe mainland was always unreachable."
)
t.new_effect.declare_victory(source_player=PlayerId.TWO, enabled=1)

# Defeat - TC destroyed
t = trigger_manager.add_trigger("[Defeat] Island Overrun")
t.new_condition.own_fewer_objects(
    quantity=1,
    source_player=PlayerId.ONE,
    object_list=BuildingInfo.TOWN_CENTER.ID
)
t.new_effect.display_instructions(
    source_player=PlayerId.ONE,
    display_time=10,
    message="<RED>DEFEAT\n\n[GRAPH STATE D]\nIsland civilization destroyed.\n\nPositional trap made V unreachable from s0.\nThe state graph had disconnected components."
)
t.new_effect.declare_victory(source_player=PlayerId.TWO, enabled=1)

# Save scenario
output_path = "u3_positional_trap.aoe2scenario"
scenario.write_to_file(output_path)
print(f"Created: {output_path}")
print("Unreachability Type: POSITIONAL_TRAP")
print("Critical State: s0 (immediate - graph has disconnected components)")
