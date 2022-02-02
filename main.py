from telegram import *
from token_file import mytoken
from telegram.ext import *
from pony.orm import *
import logging
from classes import *
from languages import *
from tutorial_journey import *
from states import *
from Bot import MyBot
import time
from threading import *


def startHandler(update : Update, context : CallbackContext):  
    utilities = Utilities(mybot, context, update)
    with db_session:
        if len(list(select(player for player in Player if player.chat_id == update.effective_chat.id))) == 0:
            town = Town(player = 0, town_hall = 0, level = 1)
            town.flush()
            player = Player(name = 'None', 
                       chat_id = update.effective_chat.id, 
                       state = 'reg', 
                       isAdmin = 0, 
                       language = ru, 
                       tutorial = 1, 
                       money = 15, 
                       level = 1, 
                       hero_id = 0,
                       temporary_hero_id = 0,
                       town = town.id, 
                       encounter = 'None', 
                       stage = -1, 
                       journey = 'None')          
            player.flush()
            player.flush()
            town.player = player.id
            town.flush()
            hero = Hero()
            hero.ini(player)
            player.send_message(utilities,  'hello')
            player.set_state(utilities, state_name = 'reg')  
            print('A new player started')


        else:
            pass
#--------------------------------------------------------------
# Основная функция универсальной обработки команд: принимает
# на вход текстовую команду, смотрит на текущее состояние игрока
# и выполняет указания этого состояния с аргументом, который 
# указал игрок
#--------------------------------------------------------------
def logicHandler(update : Update, context : CallbackContext):
    utilities = Utilities(mybot, context, update)
    with db_session:
        player = list(select(player for player in Player if player.chat_id == update.effective_chat.id))
        if len(player)>0: player = player[0]
        else: 
            return
        state = find_state(player.state)
        text = update.effective_message.text
        #--------------------------------------------------------------
        #теперь игрок и состояние идентифицированы и можно
        #менять значения и сокращадь код
        #выполняем универсальный handler и принимаем типовой ответ
        #--------------------------------------------------------------
        if state.has_bp:     
            result = state.body_precept(utilities, player, [text])
            player.flush()
            if result.newstate != None:
                player.set_state(utilities = utilities, state_name = result.newstate, args = result.args)
        commit()

def loadplayers(mybot : MyBot) -> bool:
    return True

mybot = MyBot(mytoken, logicHandler, startHandler)
loadplayers(mybot)


def logic_thread():
    utilities = Utilities(mybot)
    while True:
        with db_session:

            localtime = time.localtime()
            #result = time.strftime("%I:%M:%S %p", localtime)
            time.sleep(0.2)
            players_in_journey = list(select(player for player in Player if (player.state =='journey')))
            for i in players_in_journey:
                journey.body_precept(utilities, i, None)
               
logic_thread()






