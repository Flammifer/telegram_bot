from classes import *
from languages import *
from tutorial_journey import *

#--------------------------------------------------------------
# Стартовое меню
#--------------------------------------------------------------
def w_reg(utilities, player, args = []):
    player.send_message(utilities,  'entername')
    Precept_return(0, None)

def b_reg(utilities, player, args = []):
    _name = args[0]
    if _name.isalpha():
        if select(player for player in Player if (player.name.lower() == _name.lower()) and _name != 'None'):
            player.send_message(utilities, 'nametaken')
        else:
            player.stringbuffer = _name
            return Precept_return(0, 'reg_confirm', [_name])
    else: player.send_message(utilities,  'namecorrupted')
    return Precept_return(0, None)

s_reg = State('reg', body_precept = b_reg, welcome_precept = w_reg)

#--------------------------------------------------------------
# Подтверждение имени при регистрации
#--------------------------------------------------------------
def w_reg_confirm(utilities, player, args):
    player.send_message(utilities, 'setname',  formatparams = args, markup =m_reg_confirm)


    return Precept_return(0, None)

def b_reg_confirm(utilities, player, args):
    butpresed = m_reg_confirm.find_button(player, args[0])
    if butpresed == button_back:
        return Precept_return(0, 'reg')
    if butpresed == button_continue:
        _name = player.stringbuffer
        if select(player for player in Player if (player.name.lower() == _name.lower()) and _name != 'None'):
                player.send_message(utilities, 'nametaken')
        else:
            player.name = _name
            return Precept_return(0, 'town')
    return Precept_return(0, None)

button_continue = Button('next')
button_cancel = Button('cancel')
m_reg_confirm = Markup([[ button_cancel, button_continue]])
s_reg_confirm = State('reg_confirm', 
                      welcome_precept= w_reg_confirm, 
                      body_precept = b_reg_confirm,
                      markup=m_reg_confirm)

#--------------------------------------------------------------
# Базовое меню города 
#--------------------------------------------------------------
def town_herobutton_modifier(player:Player):
    if player.hero_id == 0:
        return ['create']
    else: 
        return ['select']
town_journeybutton = Button('b_town_journey')    
town_herobutton = Button('b_town_hero_', town_herobutton_modifier)
town_buildingsbutton = Button('b_town_buildings')
town_rulebutton = Button('b_town_rule')
m_town = Markup([[town_journeybutton, town_herobutton], [town_buildingsbutton , town_rulebutton]])

def w_town(utilities, player, args):
    if player.tutorial == 1:
        player.send_message(utilities,  'tutorial_welcome', markup = m_town )
    if player.tutorial  == 2 :
        player.send_message(utilities,   'tutorial_got_hero', markup = m_town )
    if player.tutorial > 2 and player.tutorial < 5 :
        player.send_message(utilities,   'tutorial_hero_in_action', markup = m_town )
    return Precept_return(0, None)

def b_town(utilities, player, args):
    butpresed = m_town.find_button(player, args[0])
    if ((butpresed == town_herobutton) and (player.tutorial == 1)):   
        return Precept_return(0, 'tutorial_move_to_create_hero')
    if ((butpresed == town_journeybutton) and (player.tutorial > 1 or player.tutorial == 0)): 
        return Precept_return(0, 'journey_start')

    return Precept_return(0, None)

s_town = State('town',   welcome_precept = w_town, 
                         body_precept = b_town, 
                         markup = m_town)


#--------------------------------------------------------------
# Информация о создании героя
#--------------------------------------------------------------
button_ok = Button('Ok')
m_tutorial_move_to_create_hero = Markup([[button_ok]])

def w_tutorial_move_to_create_hero(utilities, player, args):
    player.send_message(utilities, 'tutorial_move_to_create_hero', markup = s_tutorial_move_to_create_hero.markup)
    return Precept_return(0, None)

def b_tutorial_move_to_create_hero(utilities, player, args):
    if m_tutorial_move_to_create_hero.find_button(player, args[0]) == button_ok:
        return Precept_return(0, 'create_hero')
    return Precept_return(0, None)

s_tutorial_move_to_create_hero = State('tutorial_move_to_create_hero', 
                                 welcome_precept = w_tutorial_move_to_create_hero, 
                                 body_precept = b_tutorial_move_to_create_hero, 
                                 markup = m_tutorial_move_to_create_hero)


#--------------------------------------------------------------
# Меню создания героя
#--------------------------------------------------------------
button_next_hero = Button('next_hero')
button_hire = Button('hire')
button_cancel = Button('cancel')
m_create_hero = Markup([[button_next_hero], [button_hire], [button_cancel]])


