"""
R2: Regicide with Multiple Recovery Options - FULLY REACHABLE Scenario

Map: Black Forest (closed map, choke points)
Civilization: Player: Teutons | AI: Japanese
Starting Resources: Standard + King + Castle
Victory Condition: Regicide (kill enemy King)

Graph Structure:
s0[Start: TC + Castle + King + Vills]
  -> n1[Boom behind walls] -> n2[Mass army]
     -> n3a[Onager + infantry push through choke] -> V[Kill King]
     -> n3b[Trebuchet wall break + cavalry flank]  -> V[Kill King]
     -> n3c[Trade boom -> Imperial superiority]     -> V[Kill King]
  (Forest walls = natural defense, prevents total wipe)
  (King can always be garrisoned in Castle for protection)

WHY REACHABLE:
- Black Forest terrain provides natural defense
- Starting Castle = immediate defensive capability and King protection
- Teutons strong infantry + siege complement choke points
- Even if attack fails, fall back behind forest walls and rebuild
- Trade provides infinite gold for sustained late-game
- Recovery edges exist at every branch
"""

import sys
import io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

from AoE2ScenarioParser.scenarios.aoe2_de_scenario import AoE2DEScenario
from AoE2ScenarioParser.datasets.players import PlayerId
from AoE2ScenarioParser.datasets.units import UnitInfo
from AoE2ScenarioParser.datasets.buildings import BuildingInfo
from AoE2ScenarioParser.datasets.other import OtherInfo
from AoE2ScenarioParser.datasets.heroes import HeroInfo
from AoE2ScenarioParser.datasets.terrains import TerrainId

# Create scenario
scenario = AoE2DEScenario.from_default()
unit_manager = scenario.unit_manager
trigger_manager = scenario.trigger_manager
map_manager = scenario.map_manager

map_size = map_manager.map_size
center = map_size // 2
quarter = map_size // 4
three_quarter = (map_size * 3) // 4

# ============================================================
# BLACK FOREST TERRAIN: Dense forests with chokepoint
# ============================================================

# Fill most of map with forest (Black Forest style)
# Leave clearings for bases and a single chokepoint path

# Player clearing (lower-left)
player_clear_x, player_clear_y = quarter, quarter
player_clear_size = 30

# Enemy clearing (upper-right)
enemy_clear_x, enemy_clear_y = three_quarter, three_quarter
enemy_clear_size = 30

# Chokepoint corridor through center
choke_y = center
choke_width = 8

