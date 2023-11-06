import tkinter as tk
from tkinter import Canvas, PhotoImage, ttk
from tkinter import messagebox
from PIL import ImageTk, Image
from functools import partial
import time
import os
from random import randint, choice
from tabulate import tabulate

# GAME_TITLE
GAME_TITLE = "COMBAT GAME"
DEFAULT_FONT = ('Arial', 18)

DEFAULT_WIDTH = 1200
DEFAULT_HEIGHT = 700
MENU_FRAME_WIDTH = 300
MAIN_FRAME_WIDTH = 900
OFFSET = 100
BTN_WIDTH = 25

MENU_BUTTON_X = MENU_FRAME_WIDTH // 4
MENU_BUTTON_Y = DEFAULT_HEIGHT // 3
MENU_BUTTON_WIDTH = 25
MENU_BUTTON_HEIGHT = 10
COLOR_BLACK = 'black'
COLOR_WHITE = 'white'

MENU_OPTION_CHOOSE = 'Choose Character'
MENU_OPTION_START = 'Start Game'
MENU_OPTION_SETTINGS = 'Settings'
MENU_OPTION_EXIT = 'Exit'

MAIN_FRAME_BG = '#D4D4D4'

CHARACTER_PROFILE_DIMENSIONS = 200

# Constant values for padding.
PAD = 25
TRIPLE_PAD_SIZE = 3
STAR_PAD_SIGN = '*'
UNDERSCORE_PAD_SIGN = '_'

DIFFICULTY_EASY = 'easy'
DIFFICULTY_MEDIUM ='medium'
DIFFICULTY_HARD = 'hard'

# Constant values for the game.
MAX_HP = 100
DEFAULT_VALUE = 0
DEFAULT_SKILL_MULTIPLIER = 1
DEFAULT_MAX_VALUE = 100
DEFAULT_STAT = 50
DEFAULT_DAMPNER = 10
DAMAGE_TURN_EFFECT = 3
NUM_HEROES = 4
NUM_ENEMIES = 4
USER_ACTION_ATTACK = 'attack'
USER_ACTION_DEFEND = 'defend'
USER_ACTION_SKILL ='skill'
USER_ACTION_EXIT = 'exit'


# Constant values for playable characters.

# PYRO (Fire Type)
PYRO_ATTACK = 90
PYRO_SPEED = 70
PYRO_DEFENSE = 40
PYRO_MAGIC = 60
PYRO_NAME = "PYRO"
PYRO_IMAGE = "diluc.jpeg"
PYRO_PORTRAIT = "diluc.webp"
PYRO_JOB_SKILL = "Flame Warrior"
PYRO_SKILL1_NAME = "Flame Charge"
PYRO_SKILL1_FACTOR = 0.7
PYRO_SKILL1_DAMAGE_STATS = ""
PYRO_SKILL2_NAME = "Incinerate"
PYRO_SKILL2_FACTOR = 0.9
PYRO_SKILL2_DAMAGE_STATS = "burn"
PYRO_SKILL3_NAME = "Pyro Ball"
PYRO_SKILL3_FACTOR = 0.4
PYRO_SKILL3_DAMAGE_STATS = "burn"
PYRO_SKILL4_NAME = "Blaze Kick"
PYRO_SKILL4_FACTOR = 0.8
PYRO_SKILL4_DAMAGE_STATS = ""


# HYDRO (Water Type)
HYDRO_ATTACK = 70
HYDRO_SPEED = 55
HYDRO_DEFENSE = 90
HYDRO_MAGIC = 70
HYDRO_NAME = "HYDRO"
HYDRO_IMAGE = "./img/barbara.jpeg"
HYDRO_PORTRAIT = "./img/barbara.webp"
HYDRO_JOB_SKILL = "Aqua Warrior"
HYDRO_SKILL1_NAME = "Hydro Pump"
HYDRO_SKILL1_FACTOR = 0.8
HYDRO_SKILL1_DAMAGE_STATS = ""
HYDRO_SKILL2_NAME = "Water Shuriken"
HYDRO_SKILL2_FACTOR = 0.7
HYDRO_SKILL2_DAMAGE_STATS = ""
HYDRO_SKILL3_NAME = "Frost Breath"
HYDRO_SKILL3_FACTOR = 0.5
HYDRO_SKILL3_DAMAGE_STATS = "freeze"
HYDRO_SKILL4_NAME = "Subzero Slam"
HYDRO_SKILL4_FACTOR = 0.9
HYDRO_SKILL4_DAMAGE_STATS = "freeze"


