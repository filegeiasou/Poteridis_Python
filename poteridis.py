import random 
import os
from queue import Queue
import keyboard as kb

class Map:
    def __init__(self):
        self.map = ["*****************",
                    "*...*.....*.....*",
                    "*....*.......*..*",
                    "*...*...*..*....*",
                    "*......*....*...*",
                    "*...*...........*",
                    "*...****.*...*..*",
                    "*...*.....*.....*",
                    "*****************"]
    
    def pr_map(self):
        for row in self.map:
            print(row)
    
    def print_map(self, px, py, dx, dy, bx, by):
        os.system('cls')
        map_list = [list(row) for row in self.map]
        if map_list[px][py]  == '*':
            return
        if map_list[dx][dy]  == '*':
            return
        if map_list[bx][by]  == '*':
            return
        if(px,py) == (bx,by):
            map_list[px][py] = 'M'
        else:
            map_list[px][py] = 'P'
            map_list[bx][by] = 'B'
        map_list[dx][dy] = '$'
        for row in map_list:
            print("".join(row))

class Player:
    def __init__(self, game_map):
        x = random.randint(1,8)
        y = random.randint(1,16)
        while game_map[x][y] == '*':
            x = random.randint(1,8)
            y = random.randint(1,16)
        self.x = x
        self.y = y

    def move(self, move, game_map):
        if move == 'w' and game_map[self.x - 1][self.y] != '*':
            self.x -= 1
        elif move == 's' and game_map[self.x + 1][self.y] != '*':
            self.x += 1
        elif move == 'a' and game_map[self.x][self.y - 1] != '*':
            self.y -= 1
        elif move == 'd' and game_map[self.x][self.y + 1] != '*':
            self.y += 1

class Bot:
    def __init__(self, diamond, game_map):
        self.x = random.randint(1, 8)
        self.y = random.randint(1, 16)
        while game_map[self.x][self.y] == '*':
            self.x = random.randint(1,8)
            self.y = random.randint(1,16)
        self.diamond = diamond
        self.path = []

    def move(self, game_map, diamond_x, diamond_y):
        if not self.path:
            self.path = self.bfs(game_map, self.x, self.y, diamond_x, diamond_y)

        if self.path:
            next_x, next_y = self.path.pop(0)
            self.x = next_x
            self.y = next_y

    def bfs(self, game_map, start_x, start_y, end_x, end_y):
        visited = [[False for _ in range(17)] for _ in range(9)]
        queue = Queue()
        queue.put((start_x, start_y, []))

        while not queue.empty():
            current_x, current_y, path = queue.get()
            visited[current_x][current_y] = True

            if (current_x, current_y) == (end_x, end_y):
                return path

            for dx, dy in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                next_x, next_y = current_x + dx, current_y + dy

                if 1 <= next_x <= 8 and 1 <= next_y <= 16 and not visited[next_x][next_y] and game_map[next_x][next_y] != '*':
                    new_path = path + [(next_x, next_y)]
                    queue.put((next_x, next_y, new_path))

        return []

class Diamond:
    def __init__(self,game_map):
        x = random.randint(1,8)
        y = random.randint(1,16)
        while game_map[x][y] == '*':
            x = random.randint(1,8)
            y = random.randint(1,16)
        self.x = x
        self.y = y

def main():
    map = Map()
    player = Player(map.map)
    diamond = Diamond(map.map)
    bot = Bot(diamond,map.map)
    map.print_map(player.x, player.y, diamond.x, diamond.y, bot.x, bot.y)

    while True:
        #move = input("select move:")
        move = None
        while move is None:
            key = kb.read_key()
            if key in ['w', 'a', 's', 'd', 'q']:
                move = key

            while kb.is_pressed(key):
                pass

        if move == 'q':
            break
        player.move(move, map.map)
        bot.move(map.map , diamond.x, diamond.y)
        map.print_map(player.x, player.y, diamond.x, diamond.y, bot.x, bot.y)
        if (player.x, player.y) == (diamond.x, diamond.y):
            os.system('cls')
            print("You won!!")
            break
        if (bot.x, bot.y) == (diamond.x, diamond.y):
            os.system('cls')
            print("Bot won!!")
            break

if __name__ == "__main__":
    main()
