# BattleshipGame

## Setup Instructions:
1. Update the value of application in app.yaml to the app ID you have registered
	in the App Engine admin console and would like to use to host your instance of this sample.
2. Run the application on local host and ensure it's running by visiting the API Explorer:
	localhost:YOUR-SET-PORT/_ah/api/explorer.


##Game Description:
The board is represented as a 1-D list of squares with indexes as follows:
[90..........,100]
[80...........,89]
[70..............]
[60..............]
[50..............]
[40..............]
[30..............]
[20..............]
[10,11,12.....,19]
[0,1,2.........,9]

### Playing Instructions:
1. Create minimum two users using __create_user api__.
2. Create a new game with two users using __new_game api__.
3. Before starting to play, you need to place ships on boards of each user. Place ships using
	__place_ships__ api. Users need to be in the same order as while creating a new game.
	`a` and `b` indicates users whereas numbers indicates ships. To start playing, you need to
	place all four ships on board.
4. After placing ships, use __make_move__ api to play game. Enjoy!


##Files Included:
 - api.py: Contains endpoints and game playing logic.
 - app.yaml: App configuration.
 - cron.yaml: Cronjob configuration.
 - main.py: Handler for taskqueue handler.
 - models.py: Entity and message definitions including helper methods.
 - utils.py: Helper function for retrieving ndb.Models by urlsafe Key string.

##Endpoints Included:
 - **create_user**
    - Path: 'user'
    - Method: POST
    - Parameters: user_name
    - Returns: Message confirming creation of the User.
    - Description: Creates a new User. user_name provided must be unique. Will 
    raise a ConflictException if a User with that user_name already exists.
    
 - **new_game**
    - Path: 'game'
    - Method: POST
    - Parameters: user_a, user_b
    - Returns: GameForm with initial game state.
    - Description: Creates a new Game between two users `user_a` and `user_b`.
     
 - **get_game**
    - Path: 'game/{urlsafe_game_key}'
    - Method: GET
    - Parameters: urlsafe_game_key
    - Returns: GameForm with current game state.
    - Description: Returns the current state of a game.
    
 - **place_ships_on_board**
 	- Path: 'game/{urlsafe_game_key}/place_ships'
 	- Method: POST
 	- Parameters: user_a, ship_1_a, ship_2_a, ship_3_a, ship_4_a, user_b, ship_1_b,
 	 ship_2_b, ship_3_b, ship_4_b
 	- Returns: GameForm with current game state with ships placed on both boards.
 	- Description: Places ships on boards of both users to be played on and 
 	returns current game state. A number to place the ship should be between
 	0 - 99.

 - **make_move**
    - Path: 'game/{urlsafe_game_key}/move'
    - Method: POST
    - Parameters: urlsafe_game_key, user_name, move
    - Returns: GameForm with new game state.
    - Description: Accepts a move and returns the updated state of the game.
    A move is a number from 0 - 99 corresponding to one of the 100 possible
    positions on the board.
    If this causes a game to end, the game will be deleted.

 - **get_user_games**
    - Path: 'user/games'
    - Method: GET
    - Parameters: user_name
    - Returns: GameForms with 1 or more GameForm inside.
    - Description: Returns the current state of all the User's active games.
    
 - **cancel_game**
    - Path: 'game/{urlsafe_game_key}'
    - Method: DELETE
    - Parameters: urlsafe_game_key
    - Returns: StringMessage confirming deletion
    - Description: Deletes the game. If the game is already completed an error
    will be thrown.
    
 - **get_user_rankings**
    - Path: 'user/ranking'
    - Method: GET
    - Parameters: None
    - Returns: UserForms
    - Description: Rank all players that have played at least one game by their
    winning percentage and return.

 - **get_game_history**
    - Path: 'game/{urlsafe_game_key}/{user_name}/history'
    - Method: GET
    - Parameters: urlsafe_game_key
    - Returns: StringMessage containing history
    - Description: Returns current state of users playboard.


##Models Included:
 - **User**
    - Stores unique user_name and email address.
    - Also keeps track of wins and games_played.
    
 - **Game**
    - Stores unique game states. Associated with User models via KeyProperties
    user_a and user_b.
    
##Forms Included:
 - **GameForm**
    - Representation of a Game's state (urlsafe_key, user_a_shipsboard, 
    user_b_shipsboard, user_a, user_b, game_over, winner, user_a_playboard,
    user_b_playboard, next_move).
 - **NewGameForm**
    - Used to create a new game (user_a, user_b)
 - **MakeMoveForm**
    - Inbound make move form (user_name, move).
 - **UserForm**
    - Representation of User. Includes winning percentage
 - **UserForms**
    - Container for one or more UserForm.
 - **StringMessage**
    - General purpose String container.
    
    
##Design Decisions
- Added next_move, user_a, user_b, winner and game_over fields. I used game_over
  flag to mark completed games and other fields as KeyProperty to the Game.
- Added four fields to store board in Game(two for placing ships and two to play on).
  I used PickleProperty to store the board.

I could not think of a solution to change ships rotations. The ships designs 
are hardcoded and can only be placed as they are without any rotation. Also checking if each ships
is revealed by opponents making it visible for the player to be able to see that the player 
has got the hit correctly. I think that this game would be easier to design on the front-end
than the backend since most of it has to be hardcoded. It seems to be working perfectly for 
now although with some limitations, but it was fun solving some problems.