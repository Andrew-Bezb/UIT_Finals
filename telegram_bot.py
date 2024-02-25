# -*- coding: utf-8-sig -*-
import os
import time
import sys
import json

import telebot
from telebot import types
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
from thefuzz import fuzz, process

from db_requests import db

with open('config.json', 'r') as file:
    content = json.load(file)
    token = content['tg_token']
    print('bot token: ' + token)

bot_photos = {}
sessions = {}
admin_session = {}

# telegram init
bot = telebot.TeleBot(token)


# call parser


def sim_parse(call):  # chat_id, message_id, data = sim_parse(call)
    return call.message.chat.id, call.message.id, call.data


def adv_parse(call):  # chat_id, message_id, data, text, keyb = adv_parse(call)
    return call.message.chat.id, call.message.id, call.data, call.message.text, call.message.reply_markup


def freq_sort(list_):
    summ = sum(list_)
    if summ == 0:
        return list_
    for index, item in enumerate(list_):
        list_[index] = int((item / summ) * 100)
    return list_


def words_magick(word):
    tags = db.get_table_by_name('Tags', with_id=True)
    tags_list = [i[1] for i in tags]
    result = process.extract(word, tags_list, scorer=fuzz.partial_token_sort_ratio)
    result = [i for i in result if i[1] > 59]
    freq_list = []
    for item in result:
        for tag in tags:
            if tag[1] == item[0]:
                freq_list.append(tag[2])
                break
    freq_list = freq_sort(freq_list)
    final_res = []
    for index, item in enumerate(result):
        item = item[0], item[1] + freq_list[index]
        final_res.append(item)
    final_res = sorted(final_res, key=lambda index: index[1], reverse=True)
    final_res_big = []
    for item in final_res:
        for tag in tags:
            if tag[1] == item[0]:
                item = tag[0], tag[1], item[1], tag[3]
                final_res_big.append(item)
    return final_res_big[:9]


def del_photo(chat_id):
    if 'last_bot_image_id' in sessions[chat_id]:
        if sessions[chat_id]['last_bot_image_id']:
            bot.delete_message(chat_id, sessions[chat_id]['last_bot_image_id'])
            sessions[chat_id]['last_bot_image_id'] = 0


def send_photo(chat_id, img_name, path):
    if img_name in bot_photos:
        m = bot.send_photo(chat_id, bot_photos[img_name])
        sessions[chat_id]['last_bot_image_id'] = m.message_id
        print('image with tg id send')
    else:
        if os.path.isfile(path):
            with open(path, 'rb') as photo:
                print('image send')
                m = bot.send_photo(chat_id, photo)
                sessions[chat_id]['last_bot_image_id'] = m.message_id
                bot_photos[img_name] = m.photo[0].file_id


# main keyboard
start_menu_keyb = InlineKeyboardMarkup()
start_menu_keyb.add(InlineKeyboardButton('Список программ', callback_data='c;programs'))
start_menu_keyb.add(InlineKeyboardButton('Поиск инструкций', callback_data='c;tag'))
start_menu_keyb.add(InlineKeyboardButton('Добавить инструкцию', callback_data=' '))


# callback legend
# m; - movement for sliders
#
# c; - customer side
#   p; - list of programs
#   pm; - transition to manuals
#   mam; - list of manuals
#   mtx; - transition to texts
#   t; - texts
#   pos; - resolution of problems i.e. good manual
#     ci; - variation with cliks
#   sc; - score related
#   prv; - pre review
#   tag; - tag search
#   tt; - tag list
#   tet - tag text gen
#   neg; - negative instruction expirience
#
#
#
#
#
#
# a; - admin side
#
#
#

# key-gen territory

