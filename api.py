import endpoints
from protorpc import remote, messages, message_types
from google.appengine.ext import ndb
from google.appengine.api import taskqueue
from models import User, Game, Score
from models import UserForm, GameForm, UserForms, GameForms, PlaceShipsForm
from models import StringMessage, MakeMoveForm, NewGameForm
from models import ScoreForms
from models import GameHistoryForm
from utils import get_by_urlsafe, check_placement


NEW_GAME_REQUEST = endpoints.ResourceContainer(NewGameForm)
GET_GAME_REQUEST = endpoints.ResourceContainer(
        urlsafe_game_key=messages.StringField(1))
GET_USER_GAME_REQUEST = endpoints.ResourceContainer(
        urlsafe_game_key=messages.StringField(1),
        user_name=messages.StringField(2))
MAKE_MOVE_REQUEST = endpoints.ResourceContainer(MakeMoveForm,
        urlsafe_game_key=messages.StringField(1))
USER_REQUEST = endpoints.ResourceContainer(user_name=messages.StringField(1),
                                           email=messages.StringField(2))
PLACE_SHIP_REQUEST = endpoints.ResourceContainer(PlaceShipsForm,
        urlsafe_game_key=messages.StringField(1))


SHIPSA = []
SHIPSB = []


@endpoints.api(name='battle_ship', version='v1')
class BattleShipAPI(remote.Service):
    """Game API"""
    @endpoints.method(USER_REQUEST, StringMessage, name='create_user',
                      path='user', http_method='POST')
    def create_user(self, request):
        """Creates a user"""
        if User.query(User.name == request.user_name).get():
            raise endpoints.ConflictException(
                        'A user with that name already exists!')
        user = User(name=request.user_name, email=request.email)
        user.put()
        return StringMessage(message='User {} successfully created!'.format(request.user_name))

    @endpoints.method(GET_GAME_REQUEST, GameForm, name='get_game',
                      path='game/{urlsafe_game_key}', http_method='GET')
    def get_game(self, request):
        """Return the current game state"""
        game = get_by_urlsafe(request.urlsafe_game_key, Game)
        if game:
            return game.to_form()
        else:
            raise endpoints.NotFoundException('Game not found!')


    @endpoints.method(NEW_GAME_REQUEST, GameForm, name='new_game',
                      path='game', http_method='POST')
    def new_game(self, request):
        """Creates new game"""
        user_a = User.query(User.name == request.user_a).get()
        user_b = User.query(User.name == request.user_b).get()
        if not user_a and user_b:
            raise endpoints.NotFoundException('One of the users does not exist!')

        game = Game.new_game(user_a.key, user_b.key)
        return game.to_form()


    @endpoints.method(PLACE_SHIP_REQUEST, GameForm, name='place_ships',
                      path='game/{urlsafe_game_key}/place_ships',
                      http_method='PUT')
    def place_ships_on_board(self, request):
        """Places ships on board for both users in game"""
        game = get_by_urlsafe(request.urlsafe_game_key, Game)
        if not game:
            raise endpoints.NotFoundException('Game not found!')
        if game.game_over:
            raise endpoints.NotFoundException('Game is already over')

        user_a = User.query(User.name == request.user_a).get()
        user_b = User.query(User.name == request.user_b).get()
        if user_a.key != game.user_a:
            raise endpoints.BadRequestException('User_a is not you')
        if user_b.key != game.user_b:
            raise endpoints.BadRequestException('User_b is not you')


        global SHIPSA
        global SHIPSB

        position_ship_1_a = request.ship_1_a
        placement_allowed = check_placement(position_ship_1_a,1)
        if not placement_allowed:
            raise endpoints.BadRequestException(
                    'Invalid placement! Your ship placement cannot be outside the board')

        ship1a = [position_ship_1_a + 20,
                  position_ship_1_a + 10,
                  position_ship_1_a,
                  position_ship_1_a - 10,
                  position_ship_1_a - 20]

        position_ship_2_a = request.ship_2_a
        placement_allowed = check_placement(position_ship_2_a,2)
        if not placement_allowed:
            raise endpoints.BadRequestException(
                    'Invalid placement! Your ship placement cannot be outside the board')

        ship2a = [position_ship_2_a - 1,
                  position_ship_2_a,
                  position_ship_2_a + 1]


        position_ship_3_a = request.ship_3_a
        placement_allowed = check_placement(position_ship_3_a,3)
        if not placement_allowed:
            raise endpoints.BadRequestException(
                    'Invalid placement! Your ship placement cannot be outside the board')

        
        ship3a = [position_ship_3_a + 10,
                  position_ship_3_a - 1,
                  position_ship_3_a,
                  position_ship_3_a - 10]


        position_ship_4_a = request.ship_4_a
        placement_allowed = check_placement(position_ship_4_a,4)
        if not placement_allowed:
            raise endpoints.BadRequestException(
                    'Invalid placement! Your ship placement cannot be outside the board')


        ship4a = [position_ship_4_a + 9,
                  position_ship_4_a - 1,
                  position_ship_4_a,
                  position_ship_4_a - 10]


        for i in ship1a:
            if i > 99 or i < 0:
                raise endpoints.BadRequestException(
                        'Invalid placement! Your part of the ship is outside the board')
            if i in ship2a or i in ship3a or i in ship4a:
                raise endpoints.BadRequestException(
                        'Invalid placement! Your ships overlap')
            game.user_a_shipsboard[i] = 'A1'
            SHIPSA.append(ship1a)


        for i in ship2a:
            if i > 99 or i < 0:
                raise endpoints.BadRequestException(
                        'Invalid placement! Your part of the ship is outside the board')
            if i in ship1a or i in ship4a or i in ship3a:
                raise endpoints.BadRequestException(
                        'Invalid placement! Your ships overlap')
            game.user_a_shipsboard[i] = 'A2'
            SHIPSA.append(ship2a)


        for i in ship3a:
            if i > 99 or i < 0:
                raise endpoints.BadRequestException(
                        'Invalid placement! Your part of the ship is outside the board')
            if i in ship1a or i in ship2a or i in ship4a:
                raise endpoints.BadRequestException(
                        'Invalid placement! Your ships overlap')
            game.user_a_shipsboard[i] = 'A3'
            SHIPSA.append(ship3a)
        

        for i in ship4a:
            if i > 99 or i < 0:
                raise endpoints.BadRequestException(
                        'Invalid placement! Your part of the ship is outside the board')
            if i in ship1a or i in ship2a or i in ship3a:
                raise endpoints.BadRequestException(
                        'Invalid placement! Your ships overlap')
            game.user_a_shipsboard[i] = 'A4'
            SHIPSA.append(ship4a)



        position_ship_1_b = request.ship_1_b
        placement_allowed = check_placement(position_ship_1_b,1)
        if not placement_allowed:
            raise endpoints.BadRequestException(
                    'Invalid placement! Your ship placement cannot be outside the board')

        ship1b = [position_ship_1_b + 20,
                  position_ship_1_b + 10,
                  position_ship_1_b,
                  position_ship_1_b - 10,
                  position_ship_1_b - 20]


        position_ship_2_b = request.ship_2_b
        placement_allowed = check_placement(position_ship_2_b,2)
        if not placement_allowed:
            raise endpoints.BadRequestException(
                    'Invalid placement! Your ship placement cannot be outside the board')


        ship2b = [position_ship_2_b - 1,
                  position_ship_2_b,
                  position_ship_2_b + 1]


        position_ship_3_b = request.ship_3_b
        placement_allowed = check_placement(position_ship_3_b,3)
        if not placement_allowed:
            raise endpoints.BadRequestException(
                    'Invalid placement! Your ship placement cannot be outside the board')

        ship3b = [position_ship_3_b + 10,
                  position_ship_3_b - 1,
                  position_ship_3_b,
                  position_ship_3_b - 10]


        position_ship_4_b = request.ship_4_b
        placement_allowed = check_placement(position_ship_4_b,4)
        if not placement_allowed:
            raise endpoints.BadRequestException(
                    'Invalid placement! Your ship placement cannot be outside the board')

        ship4b = [position_ship_4_b + 9,
                  position_ship_4_b - 1,
                  position_ship_4_b,
                  position_ship_4_b - 10]


        for i in ship1b:
            if i > 99 or i < 0:
                raise endpoints.BadRequestException(
                        'Invalid placement! Your part of the ship is outside the board')
            if i in ship2b or i in ship3b or i in ship4b:
                raise endpoints.BadRequestException(
                        'Invalid placement! Your ships overlap')
            game.user_b_shipsboard[i] = 'B1'
            SHIPSB.append(ship1b)


        
        for i in ship2b:
            if i > 99 or i < 0:
                raise endpoints.BadRequestException(
                        'Invalid placement! Your part of the ship is outside the board')
            if i in ship1b or i in ship4b or i in ship3b:
                raise endpoints.BadRequestException(
                        'Invalid placement! Your ships overlap')
            game.user_b_shipsboard[i] = 'B2'
            SHIPSB.append(ship2b)


        for i in ship3b:
            if i > 99 or i < 0:
                raise endpoints.BadRequestException(
                        'Invalid placement! Your part of the ship is outside the board')
            if i in ship1b or i in ship2b or i in ship4b:
                raise endpoints.BadRequestException(
                        'Invalid placement! Your ships overlap')
            game.user_b_shipsboard[i] = 'B3'
            SHIPSB.append(ship3b)
        

        for i in ship4b:
            if i > 99 or i < 0:
                raise endpoints.BadRequestException(
                        'Invalid placement! Your part of the ship is outside the board')
            if i in ship1b or i in ship2b or i in ship3b:
                raise endpoints.BadRequestException(
                        'Invalid placement! Your ships overlap')
            game.user_b_shipsboard[i] = 'B4'
            SHIPSB.append(ship4b)

        if game.game_start:
            raise endpoints.BadRequestException(
                    'Game already started! Can\'t change ships positions.')
        else:
            game.game_start = True
            game.put()
        return game.to_form()


    @endpoints.method(GET_USER_GAME_REQUEST, GameHistoryForm,
                      name='get_game_history',
                      path='game/{urlsafe_game_key}/{user_name}/history')
    def get_game_history(self, request):
        """Returns users games moves history"""
        game = get_by_urlsafe(request.urlsafe_game_key, Game)
        user = User.query(User.name == request.user_name).get()
        if not game:
            raise endpoints.NotFoundException('Game not found')
        if user.key != game.user_a and user.key != game.user_b:
            raise endpoints.BadRequestException('User is not in this game')
        if user.key == game.user_a:
            return GameHistoryForm(game_status='Game Over' if game.game_over else\
                                    'Active', winner=game.winner.get().name, \
                                    game_history=str(game.user_a_game_history))
        else:
            return GameHistoryForm(game_status='Game Over' if game.game_over else\
                                    'Active', winner=game.winner.get().name, \
                                    game_history=str(game.user_b_game_history))

    
    @endpoints.method(GET_GAME_REQUEST, StringMessage, name='cancel_game',
                      path='game/{urlsafe_game_key}', http_method='DELETE')
    def cancel_game(self, request):
        """Deletes a game"""
        game = get_by_urlsafe(request.urlsafe_game_key, Game)

        if game and game.game_over:
            raise endpoints.BadRequestException('Game is already over')
        elif game and not game.game_over:
            game.key.delete()
            return StringMessage(message='Game deleted!')
        else:
            raise endpoints.NotFoundException('Game not found')


    @endpoints.method(USER_REQUEST, GameForms, name='get_user_games',
                      path='user/games', http_method='GET')
    def get_user_games(self, request):
        """Returns users all active games"""
        user = User.query(User.name == request.user_name).get()
        if not user:
            raise endpoints.BadRequestException(
                    'User with that name does not exist!')
        games = Game.query(ndb.OR(Game.user_a == user.key,
                                 Game.user_b == user.key)).\
                    filter(Game.game_over == False)
        return GameForms(items=[game.to_form() for game in games])


    @endpoints.method(MAKE_MOVE_REQUEST, GameForm, name='make_move',
                      path='game/{urlsafe_game_key}/move', http_method='PUT')
    def make_move(self, request):
        """Make a move. Returns a game state"""
        game = get_by_urlsafe(request.urlsafe_game_key, Game)
        if not game:
            raise endpoints.NotFoundException('Game not found')
        if game.game_over:
            raise endpoints.NotFoundException('Game already over')

        user = User.query(User.name == request.user_name).get()
        if user.key != game.next_move:
            raise endpoints.BadRequestException('Its not your turn!')

        move = request.move
        if move < 0 or move > 99:
            raise endpoints.BadRequestException('Invalid move! Must be\
                        0 and 99')
        if not game.game_start:
            raise endpoints.BadRequestException('Place ships to start playing')

        global SHIPSA
        global SHIPSB

        shipsa_placements = [x for y in SHIPSA for x in y]
        shipsb_placements = [x for y in SHIPSB for x in y]

        if user.key == game.user_a:
            if game.user_a_playboard[move] != '':
                raise endpoints.BadRequestException('Invalid move!')

            if move in shipsb_placements:
                game.user_a_playboard[move] = 'O'
                game.user_a_game_history.append(('O', move))
            else:
                game.user_a_playboard[move] = 'X'
                game.user_a_game_history.append(('X', move))

            game.next_move = game.user_b

        else:
            if game.user_b_playboard[move] != '':
                raise endpoints.BadRequestException('Invalid move!')

            if move in shipsa_placements:
                game.user_b_playboard[move] = 'O'
                game.user_b_game_history.append(('O', move))
            else:
                game.user_b_playboard[move] = 'X'
                game.user_b_game_history.append(('X', move))

            game.next_move = game.user_a


        counta = 0
        countb = 0
        for x in range(100):
            if game.user_b_playboard[x] == 'O':
                countb += 1

        for x in range(100):
            if game.user_a_playboard[x] == 'O':
                counta += 1
        

        if countb == 16:
            winner = game.user_b
            loser = game.user_a
            game.end_game(winner)
        elif counta == 16:
            winner = game.user_a
            loser = game.user_b
            game.end_game(winner)
        else:
            taskqueue.add(url='/tasks/send_game_move_email',
                          params={'user_key': game.next_move.urlsafe(),
                                  'game_key': game.key.urlsafe()})

        game.put()
        return game.to_form()


    @endpoints.method(USER_REQUEST, ScoreForms, name='get_user_scores',
                      path='scores/user/{user_name}', http_method='GET')
    def get_user_scores(self, request):
        """Returns all of an individual User's scores"""
        user = User.query(User.name == request.user_name).get()
        if not user:
            raise endpoints.NotFoundException(
                    'A User with that name does not exist!')
        scores = Score.query(ndb.OR(Score.winner == user.key,
                                    Score.loser == user.key))
        return ScoreForms(items=[score.to_form() for score in scores])

    @endpoints.method(message_types.VoidMessage, ScoreForms, path='scores',
                      name='get_scores', http_method='GET')
    def get_scores(self, request):
        """Return all scores"""
        return ScoreForms(items=[score.to_form() for score in Score.query()])

    @endpoints.method(message_types.VoidMessage, UserForms, 
                      path='user/ranking', name='get_user_rankings',
                      http_method='GET')
    def get_user_rankings(self, request):
        """Return all Users ranked by their win percentage"""
        users = User.query(User.games_played > 0).fetch()
        users = sorted(users, key=lambda x: x.win_percentage, reverse=True)
        return UserForms(items=[user.to_form() for user in users])

    @endpoints.method(USER_REQUEST, UserForm, name='get_user',
                      path='user/{user_name}', http_method='GET')
    def get_user(self, request):
        """Returns User"""
        user = User.query(User.name == request.user_name).get()
        if not user:
            raise endpoints.NotFoundException('User not found')
        return user.to_form()


api = endpoints.api_server([BattleShipAPI])