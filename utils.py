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
    


def check_placement(ship_placement, ship_number):
    """Returns true if ship placed inside the board"""
    ships_position_check = [0,10,20,30,40,50,60,70,80,90]
    if ship_placement > 99 or ship_placement < 0:
            return False
    if ship_number in [2,3,4]:
        if ship_placement in ships_position_check:
            return False
    return True
