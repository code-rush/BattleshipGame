import endpoints
from google.appengine.ext import ndb

def get_by_urlsafe(urlsafe, model):
    try:
        key = ndb.Key(urlsafe=urlsafe)
    except TypeError:
        raise endpoints.BadRequestException('Invalid Key')
    except Exception, e:
        if e.__class__.__name__ == 'ProtocolBufferDecodeError':
            raise endpoints.BadRequestException('Invalid Key')
        else:
            raise

    entity = key.get()
    if not entity:
        return None
    if not isinstance(entity, model):
        raise ValueError('Incorrect Kind')
    return entity
    

def check_full_ship_revealed(board, ship):
    """Returns true if a ship is revealed"""
    for cells in ship:
        if not cells in board:
            return False
        return True

def check_winner(playboard_a, playboard_b, shipsboard_a,
                 shipsboard_b, user_a, user_b):
    """Checks and returns winner if the player has hit all opponents ships"""
    if playboard_a and shipsboard_b == shipsboard_b:
        return user_a
    if playboard_b and shipsboard_a == shipsboard_a:
        return user_b
        