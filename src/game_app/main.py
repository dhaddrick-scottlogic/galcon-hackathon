from map_generation.even_distribution_map_generator import EvenDistributionMapGenerator
from bots.random_bot import RandomBot
from game.player import Player
from game.game import Game

bot_1 = RandomBot()
bot_2 = RandomBot()

player_1 = Player("Rupert", "red", bot_1.create_orders)
player_2 = Player("Sophie", "blue", bot_2.create_orders)

map = EvenDistributionMapGenerator(10, 5, [player_1, player_2]).create_map()

game = Game([player_1, player_2], map.planets, max_turn_limit=2)
game.run()

from pprint import pprint
for planet in game.current_state.planets:
    if not planet.owner == None:
        pprint(vars(planet))