# def key_gen(list_, num, fix_poz=5, flag="x", flag2="f"):
#     if len(list_) % 5 == 1:
#         fix_poz = 4
#     vkinl = VkKeyboard(**settings2)
#     if ((num + 1) * fix_poz) < len(list_):
#         end_ = ((num + 1) * fix_poz)
#     else:
#         end_ = len(list_)
#     for x in range(num * fix_poz, end_):
#         vkinl.add_callback_button(label=list_[x], color=VkKeyboardColor.SECONDARY,
#                                   payload={"type": flag2 + ' ;' + list_[x] + '; ' + str(x)})
#         vkinl.add_line()
#     if num == 0 and end_ != len(list_):
#         vkinl.add_callback_button(label="Next", color=VkKeyboardColor.PRIMARY,
#                                   payload={"type": flag + ' ' + str(num + 1)})
#     elif num != 0 and end_ == len(list_):
#         vkinl.add_callback_button(label="Back", color=VkKeyboardColor.PRIMARY,
#                                   payload={"type": flag + ' ' + str(num - 1)})
#     elif num != 0:
#         vkinl.add_callback_button(label="Next", color=VkKeyboardColor.PRIMARY,
#                                   payload={"type": flag + ' ' + str(num + 1)})
#         vkinl.add_callback_button(label="Back", color=VkKeyboardColor.PRIMARY,
#                                   payload={"type": flag + ' ' + str(num - 1)})
#     return vkinl
# keyb.add(InlineKeyboardButton('+', callback_data='c;o;r;+'),
#          InlineKeyboardButton('+', callback_data='c;o;b;+'))

def key_gen_programs_list(list_, num, fix_poz=5):
    # _list style: [(1, 'Windows'), (2, 'Winrar')]
    keyb = InlineKeyboardMarkup()
    if len(list_) % 5 == 1:
        fix_poz = 4
    if ((num + 1) * fix_poz) < len(list_):
        end_ = ((num + 1) * fix_poz)
    else:
        end_ = len(list_)
    for x in range(num * fix_poz, end_):
        keyb.add(InlineKeyboardButton(list_[x][1], callback_data=f'c;p;pm;{str(list_[x][0])}'))
    if num == 0 and end_ != len(list_):
        keyb.add(InlineKeyboardButton("Вперед", callback_data=f'c;p;m;{str(num + 1)}'))
    elif num != 0 and end_ == len(list_):
        keyb.add(InlineKeyboardButton("Назад", callback_data=f'c;p;m;{str(num - 1)}'))
    elif num != 0:
        keyb.add(InlineKeyboardButton("Назад", callback_data=f'c;p;m;{str(num - 1)}'),
                 InlineKeyboardButton("Вперед", callback_data=f'c;p;m;{str(num + 1)}'))
    keyb.add(InlineKeyboardButton("Меню", callback_data='c;main_menu'))
    return keyb


def key_gen_manuals_list(list_, num, program_id, fix_poz=5):
    # _list style: [(1, 'Установка Windows', 1), (2, 'Переустановка Windows', 1)]
    keyb = InlineKeyboardMarkup()
    if len(list_) % 5 == 1:
        fix_poz = 4
    if ((num + 1) * fix_poz) < len(list_):
        end_ = ((num + 1) * fix_poz)
    else:
        end_ = len(list_)
    for x in range(num * fix_poz, end_):
        keyb.add(InlineKeyboardButton(list_[x][1], callback_data=f'c;man;tx;{str(list_[x][0])};{str(program_id)}'))
    if num == 0 and end_ != len(list_):
        keyb.add(InlineKeyboardButton("Вперед", callback_data=f'c;man;m;{str(num + 1)};{str(program_id)}'))
    elif num != 0 and end_ == len(list_):
        keyb.add(InlineKeyboardButton("Назад", callback_data=f'c;man;m;{str(num - 1)};{str(program_id)}'))
    elif num != 0:
        keyb.add(InlineKeyboardButton("Назад", callback_data=f'c;man;m;{str(num - 1)};{str(program_id)}'),
                 InlineKeyboardButton("Вперед", callback_data=f'c;man;m;{str(num + 1)};{str(program_id)}'))
    keyb.add(InlineKeyboardButton("К списку программ", callback_data='c;programs'))
    keyb.add(InlineKeyboardButton("Меню", callback_data='c;main_menu'))
    return keyb


