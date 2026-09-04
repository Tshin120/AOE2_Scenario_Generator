"""
U2: Tech Tree Lockout - UNREACHABLE Scenario

Map: Custom Arena-style (pre-walled)
Civilization: Player: Aztecs (no cavalry, no Bombard Cannon) | AI: Koreans
Scenario Trigger: At 30 min AI receives 10 War Wagons + 5 Onagers + 4 Keeps

Graph Structure:
s0[Start: Walled base, standard resources]
  -> n1[Boom economy safely]
    -> n2[Imperial Age, full Aztec tech]
      -> n3[Available units: Eagles, Jaguar Warriors, Monks, Siege Ram, Scorpion]
        -> n4a[Eagle rush vs War Wagons] -> War Wagons hard-counter Eagles -> D
        -> n4b[Siege push] -> Onagers destroy Siege Rams -> D
        -> n4c[Monk convert] -> War Wagons high pierce armor, Onagers kill Monks -> D
        -> n4d[Mass Jaguars] -> Jaguars are infantry, Onagers obliterate infantry -> D
      -> No Bombard Cannon (Aztec tech tree), no Trebuchet counter to Keeps
      -> All paths from n3 -> D

Unreachability Point: Node n3 (full tech unlocked)
Key Insight: Reachability fails due to tech tree structural constraints, not resources.
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
# PLAYER BASE: Aztecs - Arena style with FULL resources
# Resources are NOT the limiting factor here
# ============================================================
player_base_x, player_base_y = quarter, quarter

# Town Center
unit_manager.add_unit(PlayerId.ONE, unit_const=BuildingInfo.TOWN_CENTER.ID,
                      x=player_base_x, y=player_base_y)

# Generous starting villagers
for i in range(6):
    unit_manager.add_unit(PlayerId.ONE, unit_const=UnitInfo.VILLAGER_MALE.ID,
                          x=player_base_x + 3 + i % 3, y=player_base_y + i // 3)

# Aztec Hero: Cuauhtmoc
hero = unit_manager.add_unit(PlayerId.ONE, unit_const=HeroInfo.CUAUHTEMOC.ID,
                             x=player_base_x + 8, y=player_base_y)

# Military buildings (Aztec appropriate)
unit_manager.add_unit(PlayerId.ONE, unit_const=BuildingInfo.BARRACKS.ID,
                      x=player_base_x - 6, y=player_base_y)
unit_manager.add_unit(PlayerId.ONE, unit_const=BuildingInfo.ARCHERY_RANGE.ID,
                      x=player_base_x - 6, y=player_base_y + 5)
unit_manager.add_unit(PlayerId.ONE, unit_const=BuildingInfo.MONASTERY.ID,
                      x=player_base_x - 6, y=player_base_y + 10)
unit_manager.add_unit(PlayerId.ONE, unit_const=BuildingInfo.SIEGE_WORKSHOP.ID,
                      x=player_base_x - 6, y=player_base_y + 15)

# ABUNDANT RESOURCES - not the constraint
# Gold (plenty)
for pile in range(6):
    for i in range(5):
        unit_manager.add_unit(PlayerId.GAIA, unit_const=OtherInfo.GOLD_MINE.ID,
                              x=player_base_x + 12 + pile * 6, y=player_base_y + 8 + i)

# Stone (plenty)
for pile in range(4):
    for i in range(4):
        unit_manager.add_unit(PlayerId.GAIA, unit_const=OtherInfo.STONE_MINE.ID,
                              x=player_base_x + 12 + pile * 8, y=player_base_y + 25 + i)

# Forest (plenty)
for x in range(25):
    for y in range(12):
        unit_manager.add_unit(PlayerId.GAIA, unit_const=OtherInfo.TREE_OAK.ID,
                              x=player_base_x + 20 + x, y=player_base_y - 18 + y)

# Food (plenty)
for i in range(8):
    unit_manager.add_unit(PlayerId.GAIA, unit_const=UnitInfo.SHEEP.ID,
                          x=player_base_x + 10 + i % 4, y=player_base_y - 5 + i // 4)
for i in range(6):
    unit_manager.add_unit(PlayerId.GAIA, unit_const=OtherInfo.FORAGE_BUSH.ID,
                          x=player_base_x - 10 + i, y=player_base_y + 5)

# ============================================================
# ARENA WALLS: Pre-built protection (player can boom safely)
# ============================================================
wall_size = 35
for i in range(wall_size):
    # North wall
    unit_manager.add_unit(PlayerId.GAIA, unit_const=BuildingInfo.STONE_WALL.ID,
                          x=player_base_x - 15 + i, y=player_base_y - 20)
    # South wall
    unit_manager.add_unit(PlayerId.GAIA, unit_const=BuildingInfo.STONE_WALL.ID,
                          x=player_base_x - 15 + i, y=player_base_y + 30)
    # West wall
    unit_manager.add_unit(PlayerId.GAIA, unit_const=BuildingInfo.STONE_WALL.ID,
                          x=player_base_x - 15, y=player_base_y - 20 + i)
    # East wall
    unit_manager.add_unit(PlayerId.GAIA, unit_const=BuildingInfo.STONE_WALL.ID,
                          x=player_base_x + 20, y=player_base_y - 20 + i)

# ============================================================
# ENEMY BASE: Koreans - THE UNBEATABLE COMPOSITION
# War Wagons + Onagers + Keeps = no Aztec counter exists
# ============================================================
enemy_base_x, enemy_base_y = three_quarter, three_quarter

# Enemy infrastructure
unit_manager.add_unit(PlayerId.TWO, unit_const=BuildingInfo.TOWN_CENTER.ID,
                      x=enemy_base_x, y=enemy_base_y)
unit_manager.add_unit(PlayerId.TWO, unit_const=BuildingInfo.CASTLE.ID,
                      x=enemy_base_x + 10, y=enemy_base_y)
unit_manager.add_unit(PlayerId.TWO, unit_const=BuildingInfo.CASTLE.ID,
                      x=enemy_base_x - 8, y=enemy_base_y + 5)

# 4 Keeps (tower defense - Aztecs have no Bombard Cannon to counter)
for i in range(4):
    unit_manager.add_unit(PlayerId.TWO, unit_const=BuildingInfo.KEEP.ID,
                          x=enemy_base_x - 10 + i * 7, y=enemy_base_y - 10)

# THE COUNTER COMPOSITION:
# War Wagons: High pierce armor, fast, ranged - HARD COUNTER to Eagles
for i in range(10):
    unit_manager.add_unit(PlayerId.TWO, unit_const=UnitInfo.WAR_WAGON.ID,
                          x=enemy_base_x + i % 5 * 2, y=enemy_base_y + 5 + i // 5 * 2)

# Onagers: Area damage siege - OBLITERATE infantry (Jaguars, Eagles)
for i in range(5):
    unit_manager.add_unit(PlayerId.TWO, unit_const=UnitInfo.ONAGER.ID,
                          x=enemy_base_x + i * 3, y=enemy_base_y + 12)

# Enemy walls with gates (AI owns gates)
for i in range(25):
    unit_manager.add_unit(PlayerId.TWO, unit_const=BuildingInfo.STONE_WALL.ID,
                          x=enemy_base_x - 12 + i, y=enemy_base_y - 12)
    unit_manager.add_unit(PlayerId.TWO, unit_const=BuildingInfo.STONE_WALL.ID,
                          x=enemy_base_x - 12 + i, y=enemy_base_y + 18)
    unit_manager.add_unit(PlayerId.TWO, unit_const=BuildingInfo.STONE_WALL.ID,
                          x=enemy_base_x - 12, y=enemy_base_y - 12 + i)
    unit_manager.add_unit(PlayerId.TWO, unit_const=BuildingInfo.STONE_WALL.ID,
                          x=enemy_base_x + 13, y=enemy_base_y - 12 + i)

enemy_gate = unit_manager.add_unit(PlayerId.TWO, unit_const=BuildingInfo.GATE_NORTH_TO_SOUTH.ID,
                                   x=enemy_base_x, y=enemy_base_y - 12)

# ============================================================
# TRIGGERS
# ============================================================

# Setup
t = trigger_manager.add_trigger("[Setup] U2 Tech Tree Lockout")
t.new_condition.timer(timer=1)
t.new_effect.display_instructions(
    source_player=PlayerId.ONE,
    display_time=20,
    message="<YELLOW>U2: TECH TREE LOCKOUT\n\n<RED>UNREACHABLE SCENARIO\n\nYou are the Aztecs.\nEnemy: Koreans with War Wagons + Onagers + Keeps\n\n<ORANGE>AZTEC TECH TREE GAPS:\n- NO Cavalry\n- NO Bombard Cannon\n- NO effective counter to War Wagon + Onager"
)

# Tech Tree Analysis
t = trigger_manager.add_trigger("[Analysis] Aztec Tech Tree")
t.new_condition.timer(timer=15)
t.new_effect.display_instructions(
    source_player=PlayerId.ONE,
    display_time=18,
    message="<ORANGE>[TECH TREE ANALYSIS]\n\nAztec available units:\n- Eagle Warriors: Countered by War Wagons (high PA)\n- Jaguar Warriors: Killed by Onager splash\n- Archers/Skirms: Outranged by War Wagons\n- Siege Rams: Destroyed by Onagers\n- Monks: Killed by Onagers before converting\n- Scorpions: Killed by War Wagons\n\n<RED>NO BOMBARD CANNON = Cannot kill Keeps"
)

# State s0
t = trigger_manager.add_trigger("[Analysis] State s0 - Arena Start")
t.new_condition.timer(timer=10)
t.new_effect.display_instructions(
    source_player=PlayerId.ONE,
    display_time=10,
    message="<GREEN>[GRAPH STATE s0]\nSafe behind arena walls.\nFull resources available.\n\nThe constraint is NOT resources.\nThe constraint is TECH TREE STRUCTURE."
)

# 30 minute trigger - Enemy reinforcements
t = trigger_manager.add_trigger("[30min] Enemy Reinforced")
t.new_condition.timer(timer=1800)
t.new_effect.display_instructions(
    source_player=PlayerId.ONE,
    display_time=15,
    message="<RED>[SCENARIO TRIGGER - 30 MINUTES]\n\nEnemy receives reinforcements:\n+10 War Wagons\n+5 Onagers\n+4 Keeps fortify position\n\nEven at FULL Imperial tech, Aztecs have NO counter."
)
# Spawn additional War Wagons
for i in range(10):
    t.new_effect.create_object(
        object_list_unit_id=UnitInfo.WAR_WAGON.ID,
        source_player=PlayerId.TWO,
        location_x=enemy_base_x + i % 5 * 2,
        location_y=enemy_base_y + 15 + i // 5 * 2
    )
# Spawn additional Onagers
for i in range(5):
    t.new_effect.create_object(
        object_list_unit_id=UnitInfo.ONAGER.ID,
        source_player=PlayerId.TWO,
        location_x=enemy_base_x + i * 3,
        location_y=enemy_base_y + 20
    )

# Critical State n3 - Full tech, no counter
t = trigger_manager.add_trigger("[Critical] State n3 - Full Tech No Counter")
t.new_condition.timer(timer=2400)
t.new_effect.display_instructions(
    source_player=PlayerId.ONE,
    display_time=25,
    message="<RED>[CRITICAL STATE n3 - UNREACHABILITY POINT]\n\nFull Aztec tech unlocked. Analyzing all paths:\n\nn3 -> n4a [Eagle rush]: War Wagons have +3 PA, fast, kite Eagles -> D\nn3 -> n4b [Siege push]: Onagers one-shot Siege Rams -> D\nn3 -> n4c [Monk convert]: Onagers kill Monks at range -> D\nn3 -> n4d [Mass Jaguars]: Infantry, Onagers obliterate -> D\n\n<RED>ALL PATHS FROM n3 LEAD TO D\nEdges exist, but NONE reach Victory V."
)

# Counter attempt analysis triggers
t = trigger_manager.add_trigger("[Analysis] Eagle Attempt")
t.new_condition.own_objects(
    quantity=15,
    source_player=PlayerId.ONE,
    object_list=UnitInfo.EAGLE_WARRIOR.ID
)
t.new_effect.display_instructions(
    source_player=PlayerId.ONE,
    display_time=10,
    message="<ORANGE>[PATH n4a: Eagle Rush]\nEagles massed.\n\n<RED>COUNTER: War Wagons have +3 pierce armor.\nWar Wagons are faster than Eagles.\nWar Wagons kite and destroy Eagle mass.\n\nThis path does NOT reach V."
)

t = trigger_manager.add_trigger("[Analysis] Jaguar Attempt")
t.new_condition.own_objects(
    quantity=10,
    source_player=PlayerId.ONE,
    object_list=UnitInfo.JAGUAR_WARRIOR.ID
)
t.new_effect.display_instructions(
    source_player=PlayerId.ONE,
    display_time=10,
    message="<ORANGE>[PATH n4d: Jaguar Mass]\nJaguars massed.\n\n<RED>COUNTER: Jaguars are INFANTRY.\nOnagers deal 50 splash damage.\n5 Onagers destroy Jaguar mass in 2-3 volleys.\n\nThis path does NOT reach V."
)

# Victory (technically exists)
t = trigger_manager.add_trigger("[Victory] Conquest")
t.new_condition.own_fewer_objects(
    quantity=1,
    source_player=PlayerId.TWO,
    object_list=BuildingInfo.CASTLE.ID
)
t.new_effect.display_instructions(
    source_player=PlayerId.ONE,
    display_time=10,
    message="<GREEN>VICTORY!\n\n(Tech tree lockout should prevent this)"
)
t.new_effect.declare_victory(source_player=PlayerId.ONE, enabled=1)

# Defeat - Hero dies
t = trigger_manager.add_trigger("[Defeat] Cuauhtmoc Falls")
t.new_condition.destroy_object(unit_object=hero.reference_id)
t.new_effect.display_instructions(
    source_player=PlayerId.ONE,
    display_time=10,
    message="<RED>DEFEAT\n\n[GRAPH STATE D]\nCuauhtmoc has fallen.\nThe Aztec tech tree had no answer to\nWar Wagon + Onager + Keep composition."
)
t.new_effect.declare_victory(source_player=PlayerId.TWO, enabled=1)

# Save scenario
output_path = "u2_tech_tree_lockout.aoe2scenario"
scenario.write_to_file(output_path)
print(f"Created: {output_path}")
print("Unreachability Type: TECH_TREE_LOCKOUT")
print("Critical State: n3 (full Imperial tech, no counter in tech tree)")
