"""

This is VK bot, which acts like Mr. Angelo from famous video
https://www.youtube.com/watch?v=wQ3MTcSxyE4
This file contains obscene language !!


Это ВК бот, который эмулирует поведение мистера Анджело из известного видоса
https://www.youtube.com/watch?v=wQ3MTcSxyE4
Файл содержит нецензурную лексику!!

"""

# For creating messages identifiers
import random

# For parsing user's message
import re

# For puset
import time

class Message:
    def __init__(self, message, user):
        self.message = message
        self.user = user

class IBotContext:
    def messageReadingLoop(self):
        while True:
            yield Message(input(), 0)

    def sendMessage(self, message):
        print(f"[To {message.user}]: {message.message}")

class VkBotContext(IBotContext):
    # In order to launch one have to install vk_api
    # pip3 install vk_api
    
    import vk_api
    from vk_api.longpoll import VkLongPoll, VkEventType
    
    def __init__(self, token):
        # Log in by token
        self.vk = self.vk_api.VkApi(token=token)
        
        # Message poll
        self.longpoll = self.VkLongPoll(self.vk)

    def messageReadingLoop(self):
        for event in self.longpoll.listen():
            if event.type == self.VkEventType.MESSAGE_NEW:
                if event.to_me:
                    yield  Message(event.text, event.user_id)
    
    def sendMessage(self, message):
        self.vk.method('messages.send', {'user_id': message.user, 'message': message.message, 'random_id' : random.randint(0, 1000000)})
                
class WordFixer:
    """
    Class helps fixing user input using levenshtein_distance from known words
    """
    known_words = ["кто", "извинитесь", "хуя", "бах", "извинись", "трахал", "ты", "может", "я"]
    
    def levenshtein_distance(self, a, b):
        "Calculates levenshtein distance"

        n, m = len(a), len(b)
        if n > m:
            a, b = b, a
            n, m = m, n
        current_row = range(n + 1)
        for i in range(1, m + 1):
            previous_row, current_row = current_row, [i] + [0] * n
            for j in range(1, n + 1):
                add, delete, change = previous_row[j] + 1, current_row[j - 1] + 1, previous_row[j - 1]
                if a[j - 1] != b[i - 1]:
                   change += 1
                current_row[j] = min(add, delete, change)
        return current_row[n]
    
    def getWord(self, wordToFix):
        "Finds nearest word in dictionary"

        result = ""
        for word in self.known_words:
            if(self.levenshtein_distance(word, wordToFix) < self.levenshtein_distance(wordToFix, result)):
                result = word
        return result

class AngeloBot:
    def __init__(self, context):
        self.context = context
        self.idiots = set()
        self.fixer = WordFixer()
    
    def __write(self, user, text):
        self.context.sendMessage(Message(text, user))

    def run(self):
        for message in self.context.messageReadingLoop():
            request = message.message.lower()
            words = set(self.fixer.getWord(word) for word in re.split(r'[?;,\s]\s*', request))
            write_msg = self.__write
            if {"кто"}.issubset(words):
                if(message.user not in self.idiots):
                    write_msg(message.user, "Ну, дэбил")
                    self.idiots.add(message.user)
                else:
                    write_msg(message.user, "Я!!")
                    self.idiots.remove(message.user)
            elif {"извинитесь"}.issubset(words):
                write_msg(message.user, "Да иди ты нахуй")
            elif {"извинись"}.issubset(words):
                write_msg(message.user, "А может быть ты?")
                self.idiots.add(message.user)
            elif {"хуя"}.issubset(words):
                write_msg(message.user, "Ой")
            elif {"трахал"}.issubset(words):
                write_msg(message.user, "Папарапаппа")
            elif {"бах"}.issubset(words):
                write_msg(message.user, "Я не зря помер, ДА СУКА!!!!")
            elif {"бан"}.issubset(words):
                write_msg(message.user, "Я не зря помер, ДА СУКА!!!!")
            elif {"баан"}.issubset(words):
                write_msg(message.user, "Я не зря помер, ДА СУКА!!!!")
            elif {"баах"}.issubset(words):
                write_msg(message.user, "Я не зря помер, ДА СУКА!!!!")
            elif {"ты", "может"}.issubset(words):
                write_msg(message.user, "Кто?????")
            elif {"я"}.issubset(words):
                write_msg(message.user, "Хуя")
            else:
                write_msg(message.user, "Ты дэбил?")
                if(message.user in self.idiots):
                    self.idiots.remove(message.user)

import secret
AngeloBot(VkBotContext(secret.vk_token)).run()