def key_gen_texts(list_len, num, program_id, manual_id, fix_poz=1):
    # _list style: [(1, 'Установка Windows начинается с', 1),
    keyb = InlineKeyboardMarkup()
    if ((num + 1) * fix_poz) < list_len:
        end_ = ((num + 1) * fix_poz)
    else:
        end_ = list_len
    if num == 0 and end_ != list_len:
        keyb.add(
            InlineKeyboardButton("Вперед", callback_data=f'c;t;m;{str(num + 1)};{str(program_id)};{str(manual_id)}'))
    elif num != 0 and end_ == list_len:
        keyb.add(
            InlineKeyboardButton("Назад", callback_data=f'c;t;m;{str(num - 1)};{str(program_id)};{str(manual_id)}'))
        keyb.add(InlineKeyboardButton("Инструкция не помогла", callback_data=f'c;neg;{str(manual_id)}'))
    elif num != 0:
        keyb.add(
            InlineKeyboardButton("Назад", callback_data=f'c;t;m;{str(num - 1)};{str(program_id)};{str(manual_id)}'),
            InlineKeyboardButton("Вперед", callback_data=f'c;t;m;{str(num + 1)};{str(program_id)};{str(manual_id)}'))
    keyb.add(InlineKeyboardButton("Проблема решена", callback_data=f'c;t;pos;{str(manual_id)}'))
    keyb.add(InlineKeyboardButton("К списку инструкций", callback_data=f'c;p;pm;{str(program_id)}'))
    return keyb


def key_gen_tag_texts(list_len, num, manual_id, tag_id, fix_poz=1):
    # _list style: [(1, 'Установка Windows начинается с', 1),
    keyb = InlineKeyboardMarkup()
    if ((num + 1) * fix_poz) < list_len:
        end_ = ((num + 1) * fix_poz)
    else:
        end_ = list_len
    if num == 0 and end_ != list_len:
        keyb.add(
            InlineKeyboardButton("Вперед", callback_data=f'c;tet;m;{str(num + 1)};{str(manual_id)};{str(tag_id)}'))
    elif num != 0 and end_ == list_len:
        keyb.add(
            InlineKeyboardButton("Назад", callback_data=f'c;tet;m;{str(num - 1)};{str(manual_id)};{str(tag_id)}'))
        keyb.add(InlineKeyboardButton("Инструкция не помогла", callback_data=f'c;neg;{str(manual_id)}'))
    elif num != 0:
        keyb.add(
            InlineKeyboardButton("Назад", callback_data=f'c;tet;m;{str(num - 1)};{str(manual_id)};{str(tag_id)}'),
            InlineKeyboardButton("Вперед", callback_data=f'c;tet;m;{str(num + 1)};{str(manual_id)};{str(tag_id)}'))
    keyb.add(InlineKeyboardButton("Проблема решена", callback_data=f'c;tet;pos;{str(manual_id)};{str(tag_id)}'))
    keyb.add(InlineKeyboardButton('Обратно к поиску', callback_data='c;tag'))
    return keyb


def key_gen_score(manual_id):
    keyb = InlineKeyboardMarkup()
    keyb.row(
        InlineKeyboardButton("1", callback_data=f'c;sc;1;{str(manual_id)}'),
        InlineKeyboardButton("2", callback_data=f'c;sc;2;{str(manual_id)}'),
        InlineKeyboardButton("3", callback_data=f'c;sc;3;{str(manual_id)}'),
        InlineKeyboardButton("4", callback_data=f'c;sc;4;{str(manual_id)}'),
        InlineKeyboardButton("5", callback_data=f'c;sc;5;{str(manual_id)}'))
    keyb.add(InlineKeyboardButton("Меню", callback_data='c;main_menu'))
    return keyb


def key_gen_tags(listy):
    keyb = InlineKeyboardMarkup()
    for item in listy:
        tag_id, tag_name, weight, manual_id = item
        keyb.add(InlineKeyboardButton(tag_name, callback_data=f'c;tt;{str(tag_id)};{str(manual_id)}'))
    keyb.add(InlineKeyboardButton('Обратно к поиску', callback_data='c;tag'))
    keyb.add(InlineKeyboardButton("Меню", callback_data='c;main_menu'))
    return keyb


def key_gen_bad_result():
    keyb = InlineKeyboardMarkup()
    keyb.add(InlineKeyboardButton('Обратно к поиску', callback_data='c;tag'))
    keyb.add(InlineKeyboardButton("Меню", callback_data='c;main_menu'))
    keyb.add(InlineKeyboardButton('Добавить инструкцию', callback_data=' '))
    return keyb


def key_gen_pre_review(manual_id):
    keyb = InlineKeyboardMarkup()
    keyb.add(InlineKeyboardButton("Добавить отзыв", callback_data=f'c;prv;{str(manual_id)}'))
    keyb.add(InlineKeyboardButton("Меню", callback_data='c;main_menu'))
    return keyb


