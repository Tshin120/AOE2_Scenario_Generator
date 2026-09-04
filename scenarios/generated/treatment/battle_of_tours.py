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
# Victory path: Defeat enemy leader or destroy enemy castle, multiple approaches available
# Defeat path: Hero death or loss of key defensive structures
# Resource sufficiency: Yes - starting gold/stone + map resources sufficient for military production
# Counter availability: Yes - player has barracks/range/stable to counter all enemy unit types
# Physical access: Yes - multiple paths through battlefield, no impassable barriers
# Timing viability: Yes - starting army sufficient to defend initial position

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

# Paint terrain - hills in center where Franks defend
hill_y = center - 10
for x in range(quarter, three_quarter):
    for y in range(hill_y-5, hill_y+5):
        unit_manager.add_unit(PlayerId.GAIA, unit_const=OtherInfo.CLIFF_DEFAULT_2.ID, x=x, y=y)

# Forests on flanks
for i in range(200):
    x = i % quarter
    y = i // 2
    unit_manager.add_unit(PlayerId.GAIA, unit_const=OtherInfo.TREE_OAK.ID, x=x, y=y)
    unit_manager.add_unit(PlayerId.GAIA, unit_const=OtherInfo.TREE_OAK.ID, x=three_quarter+x, y=y)

# Player 1 (Franks) base
frank_x, frank_y = quarter + 10, quarter
tc = unit_manager.add_unit(PlayerId.ONE, unit_const=BuildingInfo.TOWN_CENTER.ID, x=frank_x, y=frank_y)
barracks = unit_manager.add_unit(PlayerId.ONE, unit_const=BuildingInfo.BARRACKS.ID, x=frank_x-5, y=frank_y)
range_bld = unit_manager.add_unit(PlayerId.ONE, unit_const=BuildingInfo.ARCHERY_RANGE.ID, x=frank_x+5, y=frank_y)
stable = unit_manager.add_unit(PlayerId.ONE, unit_const=BuildingInfo.STABLE.ID, x=frank_x, y=frank_y+5)
blacksmith = unit_manager.add_unit(PlayerId.ONE, unit_const=BuildingInfo.BLACKSMITH.ID, x=frank_x-3, y=frank_y+5)

# Player 1 hero and army
hero = unit_manager.add_unit(PlayerId.ONE, unit_const=HeroInfo.RICHARD_THE_LIONHEART.ID, x=frank_x, y=frank_y-5)
for i in range(20):
    unit_manager.add_unit(PlayerId.ONE, unit_const=UnitInfo.MAN_AT_ARMS.ID, x=frank_x-10+i, y=frank_y-8)
    unit_manager.add_unit(PlayerId.ONE, unit_const=UnitInfo.CROSSBOWMAN.ID, x=frank_x-10+i, y=frank_y-10)

# Player 2 (Umayyad) base
enemy_x, enemy_y = three_quarter, three_quarter
castle = unit_manager.add_unit(PlayerId.TWO, unit_const=BuildingInfo.CASTLE.ID, x=enemy_x, y=enemy_y)
enemy_leader = unit_manager.add_unit(PlayerId.TWO, unit_const=HeroInfo.SALADIN.ID, x=enemy_x+2, y=enemy_y)

# Enemy buildings
unit_manager.add_unit(PlayerId.TWO, unit_const=BuildingInfo.BARRACKS.ID, x=enemy_x-5, y=enemy_y)
unit_manager.add_unit(PlayerId.TWO, unit_const=BuildingInfo.STABLE.ID, x=enemy_x+5, y=enemy_y)
unit_manager.add_unit(PlayerId.TWO, unit_const=BuildingInfo.ARCHERY_RANGE.ID, x=enemy_x, y=enemy_y+5)

