from termcolor import colored
import random
import os
os.system('color')


class BoardOutException(Exception):
    msg = "Ups, board out..."


class AddShipException(Exception):
    pass


class UserInputException(Exception):
    msg = "Ups, you input wrong value, try again..."


class CheckMethods:
    @staticmethod
    def check_add_ship_to_board(board, ship):
        for dot in ship.dots():
            if board[dot.y][dot.x] != 0:
                raise AddShipException
# check left
            if dot.x != 0:
                if board[dot.y][dot.x - 1] != 0:
                    raise AddShipException
# check right
            if dot.x != len(board) - 1:
                if board[dot.y][dot.x + 1] != 0:
                    raise AddShipException
# check up
            if dot.y != 0:
                if board[dot.y - 1][dot.x] != 0:
                    raise AddShipException
# check down
            if dot.y != len(board) - 1:
                if board[dot.y + 1][dot.x] != 0:
                    raise AddShipException

# check up - left
            if dot.y != 0 and dot.x != 0:
                if board[dot.y - 1][dot.x - 1] != 0:
                    raise AddShipException

# check up - right
            if dot.y != 0 and dot.x != len(board[0]) - 1:
                if board[dot.y - 1][dot.x + 1] != 0:
                    raise AddShipException

# check down - left
            if dot.y != len(board) - 1 and dot.x != 0:
                if board[dot.y + 1][dot.x - 1] != 0:
                    raise AddShipException

# check down - right
            if dot.y != len(board) - 1 and dot.x != len(board[0]) - 1:
                if board[dot.y + 1][dot.x + 1] != 0:
                    raise AddShipException
        return True

    @staticmethod
    def check_dot_board_out(board, dot):
        if dot.x > len(board[0]) - 1:
            raise BoardOutException
        if dot.y > len(board) - 1:
            raise BoardOutException

    def check_shot(self, board, dot):
        self.check_dot_board_out(board, dot)
        if board[dot.y][dot.x] == 'T':
            raise BoardOutException
        if board[dot.y][dot.x] == 'X':
            raise BoardOutException

    def check_dot_wrong_input(self, x, y):
        if not isinstance(x, int):
            raise UserInputException

        if not isinstance(y, int):
            raise UserInputException


class Dot:
    helped_methods = CheckMethods()

    def __init__(self, x, y):
        self.helped_methods.check_dot_wrong_input(x, y)
        self.x = x
        self.y = y

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def __str__(self):
        return f"{self.x}, {self.y}"

    def __repr__(self):
        return f"({self.x}, {self.y})"


class Ship:
    HORIZONTAL = "H"
    VERTICAL = "V"

    def __init__(self, long, x, y, direction):
        self.long = long
        self.coord = Dot(x, y)
        self.direction = direction
        self.live = long

    def __str__(self):
        return f"{self.coord.x}, {self.coord.y}, {self.direction}"

    def dots(self):
        ship_dots = []
        if self.direction == self.VERTICAL:
            y = self.coord.y
            while y < self.coord.y + self.long:
                ship_dots.append(Dot(self.coord.x, y))
                y += 1
        else:
            x = self.coord.x
            while x < self.coord.x + self.long:
                ship_dots.append(Dot(x, self.coord.y))
                x += 1
        return ship_dots


class Board:
    SHIP_ICON = "■"
    helped_methods = CheckMethods()

    def __init__(self, hid):
        self.hid = hid
        self.board = [
            [0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0],
        ]
        self.ships = []
        self.live_ships = 7

    def add_ship(self, ship):
        self.helped_methods.check_add_ship_to_board(self.board, ship)
        for dot in ship.dots():
            self.board[dot.y][dot.x] = self.SHIP_ICON
        self.ships.append(ship)

    def show_board(self):
        horizontal = [ind for ind in range(1, len(self.board)+1)]
        if not self.hid:
            print('\nPlayer:\n')
        else:
            print('\nComputer:\n')
        print("   ", *horizontal)
        print("   ", "_" * len(horizontal)*2)
        for index, row in enumerate(self.board):
            for ind, col in enumerate(row):
                end = "\n" if ind == len(row) -1 else ""
                text = f"{index+1} |" if ind == 0 else ""
                if col == self.SHIP_ICON and self.hid:
                    print(text, 0, end=end)
                elif col == self.SHIP_ICON:
                    print(text, colored(str(col), 'green'), end=end)
                elif col == 'T':
                    print(text, colored(str(col), 'grey'), end=end)
                elif col == 'X':
                    print(text, colored(str(col), 'red'), end=end)
                else:
                    print(text, col, end=end)

    def out(self, dot):
        try:
            self.helped_methods.check_dot_board_out(self.board, dot)
            return False
        except BoardOutException:
            return True

    def shot(self, dot):
        self.helped_methods.check_shot(self.board, dot)
        if self.board[dot.y][dot.x] == self.SHIP_ICON:
            self.board[dot.y][dot.x] = 'X'
            return True
        else:
            self.board[dot.y][dot.x] = 'T'
            return False

    def search_ship(self, dot):
        for ship in self.ships:
            if dot in ship.dots():
                return ship
        return False


