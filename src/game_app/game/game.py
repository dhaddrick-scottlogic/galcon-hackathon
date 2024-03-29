from game.galaxy import Galaxy
from game.player import Player
from game.planet import Planet
from game.fleet import Fleet
from game.order import Order
from game.utils import get_next_fleet_coords, get_distance

from typing import List
import copy

class Game:
    game_counter = 0

    def __init__(
        self,
        players: list[Player],
        starting_map: List[Planet]=None,
        history: List[Galaxy]=None,
        max_turn_limit: int=500
    ):
        if not starting_map and not history:
            raise ValueError("Either a starting_map or history arg must be passed to a Game")
        elif starting_map and history:
            raise ValueError("Can't specify both a starting_map or history arg for a Game")

        self.players=players

        if starting_map:
            self.history=[Galaxy(planets=starting_map, fleets=[])]
        else:
            self.history=history
        self.current_state = copy.deepcopy(self.history[-1])
        self.winner = None
        self.max_turn_limit=max_turn_limit
        self.id = f"G{Game.game_counter}"
        Game.game_counter += 1

    def _get_player_orders(self) -> List[Order]:
        all_orders = []
        for player in self.players:

            current_p_orders = []
            for p_order in player.get_next_orders(player, self.current_state):
                try:
                    current_p_orders.append(Order(**p_order, player=player))
                except:
                    print(f"Incorrect order passed: {p_order}")
            all_orders += current_p_orders

        return all_orders
    
    def _iterate_planets(self):
        for planet in self.current_state.planets:
            planet.run()

    def _save_state(self):
        self.history.append(copy.deepcopy(self.current_state))

    def _create_fleets(self, orders: List[Order]):
        for order in orders:
            starting_coordinates = get_next_fleet_coords(order.source.position, order.destination.position, order.source.radius)
            new_fleet = Fleet(position=starting_coordinates, destination=order.destination, troop_count=order.troop_count, owner=order.player)
            self.current_state.fleets.append(new_fleet)

    def _move_fleets(self):
        for fleet in self.current_state.fleets:
            if get_distance(fleet.position, fleet.destination.position) < fleet.speed:
                fleet.destination.arriving_fleets.append(fleet)
                self.current_state.fleets.remove(fleet)
            else:
                fleet.position = get_next_fleet_coords(fleet.position, fleet.destination.position, fleet.speed)

    def _calculate_combat(self):
        for planet in self.current_state.planets:
            if planet.arriving_fleets:
                planet.calculate_combat()

    def run(self):
        while not self.winner and len(self.history) < self.max_turn_limit:
            orders = self._get_player_orders()
            self._create_fleets(orders)
            self._move_fleets()
            self._calculate_combat()
            self._iterate_planets()
            self._save_state()
