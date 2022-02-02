from pony.orm import *
import os
from telegram import *
#from main import send_message
if os.path.isfile('playerdb.sqlite'):
    os.remove("playerdb.sqlite")
if os.path.isfile("herodb.sqlite"):
    os.remove("herodb.sqlite")

from languages import *
from random import *
from Bot import *
import enum
from random import random
from time import sleep
pdb = Database()
pdb.bind(provider='sqlite', filename='playerdb.sqlite', create_db=True)



def hero_name_generator(player):
    if player.level < 5:
        a, b = randint(0, len(ru_hero_peon_names)-1), randint(0, len(ru_hero_peon_surnames)-1)
        return txt.get(player, 'hero_cheap_name'+str(a)) + ' ' + txt.get(player, 'hero_cheap_surname'+str(b))

def empty(context = [], player = [], args = []):
    pass

def format_message(player, key, formatparams = None, markup = None):
    if len(txt.get(player, key))>0:
        text = txt.get(player, key)
        if formatparams != None:
            text =  text.format(*formatparams)
        if markup != None:
            if markup != 'dont_change':
                markup_tg= markup.gen_markup(player) 
            else: 
                markup_tg = None
        else: 
            markup_tg = ReplyKeyboardRemove()
    return text, markup_tg
#--------------------------------------------------------------
# Класс БД игрока. Хранит всю информацию о его прогрессе
#--------------------------------------------------------------

class Player(pdb.Entity):
    id = PrimaryKey(int, auto=True)
    name = Required(str)
    chat_id = Required(int)
    state = Required(str)
    isAdmin = Required(bool)
    language = Required(str)
    stringbuffer = Optional(str)
    hero_id = Required(int)
    temporary_hero_id = Required(int)
    tutorial = Required(int)
    money = Required(int)
    level = Required(int)
    town = Required(int)
    journey = Required(str)
    encounter = Required(str)
    stage = Required(int)
    postponed_message_sended = Optional(int)

    def set_state(self,  utilities,  state_name,  args = [] ):
        state = find_state(state_name)       
        if state != None:
            self.state = state_name
            state.start_state(utilities, self, args)

    def add_money(self, amount):
        self.money += amount
        return True

    def debit(self, amount) -> bool:
        if self.money-amount>0:
            self.money -= amount
            self.flush()
            return True
        else: return False
  

    def send_message(self, utilities : Utilities,   key : str,  formatparams = None, markup = None):
        text, markup_tg = format_message(self, key, formatparams, markup)
        if utilities.bot == None:
            message = context.bot.send_message(chat_id = self.chat_id, text = text, reply_markup = markup_tg)
        else:
            message = utilities.bot.updater.bot.sendMessage(chat_id=self.chat_id, text=text, reply_markup = markup_tg)
        return message


    def get_stage(self):
        return find_encounter(self.encounter).find_stage(self.stage)

    def send_postponed_message(self, utilities : Utilities):
        if self.postponed_message_sended == 0:
            if self.stringbuffer == 'None':
                return 
            text = self.stringbuffer
            state_markup = find_state('journey').markup 
            stage_markup = find_encounter(self.encounter).find_stage(self.stage).markup
            if stage_markup != None:
                mkup = state_markup.mix_markups(stage_markup)
            else:
                mkup = state_markup
            markup_tg = mkup.gen_markup(self)
            if utilities.bot == None:
                message = context.bot.send_message(chat_id = self.chat_id, text = text, reply_markup = markup_tg)
            else:
                message = utilities.bot.updater.bot.sendMessage(chat_id=self.chat_id, text=text, reply_markup = markup_tg)
            self.postponed_message_sended = 1

    def postpone_message(self, utilities : Utilities, key : str, formatparams = None, markup = None):
        self.stringbuffer = format_message(self, key, formatparams, markup)[0]
        self.postponed_message_sended = 0

    def get_hero(self):
        if self.id != 0:
            hero =  list(select(hero for hero in Hero if hero.id == self.temporary_hero_id))[0]
            return hero
        else: return None

    def get_town(self):
        town =  list(select(town for town in Town if town.id == self.town))[0]
        return town

    def act_automatically(self):
        if self.get_town.town_hall > 0:
            return True
        else: return False
