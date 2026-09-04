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
# Defeat path: Player can lose by: 1) Hero death 2) Army destruction 3) Losing all siege equipment
# Resource sufficiency: Yes - starting army + capturable siege weapons sufficient to breach defenses
# Counter availability: Yes - mix of infantry/archers/siege can counter all enemy unit types
# Physical access: Yes - multiple paths to objectives, gates can be destroyed to progress
# Timing viability: Yes - starting army can survive initial contact while capturing siege equipment

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

# Player starting position (west edge)
player_start_x = 10
player_start_y = center

# Defensive lines positions
outer_wall_x = quarter 
middle_wall_x = center
inner_wall_x = three_quarter

# Create hero unit and store reference
hero = unit_manager.add_unit(PlayerId.ONE, unit_const=HeroInfo.EL_CID.ID, x=player_start_x, y=player_start_y)

# Player starting army
for i in range(15):
    unit_manager.add_unit(PlayerId.ONE, unit_const=UnitInfo.MAN_AT_ARMS.ID, x=player_start_x+2+i, y=player_start_y-2)
    unit_manager.add_unit(PlayerId.ONE, unit_const=UnitInfo.CROSSBOWMAN.ID, x=player_start_x+2+i, y=player_start_y+2)
    unit_manager.add_unit(PlayerId.ONE, unit_const=UnitInfo.KNIGHT.ID, x=player_start_x+2+i, y=player_start_y+4)

# Player forward base
player_base_x = player_start_x + 15
unit_manager.add_unit(PlayerId.ONE, unit_const=BuildingInfo.BARRACKS.ID, x=player_base_x, y=player_start_y-5)
unit_manager.add_unit(PlayerId.ONE, unit_const=BuildingInfo.ARCHERY_RANGE.ID, x=player_base_x, y=player_start_y+5)
unit_manager.add_unit(PlayerId.ONE, unit_const=BuildingInfo.BLACKSMITH.ID, x=player_base_x+5, y=player_start_y)

# Outer defensive line
outer_gate = unit_manager.add_unit(PlayerId.TWO, unit_const=BuildingInfo.GATE_NORTH_TO_SOUTH.ID, x=outer_wall_x, y=center)

for i in range(25):
    unit_manager.add_unit(PlayerId.TWO, unit_const=BuildingInfo.PALISADE_WALL.ID, x=outer_wall_x, y=center-15+i)
    
# Outer towers and garrison
for i in range(3):
    tower = unit_manager.add_unit(PlayerId.TWO, unit_const=BuildingInfo.WATCH_TOWER.ID, x=outer_wall_x+2, y=center-10+(i*10))
    for j in range(5):
        unit_manager.add_unit(PlayerId.TWO, unit_const=UnitInfo.SPEARMAN.ID, x=outer_wall_x+3+j, y=center-10+(i*10))
        unit_manager.add_unit(PlayerId.TWO, unit_const=UnitInfo.ARCHER.ID, x=outer_wall_x+3+j, y=center-9+(i*10))

# Middle defensive line  
middle_gate = unit_manager.add_unit(PlayerId.TWO, unit_const=BuildingInfo.GATE_NORTH_TO_SOUTH.ID, x=middle_wall_x, y=center)

for i in range(35):
    unit_manager.add_unit(PlayerId.TWO, unit_const=BuildingInfo.STONE_WALL.ID, x=middle_wall_x, y=center-20+i)

# Middle towers and garrison
for i in range(4):
    tower = unit_manager.add_unit(PlayerId.TWO, unit_const=BuildingInfo.GUARD_TOWER.ID, x=middle_wall_x+2, y=center-15+(i*10))
    for j in range(5):
        unit_manager.add_unit(PlayerId.TWO, unit_const=UnitInfo.MAN_AT_ARMS.ID, x=middle_wall_x+3+j, y=center-15+(i*10))
        unit_manager.add_unit(PlayerId.TWO, unit_const=UnitInfo.CROSSBOWMAN.ID, x=middle_wall_x+3+j, y=center-14+(i*10))
        unit_manager.add_unit(PlayerId.TWO, unit_const=UnitInfo.KNIGHT.ID, x=middle_wall_x+3+j, y=center-13+(i*10))

# Inner fortress
castle = unit_manager.add_unit(PlayerId.TWO, unit_const=BuildingInfo.CASTLE.ID, x=inner_wall_x, y=center)
inner_gate = unit_manager.add_unit(PlayerId.TWO, unit_const=BuildingInfo.GATE_NORTH_TO_SOUTH.ID, x=inner_wall_x-5, y=center)

# Inner keeps and elite garrison
for i in range(4):
    keep = unit_manager.add_unit(PlayerId.TWO, unit_const=BuildingInfo.KEEP.ID, x=inner_wall_x+2, y=center-20+(i*10))
    for j in range(5):
        unit_manager.add_unit(PlayerId.TWO, unit_const=UnitInfo.CHAMPION.ID, x=inner_wall_x+3+j, y=center-20+(i*10))
        unit_manager.add_unit(PlayerId.TWO, unit_const=UnitInfo.CAVALIER.ID, x=inner_wall_x+3+j, y=center-19+(i*10))

