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

# Create the pass of Thermopylae
# Sea on right side (east)
for x in range(three_quarter, map_size):
    for y in range(0, map_size):
        tile = map_manager.get_tile(x=x, y=y)
        tile.terrain_id = TerrainId.WATER_DEEP.value

# Beach transition
beach_width = 3
for x in range(three_quarter-beach_width, three_quarter):
    for y in range(0, map_size):
        tile = map_manager.get_tile(x=x, y=y)
        tile.terrain_id = TerrainId.BEACH.value

# Mountains on left (west)
for x in range(0, quarter):
    for y in range(0, map_size, 2):
        unit_manager.add_unit(PlayerId.GAIA, unit_const=OtherInfo.CLIFF_DEFAULT_3.ID, x=x, y=y)

# Narrow pass in middle
pass_width = 10
pass_center_x = center
pass_center_y = center

# Place Spartan forces (Player ONE)
# Store hero reference for triggers
leonidas = unit_manager.add_unit(PlayerId.ONE, unit_const=HeroInfo.LEONIDAS.ID, x=pass_center_x, y=pass_center_y)

# Spartan warriors in phalanx formation
for i in range(10):
    unit_manager.add_unit(PlayerId.ONE, unit_const=UnitInfo.CHAMPION.ID, x=pass_center_x-1+i, y=pass_center_y)
    unit_manager.add_unit(PlayerId.ONE, unit_const=UnitInfo.PIKEMAN.ID, x=pass_center_x-1+i, y=pass_center_y+1)

# Spartan base
spartan_base_x = pass_center_x - 15
spartan_base_y = pass_center_y + 15

# Spartan buildings
unit_manager.add_unit(PlayerId.ONE, unit_const=BuildingInfo.TOWN_CENTER.ID, x=spartan_base_x, y=spartan_base_y)
unit_manager.add_unit(PlayerId.ONE, unit_const=BuildingInfo.BARRACKS.ID, x=spartan_base_x+4, y=spartan_base_y)
unit_manager.add_unit(PlayerId.ONE, unit_const=BuildingInfo.BLACKSMITH.ID, x=spartan_base_x+8, y=spartan_base_y)

# Persian forces (Player TWO)
# Store enemy leader for triggers
xerxes = unit_manager.add_unit(PlayerId.TWO, unit_const=HeroInfo.DARIUS.ID, x=pass_center_x+30, y=pass_center_y)