def key_gen_neg_review(manual_id):
    keyb = InlineKeyboardMarkup()
    keyb.add(InlineKeyboardButton("Меню", callback_data='c;main_menu'))
    keyb.add(InlineKeyboardButton("Добавить отзыв", callback_data=f'c;prv;{str(manual_id)}'))
    keyb.add(InlineKeyboardButton('Добавить инструкцию', callback_data=' '))
    keyb.add(InlineKeyboardButton('Связаться с тех поддержкой', callback_data=' '))
    return keyb


# start main menu
@bot.message_handler(commands=['start'])
def start(message):
    if message.chat.id not in sessions:
        sessions[message.chat.id] = {}
        print(sessions)
    m = bot.send_message(message.chat.id, 'TechBot приветствует вас!', reply_markup=start_menu_keyb)
    sessions[message.chat.id]['last_bot_message'] = m.message_id


# main menu
@bot.callback_query_handler(func=lambda call: call.data == 'c;main_menu')
def call_start(call):
    bot.answer_callback_query(callback_query_id=call.id)
    chat_id, message_id, data = sim_parse(call)
    print(data)
    bot.edit_message_text(chat_id=chat_id,
                          message_id=message_id,
                          text='TechBot приветствует вас!',
                          reply_markup=start_menu_keyb)


# programs slider
# gen programs
@bot.callback_query_handler(func=lambda call: call.data == 'c;programs')
def call_start(call):
    bot.answer_callback_query(callback_query_id=call.id)
    chat_id, message_id, data = sim_parse(call)
    print(data)
    programs_list = db.get_table_by_name('Programs', with_id=True)
    keyb = key_gen_programs_list(programs_list, 0)
    bot.edit_message_text(chat_id=chat_id,
                          message_id=message_id,
                          text='Выбирете интересующую вас программу из списка',
                          reply_markup=keyb)


@bot.callback_query_handler(func=lambda call: 'c;p;m' in call.data or 'c;p;pm' in call.data)
def order_start(call):
    bot.answer_callback_query(callback_query_id=call.id)
    chat_id, message_id, data, text, keyb = adv_parse(call)
    print(data)
    if data.split(';')[2] == 'm':
        programs_list = db.get_table_by_name('Programs', with_id=True)
        keyb = key_gen_programs_list(programs_list, int(data.split(';')[3]))
        bot.edit_message_text(chat_id=chat_id,
                              message_id=message_id,
                              text=text,
                              reply_markup=keyb)
    else:
        # gen manuals
        program_id = int(data.split(';')[3])
        manuals_list = db.get_instructions_by_program_id(program_id)
        keyb = key_gen_manuals_list(manuals_list, 0, program_id)
        text = 'Список инструкций обновляется, если вы не нашли интересующую вас ' \
               'инструкцию то рекомендуем вам вернуться позже'
        if 'last_bot_image_id' in sessions[chat_id]:
            if sessions[chat_id]['last_bot_image_id']:
                bot.delete_message(chat_id, sessions[chat_id]['last_bot_image_id'])
                sessions[chat_id]['last_bot_image_id'] = 0
        bot.edit_message_text(chat_id=chat_id,
                              message_id=message_id,
                              text=text,
                              reply_markup=keyb)


# manuals slider
@bot.callback_query_handler(func=lambda call: 'c;man;m' in call.data or 'c;man;tx' in call.data)
def order_start(call):
    bot.answer_callback_query(callback_query_id=call.id)
    chat_id, message_id, data, text, keyb = adv_parse(call)
    print(data)
    if data.split(';')[2] == 'm':
        move, program_id = int(data.split(';')[3]), int(data.split(';')[4])
        manuals_list = db.get_instructions_by_program_id(program_id)
        keyb = key_gen_manuals_list(manuals_list, move, program_id)
        bot.edit_message_text(chat_id=chat_id,
                              message_id=message_id,
                              text=text,
                              reply_markup=keyb)
    else:
        # gen text
        manual_id, program_id = int(data.split(';')[3]), int(data.split(';')[4])
        texts_list = db.get_items('Texts', str(manual_id), 'manual_id')
        if texts_list:
            text_len = len(texts_list)
            text = texts_list[0][1]
            keyb = key_gen_texts(text_len, 0, program_id, manual_id)
            img_name = 'manual' + '_' + str(manual_id) + '_' + '_' + '0' + '_' + '.png'
            path = f'img/{img_name}'
            send_photo(chat_id, img_name, path)
        bot.edit_message_text(chat_id=chat_id,
                              message_id=message_id,
                              text=text,
                              reply_markup=keyb)


