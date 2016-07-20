import endpoints
from protorpc import remote, messages, message_types
from google.appengine.ext import ndb
from models import User, Game
from models import UserForm, GameForm, UserForms, GameForms, PlaceShipsForm
from models import StringMessage, MakeMoveForm, NewGameForm
from utils import get_by_urlsafe, check_full_ship_revealed, check_winner


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


SHIP1A = []
SHIP2A = []
SHIP3A = []
SHIP4A = []
SHIP1B = []
SHIP2B = []
SHIP3B = []
SHIP4B = []


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


        position_ship_1_a = request.ship_1_a
        if position_ship_1_a < 0 or position_ship_1_a > 99:
            raise endpoints.BadRequestException(
                    'Invalid placement! Your ship placement cannot be outside the board')
        SHIP1A = [position_ship_1_a + 20,
                  position_ship_1_a + 10,
                  position_ship_1_a,
                  position_ship_1_a - 10,
                  position_ship_1_a - 20]

        for i in SHIP1A:
            if i > 99 or i < 0:
                raise endpoints.BadRequestException(
                        'Invalid placement! Your part of the ship is outside the board')
            if i in SHIP4A or i in SHIP2A or i in SHIP3A:
                raise endpoints.BadRequestException(
                        'Invalid placement! Your ships overlap')
            game.user_a_shipsboard[i] = 'A1'


        position_ship_2_a = request.ship_2_a
        if position_ship_2_a < 0 or position_ship_2_a > 99:
            raise endpoints.BadRequestException(
                    'Invalid placement! Your ship placement cannot be outside the board')

        SHIP2A = [position_ship_2_a - 1,
                  position_ship_2_a,
                  position_ship_2_a + 1]

        for i in SHIP2A:
            if i > 99 or i < 0:
                raise endpoints.BadRequestException(
                        'Invalid placement! Your part of the ship is outside the board')
            if i in SHIP1A or i in SHIP4A or i in SHIP3A:
                raise endpoints.BadRequestException(
                        'Invalid placement! Your ships overlap')
            game.user_a_shipsboard[i] = 'A2'


        position_ship_3_a = request.ship_3_a
        if position_ship_3_a < 0 or position_ship_3_a > 99:
            raise endpoints.BadRequestException(
                    'Invalid placement! Your ship placement cannot be outside the board')

        SHIP3A = [position_ship_3_a + 10,
                  position_ship_3_a - 1,
                  position_ship_3_a,
                  position_ship_3_a - 10]

        ships_position_check = [0,10,20,30,40,50,60,70,80,90]

        for i in SHIP3A:
            if i in ships_position_check:
                raise endpoints.BadRequestException(
                        'Invalid placement! Your part of the ship is outside the board')
            if i in SHIP1A or i in SHIP2A or i in SHIP4A:
                raise endpoints.BadRequestException(
                        'Invalid placement! Your ships overlap')
            game.user_a_shipsboard[i] = 'A3'


        position_ship_4_a = request.ship_4_a
        if position_ship_4_a < 0 or position_ship_4_a > 99:
            raise endpoints.BadRequestException(
                    'Invalid placement! Your ship placement cannot be outside the board')

        SHIP4A = [position_ship_4_a + 19,
                  position_ship_4_a - 1,
                  position_ship_4_a,
                  position_ship_4_a - 10]

        for i in SHIP4A:
            if i in ships_position_check:
                raise endpoints.BadRequestException(
                        'Invalid placement! Your part of the ship is outside the board')
            if i in SHIP1A or i in SHIP2A or i in SHIP3A:
                raise endpoints.BadRequestException(
                        'Invalid placement! Your ships overlap')
            game.user_a_shipsboard[i] = 'A4'



        position_ship_1_b = request.ship_1_b
        if position_ship_1_b < 0 or position_ship_1_b > 99:
            raise endpoints.BadRequestException(
                    'Invalid placement! Your ship placement cannot be outside the board')
        SHIP1A = [position_ship_1_b + 20,
                  position_ship_1_b + 10,
                  position_ship_1_b,
                  position_ship_1_b - 10,
                  position_ship_1_b - 20]

        for i in SHIP1B:
            if i > 99 or i < 0:
                raise endpoints.BadRequestException(
                        'Invalid placement! Your part of the ship is outside the board')
            if i in SHIP3B or i in SHIP2B or i in SHIP4B:
                raise endpoints.BadRequestException(
                        'Invalid placement! Your ships overlap')
            game.user_b_shipsboard[i] = 'B1'

        position_ship_2_b = request.ship_2_b
        if position_ship_2_b < 0 or position_ship_2_b > 99:
            raise endpoints.BadRequestException(
                    'Invalid placement! Your ship placement cannot be outside the board')

        SHIP2B = [position_ship_2_b - 1,
                  position_ship_2_b,
                  position_ship_2_b + 1]

        for i in SHIP2B:
            if i > 99 or i < 0:
                raise endpoints.BadRequestException(
                        'Invalid placement! Your part of the ship is outside the board')
            if i in SHIP1B or i in SHIP3B or i in SHIP4B:
                raise endpoints.BadRequestException(
                        'Invalid placement! Your ships overlap')
            game.user_b_shipsboard[i] = 'B2'


        position_ship_3_b = request.ship_3_b
        if position_ship_3_b < 0 or position_ship_3_b > 99:
            raise endpoints.BadRequestException(
                    'Invalid placement! Your ship placement cannot be outside the board')

        SHIP3B = [position_ship_3_b + 10,
                  position_ship_3_b - 1,
                  position_ship_3_b,
                  position_ship_3_b - 10]

        for i in SHIP3B:
            if i in ships_position_check and i not in SHIP1B and i not in SHIP3B and i not in SHIP4B:
                raise endpoints.BadRequestException(
                        'Invalid placement! Your part of the ship is outside the board')
            if i in SHIP1B or i in SHIP2B or i in SHIP4B:
                raise endpoints.BadRequestException(
                        'Invalid placement! Your ships overlap')
            game.user_b_shipsboard[i] = 'B3'


        position_ship_4_b = request.ship_4_b
        if position_ship_4_b < 0 or position_ship_4_b > 99:
            raise endpoints.BadRequestException(
                    'Invalid placement! Your ship placement cannot be outside the board')

        SHIP4B = [position_ship_4_b + 19,
                  position_ship_4_b - 1,
                  position_ship_4_b,
                  position_ship_4_b - 10]

        for i in SHIP4B:
            if i in ships_position_check:
                raise endpoints.BadRequestException(
                        'Invalid placement! Your part of the ship is outside the board')
            if i in SHIP1B or i in SHIP2B or i in SHIP2B:
                raise endpoints.BadRequestException(
                        'Invalid placement! Your ships overlap')
            game.user_b_shipsboard[i] = 'B4'

        
        game.put()
        return game.to_form()


    @endpoints.method(GET_USER_GAME_REQUEST, StringMessage,
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
            return StringMessage(message=str(game.user_a_playboard))
        else:
            return StringMessage(message=str(game.user_b_playboard))

    
    @endpoints.method(GET_GAME_REQUEST, StringMessage, name='cancel_game',
                      path='game/{urlsafe_game_key}', http_method='POST')
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
                      path='game/{urlsafe_game_key}/move', http_method='POST')
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

        if user.key == game.user_a:
            if game.user_a_playboard[move] != '':
                raise endpoints.BadRequestException('Invalid move!')

            if move in SHIP1B or move in SHIP2B or move in SHIP3B or move in SHIP4B:
                game.user_a_playboard[move] = 'O'
            else:
                game.user_a_playboard[move] = 'X'

            ship1_revealed = check_full_ship_revealed(user_a_playboard, SHIP1B)
            ship2_revealed = check_full_ship_revealed(user_a_playboard, SHIP2B)
            ship3_revealed = check_full_ship_revealed(user_a_playboard, SHIP3B)
            ship4_revealed = check_full_ship_revealed(user_a_playboard, SHIP4B)

            if ship1_revealed:
                for i in SHIP1B:
                    game.user_a_playboard[i] = "B1"

            if ship2_revealed:
                for i in SHIP2B:
                    game.user_a_playboard[i] = "B2"

            if ship3_revealed:
                for i in SHIP3B:
                    game.user_a_playboard[i] = "B3"

            if ship4_revealed:
                for i in SHIP4B:
                    game.user_a_playboard[i] = "B4"


        else:
            if game.user_b_playboard[move] != '':
                raise endpoints.BadRequestException('Invalid move!')

            if move in SHIP1A or move in SHIP2A or move in SHIP3A or move in SHIP4A:
                game.user_a_playboard[move] = 'O'
            else:
                game.user_a_playboard[move] = 'X'

            ship1_revealed = check_full_ship_revealed(user_b_playboard, SHIP1A)
            ship2_revealed = check_full_ship_revealed(user_b_playboard, SHIP2A)
            ship3_revealed = check_full_ship_revealed(user_b_playboard, SHIP3A)
            ship4_revealed = check_full_ship_revealed(user_b_playboard, SHIP4A)

            if ship1_revealed:
                for i in SHIP1A:
                    game.user_b_playboard[i] = "A1"

            if ship2_revealed:
                for i in SHIP2A:
                    game.user_b_playboard[i] = "A2"

            if ship3_revealed:
                for i in SHIP3A:
                    game.user_b_playboard[i] = "A3"

            if ship4_revealed:
                for i in SHIP4A:
                    game.user_b_playboard[i] = "A4"


        winner = check_winner(user_a_playboard, user_b_playboard, 
                              game.user_a_shipsboard, game.user_b_shipsboard,
                              game.user_a, game.user_b)
        if winner:
            game.end_game(winner)

        game.put()
        return game.to_form()


    @endpoints.method(message_types.VoidMessage, UserForms,
                      name='get_user_rankings', path='user/ranking',
                      http_method='GET')
    def get_user_rankings(self, request):
        """Returns all Users by their win percentage"""
        users = User.query(User.games_played > 0).fetch()
        users = sorted(users, key=lambda x: x.win_percentage, reverse=True)
        return UserForms(items=[user.to_form() for user in users])


api = endpoints.api_server([BattleShipAPI])