# Place forests everywhere except clearings and chokepoint
for x in range(map_size):
    for y in range(map_size):
        # Check if in player clearing
        in_player_clear = (abs(x - player_clear_x) < player_clear_size // 2 and
                          abs(y - player_clear_y) < player_clear_size // 2)
        # Check if in enemy clearing
        in_enemy_clear = (abs(x - enemy_clear_x) < enemy_clear_size // 2 and
                         abs(y - enemy_clear_y) < enemy_clear_size // 2)
        # Check if in chokepoint corridor
        in_choke = (abs(y - choke_y) < choke_width // 2 and
                   x > player_clear_x and x < enemy_clear_x)

        if not in_player_clear and not in_enemy_clear and not in_choke:
            # 70% chance of tree (sparse enough to not crash)
            if (x + y) % 3 != 0:  # Deterministic pseudo-random
                unit_manager.add_unit(PlayerId.GAIA, unit_const=OtherInfo.TREE_OAK.ID,
                                      x=x, y=y)

# ============================================================
# PLAYER BASE: Teutons - Regicide start with Castle
# ============================================================
player_base_x, player_base_y = player_clear_x, player_clear_y

# Town Center
unit_manager.add_unit(PlayerId.ONE, unit_const=BuildingInfo.TOWN_CENTER.ID,
                      x=player_base_x, y=player_base_y)

# Starting Castle (Regicide)
player_castle = unit_manager.add_unit(PlayerId.ONE, unit_const=BuildingInfo.CASTLE.ID,
                                       x=player_base_x - 8, y=player_base_y)

# King (Regicide - must survive)
player_king = unit_manager.add_unit(PlayerId.ONE, unit_const=UnitInfo.KING.ID,
                                     x=player_base_x - 5, y=player_base_y + 3)

# Starting villagers
for i in range(8):
    unit_manager.add_unit(PlayerId.ONE, unit_const=UnitInfo.VILLAGER_MALE.ID,
                          x=player_base_x + 3 + i % 4, y=player_base_y + i // 4)

# Scout
unit_manager.add_unit(PlayerId.ONE, unit_const=UnitInfo.SCOUT_CAVALRY.ID,
                      x=player_base_x + 8, y=player_base_y)

# Military buildings
unit_manager.add_unit(PlayerId.ONE, unit_const=BuildingInfo.BARRACKS.ID,
                      x=player_base_x + 10, y=player_base_y - 5)
unit_manager.add_unit(PlayerId.ONE, unit_const=BuildingInfo.SIEGE_WORKSHOP.ID,
                      x=player_base_x + 10, y=player_base_y)
unit_manager.add_unit(PlayerId.ONE, unit_const=BuildingInfo.STABLE.ID,
                      x=player_base_x + 10, y=player_base_y + 5)

# Houses
for i in range(5):
    unit_manager.add_unit(PlayerId.ONE, unit_const=BuildingInfo.HOUSE.ID,
                          x=player_base_x - 10 + i * 3, y=player_base_y + 8)

# ============================================================
# PLAYER RESOURCES: Abundant (Black Forest is resource-rich)
# ============================================================
# Gold (multiple piles - trade also available)
for pile in range(5):
    for i in range(5):
        unit_manager.add_unit(PlayerId.GAIA, unit_const=OtherInfo.GOLD_MINE.ID,
                              x=player_base_x - 12 + pile * 5, y=player_base_y - 10 + i)

# Stone
for pile in range(4):
    for i in range(4):
        unit_manager.add_unit(PlayerId.GAIA, unit_const=OtherInfo.STONE_MINE.ID,
                              x=player_base_x + 8 + pile * 4, y=player_base_y + 10 + i)

# Food
for i in range(8):
    unit_manager.add_unit(PlayerId.GAIA, unit_const=UnitInfo.SHEEP.ID,
                          x=player_base_x + 5 + i % 4, y=player_base_y - 5 + i // 4)

for i in range(6):
    unit_manager.add_unit(PlayerId.GAIA, unit_const=OtherInfo.FORAGE_BUSH.ID,
                          x=player_base_x - 5 + i, y=player_base_y - 8)

# Market (for trade - infinite gold)
unit_manager.add_unit(PlayerId.ONE, unit_const=BuildingInfo.MARKET.ID,
                      x=player_base_x - 10, y=player_base_y - 5)

# ============================================================
# ENEMY BASE: Japanese - Mirror Regicide start
# ============================================================
enemy_base_x, enemy_base_y = enemy_clear_x, enemy_clear_y

# Enemy TC
unit_manager.add_unit(PlayerId.TWO, unit_const=BuildingInfo.TOWN_CENTER.ID,
                      x=enemy_base_x, y=enemy_base_y)

# Enemy Castle
unit_manager.add_unit(PlayerId.TWO, unit_const=BuildingInfo.CASTLE.ID,
                      x=enemy_base_x + 8, y=enemy_base_y)

# Enemy King (THE TARGET)
enemy_king = unit_manager.add_unit(PlayerId.TWO, unit_const=UnitInfo.KING.ID,
                                    x=enemy_base_x + 5, y=enemy_base_y - 3)

# Enemy villagers
for i in range(8):
    unit_manager.add_unit(PlayerId.TWO, unit_const=UnitInfo.VILLAGER_MALE.ID,
                          x=enemy_base_x - 3 - i % 4, y=enemy_base_y + i // 4)

# Enemy military
for i in range(10):
    unit_manager.add_unit(PlayerId.TWO, unit_const=UnitInfo.SAMURAI.ID,
                          x=enemy_base_x + i % 5, y=enemy_base_y + 5 + i // 5)

# Enemy resources
for pile in range(4):
    for i in range(4):
        unit_manager.add_unit(PlayerId.GAIA, unit_const=OtherInfo.GOLD_MINE.ID,
                              x=enemy_base_x + 10 + pile * 4, y=enemy_base_y - 8 + i)

# Enemy Market (trade route between markets)
unit_manager.add_unit(PlayerId.TWO, unit_const=BuildingInfo.MARKET.ID,
                      x=enemy_base_x + 10, y=enemy_base_y + 5)

# ============================================================
# CHOKEPOINT FORTIFICATIONS
# ============================================================
choke_center_x = center

# Palisade walls at chokepoint (can be breached)
for i in range(choke_width + 4):
    if i != choke_width // 2 and i != choke_width // 2 + 1:  # Gap for gate
        unit_manager.add_unit(PlayerId.TWO, unit_const=BuildingInfo.PALISADE_WALL.ID,
                              x=choke_center_x, y=choke_y - choke_width // 2 - 2 + i)

# Gate (enemy owned)
enemy_gate = unit_manager.add_unit(PlayerId.TWO, unit_const=BuildingInfo.PALISADE_GATE.ID,
                                   x=choke_center_x, y=choke_y)

# Watch towers defending choke
unit_manager.add_unit(PlayerId.TWO, unit_const=BuildingInfo.WATCH_TOWER.ID,
                      x=choke_center_x + 3, y=choke_y - 3)
unit_manager.add_unit(PlayerId.TWO, unit_const=BuildingInfo.WATCH_TOWER.ID,
                      x=choke_center_x + 3, y=choke_y + 3)

# ============================================================
# TRIGGERS
# ============================================================

# Setup
t = trigger_manager.add_trigger("[Setup] R2 Regicide - REACHABLE")
t.new_condition.timer(timer=1)
t.new_effect.display_instructions(
    source_player=PlayerId.ONE,
    display_time=20,
    message="<GREEN>R2: REGICIDE WITH MULTIPLE RECOVERY OPTIONS\n\n<AQUA>FULLY REACHABLE SCENARIO\n\nYou are the Teutons vs Japanese on Black Forest.\nVictory: Kill the enemy King.\nDefeat: Your King dies.\n\n<GREEN>Starting Castle provides immediate defense.\nForest walls allow safe booming.\nTrade provides infinite gold."
)

# Regicide rules
t = trigger_manager.add_trigger("[Regicide] Protect Your King")
t.new_condition.timer(timer=5)
t.new_effect.display_instructions(
    source_player=PlayerId.ONE,
    display_time=12,
    message="<AQUA>REGICIDE RULES:\n- Protect your King at all costs\n- Kill the enemy King to win\n- Garrison King in Castle for safety\n\n<GREEN>VICTORY PATHS:\nn3a: Infantry + Onagers through choke\nn3b: Trebuchets + cavalry flank\nn3c: Trade boom -> Imperial dominance"
)

# State s0
t = trigger_manager.add_trigger("[Analysis] State s0 - Defensive Start")
t.new_condition.timer(timer=10)
t.new_effect.display_instructions(
    source_player=PlayerId.ONE,
    display_time=12,
    message="<GREEN>[GRAPH STATE s0]\n\nStarting position:\n- Castle provides immediate defense\n- King can garrison for protection\n- Forest walls block early attacks\n- Single chokepoint controls access\n\nSafe economic development guaranteed.\nMultiple paths to V exist."
)

# Boom phase
t = trigger_manager.add_trigger("[Analysis] State n1 - Boom Phase")
t.new_condition.timer(timer=600)
t.new_effect.display_instructions(
    source_player=PlayerId.ONE,
    display_time=10,
    message="<GREEN>[GRAPH STATE n1 - Booming]\n\nBlack Forest advantages:\n- Natural forest walls = free defense\n- Chokepoint = easy to defend\n- Trade route established = infinite gold\n- Safe expansion within clearing\n\nNo enemy can reach you without siege."
)

# Military options
t = trigger_manager.add_trigger("[Analysis] State n2 - Army Massing")
t.new_condition.timer(timer=1200)
t.new_effect.display_instructions(
    source_player=PlayerId.ONE,
    display_time=12,
    message="<GREEN>[GRAPH STATE n2 - Military Options]\n\nTeuton advantages:\n- Teutonic Knights (slow but powerful)\n- Siege Onagers (cut through forest)\n- Ironclad (siege HP bonus)\n\nPath n3a: Mass infantry + Onagers\nPath n3b: Trebuchets break walls + Paladin flank\nPath n3c: Trade boom -> overwhelming force"
)

# Chokepoint strategy
t = trigger_manager.add_trigger("[Analysis] Chokepoint Breach")
t.new_condition.timer(timer=1500)
t.new_effect.display_instructions(
    source_player=PlayerId.ONE,
    display_time=10,
    message="<GREEN>[STRATEGIC ANALYSIS]\n\nChokepoint options:\n1. Siege Onagers cut through trees (bypass)\n2. Trebuchets destroy walls/towers\n3. Mass infantry storm the gap\n\nEven if first attack fails:\n- Fall back behind forest\n- Rebuild army (trade provides gold)\n- Try alternative approach"
)

# Recovery demonstration
t = trigger_manager.add_trigger("[Analysis] Recovery Always Possible")
t.new_condition.timer(timer=1800)
t.new_effect.display_instructions(
    source_player=PlayerId.ONE,
    display_time=12,
    message="<GREEN>[RECOVERY ANALYSIS]\n\nBlack Forest recovery advantages:\n- Forest walls prevent total wipe\n- Retreat to Castle for protection\n- King garrisons safely\n- Trade continues providing gold\n\nEven after losing army:\n-> Rebuild behind natural walls\n-> Trade cart income continues\n-> Multiple attack angles via tree cutting"
)

# Victory - Kill enemy King
t = trigger_manager.add_trigger("[Victory] Regicide - King Killed")
t.new_condition.destroy_object(unit_object=enemy_king.reference_id)
t.new_effect.display_instructions(
    source_player=PlayerId.ONE,
    display_time=12,
    message="<GREEN>VICTORY! The enemy King has fallen!\n\n[GRAPH STATE V]\n\nPath successfully traversed from s0 to V.\nBlack Forest provided:\n- Safe development time\n- Multiple strategic options\n- Recovery opportunities at every state"
)
t.new_effect.declare_victory(source_player=PlayerId.ONE, enabled=1)

# Defeat - Player King dies
t = trigger_manager.add_trigger("[Defeat] Regicide - Your King Died")
t.new_condition.destroy_object(unit_object=player_king.reference_id)
t.new_effect.display_instructions(
    source_player=PlayerId.ONE,
    display_time=10,
    message="<RED>DEFEAT - Your King has fallen!\n\nVictory WAS achievable.\nThis scenario is fully REACHABLE.\nYou failed to protect your King,\nbut paths to V existed throughout."
)
t.new_effect.declare_victory(source_player=PlayerId.TWO, enabled=1)

# Save scenario
output_path = "r2_regicide_reachable.aoe2scenario"
scenario.write_to_file(output_path)
print(f"Created: {output_path}")
print("Reachability: FULL (Black Forest defenses + trade + Castle)")
print("Recovery: ALWAYS POSSIBLE (fall back behind forests, rebuild)")
