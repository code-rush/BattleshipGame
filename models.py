from datetime import date
from google.appengine.ext import ndb
from protorpc import messages


class User(ndb.Model):
    """User Profile"""
    name = ndb.StringProperty(required=True)
    email = ndb.StringProperty(required=True)
    wins = ndb.IntegerProperty(default=0)
    games_played = ndb.IntegerProperty(default=0)
    # board = ndb.PickleProperty()

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

    @classmethod
    def new_game(cls, user_a, user_b):
        """Creates and returns a new game"""
        game = Game(user_a=user_a,
                    user_b=user_b,
                    next_move=user_a)
        game.user_a_board = ['' for i in range(100)]
        game.user_b_board = ['' for i in range(100)]
        game.game_history = []
        game.put()
        return game

    def to_form(self):
        """Returns GameForm representation of Game"""
        form = GameForm(urlsafe_key=self.key.urlsafe(),
                        user_a=self.user_a.get().name,
                        user_b=self.user_b.get().name,
                        game_over=self.game_over,
                        next_move=self.next_move.get().name,
                        user_a_board=str(self.user_a_board),    # printing out the users board with
                        user_b_board=str(self.user_b_board))    # ship placements for testing purpose
        if self.winner:
            form.winner = self.winner.get().name
        return form


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


class PlaceShipsForm(messages.Message):
    """Used by users to place ships on their board"""
    user_a = messages.StringField(1, required=True)
    ship_1_a = messages.IntegerField(2, required=True)
    ship_2_a = messages.IntegerField(3, required=True)
    ship_3_a = messages.IntegerField(4, required=True)
    ship_4_a = messages.IntegerField(5, required=True)
    user_b = messages.StringField(6, required=True)
    ship_1_b = messages.IntegerField(7, required=True)
    ship_2_b = messages.IntegerField(8, required=True)
    ship_3_b = messages.IntegerField(9, required=True)
    ship_4_b = messages.IntegerField(10, required=True)



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

