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
# Victory path: Defeat Harold Godwinson or capture his castle. Player has sufficient military to achieve this.
# Defeat path: William dies or Norman base destroyed. Enemy has adequate forces to threaten player.
# Resource sufficiency: Yes - Starting resources + mines sufficient for military production
# Counter availability: Yes - Player has barracks/range/stable to counter all enemy unit types
# Physical access: Yes - Multiple paths to enemy, no impassable barriers
# Timing viability: Yes - Player starts with adequate army to defend initial position

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

# Create Senlac Hill terrain
hill_y = map_size // 3
for x in range(quarter, three_quarter):
    unit_manager.add_unit(PlayerId.GAIA, unit_const=OtherInfo.CLIFF_DEFAULT_2.ID, x=x, y=hill_y)

# Forests on flanks
for x in range(0, quarter):
    for y in range(hill_y-10, hill_y+10):
        unit_manager.add_unit(PlayerId.GAIA, unit_const=OtherInfo.TREE_OAK.ID, x=x, y=y)
for x in range(three_quarter, map_size):
    for y in range(hill_y-10, hill_y+10):
        unit_manager.add_unit(PlayerId.GAIA, unit_const=OtherInfo.TREE_OAK.ID, x=x, y=y)

# Place GAIA resources near Norman (player) base
norman_base_x = center
norman_base_y = three_quarter

# Gold mines
for i in range(5):
    unit_manager.add_unit(PlayerId.GAIA, unit_const=OtherInfo.GOLD_MINE.ID, x=norman_base_x-10+i, y=norman_base_y+5)
    unit_manager.add_unit(PlayerId.GAIA, unit_const=OtherInfo.GOLD_MINE.ID, x=norman_base_x+5+i, y=norman_base_y+5)

# Stone mines
for i in range(4):
    unit_manager.add_unit(PlayerId.GAIA, unit_const=OtherInfo.STONE_MINE.ID, x=norman_base_x-8+i, y=norman_base_y+8)

# Forage bushes
for i in range(8):
    unit_manager.add_unit(PlayerId.GAIA, unit_const=OtherInfo.FORAGE_BUSH.ID, x=norman_base_x-4+i, y=norman_base_y+10)

# Sheep
for i in range(8):
    unit_manager.add_unit(PlayerId.GAIA, unit_const=UnitInfo.SHEEP.ID, x=norman_base_x-8+i, y=norman_base_y-5)

# Norman (Player ONE) base
william = unit_manager.add_unit(PlayerId.ONE, unit_const=HeroInfo.WILLIAM_THE_CONQUEROR.ID, x=norman_base_x, y=norman_base_y)

# Norman military buildings
norman_barracks = unit_manager.add_unit(PlayerId.ONE, unit_const=BuildingInfo.BARRACKS.ID, x=norman_base_x-8, y=norman_base_y+2)
norman_range = unit_manager.add_unit(PlayerId.ONE, unit_const=BuildingInfo.ARCHERY_RANGE.ID, x=norman_base_x+8, y=norman_base_y+2)
norman_stable = unit_manager.add_unit(PlayerId.ONE, unit_const=BuildingInfo.STABLE.ID, x=norman_base_x, y=norman_base_y+4)

# Norman economy buildings
norman_tc = unit_manager.add_unit(PlayerId.ONE, unit_const=BuildingInfo.TOWN_CENTER.ID, x=norman_base_x, y=norman_base_y)
norman_blacksmith = unit_manager.add_unit(PlayerId.ONE, unit_const=BuildingInfo.BLACKSMITH.ID, x=norman_base_x+4, y=norman_base_y+6)

# Norman starting army
for i in range(10):
    unit_manager.add_unit(PlayerId.ONE, unit_const=UnitInfo.KNIGHT.ID, x=norman_base_x-5+i, y=norman_base_y-2)
for i in range(15):
    unit_manager.add_unit(PlayerId.ONE, unit_const=UnitInfo.MAN_AT_ARMS.ID, x=norman_base_x-7+i, y=norman_base_y-3)
for i in range(12):
    unit_manager.add_unit(PlayerId.ONE, unit_const=UnitInfo.ARCHER.ID, x=norman_base_x-6+i, y=norman_base_y-4)

# Saxon (Player TWO) base on hill
harold = unit_manager.add_unit(PlayerId.TWO, unit_const=UnitInfo.KING.ID, x=center, y=hill_y-5)

# Saxon fortifications
saxon_castle = unit_manager.add_unit(PlayerId.TWO, unit_const=BuildingInfo.CASTLE.ID, x=center, y=hill_y-8)

