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
