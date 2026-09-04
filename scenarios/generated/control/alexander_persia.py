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

# Create hero unit and store reference
hero = unit_manager.add_unit(PlayerId.ONE, unit_const=HeroInfo.ALEXANDER.ID, x=10, y=center)

# Player starting army
for i in range(25):
    unit_manager.add_unit(PlayerId.ONE, unit_const=UnitInfo.CHAMPION.ID, x=5+i%5, y=center-10+i//5)
    unit_manager.add_unit(PlayerId.ONE, unit_const=UnitInfo.CROSSBOWMAN.ID, x=5+i%5, y=center+10+i//5)

# Player starting siege
for i in range(3):
    unit_manager.add_unit(PlayerId.ONE, unit_const=UnitInfo.BATTERING_RAM.ID, x=15+i, y=center)
    unit_manager.add_unit(PlayerId.ONE, unit_const=UnitInfo.MANGONEL.ID, x=15+i, y=center+5)

# Player forward base
unit_manager.add_unit(PlayerId.ONE, unit_const=BuildingInfo.BARRACKS.ID, x=20, y=center-10)
unit_manager.add_unit(PlayerId.ONE, unit_const=BuildingInfo.ARCHERY_RANGE.ID, x=20, y=center+10)
unit_manager.add_unit(PlayerId.ONE, unit_const=BuildingInfo.BLACKSMITH.ID, x=25, y=center)

# Outer defenses (quarter)
outer_wall_start = quarter
for i in range(35):
    unit_manager.add_unit(PlayerId.TWO, unit_const=BuildingInfo.PALISADE_WALL.ID, x=outer_wall_start, y=center-15+i)

# Outer towers
for i in range(3):
    unit_manager.add_unit(PlayerId.TWO, unit_const=BuildingInfo.WATCH_TOWER.ID, x=outer_wall_start+2, y=center-10+i*10)

# Outer gate (enemy owned!)
outer_gate = unit_manager.add_unit(PlayerId.TWO, unit_const=BuildingInfo.GATE_NORTH_TO_SOUTH.ID, x=outer_wall_start, y=center)

# Middle defenses (center)
middle_wall_start = center-10
for i in range(45):
    unit_manager.add_unit(PlayerId.TWO, unit_const=BuildingInfo.STONE_WALL.ID, x=middle_wall_start, y=center-20+i)

# Middle towers
for i in range(5):
    unit_manager.add_unit(PlayerId.TWO, unit_const=BuildingInfo.GUARD_TOWER.ID, x=middle_wall_start+2, y=center-15+i*8)

# Middle gate
middle_gate = unit_manager.add_unit(PlayerId.TWO, unit_const=BuildingInfo.GATE_NORTH_TO_SOUTH.ID, x=middle_wall_start, y=center)

# Inner fortress (three_quarter)
castle = unit_manager.add_unit(PlayerId.TWO, unit_const=BuildingInfo.CASTLE.ID, x=three_quarter, y=center)
enemy_lord = unit_manager.add_unit(PlayerId.TWO, unit_const=HeroInfo.DARIUS.ID, x=three_quarter+2, y=center)

# Inner keeps
for i in range(6):
    unit_manager.add_unit(PlayerId.TWO, unit_const=BuildingInfo.KEEP.ID, x=three_quarter-5+i%3*5, y=center-10+i//3*20)

# Inner gate
inner_gate = unit_manager.add_unit(PlayerId.TWO, unit_const=BuildingInfo.GATE_NORTH_TO_SOUTH.ID, x=three_quarter-8, y=center)

# GAIA siege equipment
trebuchet = unit_manager.add_unit(PlayerId.GAIA, unit_const=UnitInfo.TREBUCHET.ID, x=quarter+10, y=center-15)
ram = unit_manager.add_unit(PlayerId.GAIA, unit_const=UnitInfo.BATTERING_RAM.ID, x=center-15, y=center+15)

# Setup triggers
tech_trigger = trigger_manager.add_trigger("Techs")
tech_trigger.new_condition.timer(timer=1)
tech_trigger.new_effect.research_technology(source_player=PlayerId.ONE, technology=TechInfo.SIEGE_ENGINEERS.ID)

easy_trigger = trigger_manager.add_trigger("Easy Difficulty") 
easy_trigger.new_condition.difficulty_level(quantity=0)
easy_trigger.new_effect.kill_object(source_player=PlayerId.TWO, area_x1=0, area_y1=0, area_x2=map_size, area_y2=map_size)

hard_trigger = trigger_manager.add_trigger("Hard Difficulty")
hard_trigger.new_condition.difficulty_level(quantity=3)
hard_trigger.new_effect.create_object(object_list_unit_id=UnitInfo.CHAMPION.ID, source_player=PlayerId.TWO, location_x=three_quarter, location_y=center)

patrol_trigger = trigger_manager.add_trigger("Enemy Patrol Setup")
patrol_trigger.new_condition.timer(timer=1)
patrol_trigger.new_effect.patrol(object_list_unit_id=UnitInfo.CHAMPION.ID, source_player=PlayerId.TWO, location_x=quarter, location_y=center)

map_trigger = trigger_manager.add_trigger("Map Reveal")
map_trigger.new_condition.timer(timer=1)

start_trigger = trigger_manager.add_trigger("Starting Grant")
start_trigger.new_condition.timer(timer=1)

# Discovery triggers
intro = trigger_manager.add_trigger("[D0] Intro")
intro.new_condition.timer(timer=5)
intro.new_effect.display_instructions(display_time=10, message="<YELLOW>Before you lies the enemy fortress...")

outer_sight = trigger_manager.add_trigger("[D1] Outer Wall Sighted")
outer_sight.new_condition.bring_object_to_area(unit_object=hero.reference_id, area_x1=quarter-5, area_y1=0, area_x2=quarter+5, area_y2=map_size)
outer_sight.new_effect.display_instructions(display_time=10, message="<BLUE>Scout: The outer defenses. Palisades and watchtowers.")

# Add remaining discovery triggers...

# Capture triggers
siege1_capture = trigger_manager.add_trigger("Capture Siege 1")
siege1_capture.new_condition.bring_object_to_area(unit_object=hero.reference_id, area_x1=trebuchet.x-2, area_y1=trebuchet.y-2, area_x2=trebuchet.x+2, area_y2=trebuchet.y+2)
siege1_capture.new_effect.change_ownership(source_player=PlayerId.GAIA, target_player=PlayerId.ONE, area_x1=trebuchet.x-2, area_y1=trebuchet.y-2, area_x2=trebuchet.x+2, area_y2=trebuchet.y+2)

# Add remaining capture triggers...

# Gate/Breach triggers
outer_breach = trigger_manager.add_trigger("Outer Gate Breached")
outer_breach.new_condition.destroy_object(unit_object=outer_gate.reference_id)
outer_breach.new_effect.display_instructions(display_time=10, message="The outer gate has fallen!")

# Add remaining breach triggers...

# Victory triggers
v1 = trigger_manager.add_trigger("V/1 Outer Cleared")
v1.new_condition.objects_in_area(quantity=0, object_list=UnitInfo.CHAMPION.ID, source_player=PlayerId.TWO, area_x1=0, area_y1=0, area_x2=quarter+10, area_y2=map_size)
v1.new_effect.display_instructions(display_time=10, message="Phase 1 complete: Outer defenses fallen!")

# Add remaining victory triggers...

# Objective triggers
main_obj = trigger_manager.add_trigger("[O] Main Objectives")
main_obj.new_condition.timer(timer=1)
main_obj.new_effect.display_instructions(display_time=20, message="Breach the enemy fortress and destroy their stronghold.\n1. Break through the outer defenses\n2. Breach the middle walls\n3. Storm the inner keep and destroy the castle")

# Add remaining objective triggers...

# Defeat triggers
hero_death = trigger_manager.add_trigger("Defeat - Hero Dies")
hero_death.new_condition.destroy_object(unit_object=hero.reference_id)
hero_death.new_effect.declare_victory(source_player=PlayerId.TWO, enabled=1)

# Add remaining defeat triggers...

# Save scenario
scenario.write_to_file("alexander_persian_campaign.aoe2scenario")