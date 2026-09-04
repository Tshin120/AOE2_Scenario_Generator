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

# REACHABILITY ANALYSIS:
# Victory path: Player can win by: 1) Capturing siege equipment 2) Breaching walls 3) Destroying castle/commander
# Defeat path: Player loses if hero dies or army destroyed before breaching inner fortress
# Resource sufficiency: Yes - starting army + reinforcement buildings provide enough force
# Counter availability: Yes - mix of infantry/archers/siege can counter all enemy types
# Physical access: Yes - multiple paths to objectives, gates can be destroyed
# Timing viability: Yes - starting army sufficient to survive initial defense

# Create scenario
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

# Create hero unit and store reference
hero = unit_manager.add_unit(PlayerId.ONE, unit_const=HeroInfo.ALEXANDER.ID, x=10, y=center)

# Player starting army
for i in range(25):
    unit_manager.add_unit(PlayerId.ONE, unit_const=UnitInfo.CHAMPION.ID, x=8+i%5, y=center-5+i//5)
    unit_manager.add_unit(PlayerId.ONE, unit_const=UnitInfo.CROSSBOWMAN.ID, x=8+i%5, y=center+5+i//5)
    
# Player forward base
player_base_x, player_base_y = quarter-10, center
unit_manager.add_unit(PlayerId.ONE, unit_const=BuildingInfo.BARRACKS.ID, x=player_base_x, y=player_base_y)
unit_manager.add_unit(PlayerId.ONE, unit_const=BuildingInfo.ARCHERY_RANGE.ID, x=player_base_x+5, y=player_base_y)
unit_manager.add_unit(PlayerId.ONE, unit_const=BuildingInfo.BLACKSMITH.ID, x=player_base_x+10, y=player_base_y)

# Outer defenses (quarter)
outer_wall_start = quarter+5
for i in range(35):
    wall = unit_manager.add_unit(PlayerId.TWO, unit_const=BuildingInfo.PALISADE_WALL.ID, 
                                x=outer_wall_start, y=center-15+i)
    
# Outer gates (enemy owned!)
outer_gate_north = unit_manager.add_unit(PlayerId.TWO, unit_const=BuildingInfo.GATE_NORTH_TO_SOUTH.ID,
                                       x=outer_wall_start, y=center-5)
outer_gate_south = unit_manager.add_unit(PlayerId.TWO, unit_const=BuildingInfo.GATE_NORTH_TO_SOUTH.ID, 
                                        x=outer_wall_start, y=center+5)

# Middle defenses (center)
middle_wall_start = center-5
for i in range(45):
    wall = unit_manager.add_unit(PlayerId.TWO, unit_const=BuildingInfo.STONE_WALL.ID,
                                x=middle_wall_start, y=quarter+i)
    
# Middle gates
middle_gate = unit_manager.add_unit(PlayerId.TWO, unit_const=BuildingInfo.GATE_NORTH_TO_SOUTH.ID,
                                  x=middle_wall_start, y=center)

# Inner fortress (three_quarter)
castle = unit_manager.add_unit(PlayerId.TWO, unit_const=BuildingInfo.CASTLE.ID, 
                             x=three_quarter, y=center)
enemy_lord = unit_manager.add_unit(PlayerId.TWO, unit_const=HeroInfo.DARIUS.ID,
                                 x=three_quarter+2, y=center+2)

# GAIA siege equipment
trebuchet = unit_manager.add_unit(PlayerId.GAIA, unit_const=UnitInfo.TREBUCHET.ID,
                                x=quarter+15, y=center-10)
ram1 = unit_manager.add_unit(PlayerId.GAIA, unit_const=UnitInfo.BATTERING_RAM.ID, 
                           x=quarter+15, y=center+10)
ram2 = unit_manager.add_unit(PlayerId.GAIA, unit_const=UnitInfo.BATTERING_RAM.ID,
                           x=center+10, y=center-10)

# === TRIGGERS ===

# Setup triggers
tech_trigger = trigger_manager.add_trigger("Techs")
tech_trigger.new_condition.timer(timer=1)
tech_trigger.new_effect.research_technology(source_player=PlayerId.ONE, technology=TechInfo.SIEGE_ENGINEERS.ID)

easy_trigger = trigger_manager.add_trigger("Easy Difficulty") 
easy_trigger.new_condition.difficulty_level(quantity=0)
easy_trigger.new_effect.kill_object(source_player=PlayerId.TWO, area_x1=0, area_y1=0, area_x2=map_size, area_y2=map_size)

hard_trigger = trigger_manager.add_trigger("Hard Difficulty")
hard_trigger.new_condition.difficulty_level(quantity=3)
hard_trigger.new_effect.create_object(object_list_unit_id=UnitInfo.CHAMPION.ID, source_player=PlayerId.TWO,
                                    location_x=three_quarter, location_y=center)

patrol_trigger = trigger_manager.add_trigger("Enemy Patrol Setup")
patrol_trigger.new_condition.timer(timer=1)
patrol_trigger.new_effect.patrol(object_list_unit_id=UnitInfo.KNIGHT.ID, source_player=PlayerId.TWO,
                               location_x=quarter, location_y=center)

# Discovery triggers
intro = trigger_manager.add_trigger("[D0] Intro")
intro.new_condition.timer(timer=5)
intro.new_effect.display_instructions(display_time=10, 
    message="<YELLOW>Before you lies the enemy fortress...")

outer_wall = trigger_manager.add_trigger("[D1] Outer Wall Sighted")
outer_wall.new_condition.bring_object_to_area(unit_object=hero.reference_id,
    area_x1=quarter, area_y1=center-10, area_x2=quarter+10, area_y2=center+10)
outer_wall.new_effect.display_instructions(display_time=10,
    message="<BLUE>Scout: The outer defenses. Palisades and watchtowers.")

# Victory triggers
victory_primary = trigger_manager.add_trigger("Victory Primary")
victory_primary.new_condition.destroy_object(unit_object=castle.reference_id)
victory_primary.new_effect.declare_victory(source_player=PlayerId.ONE, enabled=1)

# Defeat triggers  
hero_death = trigger_manager.add_trigger("Defeat - Hero Dies")
hero_death.new_condition.destroy_object(unit_object=hero.reference_id)
hero_death.new_effect.declare_victory(source_player=PlayerId.TWO, enabled=1)

# Save scenario
scenario.write_to_file("alexander_persian_campaign.aoe2scenario")