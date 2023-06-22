# Sea battle - backend


This project is a backend part of a global project called "Sea battle".

The subject area of ​​this project is the Sea Battle game. It is implemented by pressing mouse keys (placement of ships, 
shots at enemy ships, successful hits are fixed in red).

One game can be played by 2 users or a user and a computer. The computer will have several levels of difficulty.

The rules of the game are as follows: in a 10x10 field, the players or the player and the computer place their ships
(ships must not lie on top of each other, stand side by side, intersect) on their playing fields. The number of ships 
is 10, namely: one four-deck (one deck corresponds to one cell playing field), two three-deck, three two-deck and four 
single-deck. After arrangement ships, the players or the player and the computer alternately "shoot" at the cells of 
the opponent's playing field. If any of them managed to get into an enemy ship, then, according to the rules, the turn 
does not pass to the enemy (if the player hit the enemy ship, then he has the right to take one more shot) to next miss. 
Victory goes to the one who first destroys all enemy ships, with the loss connection will not have time to switch, will 
not make a move in the allotted time, or will want to give up. Each move is given a certain amount of time.


Project tested with: APITestCase, APITransactionTestCase, WebsocketCommunicator, pytest. 
Coverage of the project with tests - 99%.

### Launch of the project

#### 1) Clone repositories
```
git clone https://github.com/Lanterman/seabattle_backend.git
git clone https://github.com/Lanterman/seabattle_frontend.git
```
#### 2) Create and run docker-compose
```
docker-compose up --build
```
#### 3) Follow the link in the browser:
 - ##### to launch the swagger openapi:
    ```
    http://0.0.0.0:8000/swagger/
    ```
 - ##### to launch the drf openapi:
    ```
    http://0.0.0.0:8000/api/v1/
    ```
 - ##### to launch the project:
    ```
    http://localhost:3000/
    ```

Future versions of the project will include:
 - advanced authentication with JWT tokens, using third-party applications (gmai, GitHub, etc.);
 - the ability to play with bots (bots will have several difficulty levels, bots write random messages to the chat 
at certain events);
 - a diagram of move options, which depicts options for players;
 - game history.
