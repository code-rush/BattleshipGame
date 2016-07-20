import webapp2
from google.appengine.api import mail, app_identity
from google.appengine.ext import ndb
from api import BattleShipAPI
from utils import get_by_urlsafe

from models import User, Game


class SendReminderEmail(webapp2.RequestHandler):
	def get(self):
		users = User.query(User.email != None)

		for user in users:
			games = Games.query(ndb.OR(Game.user_a == user.key,
									   Game.user_b == user.key)).\
						  filter(Game.game_over == False)
			if games.count() > 0:
				subject = 'Reminder for active games'
				body = 'Hello {}, you have {} games active in progress.'\
						'Their keys are: {}'.format(user.name, games.count(),
								','.join(game.key.urlsafe() for game in games))

				mail.send_mail('noreply@{}.appspotmail.com'.format(
											app_identity.get_application_id()),
								user.email, subject, body)


class SendGameMoveMail(webapp2.RequestHandler):
	def post(self):
		user = get_by_urlsafe(self.request.get('user_key'), User)
		game = get_by_urlsafe(self.request.get('game_key'), Game)
		subject = 'Its your turn'
		body = 'Hello {}, its your turn now to play BattleShip Game. '\
				'The game key is: {}'.format(user.name, game.key.urlsafe())
		mail.send_mail('noreply@{}.appspotmail.com'.format(
									app_identity.get_application_id()),
						user.email, subject, body)


app = webapp2.WSGIApplication([
	('/crons/send_reminder', SendReminderEmail),
	('/tasks/send_game_move_email', SendGameMoveMail),
], debug=True)