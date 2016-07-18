import endpoints
from protorpc import remote, messages
from google.appengine.ext import ndb
from models import User, Game
from models import UserForm, GameForm, UserForms, GameForms
from models import StringMessage, MakeMoveForm, NewGameForm
from utils import get_by_urlsafe


NEW_GAME_REQUEST = endpoints.ResourceContainer(NewGameForm)
GET_GAME_REQUEST = endpoints.ResourceContainer(
       urlsafe_game_key=messages.StringField(1))
MAKE_MOVE_REQUEST = endpoints.ResourceContainer(MakeMoveForm,
       urlsafe_game_key=messages.StringField(1))
USER_REQUEST = endpoints.ResourceContainer(user_name=messages.StringField(1),
                                           email=messages.StringField(2))


@endpoints.api(name='battle_ship', version='v1')
class BattleShipAPI(remote.Service):
    """Game API"""
    @endpoints.method(USER_REQUEST, StringMessage, name='create_user',
                      path='user', http_method='POST')
    def create_user(self, request):
        """Creates a user"""
        if User.query(User.name == request.user_name).get():
            raise endpoints.ConflictException('A user with that name \
                    already exists!')
        user = User(name=request.user_name, email=request.email)
        user.put()
        return user

    @endpoints.method(GET_GAME_REQUEST, GameForm, name='get_game',
                      path='game/{urlsafe_game_key}', http_method='GET')
    def get_game(self, request):
        """Return the current game state"""
        game = get_by_urlsafe(request.urlsafe_game_key, Game)
        if game:
            return game.to_form()
        else:
            raise endpoints.NotFoundException('Game not found!')



api = endpoints.api_server([BattleShipAPI])