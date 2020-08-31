#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Посмотреть документацию к API GitHub, разобраться как вывести список репозиториев для
# конкретного пользователя, сохранить JSON-вывод в файле *.json.
# Изучить список открытых API. Найти среди них любое, требующее авторизацию (любого типа).
# Выполнить запросы к нему, пройдя авторизацию. Ответ сервера записать в файл.

# Оба задания будут в одном, в качестве второго публичного API использую API телеграмма
# Для выполнения задания был создан бот - t.me/parsapitestbot
# Документация по апи - https://core.telegram.org/bots/api

import requests as r
import json
import time

#Токены авторизации юудем хранить в файле, дабы не выкладывать на публичный ресурс
with open('settings.json') as f:
    ids = json.load(f)

TELEGRAM_TOKEN = ids["telegramm_token"]
GITHUB_TOKEN = ids["git_token"]
TELTGRAM_BASE_URL = 'https://api.telegram.org/bot{}'.format(TELEGRAM_TOKEN)

#Заголовки для запросов к гитхаб
git_head = {'accept': 'application/vnd.github.v3+json',
            'Authorization': 'token {}'.format(GITHUB_TOKEN)}

offset = 0  # Идентификатор сообщений бота

while True:  #Работаем до остановки/ошибке в цикле

    repo_list = []  # Здесь будет список с названиями репозиториев пользователя, pfyekztv rf;lsq wbrk

    # Формируем запрос в телеграмм апи для получения от бота обновлений
    tm_update_param = {'offset': offset,
                       'allowed_updates': '["message"]'}
    tm_update_response = r.get("{}/getUpdates".format(TELTGRAM_BASE_URL),params=tm_update_param)
    telegramm_jdata = tm_update_response.json()

    # Идем циклом по новым сообщениям боту
    for message in telegramm_jdata['result']:
        offset_c = int(message["update_id"])
        if offset_c >= offset:
            # Если номер апдейта бота больше или равен нашего смещения, то делаем его нашим офсетом со смещением на 1
            offset = offset_c+1

#        msg = message["message"]["text"]

        if message["message"]["text"][0] == '/' and message["message"]["text"] != '/start':  # Проверим что сообщение является командой боту и это не /start

            # Используем команду полученную ботом в качестве пользователя гитхаба для получения списка
            # его репозиториев.
            user_name = message["message"]["text"][1:]  # Уберем /

            git_url = 'https://api.github.com/users/{}/repos'.format(user_name)
            git_resp = r.get(git_url, headers=git_head)

            if git_resp.ok:
                git_jdata = git_resp.json() # Если вернулось 200, преобразуем ответ в json
                for i in git_jdata:
                    repo_list.append( { 'name': i['name'],
                                         'url': i['url'],
                                         'language': i['language'],
                                         'created_at': i['created_at']}
                                    )
                # Выполним первую часть задания, сохраним ответ в файл
                with open('{}_repos.json'.format(user_name), 'w') as f:
                    json.dump(repo_list,f)

                # Сформируем сообщение со списком репозиториев пользователя
                k = 1
                repos_msg = ''
                for reps in repo_list:
                    repos_msg = repos_msg + str(k) + '. Name: {}\nURL: {}\nlanguage: {}\ncreated_at: {}\n'.format(reps['name'],reps['url'],reps['language'],reps['created_at'])
#                   print(reps)
                    k+=1

                bot_message = "*Инофрмация о публичных репозиториях пользователя {}:*\n{}".format(user_name,repos_msg)
#                print(bot_message)

            elif git_resp.status_code == 404:
                bot_message = 'У пользователя {} нет публичных репозиториев на github'.format(user_name)

            else:
                bot_message = 'Что-то пошло не так, воспользуетесь сервисом позже'.format(user_name)

            tm_send_param = { 'chat_id': message["message"]["chat"]["id"],
                              'text': bot_message,
                              'parse_mode': 'Markdown'}
            tm_send_response = r.get("{}/sendMessage".format(TELTGRAM_BASE_URL), params=tm_send_param)

    time.sleep(15) # Поскольку не понял как делать "длинные" запросы без поллинга, не наглею, 4 запроса в минуту делаю