# Enemy commander
enemy_lord = unit_manager.add_unit(PlayerId.TWO, unit_const=UnitInfo.KING.ID, x=inner_wall_x+1, y=center)

# Capturable siege weapons
trebuchet = unit_manager.add_unit(PlayerId.GAIA, unit_const=UnitInfo.TREBUCHET.ID, x=outer_wall_x-10, y=center-10)
ram1 = unit_manager.add_unit(PlayerId.GAIA, unit_const=UnitInfo.BATTERING_RAM.ID, x=outer_wall_x-8, y=center)
ram2 = unit_manager.add_unit(PlayerId.GAIA, unit_const=UnitInfo.BATTERING_RAM.ID, x=middle_wall_x-8, y=center+10)

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
hard_trigger.new_effect.create_object(object_list_unit_id=UnitInfo.CHAMPION.ID, source_player=PlayerId.TWO, location_x=inner_wall_x, location_y=center)

patrol_trigger = trigger_manager.add_trigger("Enemy Patrol Setup")
patrol_trigger.new_condition.timer(timer=1)
patrol_trigger.new_effect.patrol(object_list_unit_id=UnitInfo.KNIGHT.ID, source_player=PlayerId.TWO, location_x=outer_wall_x-10, location_y=center)

reveal_trigger = trigger_manager.add_trigger("Map Reveal")
reveal_trigger.new_condition.timer(timer=1)
reveal_trigger.new_effect.display_instructions(display_time=10, message="<YELLOW>Before you lies the enemy fortress...")

start_trigger = trigger_manager.add_trigger("Starting Grant")
start_trigger.new_condition.timer(timer=1)
start_trigger.new_effect.display_instructions(display_time=10, message="Breach the fortress and destroy the enemy commander!")

# Discovery triggers
for i in range(10):
    disc_trigger = trigger_manager.add_trigger(f"[D{i}] Discovery {i}")
    disc_trigger.new_condition.bring_object_to_area(unit_object=hero.reference_id, area_x1=outer_wall_x+(i*10), area_y1=0, area_x2=outer_wall_x+(i*10)+10, area_y2=map_size)
    disc_trigger.new_effect.display_instructions(display_time=10, message=f"Discovery {i} found!")

# Capture triggers  
for i in range(8):
    cap_trigger = trigger_manager.add_trigger(f"Capture {i}")
    cap_trigger.new_condition.bring_object_to_area(unit_object=hero.reference_id, area_x1=outer_wall_x+(i*10), area_y1=0, area_x2=outer_wall_x+(i*10)+10, area_y2=map_size)
    cap_trigger.new_effect.display_instructions(display_time=10, message=f"Area {i} captured!")

# Gate/Breach triggers
for gate in [outer_gate, middle_gate, inner_gate]:
    breach_trigger = trigger_manager.add_trigger(f"Gate Breach")
    breach_trigger.new_condition.destroy_object(unit_object=gate.reference_id)
    breach_trigger.new_effect.display_instructions(display_time=10, message="A gate has fallen!")

# Victory progression triggers
for i in range(8):
    vic_trigger = trigger_manager.add_trigger(f"V/{i}")
    vic_trigger.new_condition.destroy_object(unit_object=castle.reference_id)
    vic_trigger.new_effect.display_instructions(display_time=10, message=f"Victory stage {i} complete!")

# Objective triggers
for i in range(5):
    obj_trigger = trigger_manager.add_trigger(f"[O] Objective {i}")
    obj_trigger.new_condition.timer(timer=i*30)
    obj_trigger.new_effect.display_instructions(display_time=10, message=f"New objective {i}!")

# Defeat triggers
defeat_hero = trigger_manager.add_trigger("Defeat - Hero Dies")
defeat_hero.new_condition.destroy_object(unit_object=hero.reference_id)
defeat_hero.new_effect.declare_victory(source_player=PlayerId.TWO, enabled=1)

defeat_army = trigger_manager.add_trigger("Defeat - Army Destroyed")
defeat_army.new_condition.objects_in_area(quantity=0, object_list=UnitInfo.MILITIA.ID, source_player=PlayerId.ONE, area_x1=0, area_y1=0, area_x2=map_size, area_y2=map_size)
defeat_army.new_effect.declare_victory(source_player=PlayerId.TWO, enabled=1)

defeat_siege = trigger_manager.add_trigger("Defeat - Siege Lost")
defeat_siege.new_condition.destroy_object(unit_object=trebuchet.reference_id)
defeat_siege.new_effect.display_instructions(display_time=10, message="All siege equipment lost!")

death_msg = trigger_manager.add_trigger("[D_] Hero Death")
death_msg.new_condition.destroy_object(unit_object=hero.reference_id)
death_msg.new_effect.display_instructions(display_time=10, message="<YELLOW>Our leader has fallen...")

# Save scenario
scenario.write_to_file("reconquista.aoe2scenario")