import random
import telebot
from json import load
from time import sleep
from telebot import types
from collections import defaultdict
from utils import *
from database import *
from questions import *


token = open('data/token.txt', 'r').read()
bot = telebot.TeleBot(token)
admin_ids = [273440998, 486330780]
forward_ids = [273440998, 486330780]
question_groups = ['+-a+-(+-b), целые [1; 50]',
                   '+-a+-(+-b), десятичные дроби [1; 20)',
                   'ax^2 + bx + c = 0, определение параметров',
                   'ax^2 + bx + c = 0, дискриминант']
help_text = open('data/help.txt', 'r', encoding='cp1251').read()
stickers = load(open('data/stickers.json', 'r'))

    
def init_user(message):
    log_message(message)
    user = User.get_or_none(User.chat_id == message.chat.id)
    if user is None:
        user = User.create(chat_id=message.chat.id, name=get_name(message.from_user))
        LastCommand.create(user=user, command='init')
        LastTestInfo.create(user=user)
    return user
    

@bot.message_handler(commands=['start', 'help'])
def start(message):
    user = init_user(message)
    last_command = user.last_command
    last_command.command = 'start'
    last_command.save()
    bot.send_message(message.chat.id, help_text, parse_mode='html')
    
    
@bot.message_handler(commands=['list_tests'])
def list_tests(message):
    user = init_user(message)
    last_command = user.last_command
    last_command.command = 'list_tests'
    last_command.save()
    res = ''
    for test in Test.select():
        questions = [str(question.question_id) for question in test.questions]
        res += '{}. {}. {} вопросов, включает темы {}\n\n'.format(test.id, test.name, test.n_samples, ', '.join(questions))
    if res == '':
        res = 'Пока что не создано ни одного теста.'
    bot.send_message(message.chat.id, res, parse_mode='html')
    
    
@bot.message_handler(commands=['show_results'])
def show_results(message):
    user = init_user(message)
    last_command = user.last_command
    last_command.command = 'show_results'
    last_command.save()
    res = ''
    for num, achievement in enumerate(Achievement.select().where(Achievement.user == user), 1):
        res += '{}. {}. {}/{}, {}\n'.format(num, achievement.test.name, achievement.correct_answers, achievement.test.n_samples, str_time(achievement.elapsed_time))
    if res == '':
        res = 'У тебя нет ни одного пройденного теста.'
    bot.send_message(message.chat.id, res, parse_mode='html')
    
    
@bot.message_handler(commands=['show_all_results'])
def show_all_results(message):
    user = init_user(message)
    last_command = user.last_command
    if user.chat_id not in admin_ids:
        last_command.command = 'show_all_results_denied'
        last_command.save()
        bot.send_message(message.chat.id, 'Для выполнения данной команды нужно обладать правами администратора.', parse_mode='html')
    else:
        last_command.command = 'show_all_results'
        last_command.save()
        res = ''
        for user_num, user in enumerate(User.select(), 1):
            add = ''
            for num, achievement in enumerate(Achievement.select().where(Achievement.user == user), 1):
                add += '- {}. {}/{}, {}\n'.format(achievement.test.name, achievement.correct_answers, achievement.test.n_samples, str_time(achievement.elapsed_time))
            if add != '':
                res += '{}. {}:\n'.format(user_num, user.name)
                res += add + '\n'
        if res == '':
            res = 'Никто еще не проходил тесты.'
        bot.send_message(message.chat.id, res, parse_mode='html')
    
    
@bot.message_handler(commands=['create_test'])
def create_test(message):
    user = init_user(message)
    last_command = user.last_command
    if user.chat_id not in admin_ids:
        last_command.command = 'create_test_denied'
        last_command.save()
        bot.send_message(message.chat.id, 'Для выполнения данной команды нужно обладать правами администратора.', parse_mode='html')
    else:
        last_command.command = 'create_test'
        last_command.save()
        bot.send_message(message.chat.id, 'Введите имя теста:', parse_mode='html')
    
                
@bot.message_handler(commands=['edit_test'])
def edit_test(message):
    user = init_user(message)
    last_command = user.last_command
    if user.chat_id not in admin_ids:
        last_command.command = 'create_test_denied'
        last_command.save()
        bot.send_message(message.chat.id, 'Для выполнения данной команды нужно обладать правами администратора.', parse_mode='html')
    else:
        last_command.command = 'edit_test'
        last_command.save()
        res = 'Выберите id теста:\n\n'
        for test in Test.select():
            res += '{}. {}\n'.format(test.id, test.name)
        bot.send_message(message.chat.id, res, parse_mode='html')
        
     
@bot.message_handler(commands=['start_test'])
def start_test(message):
    user = init_user(message)
    last_command = user.last_command
    last_command.command = 'start_test'
    last_command.save()
    res = 'Выберите id теста:\n\n'
    for test in Test.select():
        res += '{}. {}\n'.format(test.id, test.name)
    bot.send_message(message.chat.id, res, parse_mode='html')
        
        