class Player:
    self_board = None
    enemy_board = None

    def ask(self):
        return NotImplementedError("method ask must be implemented")

    def move(self):
        dot = self.ask()
        try:
            if self.enemy_board.shot(dot):
                ship = self.enemy_board.search_ship(dot)
                if ship:
                    ship.live -= 1
                    if not ship.live:
                        self.enemy_board.ships.remove(ship)
                        self.enemy_board.live_ships -= 1
                        if not self.enemy_board.live_ships:
                            return True
                self.enemy_board.show_board()
                self.move()
        except BoardOutException:
            self.move()


class Ai(Player):

    def ask(self):
        x = random.randint(0, len(self.enemy_board.board[0])-1)
        y = random.randint(0, len(self.enemy_board.board)-1)
        return Dot(x, y)


class User(Player):

    def ask(self):
        try:
            x = int(input('Input x coord: '))
            y = int(input('Input y coord: '))
            return Dot(x-1, y-1)
        except ValueError:
            self.ask()
        except UserInputException:
            self.ask()


class Game:
    LOGO = """
         _______  _______  _______       ______   _______ __________________ _        _______ 
        (  ____ \(  ____ \(  ___  )     (  ___ \ (  ___  )\__   __/\__   __/( \      (  ____ \\
        | (    \/| (    \/| (   ) |     | (   ) )| (   ) |   ) (      ) (   | (      | (    \/
        | (_____ | (__    | (___) |     | (__/ / | (___) |   | |      | |   | |      | (__    
        (_____  )|  __)   |  ___  |     |  __ (  |  ___  |   | |      | |   | |      |  __)   
              ) || (      | (   ) |     | (  \ \ | (   ) |   | |      | |   | |      | (      
        /\____) || (____/\| )   ( |     | )___) )| )   ( |   | |      | |   | (____/\| (____/\\
        \_______)(_______/|/     \|     |/ \___/ |/     \|   )_(      )_(   (_______/(_______/                                                                           
     """

    def __init__(self):
        self.player = User()
        self.computer = Ai()
        print("Generate board for player...")
        self.player.self_board = self.random_board(False)
        print("Generate board for computer...")
        self.computer.self_board = self.random_board(True)

        self.player.enemy_board, self.computer.enemy_board = self.computer.self_board, self.player.self_board

    def random_board(self, hid):
        b = Board(hid)
        long_ships = [3, 2, 2, 1, 1, 1, 1]
        for long in long_ships:
            trying = 0
            while trying < 1000:
                ship = self.get_random_ship(long, len(b.board), len(b.board[0]))
                try:
                    b.add_ship(ship)
                    break
                except BoardOutException:
                    trying += 1
                    continue
                except AddShipException:
                    trying += 1
                    continue
                except IndexError:
                    trying += 1
                    continue
            if trying == 1000:
                self.random_board(hid)
        if len(b.ships) != len(long_ships):
            self.random_board(hid)
        else:
            return b

    @staticmethod
    def get_random_ship(long, height_board, width_board):
        x = random.randint(0, width_board-1)
        y = random.randint(0, height_board-1)
        direction = random.choice([Ship.HORIZONTAL, Ship.VERTICAL])
        return Ship(long, x, y, direction)

    def greet(self):
        print(self.LOGO)
        print("\n\n")
        print("Rules: first enter X coord (horizontal), second enter Y coord (vertical)")

    def loop(self):
        while True:
            self.player.self_board.show_board()
            self.computer.self_board.show_board()
            if not self.computer.self_board.live_ships:
                print('Players winner!')
                break
            if not self.player.self_board.live_ships:
                print('Computer winner...')
                break
            print("Please, your turn...")
            self.player.move()
            print("Enemy turn...")
            self.computer.move()

    def start(self):
        self.greet()
        self.loop()


game = Game()
game.start()
