
ru = 'ru'
en = 'en'

class Txt:
    """Класс, с помощью которого можно легко обращаться к строкам с нужным языком.
       возможно прикручу автоперевод. 
       Потом.

       name — имя строки, которую ищем
       key — языковой ключ
    """
    alltext = {}

    def add(self, lan : str, name : str, text : str ):
        newdict = {lan: text}
        self.alltext[name] = newdict
    
    def get(self, p, name):
        return self.alltext[name][p.language]
    def get_lan(self, lan, name):
        return self.alltext[name][lan]
txt = Txt()


txt.add(ru, 'hello', 'Добро пожаловать! \n  \nThe Hero — это простая игра-рогалик, где Вам нужно развивать свое поселение, создавая героев и отправляя их на задания. Сможете ли вы найти лучшую стратегию и сделать маленькую деревушку процветающим городом?')
txt.add(ru, 'nametaken', '❌ Имя уже занято')
txt.add(ru, 'namecorrupted', '❌ Имя содержит недопустимые символы')
txt.add(ru, 'setname', 'Другие игроки будут видеть вас как {}')
txt.add(ru, 'entername', 'Давайте познакомимся — как Вас зовут?')
txt.add(ru, 'next', '✅ Продолжить')
txt.add(ru, 'cancel', '❌ Отменить')
txt.add(ru, 'b_back', '◀️ Назад')
txt.add(ru, 'b_town_hero_create', '🌟 Нанять героя')
txt.add(ru, 'b_town_hero_select', '🌟 Герой')
txt.add(ru, 'b_town_journey', '🌍 Путешествие')
txt.add(ru, 'b_town_buildings', '🏘 Строения')
txt.add(ru, 'b_town_rule', '🏛 Управление')
txt.add(ru, 'tutorial_welcome', 'Так выглядит меню вашего поселения.\n\nВ ходе игры вам предстоит развивать город, а ресурсы для новых построек будут зарабатывать 🌟 герои. Давайте отправим одного из них в путешествие и посмотрим, что получится!\n\nНаймите первого 🌟 героя в своем городе. ')
txt.add(ru, 'playername', '{}')
txt.add(ru, 'tutorial_move_to_create_hero', '🌟Героем станет один из жителей вашего поселения. Вы выбираете из тех, кто есть сейчас. Герои — люди гордые, откажете один раз и потеряете навсегда.')
txt.add(ru, 'Ok', '✅ Хорошо')
txt.add(ru, 'hire', '💰 Нанять (1💰)')
txt.add(ru, 'next_hero', '⏩ Следующий (1💰)')
txt.add(ru, 'not_enough_money', '❌ Не хватает денег!')
txt.add(ru, 'create_hero', 'У вас {} 💰 монет\n\nГерой {}\n\n🔴 Сила: {}\n🟢 Ловкость: {}\n🔵 Интеллект: {}')
txt.add(ru, 'you_will_run_out_of_money', '❌ Вы не сможете нанять следующего героя.')
txt.add(ru, 'hero_bought', 'Вы приобрели героя по имени {}.')
txt.add(ru, 'tutorial_got_hero', 'Теперь у вас есть герой, который подойдет для первого испытания! Давайте зачистим 🏛 ратушу, чтобы вы могли управлять поселением. \n\nПерейдите в 🌍 Путешествия и выберите подходящее.')
txt.add(ru, 'b_tutorial_journey', '🏛 Очистить ратушу')
txt.add(ru, 'tutorial_hero_in_action', 'Ваш герой сейчас пытается зачистить ратушу. Давайте поможем ему во вкладке 🌍 путешествия')

txt.add(ru, 'b_menu', '⚙️ Вернутся в меню')
txt.add(ru, 'journey_start_no_journey_have_hero', 'У вас нет ни одного активного 🌍 путешествия. Выберите из списка доступных и отправьте героя сражаться!')
txt.add(ru, 'journey_start_no_journey_no_hero', 'Пока что вам некого отправить в путешествие! Вернитесь в меню города и наймите нового 🌟 героя.')
txt.add(ru, 'choose_enhancement', '⚜️ Выбрать улучшение')
txt.add(ru, 'journey_start_hero_in_action', 'Ваш герой сейчас в путешествии!')
txt.add(ru, 'w_journey', 'Герой {} в путешествии!\n\n⚜️ Доступно улучшений: {}.\n❤️ Здоровье: {}.')
txt.add(ru, 'finish_journey', 'Ваш герой закончил свой путь! Подробности можно посмотреть во вкладке 🌍 путешествия.')
txt.add(ru, 'b_continue_journey', '➡️ Продолжить путешествие')
txt.add(ru, 'tq_e1_s0_w_text', '{} острожно подходит к заброшенной ратуше. Кажется, что здесь давно никого не было. Герой приоткрывает центральную дверь и проникает внутрь.\n\nГде-то на втором этаже слышны приглушенные шаги. {} достает оружие и осторожно ступает по лестнице наверх.')
txt.add(ru, 'tq_e1_s1_w_text', 'Стоило герою только поднятся на второй этаж и он лицом к лицу столкнулся с ☠️ грабителем!')

txt.add(ru, 'start_battle','⚔️ Битва')
txt.add(ru, 'creature_robber', 'Грабитель')


ru_hero_peon_surnames = ['Прутков', "Козлов", "Кузнец", "Соха", "Косой", "Кривой", "Дуболомов", "Пастух", "Холуй", "Лакей", "Деревяшко", "Молот", "Столяр", "Синяк", "Лесник"]
ru_hero_peon_names = [ 'Вано', 'Петька', 'Игорек', 'Прохор', 'Козьма', "Сорин", "Митрут", "Марку", "Равзан", "Назар"]
for i in range(len(ru_hero_peon_names)):
    txt.add(ru, 'hero_cheap_name'+str(i), ru_hero_peon_names[i])
for i in range(len(ru_hero_peon_surnames)):
    txt.add(ru, 'hero_cheap_surname'+str(i), ru_hero_peon_surnames[i])

ru_weapon_common_names = ['Гнутый', 'Ржавый', 'Старый', 'Потрепанный', 'Тупой' ]
for i in range(len(ru_weapon_common_names)):
    txt.add(ru, 'weapon_common_names'+str(i), ru_weapon_common_names[i])

txt.add(ru, 'weapon_common_sword', 'короткий меч')

txt.add(ru, 'battle_hero_deal_damage' ,'🌟 Герой попадает и наносит ❤️{} урона!')
txt.add(ru, 'battle_hero_win' ,'🌟 Герой наносит ❤️{} урона и убивает противника! ')
txt.add(ru, 'battle_hero_misses','🌟 Герой не смог попасть по врагу!' )

txt.add(ru, 'battle_hero_lose' ,'{} наносит ❤️{} урона и убивает героя!\n\nКакая трагедия!')
txt.add(ru, 'battle_enemy_deal_damage','{} попадает и наносит ❤️{} урона! Больно!')
txt.add(ru, 'battle_enemy_misses', '{} промахивается, так-то!')
txt.add(ru, 'battle_round_alive', 'Раунд закончен!\n\n🌟 Герой нанес ❤️{} урона.\n☠️ {} нанес ❤️{} урона! \n\nУ 🌟 героя осталось ❤️{} здоровья.\nУ ☠️ противника осталось ❤️{} здоровья.')
txt.add(ru, 'battle_round_hero_died', 'Ваш герой нанес ❤️{} и получил ❤️{} урона!\n\nОн погиб, проклятье! ')
txt.add(ru, 'battle_round_win', 'Ваш герой нанес ❤️{} и убил противника! Отлично!')