# texts slider
@bot.callback_query_handler(func=lambda call: 'c;t;m' in call.data or 'c;t;pos' in call.data)
def order_start(call):
    bot.answer_callback_query(callback_query_id=call.id)
    chat_id, message_id, data, text, keyb = adv_parse(call)
    print(data)
    if data.split(';')[2] == 'm':
        move, program_id, manual_id = int(data.split(';')[3]), int(data.split(';')[4]), int(data.split(';')[5])
        texts_list = db.get_items('Texts', str(manual_id), 'manual_id')
        text_len = len(texts_list)
        print(move)
        text = texts_list[move][1]
        img_name = 'manual' + '_' + str(manual_id) + '_' + '_' + str(move) + '_' + '.png'
        path = f'img/{img_name}'
        'manual_5__0_.png'
        if move + 1 == text_len:
            score = db.get_manual_score(manual_id)
            text += f'\nОценка статьи: {score}'
        del_photo(chat_id)
        print(img_name)
        send_photo(chat_id, img_name, path)
        keyb = key_gen_texts(text_len, move, program_id, manual_id)
        bot.edit_message_text(chat_id=chat_id,
                              message_id=message_id,
                              text=text,
                              reply_markup=keyb)
    else:
        # gen scorer
        del_photo(chat_id)
        manual_id = int(data.split(';')[3])
        text = 'Пожалуйста, оцените статью:'
        keyb = key_gen_score(manual_id)
        bot.edit_message_text(chat_id=chat_id,
                              message_id=message_id,
                              text=text,
                              reply_markup=keyb)


# gen pre-review
@bot.callback_query_handler(func=lambda call: 'c;sc' in call.data)
def order_start(call):
    bot.answer_callback_query(callback_query_id=call.id)
    chat_id, message_id, data, text, keyb = adv_parse(call)
    print(data)
    mark, manual_id = int(data.split(';')[2]), int(data.split(';')[3])
    text = 'Так же вы можете отправить отзыв к данной статье'
    keyb = key_gen_pre_review(manual_id)
    db.update_score(mark, manual_id)
    bot.edit_message_text(chat_id=chat_id,
                          message_id=message_id,
                          text=text,
                          reply_markup=keyb)


# gen review
@bot.callback_query_handler(func=lambda call: 'c;prv' in call.data)
def order_start(call):
    bot.answer_callback_query(callback_query_id=call.id)
    chat_id, message_id, data, text, keyb = adv_parse(call)
    manual_id = int(data.split(';')[2])
    print(data)
    bot.delete_message(chat_id, message_id)
    # manual_id = int(data.split(';')[2])
    # text = 'Запишите ваш отзыв. После потдверждения ввода отзыв будет отправлен'
    # keyb = InlineKeyboardMarkup()
    # bot.edit_message_text(chat_id=chat_id,
    #                       message_id=message_id,
    #                       text=text,
    #                       reply_markup=None)
    msg = """\
    Запишите ваш отзыв
    После потдверждения ввода отзыв будет отправлен
    """
    sessions[chat_id]['manual_rev_id'] = manual_id
    mes = bot.send_message(chat_id, 'Запишите ваш отзыв. После потдверждения ввода отзыв будет отправлен')
    bot.register_next_step_handler(mes, process_review)


def process_review(message):
    try:
        chat_id = message.chat.id
        review = message.text
        print(review+str(sessions[chat_id]['manual_rev_id']))
        bot.send_message(chat_id, 'Ваш отзыв отправлен\nМы ценим ваше мнение, спасибо за то что уделили время!')
        sessions[chat_id]['manual_rev_id'] = 0
    except Exception as e:
        bot.reply_to(message, 'oooops')


# gen tag list
@bot.callback_query_handler(func=lambda call: 'c;tag' in call.data)
def order_start(call):
    bot.answer_callback_query(callback_query_id=call.id)
    chat_id, message_id, data, text, keyb = adv_parse(call)
    print(data)
    bot.delete_message(chat_id, message_id)

    if 'last_bot_image_id' in sessions[chat_id]:
        if sessions[chat_id]['last_bot_image_id']:
            bot.delete_message(chat_id, sessions[chat_id]['last_bot_image_id'])
            sessions[chat_id]['last_bot_image_id'] = 0

    mes = bot.send_message(chat_id, 'Запишите ваш запрос\nПосле потдверждения ввода вам будет предоставлен список доступных инструкций')
    sessions[chat_id]['manual_mes_id'] = mes.id
    bot.register_next_step_handler(mes, process_instr)