pdb.generate_mapping(create_tables=True)


#--------------------------------------------------------------
# Существа
#--------------------------------------------------------------
hdb = Database()
hdb.bind(provider='sqlite', filename='herodb.sqlite', create_db=True)
class Attributes:
    def __init__(self, strength = 0, agility=0, intelligence=0):
        self.strength = strength
        self.agility = agility
        self.intelligence = intelligence

    def add_attributes(self, attributes):
        self.strength += attributes.strength
        self.agility += attributes.agility
        self.intelligence += attributes.intelligence
    def to_array(self):
        return [self.strength, self.agility, self.intelligence]
    def read_array(self, array = []):

        self.strength, self.agility, self.intelligence = array
        return self
#--------------------------------------------------------------
wdb = Database()
wdb.bind(provider='sqlite', filename='weapondb.sqlite', create_db=True)
class Weapon(wdb.Entity):
    type = Required(str)
    level = Required(int)
    name_value_1 = Required(int)
    name_value_2 = Required(int)
    damage_amplifier =  Optional(int)
    def ini(self, damage = 0):
        self.name_value_1, self.name_value_2 = self.generate_name()
        self.damage_amplifier = damage
    def get_name(self, player):
        txt.get(player, 'weapon_common_names'+str(self.name_value_1)) + ' ' + txt.get(player, 'weapon_common_'+self.type)
    def generate_name(self):
        a, b = randint(0, len(ru_weapon_common_names)-1), randint(0, len(ru_weapon_common_second_names)-1)
        return a,b
wdb.generate_mapping(create_tables=True)
class Creature:
    def __init__(self, name : str, max_hp : int, hp:int, level : int, attributes : Attributes, weapon_id : int, player = 0 ):
        self.name = name
        self.max_hp = max_hp
        self.hp = max_hp
        self.level = level
        self.attributes = attributes
        self.player = player
        self.weapon_id = weapon_id
        self.damage_amplifier = 0

    def refresh(self, hp):
        self.hp = hp
        return self
    def get_name(self, player):
        txt.get(player, self.name)

    def get_weapon(self):
        if self.weapon_id == 0: return None
        weapon = Weapon.get(id=self.weapon_id)
        return weapon
    def get_damage(self):
        damage = self.damage_amplifier
        weapon = self.get_weapon()
        if (weapon) != None:
            damage += weapon.damage_amplifier
            if (weapon.type == 'sword'):
                damage += randint(0, int(self.attributes.agility*0.4+self.attributes.strength*0.4))
            if (weapon.type == 'hammer'):
                damage += randint(0, int(self.attributes.agility*0.1+self.attributes.strength*0.7))
        else:
            damage += randint(0, int(self.attributes.strength*0.5))
        if damage == 0: damage = 1
        return damage
    def recieve_damage(self, damage):
        self.hp -= damage
        if self.hp < 1:
            return False
        else: return True

    def hit(self, other ):
        damage = self.get_damage()
        alive = other.recieve_damage(damage)
        return damage, alive


def create_new_hero(utilities, player):
    hero = Hero()
    hero.ini(player)  
    hero.flush()
    player.temporary_hero_id = hero.id
    player.flush()
    return hero