def send_hero_card(utilities, player, hero): 
    player.send_message(utilities,   'create_hero', formatparams = (player.money, hero.name, hero.strength, hero.agility, hero.intelligence), markup = m_create_hero)


def w_create_hero(utilities, player, args):
    if player.temporary_hero_id == 0:
        hero = create_new_hero(utilities, player)
    else:
        hero = list(select(hero for hero in Hero if hero.id == player.temporary_hero_id))[0]
    send_hero_card(utilities, player, hero)   

    return Precept_return(0, None)

def b_create_hero(utilities, player, args):
    butpressed = m_create_hero.find_button(player, args[0])
    if butpressed == button_next_hero:
        if (player.money == 2):
            player.send_message(utilities,   'you_will_run_out_of_money', markup = m_create_hero)
            return Precept_return(0, None)

        if (player.debit(1)):        
            hero = Hero.get(id = player.temporary_hero_id)
            hero.delete()
            hero = create_new_hero(utilities, player)
            send_hero_card(utilities, player, hero)           
        else:
            player.send_message(utilities,   'not_enough_money')

    if butpressed == button_hire:
        if (player.debit(1)):
            hero = Hero.get(id = player.temporary_hero_id)
            player.hero_id = hero.id
            player.tutorial = 2
            player.send_message(utilities,  'hero_bought', formatparams = [hero.name])
            return Precept_return(0, 'town')
    return Precept_return(0, None)
    if butpressed == button_cancel:
        return Precept_return(0, 'town')
s_create_hero = State('create_hero', 
                      welcome_precept = w_create_hero, 
                      body_precept = b_create_hero, 
                      markup = m_create_hero)

#--------------------------------------------------------------
# Меню путешествий
#--------------------------------------------------------------
def tutorial_journey_hider(player:Player):
    return (player.tutorial != 2)

def continue_journey_hider(player:Player):
    return (player.journey == 'None')
button_continue_journey = Button('b_continue_journey', hider = continue_journey_hider)
button_tutorial_journey = Button('b_tutorial_journey', hider = tutorial_journey_hider)

button_back = Button('b_back')
m_journey_start = Markup([[button_continue_journey],[button_tutorial_journey], [button_back]])

def w_journey_start(utilities, player, args = None):
    if player.journey == 'None':
        if player.hero_id > 0:
            player.send_message(utilities,  'journey_start_no_journey_have_hero', markup = m_journey_start)
        else: 
            player.send_message(utilities,  'journey_start_no_journey_no_hero', markup = m_journey_start)
    else:
        player.send_message(utilities,  'journey_start_hero_in_action', markup = m_journey_start)

    return Precept_return(0, None)

def b_journey_start(utilities, player, args = None):   
    buttpressed = m_journey_start.find_button(player, args[0])

    if button_back.is_pressed(buttpressed, player):
        return Precept_return(0, 'town')

    if button_tutorial_journey.is_pressed(buttpressed, player):
        player.tutorial = 3
        return Precept_return(0, 'journey')

    if button_continue_journey.is_pressed(buttpressed, player):
        return Precept_return(0, 'journey')

    return Precept_return(0, None)


s_journey_start = State('journey_start', 
                        welcome_precept=w_journey_start, 
                        body_precept=b_journey_start, 
                        markup = m_journey_start)

#--------------------------------------------------------------
# Экран путешествия
#--------------------------------------------------------------
button_choose_abilities = Button('choose_enhancement')  
m_journey = Markup([[button_back, button_choose_abilities]])

def w_journey(utilities, player, args = None):
    player.send_message(utilities,  'w_journey', formatparams = [player.get_hero().name, player.get_hero().get_enhancements(), player.get_hero().hp],  markup = m_journey)
    player.postponed_message_sended = 0
    if player.tutorial == 3:
        player.tutorial= 4
        tutorial_journey.start(utilities, player)
        return Precept_return(0, None)

def b_journey(utilities, player : Player, args = None):
    if args != None:
        buttpressed = m_journey.find_button(player, args[0])
        if buttpressed == button_back:
            return Precept_return(0, 'town')
        player.get_stage().b_precept(player.get_stage(), utilities, player, args)
    else:   
        player.send_postponed_message(utilities)
    return Precept_return(0, None)

button_menu = Button('b_menu')

journey = State('journey', 
                welcome_precept = w_journey, 
                body_precept = b_journey,
                markup = m_journey)