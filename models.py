from datetime import date
from google.appengine.ext import ndb


class User(ndb.Model):
	"""User Profile"""
	name = ndb.StringProperty(required=True)
	email = ndb.StringProperty(required=True)
	wins = ndb.IntegerProperty(default=0)
	games_played = ndb.IntegerProperty(default=0)


class Game(ndb.Model):
	"""Game Object"""
	board = ndb.PickleProperty(required=True)
	next_move = ndb.KeyProperty(required=True)
	user_a = ndb.KeyProperty(required=True, kind='User')
	user_b = ndb.KeyProperty(required=True, kind='User')
	game_over = ndb.BooleanProperty(required=True, default=False)
	winner = ndb.KeyProperty()
	game_history = ndb.PickleProperty(required=True)