class Hero(hdb.Entity):
    id = PrimaryKey(int, auto=True)
    max_hp = Optional(int)
    hp = Optional(int)
    name = Optional(str)
    strength  = Optional(int)
    agility = Optional(int)
    intelligence = Optional(int)
    player = Optional(int)
    level = Optional(int)
    common_enhancements = Optional(int)
    uncommon_enhancements = Optional(int)
    rare_enhancements = Optional(int)
    weapon_id = Optional(int)
    enemy_hp = Optional(int)
    def ini(self, player : Player):
        self.max_hp = 10
        self.hp = self.max_hp
        self.name = hero_name_generator(player)
        self.level = 1
        self.agility = randint(self.level, int(self.level*1.5)+1)
        self.strength = randint(self.level, int(self.level*1.5)+1)
        self.intelligence = randint(self.level, int(self.level*1.5)+1)
        self.common_enhancements = 0
        self.uncommon_enhancements = 0
        self.rare_enhancements = 0
        
        
        self.player = player.id
        self.flush()
    def to_creature(self):
        self.creature = Creature( self.name, self.max_hp, self.hp, self.level, Attributes().read_array([self.strength, self.agility, self.intelligence]), self.weapon_id, self.player )
        return self.creature
    def get_enhancements(self):
        return self.common_enhancements+self.uncommon_enhancements+self.rare_enhancements


#--------------------------------------------------------------
# База данных героев
#--------------------------------------------------------------

 

hdb.generate_mapping(create_tables=True)

#--------------------------------------------------------------
# БД поселения. Привязано к игроку, но хранится отдельно
#--------------------------------------------------------------
tdb = Database()
tdb.bind(provider='sqlite', filename='towndb.sqlite', create_db=True)
class Town(tdb.Entity):
    player = Required(int)
    level = Required(int)
    town_hall = Required(int)    
tdb.generate_mapping(create_tables=True)
#--------------------------------------------------------------
# Просто кнопки меню
#--------------------------------------------------------------
class Markup:
    buttons = []
    def __init__(self, buttons):
        self.buttons = buttons
    #преобразовывает объект в клаиваутуру для телеграмма
    def gen_markup(self, player : Player):
        markup = []
        for i in range(len(self.buttons)):
            markup.append([])
            for j in range(len(self.buttons[i])):
                tmptxt = self.buttons[i][j].get_text(player)
                if tmptxt != None:
                    markup[i].append(tmptxt)
        markup_exclude_empty = []
        for i in markup:
            if len(i) >0:
                markup_exclude_empty.append(i)
        markup = ReplyKeyboardMarkup(markup_exclude_empty)

        if len(self.buttons[0]) == 0:
            markup = ReplyKeyboardRemove()
        return markup
    #ищет кнопку в markup по тексту, который отправил игрок
    def find_button(self, player, text):
        for i in range(len(self.buttons)):
            for j in range(len(self.buttons[i])):
                if self.buttons[i][j].get_text(player) != None:
                    if (self.buttons[i][j].get_text(player)[0] == text[0]):
                        return self.buttons[i][j]
    #добавляет кнопки в клавиатуру
    def mix_markups(self, markup, position = 'begining'):
        buttons = self.buttons
        if position == 'begining':
            buttons =  markup.buttons + self.buttons 
        if position == 'end':
            buttons =   self.buttons + markup.buttons 
        return Markup(buttons)
class Button:
    """
    key  используется для обращения к основному названию кнопки, например 
       <<hero_button>>, но текст на кнопке может меняться в зависимости от 
       значения modifier(Player). Например, если у игрока уже есть герой ему предложат
       перейти к нему, а если героя нет, то на кнопке будет надпись о создании 
       нового героя

    Функция modifier это лист из двух элементов: первый это строка с дополнительным
    ключем, а второй — аргументы для форматирования подходящей строки.
    """ 
    key = None
    modifier = None
    hider = None
    def __init__(self, key, modifier = None, hider = None):
        self.key = key
        self.modifier = modifier
        self.hider = hider
    def get_text(self, player : Player):
        moded_key  = self.key
        if self.hider != None:
            if self.hider(player): return None
        if self.modifier != None:
            if len(self.modifier(player))>1:
                moded_key = moded_key+self.modifier(player)[0]
                key_to_text =  txt.get(player, moded_key).format(*(self.modifier(player)[1]))
            else:
                 moded_key = moded_key+self.modifier(player)[0]
                 key_to_text =  txt.get(player, moded_key)
        else: return txt.get(player, moded_key)
        return key_to_text

    def is_pressed(self, buttpressed, player:Player) -> bool:
        if self.hider == None:
            return self == buttpressed
        else:
            if (self == buttpressed) and (self.hider(player) == False):
                return True
            else: return False

