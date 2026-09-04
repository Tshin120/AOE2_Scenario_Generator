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

# Get map size and calculate positions
map_size = map_manager.map_size
center = map_size // 2
quarter = map_size // 4
three_quarter = (map_size * 3) // 4

# Player starting position (bottom left)
player_start_x = quarter
player_start_y = three_quarter

# Enemy fortress positions
outer_wall_x = center - 20
outer_wall_y = center - 20
middle_wall_x = center - 10 
middle_wall_y = center - 10
inner_wall_x = center
inner_wall_y = center

# Create hero unit for player
hero = unit_manager.add_unit(PlayerId.ONE, unit_const=HeroInfo.EL_CID.ID, x=player_start_x, y=player_start_y)

# Player starting army
for i in range(25):
    unit_manager.add_unit(PlayerId.ONE, unit_const=UnitInfo.CHAMPION.ID, x=player_start_x+i%5, y=player_start_y+i//5)
    unit_manager.add_unit(PlayerId.ONE, unit_const=UnitInfo.CROSSBOWMAN.ID, x=player_start_x+5+i%5, y=player_start_y+i//5)
    
# Player starting siege
for i in range(3):
    unit_manager.add_unit(PlayerId.ONE, unit_const=UnitInfo.BATTERING_RAM.ID, x=player_start_x+i, y=player_start_y+10)
    unit_manager.add_unit(PlayerId.ONE, unit_const=UnitInfo.MANGONEL.ID, x=player_start_x+i, y=player_start_y+12)

# Player forward base
unit_manager.add_unit(PlayerId.ONE, unit_const=BuildingInfo.BARRACKS.ID, x=player_start_x+15, y=player_start_y)
unit_manager.add_unit(PlayerId.ONE, unit_const=BuildingInfo.ARCHERY_RANGE.ID, x=player_start_x+20, y=player_start_y)
unit_manager.add_unit(PlayerId.ONE, unit_const=BuildingInfo.BLACKSMITH.ID, x=player_start_x+25, y=player_start_y)

# Outer defensive line
outer_gate = unit_manager.add_unit(PlayerId.TWO, unit_const=BuildingInfo.GATE_NORTH_TO_SOUTH.ID, x=outer_wall_x, y=outer_wall_y)
for i in range(30):
    unit_manager.add_unit(PlayerId.TWO, unit_const=BuildingInfo.PALISADE_WALL.ID, x=outer_wall_x+i, y=outer_wall_y)
    unit_manager.add_unit(PlayerId.TWO, unit_const=BuildingInfo.PALISADE_WALL.ID, x=outer_wall_x+i, y=outer_wall_y+30)
    
# Outer towers and garrison
for i in range(3):
    unit_manager.add_unit(PlayerId.TWO, unit_const=BuildingInfo.WATCH_TOWER.ID, x=outer_wall_x+10*i, y=outer_wall_y)
    for j in range(5):
        unit_manager.add_unit(PlayerId.TWO, unit_const=UnitInfo.SPEARMAN.ID, x=outer_wall_x+10*i+j, y=outer_wall_y+2)
        unit_manager.add_unit(PlayerId.TWO, unit_const=UnitInfo.ARCHER.ID, x=outer_wall_x+10*i+j, y=outer_wall_y+3)

# Middle defensive line  
middle_gate = unit_manager.add_unit(PlayerId.TWO, unit_const=BuildingInfo.GATE_NORTH_TO_SOUTH.ID, x=middle_wall_x, y=middle_wall_y)
for i in range(40):
    unit_manager.add_unit(PlayerId.TWO, unit_const=BuildingInfo.STONE_WALL.ID, x=middle_wall_x+i, y=middle_wall_y)
    unit_manager.add_unit(PlayerId.TWO, unit_const=BuildingInfo.STONE_WALL.ID, x=middle_wall_x+i, y=middle_wall_y+40)

# Middle towers and garrison
for i in range(5):
    unit_manager.add_unit(PlayerId.TWO, unit_const=BuildingInfo.GUARD_TOWER.ID, x=middle_wall_x+8*i, y=middle_wall_y)
    for j in range(4):
        unit_manager.add_unit(PlayerId.TWO, unit_const=UnitInfo.MAN_AT_ARMS.ID, x=middle_wall_x+8*i+j, y=middle_wall_y+2)
        unit_manager.add_unit(PlayerId.TWO, unit_const=UnitInfo.CROSSBOWMAN.ID, x=middle_wall_x+8*i+j, y=middle_wall_y+3)
        unit_manager.add_unit(PlayerId.TWO, unit_const=UnitInfo.LIGHT_CAVALRY.ID, x=middle_wall_x+8*i+j, y=middle_wall_y+4)

# Inner fortress
castle = unit_manager.add_unit(PlayerId.TWO, unit_const=BuildingInfo.CASTLE.ID, x=inner_wall_x, y=inner_wall_y)
inner_gate = unit_manager.add_unit(PlayerId.TWO, unit_const=BuildingInfo.GATE_NORTH_TO_SOUTH.ID, x=inner_wall_x-5, y=inner_wall_y)

# Inner buildings
unit_manager.add_unit(PlayerId.TWO, unit_const=BuildingInfo.TOWN_CENTER.ID, x=inner_wall_x+10, y=inner_wall_y)
unit_manager.add_unit(PlayerId.TWO, unit_const=BuildingInfo.BLACKSMITH.ID, x=inner_wall_x+15, y=inner_wall_y)
unit_manager.add_unit(PlayerId.TWO, unit_const=BuildingInfo.MONASTERY.ID, x=inner_wall_x+20, y=inner_wall_y)

# Inner towers and elite garrison
for i in range(6):
    unit_manager.add_unit(PlayerId.TWO, unit_const=BuildingInfo.KEEP.ID, x=inner_wall_x+6*i, y=inner_wall_y-5)
    for j in range(3):
        unit_manager.add_unit(PlayerId.TWO, unit_const=UnitInfo.CHAMPION.ID, x=inner_wall_x+6*i+j, y=inner_wall_y-3)
        unit_manager.add_unit(PlayerId.TWO, unit_const=UnitInfo.CAVALIER.ID, x=inner_wall_x+6*i+j, y=inner_wall_y-2)

# Enemy commander
enemy_lord = unit_manager.add_unit(PlayerId.TWO, unit_const=HeroInfo.SALADIN.ID, x=inner_wall_x+2, y=inner_wall_y+2)

# GAIA siege equipment
trebuchet = unit_manager.add_unit(PlayerId.GAIA, unit_const=UnitInfo.TREBUCHET.ID, x=outer_wall_x-10, y=outer_wall_y-10)
ram = unit_manager.add_unit(PlayerId.GAIA, unit_const=UnitInfo.BATTERING_RAM.ID, x=middle_wall_x-10, y=middle_wall_y-10)

# Setup triggers
tech_trigger = trigger_manager.add_trigger("Techs")
tech_trigger.new_condition.timer(timer=1)
tech_trigger.new_effect.research_technology(source_player=PlayerId.ONE, technology=TechInfo.SIEGE_ENGINEERS.ID)
tech_trigger.new_effect.research_technology(source_player=PlayerId.ONE, technology=TechInfo.CHEMISTRY.ID)

easy_trigger = trigger_manager.add_trigger("Easy Difficulty") 
easy_trigger.new_condition.difficulty_level(quantity=0)
easy_trigger.new_effect.kill_object(source_player=PlayerId.TWO, area_x1=0, area_y1=0, area_x2=map_size, area_y2=map_size)

hard_trigger = trigger_manager.add_trigger("Hard Difficulty")
hard_trigger.new_condition.difficulty_level(quantity=3)
hard_trigger.new_effect.create_object(object_list_unit_id=UnitInfo.CHAMPION.ID, source_player=PlayerId.TWO, location_x=inner_wall_x, location_y=inner_wall_y)

patrol_trigger = trigger_manager.add_trigger("Enemy Patrol Setup")
patrol_trigger.new_condition.timer(timer=1)
patrol_trigger.new_effect.patrol(object_list_unit_id=UnitInfo.KNIGHT.ID, source_player=PlayerId.TWO, location_x=outer_wall_x, location_y=outer_wall_y)

map_reveal = trigger_manager.add_trigger("Map Reveal")
map_reveal.new_condition.timer(timer=1)

start_grant = trigger_manager.add_trigger("Starting Grant")
start_grant.new_condition.timer(timer=1)
start_grant.new_effect.modify_attribute(source_player=PlayerId.ONE, attribute=1, amount=1000)

# Discovery triggers
intro = trigger_manager.add_trigger("[D0] Intro")
intro.new_condition.timer(timer=5)
intro.new_effect.display_instructions(display_time=10, message="<YELLOW>Before you lies the enemy fortress...")

outer_wall = trigger_manager.add_trigger("[D1] Outer Wall Sighted")
outer_wall.new_condition.bring_object_to_area(unit_object=hero.reference_id, area_x1=outer_wall_x-5, area_y1=outer_wall_y-5, area_x2=outer_wall_x+5, area_y2=outer_wall_y+5)
outer_wall.new_effect.display_instructions(display_time=10, message="<BLUE>Scout: The outer defenses. Palisades and watchtowers.")

# Continue with remaining triggers following template pattern...

# Save scenario
scenario.write_to_file("reconquista.aoe2scenario")