# Constant values for the enemy characters.

# GOBLIN
GOBLIN_ATTACK = 60
GOBLIN_SPEED = 50
GOBLIN_DEFENSE = 60
GOBLIN_IMAGE = './img/goblin.jpg'

# OGRE
OGRE_ATTACK = 70
OGRE_SPEED = 40
OGRE_DEFENSE = 70
OGRE_IMAGE = './img/ogre.png'

class MagicSkill:
    """Class representing a player's magic skill with respect to the job class"""

    def __init__(self, magic_name, magic_factor, damage_status):
        self.magic_name = magic_name
        self.magic_factor = magic_factor
        self.damage_status = damage_status

    def __str__(self):
            return f"Magic Name: {self.magic_name}, Magic Factor: {self.magic_factor},  Damage Status: {'-' if self.damage_status == '' else self.damage_status}"

class JobClass:
    """Clas representing player's job class"""

    def __init__(self):
        self.magic_skills = []

    def __str__(self):
        return f"Magic Skills: {self.magic_skills}"
    
    def get_magic_skills(self, skill_name):
        magic_skill = None
        for skill in self.magic_skills:
            if skill.magic_name == skill_name:
                magic_skill = skill
        return magic_skill

class PlayerCharacter:
    """Class representing a player character"""

    def __init__(self, hp=MAX_HP, ap=DEFAULT_VALUE, dp=DEFAULT_VALUE, sp=DEFAULT_VALUE, mp=DEFAULT_VALUE, image="", job_class=None, default_name="", name="", use_defense=False):
        """Constructor function for a player character class

        Parameters
        ----------
        hp : int
        ap : int
        dp : int
        sp : int
        mp : int
        image : str
        job_class : class object
        name : str
        """

        self.hp = hp
        self.ap = ap
        self.dp = dp
        self.sp = sp
        self.mp = mp
        self.image = image
        self.job_class = job_class
        self.default_name = default_name
        self.name = name
        self.use_defense = use_defense

    def __str__(self):
        return f"Name: {self.name}, Default Name: {self.default_name}, HP: {self.hp}, \
            AP: {self.ap}, DP: {self.dp}, SP: {self.sp}, MP: {self.mp}, \
            Image: {'-' if self.image == '' else self.image}, Job Class: {self.job_class}\
            Use Defense: {self.use_defense}"

    def reset_stats(self):
        self.hp = 100
        self.mp = 100

    def attack(self, target, skill=None):
        skill_factor = skill.magic_factor if skill != None else 0
        skill_damage = skill.damage_status if skill != None else ''
        attack_power = self.ap * (DEFAULT_SKILL_MULTIPLIER + skill_factor)
        if(target.use_defense):
            attack_power
            target.hp -= DEFAULT_DAMPNER + ((attack_power  - target.dp) // DEFAULT_DAMPNER)
            target.use_defense = False
            target.health_stats = skill_damage
        else:
            target.hp -= DEFAULT_DAMPNER + (attack_power // DEFAULT_DAMPNER)
            target.health_stats = skill_damage

    def defend(self):
        self.use_defense = True
        

    def use_skill(self, target, skill_name):
        skill = self.job_class.get_magic_skills(skill_name)
        print(f"Using skill: {skill.magic_name}...")
        self.attack(target, skill)
    
    def get_skill_list(self):
        list_skills = []
        for magic_skill in self.job_class.magic_skills:
            list_skills.append(magic_skill.magic_name)
        return list_skills

class EnemyCharacter:
    """Class representing an enemy character"""

    def __init__(self, hp=MAX_HP, ap=DEFAULT_VALUE, dp=DEFAULT_VALUE, sp=DEFAULT_VALUE, image="", enemy_type='', default_name='', health_stats="", use_defense=True):
        """Constructor function for an enemy character"""
        self.hp = hp
        self.ap = ap
        self.dp = dp
        self.sp = sp
        self.image = image
        self.enemy_type = enemy_type
        self.default_name = default_name
        self.health_stats = health_stats
        self.use_defense = use_defense

    def __str__(self):
        return f"Name: {self.default_name}, HP: {self.hp}, AP: {self.ap}, DP: {self.dp}, SP: {self.sp}, \
            Image: {'-' if self.image == '' else self.image}, Enemy Type: {self.enemy_type}, \
            Health Stats: {'-' if self.health_stats == '' else self.health_stats}, \
            Use Defense: {self.use_defense}"
    
    def attack(self, target):
        if(target.use_defense):
            target.hp -= DEFAULT_DAMPNER + ((self.ap - target.dp) // DEFAULT_DAMPNER)
            target.use_defense = False
        else:
            target.hp -= DEFAULT_DAMPNER + (self.ap // DEFAULT_DAMPNER)

    def defend(self):
        self.use_defense = True


pyro_skills = {
    'skill1': [PYRO_SKILL1_NAME, PYRO_SKILL1_FACTOR, PYRO_SKILL1_DAMAGE_STATS],
    'skill2': [PYRO_SKILL2_NAME, PYRO_SKILL2_FACTOR, PYRO_SKILL2_DAMAGE_STATS],
    'skill3': [PYRO_SKILL3_NAME, PYRO_SKILL3_FACTOR, PYRO_SKILL3_DAMAGE_STATS],
    'skill4': [PYRO_SKILL4_NAME, PYRO_SKILL4_FACTOR, PYRO_SKILL4_DAMAGE_STATS],
}

hydro_skills = {
    'skill1': [HYDRO_SKILL1_NAME, HYDRO_SKILL1_FACTOR, HYDRO_SKILL1_DAMAGE_STATS],
    'skill2': [HYDRO_SKILL2_NAME, HYDRO_SKILL2_FACTOR, HYDRO_SKILL2_DAMAGE_STATS],
    'skill3': [HYDRO_SKILL3_NAME, HYDRO_SKILL3_FACTOR, HYDRO_SKILL3_DAMAGE_STATS],
    'skill4': [HYDRO_SKILL4_NAME, HYDRO_SKILL4_FACTOR, HYDRO_SKILL4_DAMAGE_STATS],
}

playable_character_dict = {
    'pyro': {
        'hp': MAX_HP,
        'attack': PYRO_ATTACK,
        'defense': PYRO_DEFENSE,
        'speed': PYRO_SPEED,
        'magic': PYRO_MAGIC,
        'skills': pyro_skills,
        'image': PYRO_IMAGE
    },
    'hydro': {
        'hp': MAX_HP,
        'attack': HYDRO_ATTACK,
        'defense': HYDRO_DEFENSE,
        'speed': HYDRO_SPEED,
        'magic': HYDRO_MAGIC,
        'skills': hydro_skills,
        'image': HYDRO_IMAGE,
    },
}

enemy_character_dict = {
    'goblin': {
        'hp': MAX_HP,
        'attack': GOBLIN_ATTACK,
        'defense': GOBLIN_DEFENSE,
        'speed': GOBLIN_SPEED,
        'image': GOBLIN_IMAGE,
    },
    'ogre': {
        'hp': MAX_HP,
        'attack': OGRE_ATTACK,
        'defense': OGRE_DEFENSE,
        'speed': OGRE_SPEED,
        'image': OGRE_IMAGE
    },
}

user_actions = {
    '1': USER_ACTION_ATTACK,
    '2': USER_ACTION_DEFEND,
    '3': USER_ACTION_SKILL,
    '4': USER_ACTION_EXIT
}


def print_game_intro():
    print_star_pad(GAME_TITLE)
    print(f"Welcome to the {GAME_TITLE}!")
    print('Please Enter your name: ')
    user_name = input()
    return user_name

def print_star_pad(string):
    """Function to print a string with star paddings"""
    print(f"{STAR_PAD_SIGN * PAD}{string.upper().center(PAD)}{STAR_PAD_SIGN * PAD}")

def print_underscore_pad(string=''):
    """Function to print underline separation"""
    if string != '':
        print(f"{UNDERSCORE_PAD_SIGN * PAD * TRIPLE_PAD_SIZE}")
        print_star_pad(string)
        print(f"{UNDERSCORE_PAD_SIGN * PAD * TRIPLE_PAD_SIZE}")
    else:
        print(f"{UNDERSCORE_PAD_SIGN * PAD * TRIPLE_PAD_SIZE}")

def get_character_list():
    print('Available characters: ')
    characters = [key for key in playable_character_dict.keys()]
    for character in characters:
        print_underscore_pad(character)
        for key, value in playable_character_dict[character].items():
            if(key != 'skills'):
                print(f"{key.upper()} : {value}")
            elif(key != 'image'):
                print(f"{key.upper()}:")
                list(map(lambda x: x, value.values() ))
                skills = [skill for skill in value.values()]
                print(tabulate(skills, headers=['Attack Name', 'Damage Factor', 'Damage Status'], tablefmt='psql'))
    print_underscore_pad()
    return characters

def choose_character(user_name):
    """Function to print a list of available characters and allow the user to choose one"""
    is_character_set = False
    player_character = PlayerCharacter()
    characters = get_character_list()
    while not is_character_set:
        print('Enter your character choice (pyro, hydro):')
        user_character = input().lower().strip()
        print('You have selected: ', user_character)
        if(user_character in characters):
            is_character_set = True
            hp, ap, dp, sp, mp, skills, image= playable_character_dict[user_character].values()
            job_class = JobClass()
            magic_skill_list = []
            for skill in skills.keys():
                magic_name, magic_factor, damage_status = skills[skill]
                magic_skill = MagicSkill(magic_name=magic_name, magic_factor=magic_factor, damage_status=damage_status)
                magic_skill_list.append(magic_skill)
            job_class.magic_skills = magic_skill_list
            player_character = PlayerCharacter(hp = hp, ap = ap, dp = dp, sp = sp, mp = mp, job_class=job_class, image=image, default_name=user_character, name=user_name)
        else:
            print('Invalid character. Please try again.')
    return player_character

def get_game_level():
    """Function to allow user to select game difficulty level"""
    is_level_set = False
    while not is_level_set:
        print('Enter the game difficulty level (easy, medium, hard):')
        difficulty_level = input().lower().strip()
        if(difficulty_level in [DIFFICULTY_EASY, DIFFICULTY_MEDIUM, DIFFICULTY_HARD]):
            is_level_set = True
        else:
            print('Invalid difficulty level. Please try again.')
    print(f"Difficulty level: {difficulty_level}")
    return difficulty_level

def get_enemy_character(player_character=None, game_difficulty_level=DIFFICULTY_EASY):
    enemy_list = list(enemy_character_dict.keys())
    random_enemy = choice(enemy_list)
    enemy_hp, enemy_ap, enemy_dp, enemy_sp = MAX_HP, DEFAULT_VALUE, DEFAULT_VALUE, DEFAULT_VALUE
    if(game_difficulty_level == DIFFICULTY_EASY):
        enemy_ap, enemy_dp, enemy_sp = DEFAULT_STAT, DEFAULT_STAT, DEFAULT_STAT
    elif(game_difficulty_level == DIFFICULTY_MEDIUM):
        enemy_hp, enemy_ap, enemy_dp, enemy_sp = enemy_character_dict[random_enemy].values()
    else:
        min_ap, min_dp, min_sp = player_character.ap, player_character.dp, player_character.sp
        enemy_ap, enemy_dp, enemy_sp = randint(min_ap, DEFAULT_MAX_VALUE), randint(min_dp, DEFAULT_MAX_VALUE), randint(min_sp, DEFAULT_MAX_VALUE)
    enemy_character = EnemyCharacter(hp = enemy_hp, ap = enemy_ap, dp = enemy_dp, sp = enemy_sp, image="", enemy_type=random_enemy, default_name=random_enemy, health_stats="")
    return enemy_character

def print_current_hp(player_character, enemy_character):
    player_character.hp = 0 if player_character.hp <= 0 else player_character.hp
    enemy_character.hp = 0 if enemy_character.hp <= 0 else enemy_character.hp
    print(f"{tabulate([[player_character.hp, enemy_character.hp]], headers=[player_character.name.upper() + ' HP', enemy_character.default_name.upper() + ' HP'], tablefmt='grid')}\n")

def display_skill_menu(player_character):
    skills_list = player_character.get_skill_list()
    print('Available Skills: ')
    for ind, skill in enumerate(skills_list):
        print(f"{ind + 1}. {skill}")
    print(f"Select the skill you want to select (1, 2, 3, 4): ")
    option = int(input().lower().strip()) - 1
    selected_skill = skills_list[option]
    return selected_skill

def display_user_menu(player_character):
    choice = DEFAULT_VALUE
    skill_choice = None
    while(True):
        print(f"{player_character.name.upper()} Actions:")
        print('1. Attack')
        print('2. Defend')
        print('3. Skill')
        print('4. Exit')
        print('Enter your option (1, 2, 3, 4): ')
        option = input().lower().strip()
        if(option in user_actions.keys()):
            if(user_actions[option] == USER_ACTION_SKILL):
                skill_choice = display_skill_menu(player_character)
            print(f"Your option is {user_actions[option].title()} {'and ' + skill_choice if skill_choice is not None else ''}")
            choice = user_actions[option]
            break
        else:
            print('Invalid option. Please try again.')
    return choice, skill_choice

def initiate_game(player_character, enemy_character, playable_character_dict, enemy_character_dict):
    winner = None
    initial_striker = player_character if player_character.sp >= enemy_character.sp else enemy_character
    next_striker = player_character if player_character.sp < enemy_character.sp else enemy_character
    while(True):
        if(initial_striker.default_name in playable_character_dict.keys()):
            option, skill_choice = display_user_menu(player_character)
            if(option == USER_ACTION_ATTACK):
                player_character.attack(target=enemy_character)
            elif(option == USER_ACTION_DEFEND):
                player_character.defend()
            elif(option == USER_ACTION_SKILL):
                player_character.use_skill(target=enemy_character, skill_name=skill_choice)
            elif(option == USER_ACTION_EXIT):
                return enemy_character.default_name
        elif(initial_striker.default_name in enemy_character_dict.keys()):
            print(f"{initial_striker.default_name.upper()}'s Turn:")
            print(f"{initial_striker.default_name.upper()} is Attacking: ")
            enemy_character.attack(player_character)

        if(next_striker.hp <= 0):
            print_current_hp(player_character, enemy_character)
            if(initial_striker.default_name in playable_character_dict.keys()):
                winner = initial_striker.name
            else:
                winner = initial_striker.default_name
            break
        else:
            print_current_hp(player_character, enemy_character)
            initial_striker, next_striker = next_striker, initial_striker
    return winner


def game():
    is_initial_run = True
    user_name = "Player"
    winner = None
    while True:
        if (is_initial_run):
            user_name = print_game_intro()
            is_initial_run = False
        player_character = choose_character(user_name)
        game_difficulty_level = get_game_level()
        enemy_character = get_enemy_character(player_character, game_difficulty_level)
        print_current_hp(player_character, enemy_character)
        winner = initiate_game(player_character, enemy_character, playable_character_dict, enemy_character_dict)
        if winner is not None:
            print_underscore_pad(f'{winner.upper()} wins')
            break

if __name__ == '__main__':
    game()