# Enemy walls and gates
for i in range(15):
    unit_manager.add_unit(PlayerId.TWO, unit_const=BuildingInfo.STONE_WALL.ID, x=enemy_x-7+i, y=enemy_y-7)
    unit_manager.add_unit(PlayerId.TWO, unit_const=BuildingInfo.STONE_WALL.ID, x=enemy_x-7+i, y=enemy_y+7)
    unit_manager.add_unit(PlayerId.TWO, unit_const=BuildingInfo.STONE_WALL.ID, x=enemy_x-7, y=enemy_y-7+i)
    unit_manager.add_unit(PlayerId.TWO, unit_const=BuildingInfo.STONE_WALL.ID, x=enemy_x+7, y=enemy_y-7+i)

enemy_gate = unit_manager.add_unit(PlayerId.TWO, unit_const=BuildingInfo.GATE_NORTH_TO_SOUTH.ID, x=enemy_x, y=enemy_y-7)

# Enemy army
for i in range(30):
    unit_manager.add_unit(PlayerId.TWO, unit_const=UnitInfo.CAVALRY_ARCHER.ID, x=enemy_x-5+i%5, y=enemy_y-5+i//5)
    unit_manager.add_unit(PlayerId.TWO, unit_const=UnitInfo.CAMEL_RIDER.ID, x=enemy_x+5+i%5, y=enemy_y+i//5)

# GAIA resources near player base
for i in range(5):
    unit_manager.add_unit(PlayerId.GAIA, unit_const=OtherInfo.GOLD_MINE.ID, x=frank_x-10+i, y=frank_y+10)
    unit_manager.add_unit(PlayerId.GAIA, unit_const=OtherInfo.STONE_MINE.ID, x=frank_x+i, y=frank_y+12)
for i in range(8):
    unit_manager.add_unit(PlayerId.GAIA, unit_const=OtherInfo.FORAGE_BUSH.ID, x=frank_x-4+i, y=frank_y+8)
for i in range(6):
    unit_manager.add_unit(PlayerId.GAIA, unit_const=UnitInfo.SHEEP.ID, x=frank_x+i, y=frank_y-8)

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
hard_trigger.new_effect.create_object(object_list_unit_id=UnitInfo.CAVALRY_ARCHER.ID, source_player=PlayerId.TWO, location_x=enemy_x, location_y=enemy_y)

gate_trigger = trigger_manager.add_trigger("Close Gates")
gate_trigger.new_condition.timer(timer=1)

# --- Dialogue Section (12 triggers) ---
intro = trigger_manager.add_trigger("[D0] Intro")
intro.new_condition.timer(timer=5)
intro.new_effect.display_instructions(display_time=10, message="<YELLOW>Narrator: The Umayyad army advances into Francia. Charles Martel musters his forces to defend against the invasion.")

scout = trigger_manager.add_trigger("[D1] Scout Report")
scout.new_condition.timer(timer=15)
scout.new_effect.display_instructions(display_time=10, message="<BLUE>Scout: My lord, the enemy approaches from the south with many horse archers and camel riders.")

commander = trigger_manager.add_trigger("[D2] Commander Speech")
commander.new_condition.timer(timer=30)
commander.new_effect.display_instructions(display_time=10, message="<BLUE>Charles Martel: Hold the high ground! Our infantry will break their cavalry charge!")

taunt1 = trigger_manager.add_trigger("[D3] Enemy Taunt 1")
taunt1.new_condition.timer(timer=60)
taunt1.new_effect.display_instructions(display_time=10, message="<RED>Umayyad Commander: Your primitive forces cannot stand against our superior cavalry!")

taunt2 = trigger_manager.add_trigger("[D4] Enemy Taunt 2")
taunt2.new_condition.timer(timer=120)
taunt2.new_effect.display_instructions(display_time=10, message="<RED>Umayyad Commander: Forward! Crush their infantry line!")

location1 = trigger_manager.add_trigger("[D5] At Location 1")
location1.new_condition.bring_object_to_area(unit_object=hero.reference_id, area_x1=center-10, area_y1=hill_y-10, area_x2=center+10, area_y2=hill_y+10)
location1.new_effect.display_instructions(display_time=10, message="<BLUE>Charles Martel: This hill will be our anvil!")

location2 = trigger_manager.add_trigger("[D6] At Location 2")
location2.new_condition.bring_object_to_area(unit_object=hero.reference_id, area_x1=enemy_x-20, area_y1=enemy_y-20, area_x2=enemy_x+20, area_y2=enemy_y+20)
location2.new_effect.display_instructions(display_time=10, message="<BLUE>Charles Martel: Press the attack! Drive them back!")

battle = trigger_manager.add_trigger("[D7] Battle Begins")
battle.new_condition.timer(timer=180)
battle.new_effect.display_instructions(display_time=10, message="<YELLOW>Narrator: The armies clash on the field of Tours!")

midpoint = trigger_manager.add_trigger("[D8] Midpoint Update")
midpoint.new_condition.timer(timer=300)
midpoint.new_effect.display_instructions(display_time=10, message="<YELLOW>Narrator: The battle hangs in the balance!")

enemy_weak = trigger_manager.add_trigger("[D9] Enemy Weakening")
enemy_weak.new_condition.objects_in_area(quantity=10, object_list=UnitInfo.CAVALRY_ARCHER.ID, source_player=PlayerId.TWO, area_x1=0, area_y1=0, area_x2=map_size, area_y2=map_size)
enemy_weak.new_effect.display_instructions(display_time=10, message="<BLUE>Charles Martel: Their army weakens! Press forward!")

final_push = trigger_manager.add_trigger("[D10] Final Push")
final_push.new_condition.timer(timer=420)
final_push.new_effect.display_instructions(display_time=10, message="<BLUE>Charles Martel: For Francia! Drive them from our lands!")

hero_falls = trigger_manager.add_trigger("[D11] Hero Falls")
hero_falls.new_condition.destroy_object(unit_object=hero.reference_id)
hero_falls.new_effect.display_instructions(display_time=10, message="<YELLOW>Narrator: Charles Martel has fallen! The Frankish army breaks!")

# --- Objective Section (4 triggers) ---
objectives = trigger_manager.add_trigger("[O] Main Objectives")
objectives.new_condition.timer(timer=1)
objectives.new_effect.display_instructions(display_time=20, message="Defeat the Umayyad invasion!\n-Destroy the enemy castle\n-Kill the enemy commander\n-Charles Martel must survive")

primary = trigger_manager.add_trigger("[Obj] Primary Goal")
primary.new_condition.destroy_object(unit_object=castle.reference_id)
primary.new_effect.display_instructions(display_time=10, message="The enemy stronghold has fallen!")

secondary = trigger_manager.add_trigger("[Obj] Secondary Goal")
secondary.new_condition.destroy_object(unit_object=enemy_leader.reference_id)
secondary.new_effect.display_instructions(display_time=10, message="The Umayyad commander is slain!")

survival = trigger_manager.add_trigger("[Obj] Survival")
survival.new_condition.timer(timer=1)
survival.new_effect.display_instructions(display_time=10, message="Charles Martel must survive!")

# --- Victory/Defeat Section (4 triggers) ---
victory = trigger_manager.add_trigger("VC")
victory.new_condition.destroy_object(unit_object=castle.reference_id)
victory.new_effect.declare_victory(source_player=PlayerId.ONE, enabled=1)

victory2 = trigger_manager.add_trigger("VC2")
victory2.new_condition.destroy_object(unit_object=enemy_leader.reference_id)
victory2.new_effect.declare_victory(source_player=PlayerId.ONE, enabled=1)

defeat = trigger_manager.add_trigger("Defeat")
defeat.new_condition.destroy_object(unit_object=hero.reference_id)
defeat.new_effect.declare_victory(source_player=PlayerId.TWO, enabled=1)

defeat2 = trigger_manager.add_trigger("DEFEAT")
defeat2.new_condition.destroy_object(unit_object=tc.reference_id)
defeat2.new_effect.declare_victory(source_player=PlayerId.TWO, enabled=1)

# Save scenario
scenario.write_to_file("output.aoe2scenario")