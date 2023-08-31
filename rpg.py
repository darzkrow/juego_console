# Simple RPG Game
# Autor: 
# Post: https://balau82.wordpress.com/2010/06/28/simplest-rpg-game-in-python/

# Actualizacion del Codigo de python 2.x 3.x
# Franco Dev
import random



class Character:
    def __init__(self):
        self.name = ""
        self.health = 1
        self.health_max = 1
    
    def do_damage(self, enemy):
        damage = min(
            max(random.randint(0, self.health) - random.randint(0, enemy.health), 0),
            enemy.health)
        enemy.health = enemy.health - damage
        if damage == 0:
            print(f"{enemy.name} evades {self.name}'s attack.")
        else:
            print(f"{self.name} hurts {enemy.name}!")
        return enemy.health <= 0

class Enemy(Character):
    def __init__(self, player):
        super().__init__()
        self.name = 'a goblin'
        self.health = random.randint(1, player.health)

class Player(Character):
    def __init__(self):
        super().__init__()
        self.state = 'normal'
        self.health = 10
        self.health_max = 10
    
    def quit(self):
        print(f"{self.name} can't find the way back home, and dies of starvation.\nR.I.P.")
        self.health = 0
    
    def help(self):
        print(list(Commands.keys()))
    
    def status(self):
        print(f"{self.name}'s health: {self.health}/{self.health_max}")
    
    def tired(self):
        print(f"{self.name} feels tired.")
        self.health = max(1, self.health - 1)
    
    def rest(self):
        if self.state != 'normal':
            print(f"{self.name} can't rest now!")
            self.enemy_attacks()
        else:
            print(f"{self.name} rests.")
            if random.randint(0, 1):
                self.enemy = Enemy(self)
                print(f"{self.name} is rudely awakened by {self.enemy.name}!")
                self.state = 'fight'
                self.enemy_attacks()
            else:
                if self.health < self.health_max:
                    self.health = self.health + 1
                else:
                    print(f"{self.name} slept too much.")
                    self.health = self.health - 1
    
    def explore(self):
        if self.state != 'normal':
            print(f"{self.name} is too busy right now!")
            self.enemy_attacks()
        else:
            print(f"{self.name} explores a twisty passage.")
            if random.randint(0, 1):
                self.enemy = Enemy(self)
                print(f"{self.name} encounters {self.enemy.name}!")
                self.state = 'fight'
            else:
                if random.randint(0, 1):
                    self.tired()
    
    def flee(self):
        if self.state != 'fight':
            print(f"{self.name} runs in circles for a while.")
            self.tired()
        else:
            if random.randint(1, self.health + 5) > random.randint(1, self.enemy.health):
                print(f"{self.name} flees from {self.enemy.name}.")
                self.enemy = None
                self.state = 'normal'
            else:
                print(f"{self.name} couldn't escape from {self.enemy.name}!")
                self.enemy_attacks()
    
    def attack(self):
        if self.state != 'fight':
            print(f"{self.name} swats the air, without notable results.")
            self.tired()
        else:
            if self.do_damage(self.enemy):
                print(f"{self.name} executes {self.enemy.name}!")
                self.enemy = None
                self.state = 'normal'
                if random.randint(0, self.health) < 10:
                    self.health = self.health + 1
                    self.health_max = self.health_max + 1
                    print(f"{self.name} feels stronger!")
            else:
                self.enemy_attacks()
    
    def enemy_attacks(self):
        if self.enemy.do_damage(self):
            print(f"{self.name} was slaughtered by {self.enemy.name}!!!\nR.I.P.")

Commands = {
    'quit': Player.quit,
    'help': Player.help,
    'status': Player.status,
    'rest': Player.rest,
    'explore': Player.explore,
    'flee': Player.flee,
    'attack': Player.attack,
}

p = Player()
p.name = input("What is your character's name? ")
print("(type help to get a list of actions)\n")
print(f"{p.name} enters a dark cave, searching for adventure.")

while p.health > 0:
    line = input("> ")
    args = line.split()
    if len(args) > 0:
        commandFound = False
        for c in Commands.keys():
            if args[0] == c[:len(args[0])]:
                Commands[c](p)
                commandFound = True
                break
        if not commandFound:
            print(f"{p.name} doesn't understand the suggestion.")
