from datetime import date
from google.appengine.ext import ndb
from protorpc import messages


class User(ndb.Model):
    """User Profile"""
    name = ndb.StringProperty(required=True)
    email = ndb.StringProperty(required=True)
    wins = ndb.IntegerProperty(default=0)
    games_played = ndb.IntegerProperty(default=0)
    board = ndb.PickleProperty()

class Game(ndb.Model):
    """Game Object"""
    user_a_board = ndb.PickleProperty(required=True)
    user_b_board = ndb.PickleProperty(required=True)
    next_move = ndb.KeyProperty(required=True)
    user_a = ndb.KeyProperty(required=True, kind='User')
    user_b = ndb.KeyProperty(required=True, kind='User')
    game_over = ndb.BooleanProperty(required=True, default=False)
    winner = ndb.KeyProperty()
    game_history = ndb.PickleProperty(required=True)


class GameForm(messages.Message):
    """GameForm for outbound game state information"""
    urlsafe_key = messages.StringField(1, required=True)
    user_a_board = messages.StringField(2, required=True)
    user_b_board = messages.StringField(3, required=True)
    next_move = messages.StringField(4, required=True)
    user_a = messages.StringField(5, required=True)
    user_b = messages.StringField(6, required=True)
    game_over = messages.BooleanField(7, required=True)
    winner = messages.StringField(8)


class UserForm(messages.Message):
    """User Form"""
    name = messages.StringField(1, required=True)
    email = messages.StringField(2)
    wins = messages.IntegerField(3, required=True)
    games_played = messages.IntegerField(4, required=True)


class NewGameForm(messages.Message):
    """Used to create a new game"""
    user_a = messages.StringField(1, required=True)
    user_b = messages.StringField(2, required=True)


class MakeMoveForm(messages.Message):
    """Used to create a move"""
    user_name = messages.StringField(1, required=True)
    move = messages.IntegerField(2, required=True)

class GameForms(messages.Message):
    """Container for multiple Game Forms"""
    items = messages.MessageField(GameForm, 1, repeated=True)

class UserForms(messages.Message):
    """Container for multiple User Forms"""
    items = messages.MessageField(UserForm, 1, repeated=True)

class StringMessage(messages.Message):
    """Single outbound string message"""
    message = messages.StringField(1, required=True)

