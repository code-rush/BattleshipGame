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

### Ship Placements:
- Ship placements are static, there is no rotation applied to them. 
- Ships cannot overlap with each other.
- A part of the ship cannot be outside the board.

If you can't place ships. Read through below instructions on how the
ships are designed and do calculations taking board into consideration 
to get the answers.

There are four types of ships:
1) Vertical Ship: Takes five cell placements vertically, mid point as the center

    [center + 20]
    [center + 10]
    [  center   ]
    [center - 10]
    [center - 20]

2) Horizontal Ship: Takes three cell placements horizontally, mid point as the center

    [center - 1][center][center + 1]

3) T shape ship: Takes 4 cell placements.

                [center + 10]
    [center - 1][   center  ]
                [center - 10]

4) Number 4 shape ship: Takes four cell placements,

    [center + 9 ]
    [center - 1 ][  center   ]
                 [center - 10]

_Note:_ 2nd, 3rd and 4th ship will not be allowed to be placed at 0,10,20,30,40...100 positions 
beacuse if they are placed there, part of the ship will be outside the board.


### Playing Instructions:
1. Create minimum two users using __create_user__ endpoint.
2. Create a new game with two users using __new_game__ endpoint.
3. Before starting to play, you need to place ships on boards of each user. Place ships using
	__place_ships__ endpoint. Users need to be in the same order as while creating a new game.
	`a` and `b` indicates users whereas numbers indicates ships. To start playing, you need to
	place all four ships on board.
4. After placing ships, use __make_move__ endpoint to play game. 
5. When you place a move, 'O' will be used to show if you hit the ship else 'X' will be showed.

__Note:__ Total there are four boards. There are two boards to place ships and two boards to play. 
The user who places ships on their ships board is being played by the opponent.

Enjoy!


## Score Counts:
Score is stored as win percentage which is calculated per user on their wins divided by
total number of games played. The Users are ranked by the win percentage in descending order.


##Files Included:
 - api.py: Contains endpoints and game playing logic.
 - app.yaml: App configuration.
 - cron.yaml: Cronjob configuration.
 - main.py: Handler for taskqueue handler.
 - models.py: Entity and message definitions including helper methods.
 - utils.py: Helper function for retrieving ndb.Models by urlsafe Key string.

##Models Included:
 - **User**
    - Stores unique user_name and email address.
    - Also keeps track of wins and games_played.
    
 - **Game**
    - Stores unique game states. Associated with User models via KeyProperties
    user_a and user_b.

 - **Score**
    - Records completed games. Associated with Users model via KeyProperty as
    well.

    
##Forms Included:
 - **GameForm**
    - Representation of a Game's state (urlsafe_key, user_a_shipsboard, 
    user_b_shipsboard, user_a, user_b, game_over, winner, user_a_playboard,
    user_b_playboard, next_move).
 - **NewGameForm**
    - Used to create a new game (user_a, user_b)
 - **MakeMoveForm**
    - Inbound make move form (user_name, move).
 - **PlaceShipsForm**
    - Used to place ships on users ships board.
 - **ScoreForm**
    - Representation of a completed game's Score (date, winner, loser).
 - **ScoreForms**
    - Multiple ScoreForm container.
 - **UserForm**
    - Representation of User. Includes winning percentage
 - **UserForms**
    - Container for one or more UserForm.
 - **StringMessage**
    - General purpose String container.


##Endpoints Included:
 - **create_user**
    - Path: 'user'
    - Method: POST
    - Parameters: user_name, email
    - Returns: Message confirming creation of the User.
    - Description: Creates a new User. user_name provided must be unique. Will 
    raise a ConflictException if a User with that user_name already exists.
    email is required.
    
 - **new_game**
    - Path: 'game'
    - Method: POST
    - Parameters: user_a, user_b
    - Returns: GameForm with initial game state.
    - Description: Creates a new Game between two users `user_a` and `user_b`.

 - **get_scores**
    - Path: 'scores'
    - Method: GET
    - Parameters: None
    - Returns: ScoreForms.
    - Description: Returns all Scores in the database (unordered).
    
 - **get_user_scores**
    - Path: 'scores/user/{user_name}'
    - Method: GET
    - Parameters: user_name
    - Returns: ScoreForms. 
    - Description: Returns all Scores recorded by the provided player (unordered).
    Will raise a NotFoundException if the User does not exist.

 - **get_game**
    - Path: 'game/{urlsafe_game_key}'
    - Method: GET
    - Parameters: urlsafe_game_key
    - Returns: GameForm with current game state.
    - Description: Returns the current state of a game.
    
 - **place_ships**
 	- Path: 'game/{urlsafe_game_key}/place_ships'
 	- Method: PUT
 	- Parameters: user_a, ship_1_a, ship_2_a, ship_3_a, ship_4_a, user_b, ship_1_b,
 	 ship_2_b, ship_3_b, ship_4_b
 	- Returns: GameForm with current game state with ships placed on both boards.
 	- Description: Places ships on boards of both users to be played on and 
 	returns current game state. A number to place the ship should be between
 	0 - 99.

 - **make_move**
    - Path: 'game/{urlsafe_game_key}/move'
    - Method: PUT
    - Parameters: urlsafe_game_key, user_name, move
    - Returns: GameForm with new game state.
    - Description: Accepts a move and returns the updated state of the game.
    A move is a number from 0 - 99 corresponding to one of the 100 possible tile
    positions on the board.
    If a move causes a game to end declaring a winner, the will be deleted.

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
    - Returns: GameHistoryForm containing history
    - Description: Returns history of moves the user made in the game with the 
    corresponding output, the current state of game and the winner if game 
    is completed.

- **get_user**
    - Path: 'user/{user_name}'
    - Method: GET
    - Parameters: user_name
    - Returns: UserForm with all user details
    - Description: Returns requested user with all user information and personal 
    win counts and total games played.