# Persian army
for i in range(20):
    unit_manager.add_unit(PlayerId.TWO, unit_const=UnitInfo.IMMORTAL_MELEE.ID, x=pass_center_x+25+i%5, y=pass_center_y+i//5)
    unit_manager.add_unit(PlayerId.TWO, unit_const=UnitInfo.IMMORTAL_RANGED.ID, x=pass_center_x+25+i%5, y=pass_center_y+5+i//5)

# Persian base
persian_base_x = pass_center_x + 40
persian_base_y = pass_center_y

# Persian buildings with walls
unit_manager.add_unit(PlayerId.TWO, unit_const=BuildingInfo.CASTLE.ID, x=persian_base_x, y=persian_base_y)
unit_manager.add_unit(PlayerId.TWO, unit_const=BuildingInfo.BARRACKS.ID, x=persian_base_x+5, y=persian_base_y)
unit_manager.add_unit(PlayerId.TWO, unit_const=BuildingInfo.ARCHERY_RANGE.ID, x=persian_base_x+10, y=persian_base_y)

# Walls around Persian base
for i in range(15):
    unit_manager.add_unit(PlayerId.TWO, unit_const=BuildingInfo.STONE_WALL.ID, x=persian_base_x-5+i, y=persian_base_y-5)
    unit_manager.add_unit(PlayerId.TWO, unit_const=BuildingInfo.STONE_WALL.ID, x=persian_base_x-5+i, y=persian_base_y+10)

# Persian-owned gate
persian_gate = unit_manager.add_unit(PlayerId.TWO, unit_const=BuildingInfo.GATE_NORTH_TO_SOUTH.ID, x=persian_base_x, y=persian_base_y-5)

# GAIA resources near Spartan base
# Gold
for i in range(5):
    unit_manager.add_unit(PlayerId.GAIA, unit_const=OtherInfo.GOLD_MINE.ID, x=spartan_base_x-5+i, y=spartan_base_y-10)

# Stone
for i in range(4):
    unit_manager.add_unit(PlayerId.GAIA, unit_const=OtherInfo.STONE_MINE.ID, x=spartan_base_x-5+i, y=spartan_base_y-15)

# Food
for i in range(8):
    unit_manager.add_unit(PlayerId.GAIA, unit_const=OtherInfo.FORAGE_BUSH.ID, x=spartan_base_x+i, y=spartan_base_y-5)
    unit_manager.add_unit(PlayerId.GAIA, unit_const=UnitInfo.SHEEP.ID, x=spartan_base_x-10+i, y=spartan_base_y)

# === TRIGGERS ===

# --- Setup Section (5 triggers) ---
tech_trigger = trigger_manager.add_trigger("Techs")
tech_trigger.new_condition.timer(timer=1)
tech_trigger.new_effect.research_technology(source_player=PlayerId.ONE, technology=TechInfo.FORGING.ID)
tech_trigger.new_effect.research_technology(source_player=PlayerId.ONE, technology=TechInfo.SCALE_MAIL_ARMOR.ID)

walls_trigger = trigger_manager.add_trigger("Walls")
walls_trigger.new_condition.timer(timer=1)

easy_trigger = trigger_manager.add_trigger("Easy Difficulty")
easy_trigger.new_condition.difficulty_level(quantity=0)
easy_trigger.new_effect.kill_object(source_player=PlayerId.TWO, area_x1=0, area_y1=0, area_x2=map_size, area_y2=map_size)

hard_trigger = trigger_manager.add_trigger("Hardmode")
hard_trigger.new_condition.difficulty_level(quantity=3)
hard_trigger.new_effect.create_object(object_list_unit_id=UnitInfo.IMMORTAL_MELEE.ID, source_player=PlayerId.TWO, location_x=persian_base_x, location_y=persian_base_y)

gates_trigger = trigger_manager.add_trigger("Close Gates")
gates_trigger.new_condition.timer(timer=1)

# --- Dialogue Section (12 triggers) ---
intro = trigger_manager.add_trigger("[D0] Intro")
intro.new_condition.timer(timer=5)
intro.new_effect.display_instructions(display_time=10, message="<YELLOW>Narrator: The mighty Persian army approaches the pass of Thermopylae...")

scout = trigger_manager.add_trigger("[D1] Scout Report")
scout.new_condition.timer(timer=15)
scout.new_effect.display_instructions(display_time=10, message="<BLUE>Scout: My king, the Persians number in the thousands!")

speech = trigger_manager.add_trigger("[D2] Commander Speech")
speech.new_condition.timer(timer=30)
speech.new_effect.display_instructions(display_time=10, message="<BLUE>Leonidas: Spartans! Tonight we dine in hell!")

taunt1 = trigger_manager.add_trigger("[D3] Enemy Taunt 1")
taunt1.new_condition.timer(timer=60)
taunt1.new_effect.display_instructions(display_time=10, message="<RED>Xerxes: Your spears will shatter upon the endless waves of my army!")

taunt2 = trigger_manager.add_trigger("[D4] Enemy Taunt 2")
taunt2.new_condition.timer(timer=120)
taunt2.new_effect.display_instructions(display_time=10, message="<RED>Xerxes: Lay down your weapons and you may yet live as slaves!")

location1 = trigger_manager.add_trigger("[D5] At Location 1")
location1.new_condition.bring_object_to_area(unit_object=leonidas.reference_id, area_x1=pass_center_x-5, area_y1=pass_center_y-5, area_x2=pass_center_x+5, area_y2=pass_center_y+5)

location2 = trigger_manager.add_trigger("[D6] At Location 2")
location2.new_condition.bring_object_to_area(unit_object=leonidas.reference_id, area_x1=pass_center_x+10, area_y1=pass_center_y-5, area_x2=pass_center_x+20, area_y2=pass_center_y+5)

battle = trigger_manager.add_trigger("[D7] Battle Begins")
battle.new_condition.timer(timer=180)
battle.new_effect.display_instructions(display_time=10, message="<YELLOW>Narrator: The Persian host crashes against the Spartan shield wall!")

midpoint = trigger_manager.add_trigger("[D8] Midpoint Update")
midpoint.new_condition.timer(timer=300)
midpoint.new_effect.display_instructions(display_time=10, message="<YELLOW>Narrator: The narrow pass negates the Persian numbers!")

enemy_weak = trigger_manager.add_trigger("[D9] Enemy Weakening")
enemy_weak.new_condition.objects_in_area(quantity=10, object_list=UnitInfo.IMMORTAL_MELEE.ID, source_player=PlayerId.TWO, area_x1=0, area_y1=0, area_x2=map_size, area_y2=map_size)

final_push = trigger_manager.add_trigger("[D10] Final Push")
final_push.new_condition.timer(timer=420)
final_push.new_effect.display_instructions(display_time=10, message="<BLUE>Leonidas: Push them back! For Sparta!")

hero_falls = trigger_manager.add_trigger("[D11] Hero Falls")
hero_falls.new_condition.destroy_object(unit_object=leonidas.reference_id)
hero_falls.new_effect.display_instructions(display_time=10, message="<YELLOW>Narrator: Leonidas has fallen!")

# --- Objective Section (4 triggers) ---
objectives = trigger_manager.add_trigger("[O] Main Objectives")
objectives.new_condition.timer(timer=1)
objectives.new_effect.display_instructions(display_time=20, message="Objectives:\n-Defend the pass\n-Leonidas must survive\n-Defeat Xerxes")

primary = trigger_manager.add_trigger("[Obj] Primary Goal")
primary.new_condition.destroy_object(unit_object=xerxes.reference_id)

secondary = trigger_manager.add_trigger("[Obj] Secondary Goal")
secondary.new_condition.objects_in_area(quantity=30, object_list=UnitInfo.IMMORTAL_MELEE.ID, source_player=PlayerId.TWO, area_x1=0, area_y1=0, area_x2=map_size, area_y2=map_size)

survival = trigger_manager.add_trigger("[Obj] Survival")
survival.new_condition.timer(timer=1)
survival.new_effect.display_instructions(display_time=10, message="Leonidas must survive!")

# --- Victory/Defeat Section (4 triggers) ---
victory = trigger_manager.add_trigger("VC")
victory.new_condition.destroy_object(unit_object=xerxes.reference_id)
victory.new_effect.declare_victory(source_player=PlayerId.ONE, enabled=1)

victory2 = trigger_manager.add_trigger("VC2")
victory2.new_condition.timer(timer=900)
victory2.new_effect.declare_victory(source_player=PlayerId.ONE, enabled=1)

defeat = trigger_manager.add_trigger("Defeat")
defeat.new_condition.destroy_object(unit_object=leonidas.reference_id)
defeat.new_effect.declare_victory(source_player=PlayerId.TWO, enabled=1)

defeat2 = trigger_manager.add_trigger("DEFEAT")
defeat2.new_condition.destroy_object(unit_object=persian_gate.reference_id)
defeat2.new_effect.declare_victory(source_player=PlayerId.TWO, enabled=1)

# Save scenario
scenario.write_to_file("thermopylae.aoe2scenario")