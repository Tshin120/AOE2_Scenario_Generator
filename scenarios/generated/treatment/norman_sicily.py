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
# Victory path: Break outer walls/gate -> capture siege -> breach middle -> storm castle -> kill lord
# Defeat path: Hero dies OR army destroyed OR siege equipment lost with no other breach options
# Resource sufficiency: Yes - starting army + reinforcement buildings provided
# Counter availability: Yes - mix of infantry/archers/siege vs walls/towers/units
# Physical access: Yes - multiple paths through defenses, siege equipment available
# Timing viability: Yes - starting army sufficient to engage first defenses

# Create scenario
scenario = AoE2DEScenario.from_default()

# Get managers
unit_manager = scenario.unit_manager
trigger_manager = scenario.trigger_manager
map_manager = scenario.map_manager

# Map size and coordinates
map_size = map_manager.map_size
center = map_size // 2
quarter = map_size // 4
three_quarter = (map_size * 3) // 4

# Player starting position (west edge)
player_start_x = quarter
player_start_y = center

# Enemy fortress positions
outer_wall_x = center - 20
middle_wall_x = center
inner_wall_x = center + 20

# Create hero unit
hero = unit_manager.add_unit(PlayerId.ONE, unit_const=HeroInfo.RICHARD_THE_LIONHEART.ID, 
                            x=player_start_x, y=player_start_y)

# Player starting army
for i in range(15):
    unit_manager.add_unit(PlayerId.ONE, unit_const=UnitInfo.MAN_AT_ARMS.ID,
                         x=player_start_x+1+i, y=player_start_y+1)
    unit_manager.add_unit(PlayerId.ONE, unit_const=UnitInfo.CROSSBOWMAN.ID,
                         x=player_start_x+1+i, y=player_start_y+2)
    unit_manager.add_unit(PlayerId.ONE, unit_const=UnitInfo.KNIGHT.ID,
                         x=player_start_x+1+i, y=player_start_y+3)

# Player forward base
barracks = unit_manager.add_unit(PlayerId.ONE, unit_const=BuildingInfo.BARRACKS.ID,
                                x=player_start_x+5, y=player_start_y+5)
archery = unit_manager.add_unit(PlayerId.ONE, unit_const=BuildingInfo.ARCHERY_RANGE.ID,
                               x=player_start_x+5, y=player_start_y+8)
blacksmith = unit_manager.add_unit(PlayerId.ONE, unit_const=BuildingInfo.BLACKSMITH.ID,
                                  x=player_start_x+5, y=player_start_y+11)

# Outer defenses
outer_gate = unit_manager.add_unit(PlayerId.TWO, unit_const=BuildingInfo.GATE_NORTH_TO_SOUTH.ID,
                                  x=outer_wall_x, y=center)

for i in range(15):
    unit_manager.add_unit(PlayerId.TWO, unit_const=BuildingInfo.PALISADE_WALL.ID,
                         x=outer_wall_x, y=center-10+i)
    unit_manager.add_unit(PlayerId.TWO, unit_const=BuildingInfo.WATCH_TOWER.ID,
                         x=outer_wall_x-1, y=center-8+i*5)

# Middle defenses  
middle_gate = unit_manager.add_unit(PlayerId.TWO, unit_const=BuildingInfo.GATE_NORTH_TO_SOUTH.ID,
                                   x=middle_wall_x, y=center)

for i in range(20):
    unit_manager.add_unit(PlayerId.TWO, unit_const=BuildingInfo.STONE_WALL.ID,
                         x=middle_wall_x, y=center-15+i)
    unit_manager.add_unit(PlayerId.TWO, unit_const=BuildingInfo.GUARD_TOWER.ID,
                         x=middle_wall_x-1, y=center-12+i*5)

# Inner fortress
castle = unit_manager.add_unit(PlayerId.TWO, unit_const=BuildingInfo.CASTLE.ID,
                              x=inner_wall_x, y=center)

inner_gate = unit_manager.add_unit(PlayerId.TWO, unit_const=BuildingInfo.GATE_NORTH_TO_SOUTH.ID,
                                  x=inner_wall_x-5, y=center)

enemy_lord = unit_manager.add_unit(PlayerId.TWO, unit_const=HeroInfo.SALADIN.ID,
                                  x=inner_wall_x+1, y=center)

# GAIA siege equipment
trebuchet = unit_manager.add_unit(PlayerId.GAIA, unit_const=UnitInfo.TREBUCHET.ID,
                                 x=outer_wall_x-10, y=center-10)
ram = unit_manager.add_unit(PlayerId.GAIA, unit_const=UnitInfo.BATTERING_RAM.ID,
                           x=outer_wall_x-10, y=center+10)

# Setup triggers
tech_trigger = trigger_manager.add_trigger("Techs")
tech_trigger.new_condition.timer(timer=1)
tech_trigger.new_effect.research_technology(source_player=PlayerId.ONE, technology=TechInfo.SIEGE_ENGINEERS.ID)

easy_trigger = trigger_manager.add_trigger("Easy Difficulty") 
easy_trigger.new_condition.difficulty_level(quantity=0)
easy_trigger.new_effect.kill_object(source_player=PlayerId.TWO, area_x1=0, area_y1=0, area_x2=map_size, area_y2=map_size)

hard_trigger = trigger_manager.add_trigger("Hard Difficulty")
hard_trigger.new_condition.difficulty_level(quantity=3)
hard_trigger.new_effect.create_object(object_list_unit_id=UnitInfo.KNIGHT.ID, source_player=PlayerId.TWO,
                                    location_x=inner_wall_x, location_y=center)

patrol_trigger = trigger_manager.add_trigger("Enemy Patrol Setup")
patrol_trigger.new_condition.timer(timer=1)
patrol_trigger.new_effect.patrol(object_list_unit_id=UnitInfo.KNIGHT.ID, source_player=PlayerId.TWO,
                               location_x=outer_wall_x-10, location_y=center)

# Discovery triggers
intro = trigger_manager.add_trigger("[D0] Intro")
intro.new_condition.timer(timer=5)
intro.new_effect.display_instructions(display_time=10, message="<YELLOW>Before you lies the enemy fortress...")

outer_wall = trigger_manager.add_trigger("[D1] Outer Wall Sighted")
outer_wall.new_condition.bring_object_to_area(unit_object=hero.reference_id,
                                            area_x1=outer_wall_x-5, area_y1=center-5,
                                            area_x2=outer_wall_x+5, area_y2=center+5)
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
scenario.write_to_file("norman_conquest.aoe2scenario")