def process_instr(message):
    try:
        chat_id = message.chat.id
        search_word = message.text
        bot.delete_message(chat_id, sessions[chat_id]['manual_mes_id'])
        tags_list = words_magick(search_word)
        if tags_list:
            keyb = key_gen_tags(tags_list)
            bot.send_message(message.chat.id, 'Доступные инструкции:', reply_markup=keyb)
        else:
            keyb = key_gen_bad_result()
            bot.send_message(message.chat.id, 'По вашему запросу нет результатов', reply_markup=keyb)
        print(search_word)
        print(tags_list)
    except Exception as e:
        bot.reply_to(message, 'oooops')


# tag list react
@bot.callback_query_handler(func=lambda call: any(cllb in call.data for cllb in ['c;tet;m', 'c;tet;pos', 'c;tt', 'c;neg']))
def order_start(call):
    bot.answer_callback_query(callback_query_id=call.id)
    chat_id, message_id, data, text, keyb = adv_parse(call)
    print(data)
    if data.split(';')[2] == 'm':
        'c;tet;m;{str(num + 1)};{str(manual_id)};{str(tag_id)}'
        move, manual_id, tag_id = int(data.split(';')[3]), int(data.split(';')[4]), int(data.split(';')[5])
        texts_list = db.get_items('Texts', str(manual_id), 'manual_id')
        text_len = len(texts_list)
        text = texts_list[move][1]
        img_name = 'manual' + '_' + str(manual_id) + '_' + '_' + str(move) + '_' + '.png'
        path = f'img/{img_name}'
        'manual_5__0_.png'
        if move + 1 == text_len:
            score = db.get_manual_score(manual_id)
            text += f'\nОценка статьи: {score}'
        del_photo(chat_id)
        send_photo(chat_id, img_name, path)
        keyb = key_gen_tag_texts(text_len, move, manual_id, tag_id)
        bot.edit_message_text(chat_id=chat_id,
                              message_id=message_id,
                              text=text,
                              reply_markup=keyb)
    elif data.split(';')[2] == 'pos':
        # gen scorer
        del_photo(chat_id)
        manual_id, tag_id = int(data.split(';')[3]), int(data.split(';')[4])
        db.update_tag_clicks(tag_id)
        print(tag_id, 'tag_id')
        text = 'Пожалуйста, оцените статью:'
        keyb = key_gen_score(manual_id)
        bot.edit_message_text(chat_id=chat_id,
                              message_id=message_id,
                              text=text,
                              reply_markup=keyb)
    elif data.split(';')[1] == 'tt':
        """f'c;tt;{str(tag_id)};{str(manual_id)}'"""
        # gen text from tags
        tag_id, manual_id = int(data.split(';')[2]), int(data.split(';')[3])
        texts_list = db.get_items('Texts', str(manual_id), 'manual_id')
        if texts_list:
            text_len = len(texts_list)
            text = texts_list[0][1]
            keyb = key_gen_tag_texts(text_len, 0, manual_id, tag_id)
            img_name = 'manual' + '_' + str(manual_id) + '_' + '_' + '0' + '_' + '.png'
            path = f'img/{img_name}'
            send_photo(chat_id, img_name, path)
            bot.edit_message_text(chat_id=chat_id,
                                  message_id=message_id,
                                  text=text,
                                  reply_markup=keyb)
    elif data.split(';')[1] == 'neg':
        # gen neg response
        manual_id = int(data.split(';')[2])
        del_photo(chat_id)
        keyb = key_gen_neg_review(manual_id)
        text = 'Сожалеем, что инструкция не была вам полезна'
        bot.edit_message_text(chat_id=chat_id,
                              message_id=message_id,
                              text=text,
                              reply_markup=keyb)

print("Ready")
bot.infinity_polling()


"""
if 'last_bot_image_id' in sessions[chat_id]:
    if sessions[chat_id]['last_bot_image_id']:
        bot.delete_message(chat_id, sessions[chat_id]['last_bot_image_id'])
        sessions[chat_id]['last_bot_image_id'] = 0

"""