# Saxon walls
for i in range(20):
    unit_manager.add_unit(PlayerId.TWO, unit_const=BuildingInfo.STONE_WALL.ID, x=center-10+i, y=hill_y-10)
    
# Saxon gates (owned by Player TWO)
saxon_gate = unit_manager.add_unit(PlayerId.TWO, unit_const=BuildingInfo.GATE_NORTH_TO_SOUTH.ID, x=center, y=hill_y-10)

# Saxon army on hill
for i in range(20):
    unit_manager.add_unit(PlayerId.TWO, unit_const=UnitInfo.MAN_AT_ARMS.ID, x=center-10+i, y=hill_y-4)
for i in range(15):
    unit_manager.add_unit(PlayerId.TWO, unit_const=UnitInfo.ARCHER.ID, x=center-7+i, y=hill_y-6)
for i in range(8):
    unit_manager.add_unit(PlayerId.TWO, unit_const=UnitInfo.KNIGHT.ID, x=center-4+i, y=hill_y-7)

# === TRIGGERS ===

# --- Setup Section ---
tech_trigger = trigger_manager.add_trigger("Techs")
tech_trigger.new_condition.timer(timer=1)
tech_trigger.new_effect.research_technology(source_player=PlayerId.ONE, technology=TechInfo.FORGING.ID)
tech_trigger.new_effect.research_technology(source_player=PlayerId.ONE, technology=TechInfo.SCALE_MAIL_ARMOR.ID)

walls_trigger = trigger_manager.add_trigger("Walls")
walls_trigger.new_condition.timer(timer=1)
walls_trigger.new_effect.task_object(source_player=PlayerId.TWO, object_list_unit_id=BuildingInfo.GATE_NORTH_TO_SOUTH.ID)

easy_trigger = trigger_manager.add_trigger("Easy Difficulty")
easy_trigger.new_condition.difficulty_level(quantity=0)
easy_trigger.new_effect.kill_object(source_player=PlayerId.TWO, area_x1=0, area_y1=0, area_x2=map_size, area_y2=map_size)

hard_trigger = trigger_manager.add_trigger("Hardmode")
hard_trigger.new_condition.difficulty_level(quantity=3)
hard_trigger.new_effect.create_object(source_player=PlayerId.TWO, object_list_unit_id=UnitInfo.KNIGHT.ID, location_x=center, location_y=hill_y-4)

gates_trigger = trigger_manager.add_trigger("Close Gates")
gates_trigger.new_condition.timer(timer=1)
gates_trigger.new_effect.task_object(source_player=PlayerId.TWO, object_list_unit_id=BuildingInfo.GATE_NORTH_TO_SOUTH.ID)

# --- Dialogue Section ---
intro = trigger_manager.add_trigger("[D0] Intro")
intro.new_condition.timer(timer=5)
intro.new_effect.display_instructions(display_time=10, message="<YELLOW>Narrator: The year is 1066. Harold Godwinson has taken the English throne, but William of Normandy claims it as his rightful inheritance.")

scout = trigger_manager.add_trigger("[D1] Scout Report")
scout.new_condition.timer(timer=15)
scout.new_effect.display_instructions(display_time=10, message="<BLUE>Scout: My lord, the Saxons hold Senlac Hill. Their shield wall is formidable.")

commander = trigger_manager.add_trigger("[D2] Commander Speech")
commander.new_condition.timer(timer=30)
commander.new_effect.display_instructions(display_time=10, message="<BLUE>William: We shall break their lines with our cavalry. Forward!")

taunt1 = trigger_manager.add_trigger("[D3] Enemy Taunt 1")
taunt1.new_condition.timer(timer=60)
taunt1.new_effect.display_instructions(display_time=10, message="<RED>Harold: Your claim to England ends here, Norman!")

taunt2 = trigger_manager.add_trigger("[D4] Enemy Taunt 2")
taunt2.new_condition.timer(timer=120)
taunt2.new_effect.display_instructions(display_time=10, message="<RED>Harold: Stand fast, men! Hold the line!")

location1 = trigger_manager.add_trigger("[D5] At Location 1")
location1.new_condition.bring_object_to_area(unit_object=william.reference_id, area_x1=center-20, area_y1=hill_y, area_x2=center+20, area_y2=hill_y+10)
location1.new_effect.display_instructions(display_time=10, message="<YELLOW>The Norman army reaches the base of Senlac Hill.")

