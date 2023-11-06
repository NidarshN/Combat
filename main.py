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
PYRO_IMAGE = "./img/diluc.jpeg"
PYRO_PORTRAIT = "./img/diluc.webp"
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

class MyGUI:
    
    activated_btn = None
    selected_char_btn = None
    chosen_player = None

    def __init__(self, root=tk.Tk(screenName=GAME_TITLE, baseName=GAME_TITLE, className=GAME_TITLE.lower()), 
                                    font=DEFAULT_FONT, main_frame= None, current_frame=None, menu_btns_dict=dict(),
                                    game_difficulty=DIFFICULTY_EASY):
        self.root = root
        self.root.geometry(f'{DEFAULT_WIDTH}x{DEFAULT_HEIGHT}')
        self.root.resizable(0,0)
        self.font = font
        self.main_frame = main_frame
        self.current_frame = current_frame
        self.menu_btns_dict = menu_btns_dict
        self.character_var = 'pyro'
        self.player_character = self.get_character(self.character_var)
        self.game_difficulty = game_difficulty
        self.audio_var = DEFAULT_VALUE
        self.language_options = ['English', 'Japanese']
        self.language_var = self.language_options[0]
        self.game_difficulty_val = 0
        self.enemy_character = self.get_enemy_character(self.player_character, self.game_difficulty)
        self.enemy_progress_bar = None
        self.character_progress_bar = None
        self.action_box_frame=None
        self.message_box_frame = None
        self.winner = None

    def reset_activate(self):
        for btn_key in self.menu_btns_dict:
            self.menu_btns_dict[btn_key][0].config(fg='black')
    

    def clear_selected_frame(self, frame_name):
        for widgets in frame_name.winfo_children():
            widgets.destroy()
        frame_name.pack_forget()

    def clear_main_frame(self):
        for widgets in self.main_frame.winfo_children():
            widgets.destroy()

    def activate(self, text, btn):
        self.reset_activate()
        btn.config(fg='blue')
        self.activated_btn = btn
        page = self.menu_btns_dict[text][1]
        self.clear_main_frame()
        page()

    def get_menu_button(self, root, text):
        btn = tk.Button(root, text=text, font=self.font, bd=0,
                            bg=MAIN_FRAME_BG,
                            fg=COLOR_BLACK, 
                            justify='center',
                            width=MENU_BUTTON_WIDTH
                            )
        btn.config(command=lambda: self.activate(text, btn))
        return btn
    
    def get_character(self, name):
        hp, ap, dp, sp, mp, skills, image = playable_character_dict[name].values()
        job_class = JobClass()
        magic_skill_list = []
        for skill in skills.keys():
            magic_name, magic_factor, damage_status = skills[skill]
            magic_skill = MagicSkill(magic_name=magic_name, magic_factor=magic_factor, damage_status=damage_status)
            magic_skill_list.append(magic_skill)
        job_class.magic_skills = magic_skill_list
        player_character = PlayerCharacter(hp = hp, ap = ap, dp = dp, sp = sp, mp = mp, image=image, job_class=job_class, default_name=name, name=name)
        return player_character        

    def character_set(self, val ):        
        if(val == '0'):
            self.character_var = 'pyro'
        elif(val == '1'):
            self.character_var = 'hydro'
        self.player_character = self.get_character(self.character_var)
        self.enemy_character = self.get_enemy_character(self.player_character, self.game_difficulty)
        

    def get_character_card(self, root, name, img_file):
        bg = ''
        if(name == PYRO_NAME):
            bg = '#e25822'
        else:
            bg = '#0088DD' 
        
        title_label = tk.Label(root, text=name,  bg=bg,fg='white', font=self.font, pady=10)
        title_label.place(relx=.4, rely=.05)

        char_img = Image.open(img_file)
        resize_img = char_img.resize((CHARACTER_PROFILE_DIMENSIONS, CHARACTER_PROFILE_DIMENSIONS))
        char_resized_img = ImageTk.PhotoImage(resize_img, width=CHARACTER_PROFILE_DIMENSIONS, height=CHARACTER_PROFILE_DIMENSIONS)

        char_img_canvas = tk.Label(master=root, image=char_resized_img, width=CHARACTER_PROFILE_DIMENSIONS, height=CHARACTER_PROFILE_DIMENSIONS, borderwidth=2, relief='solid')
        char_img_canvas.image = char_resized_img
        char_img_canvas.place(relx= .25, rely=.15)

        set_x = .1
        set_y = .5
        offset_y = .05
        base_offset = .5

        for key, val in playable_character_dict[name.lower()].items():
            if(key != 'skills'):
                char_label = tk.Label(root, text=f'{key.title()}: {val}', bg=bg,fg='white', font=self.font, pady=10)
                char_label.place(relx= set_x, rely=set_y)
                set_y += offset_y
            else:
                char_label = tk.Label(root, text=f'{key.title()}:', bg=bg,fg='white', font=self.font, pady=10)
                char_label.place(relx= set_x, rely=set_y)
            
                count = 0
                relx = set_x
                rely = set_y + offset_y

                for _, skill_val in val.items():
                    if(count == 1):
                        relx = set_x + base_offset
                    elif(count == 2):
                        relx = set_x
                        rely += offset_y
                    elif(count == 3):
                        relx = set_x + base_offset
                    
                    char_label = tk.Label(root, text=f'{skill_val[0].title()}: {skill_val[1]}', bg=bg, fg='white', font=self.font, pady=10)
                    char_label.place(relx= relx, rely=rely)
                    count += 1

    def get_enemy_character(self, player_character=None, game_difficulty_level=DIFFICULTY_EASY):
        enemy_list = list(enemy_character_dict.keys())
        random_enemy = choice(enemy_list)
        enemy_image = enemy_character_dict[random_enemy]['image']
        enemy_hp, enemy_ap, enemy_dp, enemy_sp = MAX_HP, DEFAULT_VALUE, DEFAULT_VALUE, DEFAULT_VALUE
        if(game_difficulty_level == DIFFICULTY_EASY):
            enemy_ap, enemy_dp, enemy_sp = DEFAULT_STAT, DEFAULT_STAT, DEFAULT_STAT
        elif(game_difficulty_level == DIFFICULTY_MEDIUM):
            enemy_hp, enemy_ap, enemy_dp, enemy_sp, enemy_image = enemy_character_dict[random_enemy].values()
        else:
            min_ap, min_dp, min_sp = player_character.ap, player_character.dp, player_character.sp
            enemy_ap, enemy_dp, enemy_sp = randint(min_ap, DEFAULT_MAX_VALUE), randint(min_dp, DEFAULT_MAX_VALUE), randint(min_sp, DEFAULT_MAX_VALUE)
        enemy_character = EnemyCharacter(hp = enemy_hp, ap = enemy_ap, dp = enemy_dp, sp = enemy_sp, image=enemy_image, 
                                        enemy_type=random_enemy, default_name=random_enemy, health_stats="")
        return enemy_character

    def character_screen(self):
        character_frames = tk.Frame(self.main_frame, bg=MAIN_FRAME_BG)

        pyro_frame = tk.Frame(character_frames, bg='#e25822')
        pyro_frame.configure(width=MAIN_FRAME_WIDTH // 2, height=DEFAULT_HEIGHT)
        self.get_character_card(root=pyro_frame, name=PYRO_NAME, img_file=PYRO_PORTRAIT)
        pyro_frame.pack(side=tk.LEFT)
        pyro_frame.pack_propagate(False)
        
        
        hydro_frame = tk.Frame(character_frames, bg='#0088DD')
        hydro_frame.configure(width=MAIN_FRAME_WIDTH // 2, height=DEFAULT_HEIGHT)
        self.get_character_card(root=hydro_frame, name=HYDRO_NAME, img_file=HYDRO_PORTRAIT)
        hydro_frame.pack(side=tk.LEFT)
        hydro_frame.pack_propagate(False)

        character_val = tk.IntVar()
        character_val.set(0 if self.character_var == 'pyro' else 1)

        character_slider = tk.Scale(character_frames, variable=character_val, 
                                        from_=0, to=1, resolution=1,
                                        orient='horizontal',
                                        state='active',
                                        showvalue=False, relief='sunken',
                                        command=self.character_set,
                                        length=150,
                                    )
        character_slider.focus()
        character_labels = tk.Label(character_frames, text='Select')
        character_labels.place(relx=.475, rely=.92)
        character_slider.place(relx=.42, rely=.95)
        character_frames.pack()


    def update_progress_bar(self, progress_bar, val):
        progress_bar['value'] = val


    def enemy_attack(self):
        self.check_winner()
        self.enemy_character.attack(target=self.player_character)
        self.update_progress_bar(self.character_progress_bar, self.player_character.hp)
        self.check_winner()


    def player_attack(self):
        self.check_winner()
        self.player_character.attack(target=self.enemy_character)
        self.update_progress_bar(self.enemy_progress_bar, self.enemy_character.hp)
        self.check_winner()


    def player_skill(self, skill_name):
        self.check_winner()
        self.player_character.use_skill(self.enemy_character, skill_name)
        self.update_progress_bar(self.enemy_progress_bar, self.enemy_character.hp)
        self.check_winner()


    def clear_skill_message(self, skill_name):
        self.clear_selected_frame(self.message_box_frame)
        self.player_skill(skill_name)

    def use_skill(self, root, skill_name):
        self.check_winner()
        if(self.player_character.sp >= self.enemy_character.sp):
            self.display_message(root, f'{self.player_character.name.title()} used {skill_name}')
            self.message_box_frame.after(1000, lambda: self.clear_skill_message(skill_name))
            self.enemy_attack()
        elif(self.player_character.sp < self.enemy_character.sp): 
            self.enemy_attack()
        self.check_winner()
        


        self.clear_selected_frame(root)
        

    def clear_defend_message(self):
        self.clear_selected_frame(self.message_box_frame)
        self.player_character.defend()
        self.enemy_attack()

    def use_defend(self, root):
        self.display_message(root, f'{self.player_character.name.title()} used Defend')
        self.message_box_frame.after(1000, self.clear_defend_message)
        self.check_winner()


    def clear_attack_message(self):
        self.clear_selected_frame(self.message_box_frame)
        self.player_attack()

    def use_attack(self, root):
        print(self.player_character.hp, self.enemy_character.hp)
        if(self.player_character.hp < 0 and self.enemy_character.hp <0):
            self.check_winner()
        elif(self.player_character.hp > 0 and self.enemy_character.hp >0):
            if(self.player_character.sp >= self.enemy_character.sp):
                self.display_message(root, f'{self.player_character.name.title()} Attacking')
                self.message_box_frame.after(1000, self.clear_attack_message)
                self.enemy_attack()
            elif(self.player_character.sp < self.enemy_character.sp): 
                self.enemy_attack()
                self.display_message(root, f'{self.player_character.name.title()} Attacking')
                self.message_box_frame.after(1000, self.clear_attack_message)
        self.check_winner()
        

    def display_message(self, root, text):
        message_box_frame = tk.Frame(self.action_box_frame, borderwidth=5)
        message_box_frame.configure(width=MAIN_FRAME_WIDTH, height=DEFAULT_HEIGHT//4,
                                    highlightthickness=5, highlightbackground='black')
        self.message_box_frame = message_box_frame
        message_label = tk.Label(message_box_frame, text=text, font=self.font)
        message_label.pack()
        message_box_frame.pack()
        message_box_frame.pack_propagate(False)

    def display_skill_menu(self, root):
        character_skills = self.player_character.get_skill_list()
        menu_frame = tk.Frame(root, bg=MAIN_FRAME_BG)

        menu_frame.configure(width=MAIN_FRAME_WIDTH, height=DEFAULT_HEIGHT//4,
                                    highlightthickness=5, highlightbackground='black')
        
        skill1_btn = tk.Button(menu_frame, text=f"{character_skills[0]}", 
                                bg=MAIN_FRAME_BG, highlightbackground='black', 
                                highlightthickness = 0, borderwidth=2,
                                width=40, height=2)
        skill1_btn.config(command=lambda: self.use_skill(menu_frame, character_skills[0]))
        skill1_btn.place(relx=.01, rely=.1)

        skill2_btn = tk.Button(menu_frame, text=f"{character_skills[1]}", 
                                bg=MAIN_FRAME_BG, highlightbackground='black', 
                                highlightthickness = 0, borderwidth=2,
                                width=40, height=2)
        skill2_btn.config(command=lambda: self.use_skill(menu_frame, character_skills[1]))
        skill2_btn.place(relx=.5, rely=.1)

        skill3_btn = tk.Button(menu_frame, text=f"{character_skills[2]}", 
                                bg=MAIN_FRAME_BG, highlightbackground='black', 
                                highlightthickness = 0, borderwidth=2,
                                width=40, height=2)
        skill3_btn.config(command=lambda: self.use_skill(menu_frame, character_skills[2]))
        skill3_btn.place(relx=.01, rely=.5)

        skill4_btn = tk.Button(menu_frame, text=f"{character_skills[3]}", 
                                bg=MAIN_FRAME_BG, highlightbackground='black', 
                                highlightthickness = 0, borderwidth=2,
                                width=40, height=2)
        skill4_btn.config(command=lambda: self.use_skill(menu_frame, character_skills[3]))
        skill4_btn.place(relx=.5, rely=.5)

        menu_frame.pack()

        
        
    def restart(self):
        pass

    

    def display_user_menu(self, root):
        action_box_frame = tk.Frame(root, borderwidth=5)
        action_box_frame.configure(width=MAIN_FRAME_WIDTH, height=DEFAULT_HEIGHT//4,
                                    highlightthickness=5, highlightbackground='black')
        self.action_box_frame = action_box_frame
        attack_btn = tk.Button(action_box_frame, text="Attack", 
                                bg=MAIN_FRAME_BG, highlightbackground='black', 
                                highlightthickness = 0, borderwidth=2,
                                width=40, height=2)
        attack_btn.config(command=lambda: self.use_attack(root=action_box_frame))
        attack_btn.place(relx=.01, rely=.1)



        defense_btn = tk.Button(action_box_frame, text="Defend", 
                                bg=MAIN_FRAME_BG, highlightbackground='black', 
                                highlightthickness = 0, borderwidth=2,
                                width=40, height=2)
        defense_btn.config(command=lambda: self.use_defend(root=action_box_frame))
        defense_btn.place(relx=.5, rely=.1)

        skills_btn = tk.Button(action_box_frame, text="Skills", 
                                bg=MAIN_FRAME_BG, highlightbackground='black', 
                                highlightthickness = 0, borderwidth=2,
                                width=40, height=2)
        skills_btn.config(command=lambda: self.display_skill_menu(root=action_box_frame))
        skills_btn.place(relx=.01, rely=.5)

        exit_btn = tk.Button(action_box_frame, text="Exit", 
                                bg=MAIN_FRAME_BG, highlightbackground='black', 
                                highlightthickness = 0, borderwidth=2,
                                width=40, height=2)
        exit_btn.config(command=lambda: self.exit_screen())
        exit_btn.place(relx=.5, rely=.5)
        
        action_box_frame.pack(side="bottom")

    def check_winner(self):
        winner = None
        if(self.player_character.hp <= 0):
            winner = self.enemy_character.default_name
        elif(self.enemy_character.hp <=0):
            winner = self.player_character.default_name
        self.winner = winner
        if(winner != None):
            winner_frame = tk.Frame(self.action_box_frame, bg=MAIN_FRAME_BG)
            winner_frame.configure(width=MAIN_FRAME_WIDTH, height=DEFAULT_HEIGHT)
            winner_label = tk.Label(winner_frame, bg=MAIN_FRAME_BG, text=f"{winner.title()} wins", font=self.font)
            winner_label.pack()
            winner_frame.pack()
            winner_frame.pack_propagate(False)
        


    def start_screen(self):
        if(self.winner != None):
            self.player_character.hp = MAX_HP
            self.enemy_character.hp = MAX_HP
            self.winner = None
        start_frame = tk.Frame(self.main_frame, bg=MAIN_FRAME_BG)
        start_frame.configure(width=MAIN_FRAME_WIDTH, height=DEFAULT_HEIGHT)

        character_display_frame = tk.Frame(start_frame, bg=MAIN_FRAME_BG)
        character_display_frame.configure(width=MAIN_FRAME_WIDTH, height=3*DEFAULT_HEIGHT//4,
                                            highlightthickness=2, highlightbackground='black')
        
        enemy_health_label = tk.Label(character_display_frame, text=f"{self.enemy_character.default_name.title()}'s Health", font=self.font, bg=MAIN_FRAME_BG)
        enemy_health_label.place(relx=.1, rely=.05)
        enemy_health_progress = ttk.Progressbar(character_display_frame, orient = 'horizontal',
        value=self.enemy_character.hp, length = 500, mode = 'determinate')
        self.enemy_progress_bar = enemy_health_progress
        enemy_health_progress.place(relx=.1, rely=.1)
        

        enemy_img = Image.open(self.enemy_character.image)
        enemy_resize_img = enemy_img.resize((CHARACTER_PROFILE_DIMENSIONS, CHARACTER_PROFILE_DIMENSIONS))
        enemy_resized_img = ImageTk.PhotoImage(enemy_resize_img, width=CHARACTER_PROFILE_DIMENSIONS, height=CHARACTER_PROFILE_DIMENSIONS)

        enemy_img_canvas = tk.Label(master=character_display_frame, image=enemy_resized_img, width=CHARACTER_PROFILE_DIMENSIONS, height=CHARACTER_PROFILE_DIMENSIONS, borderwidth=0, relief='solid')
        enemy_img_canvas.image = enemy_resized_img
        enemy_img_canvas.place(relx=.7, rely=.01)


        char_health_label = tk.Label(character_display_frame, text=f"{self.player_character.name.title()}'s Health", font=self.font, bg=MAIN_FRAME_BG)
        char_health_label.place(relx=.83, rely=.65)

        char_health_progress = ttk.Progressbar(character_display_frame, orient = 'horizontal',
        value=self.player_character.hp, length = 500, mode = 'determinate')
        self.character_progress_bar = char_health_progress
        char_health_progress.place(relx=.4, rely=.7)

        char_img = Image.open(self.player_character.image)
        resize_img = char_img.resize((CHARACTER_PROFILE_DIMENSIONS, CHARACTER_PROFILE_DIMENSIONS))
        char_resized_img = ImageTk.PhotoImage(resize_img, width=CHARACTER_PROFILE_DIMENSIONS, height=CHARACTER_PROFILE_DIMENSIONS)

        char_img_canvas = tk.Label(master=character_display_frame, image=char_resized_img, width=CHARACTER_PROFILE_DIMENSIONS, height=CHARACTER_PROFILE_DIMENSIONS, borderwidth=0, relief='solid')
        char_img_canvas.image = char_resized_img
        char_img_canvas.place(relx=.1, rely=.6)

        character_display_frame.pack(side="top")

        self.display_user_menu(start_frame)
            
        start_frame.pack()
        start_frame.pack_propagate(False)

    def audio_set(self, val):
        print(f"Audio Option: {'ON' if val.get() == 1 else 'OFF'}")
        self.audio_var = val.get()
        

    def lang_set(self, val ):
        print(f'Language Option: {val}')
        self.language_var = val

    def difficulty_set(self, val):
        if(val == '0'):
            self.game_difficulty = DIFFICULTY_EASY
        elif(val == '5'):
            self.game_difficulty = DIFFICULTY_MEDIUM
        elif(val == '10'):
            self.game_difficulty = DIFFICULTY_HARD
        self.game_difficulty_val = val
        


    def settings_screen(self):
        settings_frame = tk.Frame(self.main_frame, bg=MAIN_FRAME_BG)
        settings_frame.configure(width=MAIN_FRAME_WIDTH, height=DEFAULT_HEIGHT)
        label = tk.Label(settings_frame, text='Settings', font=self.font, bg=MAIN_FRAME_BG)
        label.pack()

        audio_label = tk.Label(settings_frame, text='Audio', font=self.font, bg=MAIN_FRAME_BG)
        audio_label.place(relx=.3, rely=.3)

        audio_val = tk.IntVar()
        audio_val.set(self.audio_var)

        audio_on_radiotbn = tk.Radiobutton(settings_frame, text="ON", bg=MAIN_FRAME_BG, variable=audio_val, value=1, command=lambda: self.audio_set(audio_val))
        audio_on_radiotbn.place(relx=.5, rely=.3)

        audio_off_radiotbn = tk.Radiobutton(settings_frame, text="OFF", bg=MAIN_FRAME_BG, variable=audio_val, value=0, command=lambda: self.audio_set(audio_val))
        audio_off_radiotbn.place(relx=.7, rely=.3)
        
        language_val = tk.StringVar()
        language_val.set(self.language_var)
        
        language_label = tk.Label(settings_frame, text='Language', font=self.font, bg=MAIN_FRAME_BG)
        language_label.place(relx=.3, rely=.4)
        
        language_dropdown = tk.OptionMenu(settings_frame, language_val, *self.language_options, command=self.lang_set)
        language_dropdown.place(relx=.5, rely=.4)

        difficulty_val = tk.IntVar()
        difficulty_val.set(self.game_difficulty_val)
        difficulty_label = tk.Label(settings_frame, text='Difficulty Level', font=self.font, bg=MAIN_FRAME_BG)
        difficulty_label.place(relx=.3, rely=.5)

        difficulty_slider = tk.Scale(settings_frame, variable=difficulty_val, 
                                        from_=0, to=10, resolution=5,
                                        orient='horizontal',
                                        state='active',
                                        showvalue=False, relief='sunken',
                                        command=self.difficulty_set,
                                        length=125
                                    )
        difficulty_slider.focus()
        difficulty_tick_label = tk.Label(settings_frame, text='Easy  Medium  Hard', bg=MAIN_FRAME_BG)
        difficulty_tick_label.place(relx=.5, rely=.55)
        difficulty_slider.place(relx=.5, rely=.5)

        settings_frame.pack()
        settings_frame.pack_propagate(False)


    def exit_screen(self):
        self.clear_main_frame()
        self.on_closing()

    def load_frames(self):
        menu_frame = tk.Frame(self.root, bg='black')

        game_title = tk.Label(menu_frame, text=GAME_TITLE, font=self.font, bg=COLOR_BLACK, fg=COLOR_WHITE)
        game_title.place(x=MENU_BUTTON_X, y=MENU_BUTTON_Y - OFFSET)

        character_btn = self.get_menu_button(menu_frame, text=MENU_OPTION_CHOOSE)
        start_btn = self.get_menu_button(menu_frame, MENU_OPTION_START)
        settings_btn = self.get_menu_button(menu_frame, MENU_OPTION_SETTINGS)
        # exit_btn = self.get_menu_button(menu_frame, MENU_OPTION_EXIT)

        self.menu_btns_dict = {
            MENU_OPTION_CHOOSE: [character_btn, self.character_screen], 
            MENU_OPTION_START: [start_btn, self.start_screen], 
            MENU_OPTION_SETTINGS: [settings_btn, self.settings_screen], 
            # MENU_OPTION_EXIT: [exit_btn, self.exit_screen]
        }
        
        for ind, btn_key in enumerate(self.menu_btns_dict):
            self.menu_btns_dict[btn_key][0].place(x=0, y = MENU_BUTTON_Y + (ind * OFFSET))

        menu_frame.pack(side=tk.LEFT)
        menu_frame.pack_propagate(True)
        menu_frame.configure(width=DEFAULT_WIDTH // 4, height=DEFAULT_HEIGHT)

        self.main_frame = tk.Frame(self.root, bg=MAIN_FRAME_BG, highlightbackground='black',
                                highlightthickness=1)
        welcome_label = tk.Label(self.main_frame, bg=MAIN_FRAME_BG, text=f"Welcome \n\n to the \n\n {GAME_TITLE}".upper(), font=self.font)
        welcome_label.place(relx=.4, rely=.4)
        self.main_frame.pack(side=tk.LEFT)
        self.main_frame.pack_propagate(True)
        self.main_frame.configure(height=DEFAULT_HEIGHT, width=DEFAULT_WIDTH * 3 // 4)


    def on_closing(self):
        if(messagebox.askyesno(title="Quit?", message="Do you really want to quit the game?")):
            print(self.chosen_player)
            self.root.destroy()
        else:
            pass

    def main(self):
        self.get_main_screen()
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.root.mainloop()

    def get_main_screen(self):
        self.load_frames()

if __name__ == "__main__":
    myGUI = MyGUI()
    myGUI.main()