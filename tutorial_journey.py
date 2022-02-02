from classes import *
from languages import *
from Bot import MyBot


button_next = Button('next')
m_tq_eq_s0 = Markup([[button_next]])

def w_tq_e1_s0(stage : Stage, utilities, player : Player, args = []):
    player.postpone_message(utilities, 'tq_e1_s0_w_text', [player.get_hero().name, player.get_hero().name], markup = m_tq_eq_s0)

   
def b_tq_e1_s0(stage : Stage, utilities, player : Player, args = []):
    buttpressed = stage.markup.find_button(player, args[0])
    if buttpressed == button_next:
        stage.finish(utilities, player)
tq_e1_s0 = Stage(StageSpec.descriptive, 0, 1, w_precept = w_tq_e1_s0, b_precept = b_tq_e1_s0, markup = m_tq_eq_s0)


#----------------------------------------------------------------------------------------------------
#грабитель в ратуше
robber = Creature('creature_robber',
                  6, 6, 1,
                  Attributes(1,2,0),
                  0, 0)
def w_tq_e1_s1(stage : Stage,utilities : Utilities, player : Player, args = [] ):
    print('welcome')
    player.postpone_message(utilities, 'tq_e1_s1_w_text', markup = m_tq_eq_s1)
    player.get_hero().enemy_hp = stage.enemy.hp

def b_tq_e1_s1(stage : Stage, utilities : Utilities, player : Player, args = [] ):
    buttpressed = stage.markup.find_button(player, args[0])
    if buttpressed == button_start_battle:
        stage.battle_round(utilities, player)

button_start_battle = Button('start_battle')
m_tq_eq_s1 = Markup([[button_start_battle]])

tq_e1_s1 = Stage(StageSpec.battle, 1, -1, 
                 w_precept = w_tq_e1_s1, 
                 b_precept = b_tq_e1_s1, 
                 markup = m_tq_eq_s1, enemy = robber)

tq_e1 = Encounter('tq_e1', [1, 10], common, [tq_e1_s0, tq_e1_s1])
tutorial_journey = Journey(name = 'tutorial_journey', level = 1)
tutorial_journey.add_encounter(tq_e1)   