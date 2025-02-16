from src.player import Player
from src.map import Map
from src.robot_controller import RobotController
from src.game_constants import Team, Tile, GameConstants, Direction, BuildingType, UnitType

from src.units import Unit
from src.buildings import Building

def calc_threat_level(rc: RobotController, enemy_ids,home_x,home_y):
        threat_level = 0
        for unit_id in enemy_ids:
            unit = rc.get_unit_from_id(unit_id)
            if (rc.chebyshev_distance_valid(unit.x, unit.y, home_x, home_y, 10)):
                threat_level += unit.cost
            else:
                threat_level += 1/2 * unit.cost

class BotPlayer(Player):
    def __init__(self, map: Map):
        self.map = map

    def play_turn(self, rc: RobotController):
        
        team = rc.get_ally_team()
        ally_castle_id = -1 #stays -1 if ally has no buildings

        ally_buildings = rc.get_buildings(team)
        for building in ally_buildings:
            if building.type == BuildingType.MAIN_CASTLE:
                ally_castle_id = rc.get_id_from_building(building)[1]
                break
        
        ally_units = rc.get_units(team)

        home_x = rc.get_building_from_id(ally_castle_id).x
        home_y = rc.get_building_from_id(ally_castle_id).y

        enemy = rc.get_enemy_team()
        enemy_castle_id = -1

        enemy_buildings = rc.get_buildings(enemy)
        for building in enemy_buildings:
            if building.type == BuildingType.MAIN_CASTLE:
                enemy_castle_id = rc.get_id_from_building(building)[1]
                break

        enemy_castle = rc.get_building_from_id(enemy_castle_id)
        if enemy_castle is None: 
            return
        
         # if threat level is above a certain level build catapults
        if (calc_threat_level(rc, rc.get_unit_ids(enemy),home_x,home_y) - rc.get_balance >= 1/2 * rc.get_balance):
            if rc.can_spawn_unit(UnitType.CATAPULT, ally_castle_id):
                rc.spawn_unit(UnitType.CATAPULT, ally_castle_id)
        else:
            # Otherwise build farms in squares +-two left and right up and down from home base.
            for i in [2,-2]:
                for j in [2,-2]:
                    if (rc.can_build_building(BuildingType.FARM1,home_x+i,home_y+j)):
                        rc.build_building(BuildingType.FARM1,home_x+i,home_y)

        return