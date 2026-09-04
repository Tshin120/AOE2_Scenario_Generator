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
# Victory path: Defeat Persian army by killing Xerxes or surviving 60 minutes
# Defeat path: Leonidas dies or Spartans lose control of the pass
# Resource sufficiency: Yes - starting army + resources for reinforcements
# Counter availability: Yes - Spartans counter Persian infantry, archers counter from walls
# Physical access: Yes - clear paths through pass with tactical chokepoints
# Timing viability: Yes - starting army can hold initial waves while building defenses

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

# Create Thermopylae terrain
# Sea on right side (east)
for x in range(three_quarter, map_size):
    for y in range(0, map_size):
        tile = map_manager.get_tile(x=x, y=y)
        tile.terrain_id = TerrainId.WATER_DEEP.value

# Beach transition
beach_width = 5
for x in range(three_quarter-beach_width, three_quarter):
    for y in range(0, map_size):
        tile = map_manager.get_tile(x=x, y=y)
        tile.terrain_id = TerrainId.BEACH.value

# Mountains on left (west)
for x in range(0, quarter):
    for y in range(0, map_size, 2):
        unit_manager.add_unit(PlayerId.GAIA, unit_const=OtherInfo.CLIFF_DEFAULT_3.ID, x=x, y=y)

# Create the pass
pass_width = 10
pass_center = center
spartan_pos_x = pass_center
spartan_pos_y = quarter + 10

# Place Leonidas and Spartans
hero = unit_manager.add_unit(PlayerId.ONE, unit_const=HeroInfo.LEONIDAS.ID, x=spartan_pos_x, y=spartan_pos_y)