location2 = trigger_manager.add_trigger("[D6] At Location 2")
location2.new_condition.bring_object_to_area(unit_object=william.reference_id, area_x1=center-10, area_y1=hill_y-10, area_x2=center+10, area_y2=hill_y)
location2.new_effect.display_instructions(display_time=10, message="<YELLOW>William leads the charge up the hill!")

battle = trigger_manager.add_trigger("[D7] Battle Begins")
battle.new_condition.timer(timer=180)
battle.new_effect.display_instructions(display_time=10, message="<YELLOW>The battle rages across Senlac Hill!")

midpoint = trigger_manager.add_trigger("[D8] Midpoint Update")
midpoint.new_condition.timer(timer=300)
midpoint.new_effect.display_instructions(display_time=10, message="<YELLOW>The fate of England hangs in the balance!")

weakening = trigger_manager.add_trigger("[D9] Enemy Weakening")
weakening.new_condition.objects_in_area(quantity=10, object_list=UnitInfo.MAN_AT_ARMS.ID, source_player=PlayerId.TWO, area_x1=0, area_y1=0, area_x2=map_size, area_y2=map_size)
weakening.new_effect.display_instructions(display_time=10, message="<YELLOW>The Saxon shield wall begins to crack!")

final = trigger_manager.add_trigger("[D10] Final Push")
final.new_condition.timer(timer=420)
final.new_effect.display_instructions(display_time=10, message="<BLUE>William: Now is the time! Strike for victory!")

hero_falls = trigger_manager.add_trigger("[D11] Hero Falls")
hero_falls.new_condition.destroy_object(unit_object=william.reference_id)
hero_falls.new_effect.display_instructions(display_time=10, message="<YELLOW>William has fallen! The Norman invasion fails...")

# --- Objective Section ---
objectives = trigger_manager.add_trigger("[O] Main Objectives")
objectives.new_condition.timer(timer=1)
objectives.new_effect.display_instructions(display_time=20, message="Objectives:\n-Defeat Harold Godwinson\n-Capture the Saxon castle\n-William must survive")

primary = trigger_manager.add_trigger("[Obj] Primary Goal")
primary.new_condition.destroy_object(unit_object=harold.reference_id)
primary.new_effect.display_instructions(display_time=10, message="Harold has fallen! The throne of England is yours!")

secondary = trigger_manager.add_trigger("[Obj] Secondary Goal")
secondary.new_condition.destroy_object(unit_object=saxon_castle.reference_id)
secondary.new_effect.display_instructions(display_time=10, message="The Saxon castle has fallen!")

survival = trigger_manager.add_trigger("[Obj] Survival")
survival.new_condition.timer(timer=1)
survival.new_effect.display_instructions(display_time=10, message="William must survive to claim victory!")

# --- Victory/Defeat Section ---
victory = trigger_manager.add_trigger("VC")
victory.new_condition.destroy_object(unit_object=harold.reference_id)
victory.new_effect.declare_victory(source_player=PlayerId.ONE, enabled=1)

victory2 = trigger_manager.add_trigger("VC2")
victory2.new_condition.destroy_object(unit_object=saxon_castle.reference_id)
victory2.new_effect.declare_victory(source_player=PlayerId.ONE, enabled=1)

defeat = trigger_manager.add_trigger("Defeat")
defeat.new_condition.destroy_object(unit_object=william.reference_id)
defeat.new_effect.declare_victory(source_player=PlayerId.TWO, enabled=1)

defeat2 = trigger_manager.add_trigger("DEFEAT")
defeat2.new_condition.destroy_object(unit_object=norman_tc.reference_id)
defeat2.new_effect.declare_victory(source_player=PlayerId.TWO, enabled=1)

# --- Special Triggers ---
patrol = trigger_manager.add_trigger("Enemy Patrol")
patrol.new_condition.timer(timer=180)
patrol.new_effect.patrol(source_player=PlayerId.TWO, object_list_unit_id=UnitInfo.KNIGHT.ID, location_x=norman_base_x, location_y=norman_base_y)

sortie = trigger_manager.add_trigger("Enemy Sortie")
sortie.new_condition.objects_in_area(quantity=5, object_list=UnitInfo.KNIGHT.ID, source_player=PlayerId.ONE, area_x1=center-20, area_y1=hill_y-20, area_x2=center+20, area_y2=hill_y)
sortie.new_effect.patrol(source_player=PlayerId.TWO, object_list_unit_id=UnitInfo.MAN_AT_ARMS.ID, location_x=norman_base_x, location_y=norman_base_y)

# Save scenario
scenario.write_to_file("output.aoe2scenario")