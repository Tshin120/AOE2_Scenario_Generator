import sys
import io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

from AoE2ScenarioParser.scenarios.aoe2_de_scenario import AoE2DEScenario
from AoE2ScenarioParser.datasets.players import PlayerId
from AoE2ScenarioParser.datasets.units import UnitInfo
from AoE2ScenarioParser.datasets.buildings import BuildingInfo
from AoE2ScenarioParser.datasets.trigger_lists import *
from AoE2ScenarioParser.datasets.techs import TechInfo
from AoE2ScenarioParser.datasets.heroes import HeroInfo
from AoE2ScenarioParser.datasets.other import OtherInfo
from AoE2ScenarioParser.datasets.terrains import TerrainId

# Create new scenario
scenario = AoE2DEScenario.from_default()

# Get managers
unit_manager = scenario.unit_manager
trigger_manager = scenario.trigger_manager
map_manager = scenario.map_manager

# Get map size
map_size = map_manager.map_size
center = map_size // 2
quarter = map_size // 4
three_quarter = (map_size * 3) // 4

# Paint terrain
# Act 1 zone (first third)
for x in range(0, map_size//3):
    for y in range(0, map_size):
        tile = map_manager.get_tile(x=x, y=y)
        tile.terrain_id = TerrainId.GRASS_1.value

# Act 2 zone (middle third) 
for x in range(map_size//3, 2*map_size//3):
    for y in range(0, map_size):
        tile = map_manager.get_tile(x=x, y=y)
        tile.terrain_id = TerrainId.GRASS_2.value
        
# Act 3 zone (final third)
for x in range(2*map_size//3, map_size):
    for y in range(0, map_size):
        tile = map_manager.get_tile(x=x, y=y)
        tile.terrain_id = TerrainId.DIRT_1.value

# Player 1 starting area (Act 1)
player_start_x = quarter
player_start_y = quarter

# Player base
tc = unit_manager.add_unit(PlayerId.ONE, unit_const=BuildingInfo.TOWN_CENTER.ID, x=player_start_x, y=player_start_y)
barracks = unit_manager.add_unit(PlayerId.ONE, unit_const=BuildingInfo.BARRACKS.ID, x=player_start_x+5, y=player_start_y)
range_bld = unit_manager.add_unit(PlayerId.ONE, unit_const=BuildingInfo.ARCHERY_RANGE.ID, x=player_start_x+5, y=player_start_y+5)
stable = unit_manager.add_unit(PlayerId.ONE, unit_const=BuildingInfo.STABLE.ID, x=player_start_x+10, y=player_start_y)
blacksmith = unit_manager.add_unit(PlayerId.ONE, unit_const=BuildingInfo.BLACKSMITH.ID, x=player_start_x+10, y=player_start_y+5)

# Player starting units
hero = unit_manager.add_unit(PlayerId.ONE, unit_const=HeroInfo.ALEXANDER.ID, x=player_start_x+2, y=player_start_y+2)
for i in range(10):
    unit_manager.add_unit(PlayerId.ONE, unit_const=UnitInfo.MILITIA.ID, x=player_start_x+i, y=player_start_y+8)

# Enemy base (Act 3)
enemy_base_x = three_quarter
enemy_base_y = three_quarter

# Enemy fortress
villain_castle = unit_manager.add_unit(PlayerId.TWO, unit_const=BuildingInfo.CASTLE.ID, x=enemy_base_x, y=enemy_base_y)
villain = unit_manager.add_unit(PlayerId.TWO, unit_const=HeroInfo.DARIUS.ID, x=enemy_base_x+2, y=enemy_base_y+2)

# Enemy walls and gates
for i in range(15):
    unit_manager.add_unit(PlayerId.TWO, unit_const=BuildingInfo.STONE_WALL.ID, x=enemy_base_x-10+i, y=enemy_base_y-10)
    unit_manager.add_unit(PlayerId.TWO, unit_const=BuildingInfo.STONE_WALL.ID, x=enemy_base_x-10+i, y=enemy_base_y+10)
    unit_manager.add_unit(PlayerId.TWO, unit_const=BuildingInfo.STONE_WALL.ID, x=enemy_base_x-10, y=enemy_base_y-10+i)
    unit_manager.add_unit(PlayerId.TWO, unit_const=BuildingInfo.STONE_WALL.ID, x=enemy_base_x+10, y=enemy_base_y-10+i)

enemy_gate = unit_manager.add_unit(PlayerId.TWO, unit_const=BuildingInfo.GATE_NORTH_TO_SOUTH.ID, x=enemy_base_x, y=enemy_base_y-10)

# Enemy military buildings
unit_manager.add_unit(PlayerId.TWO, unit_const=BuildingInfo.BARRACKS.ID, x=enemy_base_x+5, y=enemy_base_y+5)
unit_manager.add_unit(PlayerId.TWO, unit_const=BuildingInfo.ARCHERY_RANGE.ID, x=enemy_base_x+5, y=enemy_base_y-5)
unit_manager.add_unit(PlayerId.TWO, unit_const=BuildingInfo.STABLE.ID, x=enemy_base_x-5, y=enemy_base_y+5)

# Enemy troops
for i in range(30):
    unit_manager.add_unit(PlayerId.TWO, unit_const=UnitInfo.IMMORTAL_MELEE.ID, x=enemy_base_x-5+i%5, y=enemy_base_y-5+i//5)

# Ally base (Act 1)
ally_base_x = quarter + 20
ally_base_y = quarter + 20

ally_tc = unit_manager.add_unit(PlayerId.THREE, unit_const=BuildingInfo.TOWN_CENTER.ID, x=ally_base_x, y=ally_base_y)
ally1 = unit_manager.add_unit(PlayerId.THREE, unit_const=HeroInfo.LEONIDAS.ID, x=ally_base_x+2, y=ally_base_y+2)

# Story props
flag1 = unit_manager.add_unit(PlayerId.GAIA, unit_const=OtherInfo.FLAG_A.ID, x=player_start_x+15, y=player_start_y+15)
ruins1 = unit_manager.add_unit(PlayerId.GAIA, unit_const=OtherInfo.ROMAN_RUINS.ID, x=center, y=center)

# GAIA resources near player start
for i in range(5):
    unit_manager.add_unit(PlayerId.GAIA, unit_const=OtherInfo.GOLD_MINE.ID, x=player_start_x+5+i, y=player_start_y-5)
    unit_manager.add_unit(PlayerId.GAIA, unit_const=OtherInfo.STONE_MINE.ID, x=player_start_x-5+i, y=player_start_y+10)
    unit_manager.add_unit(PlayerId.GAIA, unit_const=OtherInfo.FORAGE_BUSH.ID, x=player_start_x+10+i, y=player_start_y+10)
    unit_manager.add_unit(PlayerId.GAIA, unit_const=UnitInfo.SHEEP.ID, x=player_start_x+i, y=player_start_y-10)
    unit_manager.add_unit(PlayerId.GAIA, unit_const=UnitInfo.DEER.ID, x=player_start_x-10+i, y=player_start_y-5)

# === TRIGGERS ===

# Setup triggers
tech_trigger = trigger_manager.add_trigger("Techs")
tech_trigger.new_condition.timer(timer=1)
tech_trigger.new_effect.research_technology(source_player=PlayerId.ONE, technology=TechInfo.FORGING.ID)

easy_trigger = trigger_manager.add_trigger("Easy Difficulty") 
easy_trigger.new_condition.difficulty_level(quantity=0)
easy_trigger.new_effect.kill_object(source_player=PlayerId.TWO, area_x1=0, area_y1=0, area_x2=map_size, area_y2=map_size)

hard_trigger = trigger_manager.add_trigger("Hard Difficulty")
hard_trigger.new_condition.difficulty_level(quantity=3)
hard_trigger.new_effect.create_object(object_list_unit_id=UnitInfo.IMMORTAL_MELEE.ID, source_player=PlayerId.TWO, location_x=enemy_base_x, location_y=enemy_base_y)

enemy_ai = trigger_manager.add_trigger("Enemy AI Setup")
enemy_ai.new_condition.timer(timer=1)
enemy_ai.new_effect.patrol(object_list_unit_id=UnitInfo.IMMORTAL_MELEE.ID, source_player=PlayerId.TWO, location_x=center, location_y=center)

init_state = trigger_manager.add_trigger("Initial State")
init_state.new_condition.timer(timer=1)
init_state.new_effect.display_instructions(display_time=10, message="<YELLOW>Welcome to The Rise of Rome")

ally_ai = trigger_manager.add_trigger("Ally AI Setup")
ally_ai.new_condition.timer(timer=1)
ally_ai.new_effect.patrol(object_list_unit_id=UnitInfo.SPEARMAN.ID, source_player=PlayerId.THREE, location_x=ally_base_x+10, location_y=ally_base_y+10)

# Act 1 triggers
intro = trigger_manager.add_trigger("[D0] Intro")
intro.new_condition.timer(timer=5)
intro.new_effect.display_instructions(display_time=15, message="<YELLOW>In the early days of Rome, a young leader rises...")

hero_start = trigger_manager.add_trigger("[D1] Hero Awakens")
hero_start.new_condition.bring_object_to_area(unit_object=hero.reference_id, area_x1=player_start_x, area_y1=player_start_y, area_x2=player_start_x+10, area_y2=player_start_y+10)
hero_start.new_effect.display_instructions(display_time=10, message="<BLUE>We must unite the tribes of Italy")

# Add remaining Act 1-3 triggers following template...
# Add all objective triggers...
# Add all victory/defeat triggers...

# Victory condition
victory = trigger_manager.add_trigger("VC Primary")
victory.new_condition.destroy_object(unit_object=villain.reference_id)
victory.new_effect.declare_victory(source_player=PlayerId.ONE, enabled=1)

# Defeat condition
defeat = trigger_manager.add_trigger("Defeat - Hero Dies")
defeat.new_condition.destroy_object(unit_object=hero.reference_id)
defeat.new_effect.declare_victory(source_player=PlayerId.TWO, enabled=1)

# Save scenario
scenario.write_to_file("rise_of_rome.aoe2scenario")