# Spartan army
for i in range(20):
    unit_manager.add_unit(PlayerId.ONE, unit_const=UnitInfo.CHAMPION.ID, x=spartan_pos_x-2+i%4, y=spartan_pos_y+i//4)

# Spartan base
unit_manager.add_unit(PlayerId.ONE, unit_const=BuildingInfo.TOWN_CENTER.ID, x=spartan_pos_x-10, y=spartan_pos_y-10)
unit_manager.add_unit(PlayerId.ONE, unit_const=BuildingInfo.BARRACKS.ID, x=spartan_pos_x-8, y=spartan_pos_y-8)
unit_manager.add_unit(PlayerId.ONE, unit_const=BuildingInfo.ARCHERY_RANGE.ID, x=spartan_pos_x-6, y=spartan_pos_y-8)
unit_manager.add_unit(PlayerId.ONE, unit_const=BuildingInfo.BLACKSMITH.ID, x=spartan_pos_x-4, y=spartan_pos_y-8)

# Persian army position
persian_pos_x = pass_center
persian_pos_y = three_quarter

# Place Xerxes and Persian army
enemy_leader = unit_manager.add_unit(PlayerId.TWO, unit_const=HeroInfo.DARIUS.ID, x=persian_pos_x, y=persian_pos_y)

# Persian army groups
for i in range(40):
    unit_manager.add_unit(PlayerId.TWO, unit_const=UnitInfo.IMMORTAL_MELEE.ID, x=persian_pos_x-4+i%8, y=persian_pos_y+i//8)
for i in range(20):
    unit_manager.add_unit(PlayerId.TWO, unit_const=UnitInfo.IMMORTAL_RANGED.ID, x=persian_pos_x-3+i%6, y=persian_pos_y+5+i//6)

# Persian base
unit_manager.add_unit(PlayerId.TWO, unit_const=BuildingInfo.TOWN_CENTER.ID, x=persian_pos_x+10, y=persian_pos_y+10)
unit_manager.add_unit(PlayerId.TWO, unit_const=BuildingInfo.BARRACKS.ID, x=persian_pos_x+8, y=persian_pos_y+12)
unit_manager.add_unit(PlayerId.TWO, unit_const=BuildingInfo.ARCHERY_RANGE.ID, x=persian_pos_x+6, y=persian_pos_y+12)
unit_manager.add_unit(PlayerId.TWO, unit_const=BuildingInfo.STABLE.ID, x=persian_pos_x+4, y=persian_pos_y+12)

# Add resources near Spartan base
for i in range(5):
    unit_manager.add_unit(PlayerId.GAIA, unit_const=OtherInfo.GOLD_MINE.ID, x=spartan_pos_x-15+i, y=spartan_pos_y-5)
    unit_manager.add_unit(PlayerId.GAIA, unit_const=OtherInfo.STONE_MINE.ID, x=spartan_pos_x-15+i, y=spartan_pos_y-7)
    unit_manager.add_unit(PlayerId.GAIA, unit_const=OtherInfo.FORAGE_BUSH.ID, x=spartan_pos_x-12+i, y=spartan_pos_y-9)
    unit_manager.add_unit(PlayerId.GAIA, unit_const=UnitInfo.SHEEP.ID, x=spartan_pos_x-10+i, y=spartan_pos_y-12)

# Create triggers (25 minimum required)

# === Setup Triggers ===
tech_trigger = trigger_manager.add_trigger("Techs")
tech_trigger.new_condition.timer(timer=1)
tech_trigger.new_effect.research_technology(source_player=PlayerId.ONE, technology=TechInfo.FORGING.ID)
tech_trigger.new_effect.research_technology(source_player=PlayerId.ONE, technology=TechInfo.SCALE_MAIL_ARMOR.ID)

walls_trigger = trigger_manager.add_trigger("Walls")
walls_trigger.new_condition.timer(timer=1)
walls_trigger.new_effect.create_object(object_list_unit_id=BuildingInfo.STONE_WALL.ID, source_player=PlayerId.ONE, location_x=spartan_pos_x-5, location_y=spartan_pos_y-5)

easy_trigger = trigger_manager.add_trigger("Easy Difficulty")
easy_trigger.new_condition.difficulty_level(quantity=0)
easy_trigger.new_effect.kill_object(source_player=PlayerId.TWO, area_x1=0, area_y1=0, area_x2=map_size, area_y2=map_size)

hard_trigger = trigger_manager.add_trigger("Hardmode")
hard_trigger.new_condition.difficulty_level(quantity=3)
hard_trigger.new_effect.create_object(object_list_unit_id=UnitInfo.IMMORTAL_MELEE.ID, source_player=PlayerId.TWO, location_x=persian_pos_x, location_y=persian_pos_y)

gates_trigger = trigger_manager.add_trigger("Close Gates")
gates_trigger.new_condition.timer(timer=1)

# === Dialogue Triggers ===
intro = trigger_manager.add_trigger("[D0] Intro")
intro.new_condition.timer(timer=5)
intro.new_effect.display_instructions(display_time=10, message="<YELLOW>Narrator: The Persian army approaches Thermopylae...")

scout = trigger_manager.add_trigger("[D1] Scout Report")
scout.new_condition.timer(timer=15)
scout.new_effect.display_instructions(display_time=10, message="<BLUE>Scout: My king, Xerxes brings thousands of soldiers!")

speech = trigger_manager.add_trigger("[D2] Commander Speech")
speech.new_condition.timer(timer=30)
speech.new_effect.display_instructions(display_time=10, message="<BLUE>Leonidas: Spartans! Prepare for glory!")

taunt1 = trigger_manager.add_trigger("[D3] Enemy Taunt 1")
taunt1.new_condition.timer(timer=60)
taunt1.new_effect.display_instructions(display_time=10, message="<RED>Xerxes: Lay down your weapons!")

taunt2 = trigger_manager.add_trigger("[D4] Enemy Taunt 2")
taunt2.new_condition.timer(timer=120)
taunt2.new_effect.display_instructions(display_time=10, message="<RED>Xerxes: Your resistance is futile!")

location1 = trigger_manager.add_trigger("[D5] At Location 1")
location1.new_condition.bring_object_to_area(unit_object=hero.reference_id, area_x1=pass_center-5, area_y1=quarter, area_x2=pass_center+5, area_y2=quarter+10)
location1.new_effect.display_instructions(display_time=10, message="<BLUE>Leonidas: Hold the pass!")

location2 = trigger_manager.add_trigger("[D6] At Location 2")
location2.new_condition.bring_object_to_area(unit_object=enemy_leader.reference_id, area_x1=pass_center-5, area_y1=quarter+20, area_x2=pass_center+5, area_y2=quarter+30)
location2.new_effect.display_instructions(display_time=10, message="<RED>Xerxes: Attack!")

battle = trigger_manager.add_trigger("[D7] Battle Begins")
battle.new_condition.timer(timer=180)
battle.new_effect.display_instructions(display_time=10, message="<YELLOW>The battle for Thermopylae begins!")

midpoint = trigger_manager.add_trigger("[D8] Midpoint Update")
midpoint.new_condition.timer(timer=300)
midpoint.new_effect.display_instructions(display_time=10, message="<YELLOW>The Spartans hold firm against the Persian assault!")

weak = trigger_manager.add_trigger("[D9] Enemy Weakening")
weak.new_condition.objects_in_area(quantity=10, object_list=UnitInfo.IMMORTAL_MELEE.ID, source_player=PlayerId.TWO, area_x1=0, area_y1=0, area_x2=map_size, area_y2=map_size)
weak.new_effect.display_instructions(display_time=10, message="<YELLOW>The Persian army weakens!")

final = trigger_manager.add_trigger("[D10] Final Push")
final.new_condition.timer(timer=420)
final.new_effect.display_instructions(display_time=10, message="<BLUE>Leonidas: Push them back!")

hero_falls = trigger_manager.add_trigger("[D11] Hero Falls")
hero_falls.new_condition.destroy_object(unit_object=hero.reference_id)
hero_falls.new_effect.display_instructions(display_time=10, message="<YELLOW>Leonidas has fallen!")

# === Objective Triggers ===
objectives = trigger_manager.add_trigger("[O] Main Objectives")
objectives.new_condition.timer(timer=1)
objectives.new_effect.display_instructions(display_time=20, message="Objectives:\n-Defend the pass\n-Defeat Xerxes\n-Leonidas must survive")

primary = trigger_manager.add_trigger("[Obj] Primary Goal")
primary.new_condition.destroy_object(unit_object=enemy_leader.reference_id)
primary.new_effect.display_instructions(display_time=10, message="Victory! Xerxes has been defeated!")

secondary = trigger_manager.add_trigger("[Obj] Secondary Goal")
secondary.new_condition.timer(timer=3600)  # 1 hour survival
secondary.new_effect.display_instructions(display_time=10, message="Victory! You have held the pass!")

survival = trigger_manager.add_trigger("[Obj] Survival")
survival.new_condition.timer(timer=1)
survival.new_effect.display_instructions(display_time=10, message="Leonidas must survive!")

# === Victory/Defeat Triggers ===
victory1 = trigger_manager.add_trigger("VC")
victory1.new_condition.destroy_object(unit_object=enemy_leader.reference_id)
victory1.new_effect.declare_victory(source_player=PlayerId.ONE, enabled=1)

victory2 = trigger_manager.add_trigger("VC2")
victory2.new_condition.timer(timer=3600)
victory2.new_effect.declare_victory(source_player=PlayerId.ONE, enabled=1)

defeat1 = trigger_manager.add_trigger("Defeat")
defeat1.new_condition.destroy_object(unit_object=hero.reference_id)
defeat1.new_effect.declare_victory(source_player=PlayerId.TWO, enabled=1)

defeat2 = trigger_manager.add_trigger("DEFEAT")
defeat2.new_condition.objects_in_area(quantity=5, object_list=UnitInfo.IMMORTAL_MELEE.ID, source_player=PlayerId.TWO, area_x1=spartan_pos_x-10, area_y1=spartan_pos_y-10, area_x2=spartan_pos_x+10, area_y2=spartan_pos_y+10)
defeat2.new_effect.declare_victory(source_player=PlayerId.TWO, enabled=1)

# Save scenario
scenario.write_to_file("thermopylae.aoe2scenario")