#--------------------------------------------------------------
# Объекты этого типа возвращаются в logicHandler чтобы 
# удобно обрабатывать результат precept'ов
#--------------------------------------------------------------
class Precept_return:
    exitcode = 0
    newstate = None
    args = []
    def __init__(self, exitcode = 0, newstate = None, args = []):
        self.exitcode = exitcode
        self.newstate = newstate
        self.args = args

#--------------------------------------------------------------

#--------------------------------------------------------------
all_states = []
class State:
    """Класс состояний, в которых находится игрок 
        Каждый объект состояния должен начинаться с s_
        Каждая функция precept'a состояния должна принимать первым 
        аргументом контекст, затем объект игрока"""
    id = None
    substate = 0
    name = None
    buttons = None
    welcome_precept =None
    body_precept = None
    has_bp = False
    has_wp = False
    markup = None
    def __init__(self, _name : str,  
                 buttons = None, 
                 welcome_precept = empty, 
                 body_precept = empty , 
                 markup = Markup([[]])):
        all_states.append(self)
        self.name = _name
        self.id = len(all_states)
        self.body_precept = body_precept
        self.buttons = buttons 
        self.welcome_precept = welcome_precept
        if body_precept != empty:
            self.has_bp = True
        if welcome_precept != empty:
            self.has_wp = True         
        self.markup = markup 
    def start_state(self, utilities, player : Player, args = [] ):
        a = args 
        if self.markup != None:
            a.append(self.markup)
        self.welcome_precept(utilities, player, a)

def find_state(name):
    for i in all_states:
        if name == i.name:
            return i
    return None

class StageSpec(enum.Enum):
    battle = 1
    descriptive = 0
    alternatives = 2
    skillcheck = 3
    not_defined = -1

class StageResult(enum.Enum):
    success = 0
    death = 1

encounter_rarities = []
class EncountersRarity():   
    def __init__(self, name, probability):
        self.name = name
        self.probability = probability
        self.id = len(encounter_rarities)
        encounter_rarities.append(self)
        
    def get_probability(self):
        if self.name == 'common':
            p = 0
            for i in encounter_rarities:
                p += i.probability
            return 1-p
        else:
            return self.probability
            
def get_rarity_random():
    p = random()
    rarity_limit = 0.0
    for i in encounter_rarities:
        rarity_limit += i.get_probability()
        if p<rarity_limit:
            return i
    return encounter_rarities[-1]

common = EncountersRarity('common', 0)
uncommon = EncountersRarity('uncommon', 0.3)
rare = EncountersRarity('rare', 0.2)


"""
    Journey это генератор последующих энкаунтеров и менеджер событий, которые происходят с героем игрока
"""
journeys = []
def find_journey(name):
    for i in journeys:
        if i.name == name:
            return i
    return None

class Journey:
    level = 0
    name = None
    encounter_queue = []
    prize = 0
    def __init__(self, name, level):
        self.name = name
        self.level = level
        journeys.append(self)

    def add_encounter(self, encounter = None , name = None, player = None):
        if encounter == None:
            if name == None:
                self.encounter_queue.append(self.generate_encounter(player))
            else:
                self.encounter_queue.append(self.find_encounter(name))
            self.encounter_queue[-1].journey = self
        else:
            encounter.journey = self
            self.encounter_queue.append(encounter)

    def start(self, utilities, player : Player):
        player.journey = self.name
        self.encounter_queue[0].start(utilities, player)
       
    def generate_enounter(self, player):
        pool =[]
        rarity = get_encounter_raity()
        for i in encounters:
            if (i.levels[0] <=  player.get_hero().level) and  (player.get_hero().level  <= i.levels[1]):
                if i.rarity.id == rarity.id:
                    pool.append(i)

        if len(pool) == 0:
            return encounters[randint(0,len(encounters)-1)]
        return pool[randint(0,len(pool)-1)]
                
    def find_encounter(self, name):
        for i in encounters:
            if i.name == name:
                return i
        return None
    def finish(self, utilities, player : Player):
        player.money += self.prize
        player.hero_id = 0 
        player.journey = 'None'
        player.encounter = 'None'
        player.send_message(utilities = utilities, key = 'finish_journey', markup = 'dont_change')
        if player.state == 'journey':
            player.set_state(utilities, 'town')
        if self.name == 'tutorial_journey':
            player.tutorial = 5
