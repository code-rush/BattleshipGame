from datetime import date
from google.appengine.ext import ndb
from protorpc import messages


class User(ndb.Model):
    """User Profile"""
    name = ndb.StringProperty(required=True)
    email = ndb.StringProperty(required=True)
    wins = ndb.IntegerProperty(default=0)
    games_played = ndb.IntegerProperty(default=0)

    @property
    def win_percentage(self):
        if self.games_played > 0:
            return float(self.wins) / float(self.games_played)
        else:
            return 0

    def to_form(self):
        return UserForm(name=self.name,
                    email=self.email,
                    wins=self.wins,
                    games_played=self.games_played,
                    wins_percentage=self.win_percentage)

    def add_win(self):
        """Add a win"""
        self.wins += 1
        self.games_played += 1
        self.put()

    def add_loss(self):
        """Add a loss"""
        self.games_played += 1
        self.put()


class Game(ndb.Model):
    """Game Object"""
    user_a_shipsboard = ndb.PickleProperty(required=True)
    user_b_shipsboard = ndb.PickleProperty(required=True)
    next_move = ndb.KeyProperty(required=True)
    user_a = ndb.KeyProperty(required=True, kind='User')
    user_b = ndb.KeyProperty(required=True, kind='User')
    game_over = ndb.BooleanProperty(required=True, default=False)
    winner = ndb.KeyProperty()
    user_a_playboard = ndb.PickleProperty(required=True)
    user_b_playboard = ndb.PickleProperty(required=True)

    @classmethod
    def new_game(cls, user_a, user_b):
        """Creates and returns a new game"""
        game = Game(user_a=user_a,
                    user_b=user_b,
                    next_move=user_a)
        game.user_a_shipsboard = ['' for i in range(100)]
        game.user_b_shipsboard = ['' for i in range(100)]
        game.user_a_playboard = ['' for i in range(100)]
        game.user_b_playboard = ['' for i in range(100)]
        game.put()
        return game

    def to_form(self):
        """Returns GameForm representation of Game"""
        form = GameForm(urlsafe_key=self.key.urlsafe(),
                        user_a=self.user_a.get().name,
                        user_b=self.user_b.get().name,
                        game_over=self.game_over,
                        next_move=self.next_move.get().name,
                        user_a_shipsboard=str(self.user_a_shipsboard),    # printing out the users board with
                        user_b_shipsboard=str(self.user_b_shipsboard),    # ship placements for testing purpose
                        user_a_playboard=str(self.user_a_playboard),
                        user_b_playboard=str(self.user_b_playboard))    
        if self.winner:
            form.winner = self.winner.get().name
        return form

    def end_game(self, winner):
        """Ends the game"""
        self.winner = winner
        self.game_over = True
        self.put()
        loser = self.user_a if winner == self.user_b else self.user_b
        winner.get().add_win
        loser.get().add_loss

class Score(ndb.Model):
    """Score Object"""
    date = ndb.DateProperty(required=True)
    winner = ndb.KeyProperty(required=True)
    loser = ndb.KeyProperty(required=True)

    def to_form(self):
        return ScoreForm(date=str(self.date),
                         winner=self.winner.get().name,
                         loser=self.loser.get().name)


class GameForm(messages.Message):
    """GameForm for outbound game state information"""
    urlsafe_key = messages.StringField(1, required=True)
    user_a_shipsboard = messages.StringField(2, required=True)
    user_b_shipsboard = messages.StringField(3, required=True)
    next_move = messages.StringField(4, required=True)
    user_a = messages.StringField(5, required=True)
    user_b = messages.StringField(6, required=True)
    game_over = messages.BooleanField(7, required=True)
    winner = messages.StringField(8)
    user_a_playboard = messages.StringField(9, required=True)
    user_b_playboard = messages.StringField(10, required=True)


class UserForm(messages.Message):
    """User Form"""
    name = messages.StringField(1, required=True)
    email = messages.StringField(2)
    wins = messages.IntegerField(3, required=True)
    games_played = messages.IntegerField(4, required=True)
    wins_percentage = messages.FloatField(5, required=True)

class ScoreForm(messages.Message):
    """ScoreForm for outbound Score information"""
    date = messages.StringField(1, required=True)
    winner = messages.StringField(2, required=True)
    loser = messages.StringField(3, required=True)


class ScoreForms(messages.Message):
    """Return multiple ScoreForms"""
    items = messages.MessageField(ScoreForm, 1, repeated=True)


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

