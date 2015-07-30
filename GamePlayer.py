from Brisk import Brisk;
import time

class GamePlayer:
	def __init__(self):
		self.brisk = Brisk();
		self.map = Map(self.brisk)
		self.me = Player_Status(self.brisk, self.map, True)
		self.winner = None
		
		# self.enemy_player_state = Player_State()

	def start(self):
		while True:
			player_state = self.brisk.get_player_status()
			if player_state['winner']:
				self.winner = player_state['winner']
				print str(self.winner) + " WON!"
				return
			elif player_state['current_turn']:
				t0  = time.time()
				self.take_turn(player_state)
				print "Took " + str(time.time() - t0) + "seconds"

	def take_turn(self, player_state):
		self.update_information(player_state)
		# get first territory that is available

		# NEED TO IMPLEMENT
		# self.place_armies()

		# NEED TO IMPLEMENT
		self.launch_attack()

		# NEED TO IMPLEMENT
		# self.transfer_armies_or_end_turn()

		self.brisk.end_turn()

	def update_information(self, player_state_response):
		self.me.update(player_state_response)
		# self.enemy_player_state.update(asdf)update

	def place_armies(self):
		possible_actions = self.get_possible_place_armies() # DO THIS
		best_value = 0
		best_action = None
		for action in possible_actions:
			fake_do(action) # alter our game board in place DO THIS
			value = self.eval_place_armies() #see if we like the state of the board DO THIS
			if (value > best_value):
				best_value = value
				best_action = action
			fake_undo(action) # DO THIS
		execute_action(action)
		# update relevant information DO THIS

		num_reserves = self.me.num_reserves
		self.brisk.place_armies(self.me.territories[0].id, num_reserves)

	def launch_attack(self):
		for territory in self.me.territories:
			if len(territory.adjacent_territories) > 1:
				adjacent_territory_id = territory.adjacent_territories[0]
				if (not self.me.owns_territory(adjacent_territory_id)):
					sending = min(self.me.territory_map[territory.id]['num_armies'] - 1, 3)
					if sending <= 0:
						continue
					print '-----------------'
					print 'Game won: '+str(self.winner)
					print 'Attacking territory id: '+str(territory.id)
					print 'Defendig territory id: '+str(adjacent_territory_id)
					print 'Attacking territory: '+str(self.me.territory_map[territory.id])
					print 'Sending: '+str(sending)
					self.brisk.attack(territory.id, adjacent_territory_id, sending)
					break


class Map:
	def __init__(self, brisk):
		self.brisk = brisk
		self.update()

	def update(self, params = None):
		if not params:
			params = self.brisk.get_map_layout()
		self.territories = params['territories']
		self.version = params['version']
		self.continents = params['continents']
		self.serivce = params['service']

	def find(self, territory_id):
		for territory in self.territories:
			if territory['territory'] == territory_id:
				return territory
		return 'No such territory id'


class Player_Status:

	def __init__(self, brisk, map, is_me):
		self.brisk = brisk
		self.map = map
		self.territory_map = {}
		# if is_me:
		self.update()
		# else:
		# 	self.update(self.brisk.get_enemy_player_state())

	def update(self, params=None):
		if not params:
			params = self.brisk.get_player_status()
		self.version = params['version']
		self.service = params['service']
		# self.game = params['game']
		# self.player = params['player']
		self.current_turn = params['current_turn']
		self.eliminated = params['eliminated']
		self.winner = params['winner']
		self.num_armies = params['num_armies']
		self.num_reserves = params['num_reserves']
		self.territories = []
		for territory in params['territories']:
			territory_id = territory['territory']
			self.territory_map[territory_id] = territory
			self.territories.append( Territory(territory['territory'], territory['num_armies'], self) )

	def owns_territory(self, territory_id):
		return territory_id in self.territory_map

class Territory:
	def __init__(self, territory_id, num_armies, player_state):
		self.id = territory_id
		self.num_armies = num_armies
		self.owner = player_state
		self.brisk = self.owner.brisk
		self.map = self.owner.map
		self.adjacent_territories = self.map.find(self.id)['adjacent_territories']
		self.adjacent_territories = self.map.find(self.id)['adjacent_territories']

g = GamePlayer()
g.start()