encounters = []
def find_encounter(name):
    for i in encounters:
        if i.name == name:
            return i
    return None
class Encounter:
    """
    Encounter это наибольшая самостоятельная единица повествования, состоящая из различных stages.
    Encounter необходимо создать заранее, а затем Journey будет подтягивать нужные ей Encncounters
    """
    levels = []
    stages = []
    rarity = None
    journey = None
    def __init__(self, name,  levels, rarity : EncountersRarity, stages = []):
        self.levels = levels
        self.stages = stages
        self.name = name 
        for i in self.stages:       
            i.encounter = self

        for i in encounters:
            if i.name == self.name:
                print('Same names for encounters: '+name)
                return None
        encounters.append(self)
    #ищет состояние по его id
    def find_stage(self, stage_id):
        for i in self.stages:
            if i.id == stage_id:
                return i
        return None
    #запускает encounter для игрока
    def start(self, utilities, player):
        self.start_stage( utilities, 0, player)
        player.encounter = self.name
        player.stage = 0

    #запускает определенный stage
    def start_stage(self, utilities, stage_id, player):
        print('starting stage '+str(stage_id))
        if stage_id == -1:
            self.finish(utilities, player)   
        player.stage = stage_id
        stage = self.find_stage(stage_id)
        if stage != None:
            stage.start(utilities, player)
    #завершает encounter    
    def finish(self, utilities,  player):
        self.journey.finish(utilities, player)
 
class Stage:
    """
        Stage — атомарная единица повествования, например битва с определенным типом монстров или
        проверка характеристик. 
    """   
    specialization = StageSpec.not_defined
    id : int #stage id used inside encounter
    next_stage : int  
    encounter = None
    markup = None
    def __init__(self, spec, id, next_stage,  w_precept = None,b_precept = None, markup = None, enemy = None):
        self.id = id
        self.next_stage = next_stage
        self.specialization = spec
        self.w_precept = w_precept
        self.b_precept = b_precept
        self.markup = markup
        self.enemy = enemy
    def start(self, utilities,  player):      
        self.w_precept(self, utilities, player)

        #self.finish(utilities,  player)

    def finish(self, utilities, player):
        self.encounter.start_stage(utilities, self.next_stage, player)
    def battle_round(self, utilities, player):
        if self.enemy == None: return
        hero = player.get_hero().to_creature()  
        enemy = self.enemy.refresh(player.get_hero().enemy_hp)
        print('round started')
        hero_damage, enemy_alive = hero.hit(enemy)
        if enemy_alive:
            enemy_damage, hero_alive = enemy.hit(hero)
            player.get_hero().enemy_hp = enemy.hp
            player.get_hero().hp = hero.hp
            if hero_alive:
                player.postpone_message(utilities, 'battle_round_alive', [hero_damage, enemy.get_name(player), enemy_damage, str(hero.hp), str(enemy.hp)], markup ='dont_change')
            else:
                player.postpone_message(utilities, 'battle_round_hero_died', [hero_damage, enemy_damage, str(hero.hp), str(enemy.hp)], markup ='dont_change')
        else:
            player.postpone_message(utilities, 'battle_round_win', [hero_damage], markup ='dont_change')
            player.get_hero().enemy_hp = -1
            self.finish(utilities, player)