from telebot.custom_filters import AdvancedCustomFilter
from telebot.types import Message, CallbackQuery
from modules.utils.IGT_Mongo import Database

import logging

class isRepeatModeFilter(AdvancedCustomFilter):

    def __init__(self, bot):
        self.bot = bot

    def isRepeatModeUser(self, userId):
        
        DB: Database = self.bot.db_connection

        if DB.isRepeatMode(userId):
            return True
        else:
            return False
  


    key = 'isRepeatModeUser'
  
    def check(self, message: Message, text):
        
        if isinstance(message, Message):
            chat_id = message.chat.id
            user_id = message.from_user.id


        # if isinstance(message, CallbackQuery):
        #     chat_id = message.message.chat.id
        #     user_id = message.from_user.id
        #     message = message.message

        return self.isRepeatModeUser(user_id)


class isRequestNewModuleNameMode(AdvancedCustomFilter):

    def __init__(self, bot):
        self.bot = bot

    def isRequestNewModuleNameMode(self, userId):
        
        DB: Database = self.bot.db_connection

        if DB.isRequestNewModuleNameMode(userId):
            return True
        else:
            return False
  


    key = 'isRequestNewModuleNameMode'
  
    def check(self, message: Message, text):
        
        if isinstance(message, Message):
            chat_id = message.chat.id
            user_id = message.from_user.id


        # if isinstance(message, CallbackQuery):
        #     chat_id = message.message.chat.id
        #     user_id = message.from_user.id
        #     message = message.message

        return self.isRequestNewModuleNameMode(user_id)