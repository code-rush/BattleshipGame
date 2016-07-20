import endpoints
from protorpc import remote, messages
from google.appengine.ext import ndb
from models import User, Game
from models import UserForm, GameForm, UserForms, GameForms, PlaceShipsForm
from models import StringMessage, MakeMoveForm, NewGameForm
from utils import get_by_urlsafe


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
                      http_method='POST')
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


        ship1a = []
        ship2a = []
        ship3a = []
        ship4a = []
        ship1b = []
        ship2b = []
        ship3b = []
        ship4b = []
        position_ship_1_a = request.ship_1_a
        if position_ship_1_a < 0 or position_ship_1_a > 99:
            raise endpoints.BadRequestException(
                    'Invalid placement! Your ship placement cannot be outside the board')
        ship1a = [position_ship_1_a + 20,
                  position_ship_1_a + 10,
                  position_ship_1_a,
                  position_ship_1_a - 10,
                  position_ship_1_a - 20]

        for i in ship1a:
            if i > 99 or i < 0:
                raise endpoints.BadRequestException(
                        'Invalid placement! Your part of the ship is outside the board')
            if i in ship4a or i in ship2a or i in ship3a:
                raise endpoints.BadRequestException(
                        'Invalid placement! Your ships overlap')
            game.user_a_board[i] = 'A1'


        position_ship_2_a = request.ship_2_a
        if position_ship_2_a < 0 or position_ship_2_a > 99:
            raise endpoints.BadRequestException(
                    'Invalid placement! Your ship placement cannot be outside the board')

        ship2a = [position_ship_2_a - 1,
                  position_ship_2_a,
                  position_ship_2_a + 1]

        for i in ship2a:
            if i > 99 or i < 0:
                raise endpoints.BadRequestException(
                        'Invalid placement! Your part of the ship is outside the board')
            if i in ship1a or i in ship4a or i in ship3a:
                raise endpoints.BadRequestException(
                        'Invalid placement! Your ships overlap')
            game.user_a_board[i] = 'A2'


        position_ship_3_a = request.ship_3_a
        if position_ship_3_a < 0 or position_ship_3_a > 99:
            raise endpoints.BadRequestException(
                    'Invalid placement! Your ship placement cannot be outside the board')

        ship3a = [position_ship_3_a + 10,
                  position_ship_3_a - 1,
                  position_ship_3_a,
                  position_ship_3_a - 10]

        ships_position_check = [0,10,20,30,40,50,60,70,80,90]

        for i in ship3a:
            if i in ships_position_check:
                raise endpoints.BadRequestException(
                        'Invalid placement! Your part of the ship is outside the board')
            if i in ship1a or i in ship2a or i in ship4a:
                raise endpoints.BadRequestException(
                        'Invalid placement! Your ships overlap')
            game.user_a_board[i] = 'A3'


        position_ship_4_a = request.ship_4_a
        if position_ship_4_a < 0 or position_ship_4_a > 99:
            raise endpoints.BadRequestException(
                    'Invalid placement! Your ship placement cannot be outside the board')

        ship4a = [position_ship_4_a + 19,
                  position_ship_4_a - 1,
                  position_ship_4_a,
                  position_ship_4_a - 10]

        for i in ship4a:
            if i in ships_position_check:
                raise endpoints.BadRequestException(
                        'Invalid placement! Your part of the ship is outside the board')
            if i in ship1a or i in ship2a or i in ship3a:
                raise endpoints.BadRequestException(
                        'Invalid placement! Your ships overlap')
            game.user_a_board[i] = 'A4'



        position_ship_1_b = request.ship_1_b
        if position_ship_1_b < 0 or position_ship_1_b > 99:
            raise endpoints.BadRequestException(
                    'Invalid placement! Your ship placement cannot be outside the board')
        ship1a = [position_ship_1_b + 20,
                  position_ship_1_b + 10,
                  position_ship_1_b,
                  position_ship_1_b - 10,
                  position_ship_1_b - 20]

        for i in ship1b:
            if i > 99 or i < 0:
                raise endpoints.BadRequestException(
                        'Invalid placement! Your part of the ship is outside the board')
            if i in ship3b or i in ship2b or i in ship4b:
                raise endpoints.BadRequestException(
                        'Invalid placement! Your ships overlap')
            game.user_b_board[i] = 'B1'

        position_ship_2_b = request.ship_2_b
        if position_ship_2_b < 0 or position_ship_2_b > 99:
            raise endpoints.BadRequestException(
                    'Invalid placement! Your ship placement cannot be outside the board')

        ship2b = [position_ship_2_b - 1,
                  position_ship_2_b,
                  position_ship_2_b + 1]

        for i in ship2b:
            if i > 99 or i < 0:
                raise endpoints.BadRequestException(
                        'Invalid placement! Your part of the ship is outside the board')
            if i in ship1b or i in ship3b or i in ship4b:
                raise endpoints.BadRequestException(
                        'Invalid placement! Your ships overlap')
            game.user_b_board[i] = 'B2'


        position_ship_3_b = request.ship_3_b
        if position_ship_3_b < 0 or position_ship_3_b > 99:
            raise endpoints.BadRequestException(
                    'Invalid placement! Your ship placement cannot be outside the board')

        ship3b = [position_ship_3_b + 10,
                  position_ship_3_b - 1,
                  position_ship_3_b,
                  position_ship_3_b - 10]

        for i in ship3b:
            if i in ships_position_check and i not in ship1b and i not in ship3b and i not in ship4b:
                raise endpoints.BadRequestException(
                        'Invalid placement! Your part of the ship is outside the board')
            if i in ship1b or i in ship2b or i in ship4b:
                raise endpoints.BadRequestException(
                        'Invalid placement! Your ships overlap')
            game.user_b_board[i] = 'B3'


        position_ship_4_b = request.ship_4_b
        if position_ship_4_b < 0 or position_ship_4_b > 99:
            raise endpoints.BadRequestException(
                    'Invalid placement! Your ship placement cannot be outside the board')

        ship4b = [position_ship_4_b + 19,
                  position_ship_4_b - 1,
                  position_ship_4_b,
                  position_ship_4_b - 10]

        for i in ship4b:
            if i in ships_position_check:
                raise endpoints.BadRequestException(
                        'Invalid placement! Your part of the ship is outside the board')
            if i in ship1b or i in ship2b or i in ship2b:
                raise endpoints.BadRequestException(
                        'Invalid placement! Your ships overlap')
            game.user_b_board[i] = 'B4'

        
        game.put()
        return game.to_form()


        @endpoints.method(GET_USER_GAME_REQUEST, StringMessage,
                          name='get_game_history',
                          path='game/{urlsafe_game_key}/{user}/history')
        def get_game_history(self, request):
            game = get_by_urlsafe(urlsafe_game_key, Game)
            user = User.query(User.name = request.user_name).get()
            if not game:
                raise endpoints.NotFoundException('Game not found')
            if user.key != game.user_a and user.key != game.user_b:
                raise endpoints.BadRequestException('User is not in this game')
            if user.key == game.user_a:
                return StringMessage(message=str(game.user_a_game_history))
            else:
                return StringMessage(message=str(game.user_b_game_history))



api = endpoints.api_server([BattleShipAPI])