@bot.message_handler(content_types=['text'])
def reply_all_messages(message):
    user = init_user(message)
    last_command = user.last_command
    if last_command.command == 'create_test':
        res = 'Выберите список групп вопросов для этого теста:\n\n'
        for num, question_group in enumerate(question_groups, 1):
            res += '{}) {}\n'.format(num, question_group)
        last_command.command = 'create_test1'
        last_command.test_name = message.text
        last_command.save()
        bot.send_message(message.chat.id, res, parse_mode='html')
    elif last_command.command == 'create_test1':
        ids = parse_int_list(message.text)
        if len(ids) == 0:
            bot.send_message(message.chat.id, 'Список должен быть не пустым', parse_mode='html')
            return
        for id in ids:
            if id < 1 or id > len(question_groups):
                bot.send_message(message.chat.id, 'Недопустимый номер вопроса: {}'.format(id), parse_mode='html')
                return
        last_command.command = 'create_test2'
        last_command.question_ids = message.text
        last_command.save()
        bot.send_message(message.chat.id, 'Введите количество вопросов в тесте:', parse_mode='html')
    elif last_command.command == 'create_test2':
        n_samples = parse_int_list(message.text)
        if len(n_samples) != 1 or n_samples[0] == 0:
            bot.send_message(message.chat.id, 'Введите корректное количество вопросов в тесте:', parse_mode='html')
            return
        try:
            test_name = last_command.test_name
            question_ids = parse_int_list(last_command.question_ids)
            question_ids = unique_elements(question_ids)
            test = Test.create(n_samples=n_samples[0], name=test_name)
            for question_id in question_ids:
                Question.create(test=test, question_id=question_id)
            last_command.command = 'success'
            last_command.save()
            bot.send_message(message.chat.id, 'Тест "{}" успешно создан'.format(test_name), parse_mode='html')
        except Exception as E:
            last_command.command = 'invalid'
            last_command.save()
            bot.send_message(message.chat.id, str(E), parse_mode='html')
            
            
    elif last_command.command == 'edit_test':
        test_id = parse_int_list(message.text)
        if len(test_id) != 1:
            bot.send_message(message.chat.id, 'Введите корректное id теста:', parse_mode='html')
            return
        test = Test.get_or_none(Test.id == test_id[0])
        if test is None:
            bot.send_message(message.chat.id, 'Введите корректное id теста:', parse_mode='html')
            return
        last_command.command = 'edit_test1'
        last_command.edit_test_id = test_id[0]
        last_command.save()
        bot.send_message(message.chat.id, 'Введите новое имя теста (или прочерк, чтобы оставить прежнее):', parse_mode='html')
    elif last_command.command == 'edit_test1':
        last_command.test_name = message.text
        res = 'Введите список групп вопросов для этого теста (или прочерк, чтобы оставить прежний):\n\n'
        for num, question_group in enumerate(question_groups, 1):
            res += '{}) {}\n'.format(num, question_group)
        last_command.command = 'edit_test2'
        last_command.save()
        bot.send_message(message.chat.id, res, parse_mode='html')
    elif last_command.command == 'edit_test2':
        if message.text != '-':
            ids = parse_int_list(message.text)
            if len(ids) == 0:
                bot.send_message(message.chat.id, 'Список должен быть не пустым', parse_mode='html')
                return
            for id in ids:
                if id < 1 or id > len(question_groups):
                    bot.send_message(message.chat.id, 'Недопустимый номер вопроса: {}'.format(id), parse_mode='html')
                    return
        last_command.command = 'edit_test3'
        last_command.question_ids = message.text
        last_command.save()
        bot.send_message(message.chat.id, 'Введите количество вопросов в тесте (или прочерк, чтобы оставить прежнее):', parse_mode='html')
    elif last_command.command == 'edit_test3':
        n_samples = parse_int_list(message.text)
        if message.text != '-' and (len(n_samples) != 1 or n_samples[0] == 0):
            bot.send_message(message.chat.id, 'Введите корректное количество вопросов в тесте:', parse_mode='html')
            return
        try:
            test_name = last_command.test_name
            question_ids = parse_int_list(last_command.question_ids)
            question_ids = unique_elements(question_ids)
            test = Test.get(Test.id == last_command.edit_test_id)
            if test_name != '-':
                test.name = test_name
            if message.text != '-':
                test.n_samples = n_samples[0]
            test.save()
            if last_command.question_ids != '-':
                Question.get(Question.test == test).delete_instance()
                for question_id in question_ids:
                    Question.create(test=test, question_id=question_id)
            last_command.command = 'success'
            last_command.save()
            bot.send_message(message.chat.id, 'Тест "{}" успешно обновлен'.format(test.name), parse_mode='html')
        except Exception as E:
            print(E)
            last_command.command = 'invalid'
            last_command.save()
            bot.send_message(message.chat.id, str(E), parse_mode='html')    
    
    elif last_command.command == 'start_test':
        test_id = parse_int_list(message.text)
        if len(test_id) != 1:
            bot.send_message(message.chat.id, 'Введите корректное id теста:', parse_mode='html')
            return
        test = Test.get_or_none(Test.id == test_id[0])
        if test is None:
            bot.send_message(message.chat.id, 'Введите корректное id теста:', parse_mode='html')
            return
        question, answer = get_question(test)
        last_command.command = 'process_test'
        last_test = user.last_test
        last_test.test = test
        last_test.questions = 0
        last_test.correct_answers = 0
        last_test.start_time = time()
        last_test.last_answer = answer
        last_test.save()
        last_command.save()
        for chat_id in unique_elements([message.chat.id] + forward_ids):
            bot.send_message(chat_id, 'Задание №{}. {}'.format(last_test.questions + 1, question), parse_mode='html')
    elif last_command.command == 'process_test':
        last_test = user.last_test
        answer_len = len(parse_float_list(message.text))
        ok_len = len(parse_float_list(last_test.last_answer))
        if answer_len != ok_len:
            res = 'Введите корректное число'
            if ok_len >= 2:
                res = 'Введите корректную последовательность из {} чисел'.format(ok_len)
            bot.send_message(message.chat.id, res, parse_mode='html')
            return
        if check_answer(last_test.last_answer, message.text):
            last_test.correct_answers += 1
            last_test.save()
            res = 'Правильно!\n\n'
        else:
            res = 'Неправильно, ответ равен {}\n\n'.format(last_test.last_answer)
        last_test.questions += 1
        if last_test.questions == last_test.test.n_samples:
            last_command.command = 'success_test'
            last_command.save()
            res += '<b>Итоговый результат</b>: {}/{}.\n{}\n\n'.format(last_test.correct_answers, last_test.questions, get_text_comment(last_test.get_percentage()))
            elapsed_time = round_to(last_test.get_elapsed_time(), 1)
            res += '<b>Затраченное время</b>: {}.\n\n'.format(str_time(elapsed_time))
            achievement = Achievement.get_or_none(Achievement.user == last_test.user, Achievement.test == last_test.test)
            if achievement is None:
                achievement = Achievement.create(user=last_test.user, test=last_test.test, correct_answers=last_test.correct_answers, elapsed_time=elapsed_time)
            sticker = ''
            if (achievement.correct_answers, -achievement.elapsed_time) < (last_test.correct_answers, -elapsed_time):
                improvement_message = ''
                if achievement.correct_answers < last_test.correct_answers:
                    sticker = 'quality'
                    if last_test.correct_answers - achievement.correct_answers == 1:
                        improvement_message += ' на 1 правильный ответ'
                    elif last_test.correct_answers - achievement.correct_answers <= 4:
                        improvement_message += ' на {} правильных ответа'.format(last_test.correct_answers - achievement.correct_answers)
                    else:
                        improvement_message += ' на {} правильных ответов'.format(last_test.correct_answers - achievement.correct_answers)
                if achievement.elapsed_time > elapsed_time:
                    sticker = 'speed'
                    if improvement_message != '':
                        improvement_message += ' и '
                    else:
                        improvement_message += ': '
                    improvement_message += 'стал быстрее на {}'.format(str_time(achievement.elapsed_time - elapsed_time))
                res += 'Ты улучшил свой персональный рекорд{}!'.format(improvement_message)
                if achievement.correct_answers < last_test.correct_answers:
                    sticker = 'quality'
                achievement.correct_answers = last_test.correct_answers
                achievement.elapsed_time = elapsed_time
                achievement.save()
            if last_test.correct_answers == last_test.questions and sticker != 'speed':
                sticker = 'maximum'
            if last_test.get_percentage() < 0.5:
                sticker = 'bad'
            for chat_id in unique_elements([message.chat.id] + forward_ids):
                bot.send_message(chat_id, res, parse_mode='html')
                if sticker != '':
                    bot.send_sticker(chat_id, stickers[sticker])
        else:
            question, answer = get_question(last_test.test)
            last_test.last_answer = answer
            last_test.save()
            res += 'Задание №{}. {}'.format(last_test.questions + 1, question)
            for chat_id in unique_elements([message.chat.id] + forward_ids):
                bot.send_message(chat_id, res, parse_mode='html')

@bot.message_handler(content_types=['sticker'])
def reply_all_messages(message):
    print(message.sticker.file_id)
    
            
def log_message(message):
    for forward_id in forward_ids:
        if forward_id != message.chat.id:
            bot.forward_message(forward_id, message.chat.id, message.message_id)


if __name__ == '__main__':
    restarts = 0
    while True:
        try:
            print('Start polling')
            bot.polling(none_stop=True)
        except Exception as E:
            print('Some exception while polling')
            print(E)
            sleep_time = 10
            print('Sleep for {} seconds...'.format(sleep_time))
            sleep(sleep_time)
            restarts += 1
            print('Restart #{}'.format(restarts))
