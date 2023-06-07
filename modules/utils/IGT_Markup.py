#in this module markup menus are defined for messages
import telebot
from telebot import types


#класс который определяет как будут выглядеть Markup у сообщений - то есть как будут выглядеть кнопочки под сообщениями

class IGT_Markup(object):

#Устаревший markup
#
    @staticmethod
    def getShowAllWords(userId):
        
        markup = telebot.types.InlineKeyboardMarkup()
 
        markup.row(telebot.types.InlineKeyboardButton("Показать сохраненные слова", callback_data=f'show_all_cards_{userId}'))
        
        return markup

# генерирование маркапа для команды /status
    @staticmethod
    def getStatusMarkup(userId):
        
        markup = telebot.types.InlineKeyboardMarkup()
 
        markup.row(telebot.types.InlineKeyboardButton("Показать все слова", callback_data=f'show_all_cards_{userId}'))
        markup.row(telebot.types.InlineKeyboardButton("Показать все модули", callback_data=f'show_all_modules_{userId}'))
        markup.row(telebot.types.InlineKeyboardButton("Добавить новый модуль", callback_data=f'add_new_module_{userId}'))
        
        return markup


# генерирование маркапа для 
    @staticmethod
    def moduleInfoMarkup(userId, moduleId, isGeneral):
        markup=telebot.types.InlineKeyboardMarkup()
        markup.row(telebot.types.InlineKeyboardButton("Показать все слова модуля", callback_data=f'show_all_module_cards_{userId}_{moduleId}'))
            
        if not isGeneral:
            markup.row(telebot.types.InlineKeyboardButton("Удалить модуль", callback_data=f'delete_module_{userId}_{moduleId}_{isGeneral}'))
            return markup
        else:
            markup.row(telebot.types.InlineKeyboardButton("Удалить все слова из модуля", callback_data=f'delete_module_{userId}_{moduleId}_{isGeneral}'))
            return markup

#генерирование маркапа для карточки слова    
    @staticmethod
    def cardInfo(userId, cardId):
        markup=telebot.types.InlineKeyboardMarkup()
        markup.row(telebot.types.InlineKeyboardButton("Удалить слово", callback_data=f'delete_card_{userId}_{cardId}'))
        markup.row(telebot.types.InlineKeyboardButton("Изменить модуль", callback_data=f'move_card_{userId}_{cardId}'))
        return markup

#герерирование маркапа для переноса карточки в другой модуль. То есть список всех модулей
    @staticmethod
    def cardChangeMarkup(cardId, currentModuleId, userModules):
        markup=telebot.types.InlineKeyboardMarkup()
        for module in userModules:
            if currentModuleId!=module['_id']:
                newModuleId=module['_id']
                moduleName=module['module_name']
            
                markup.row(telebot.types.InlineKeyboardButton(moduleName, callback_data=f'move_to_module_{cardId}_{newModuleId}'))
        
        return markup

#генерирование маркапа для выборка модуля для повторения
    @staticmethod
    def getModulesToRepeat(userModules):
        markup=telebot.types.InlineKeyboardMarkup()
        for module in userModules:
            moduleId=module['_id']
            moduleName=module['module_name']
            userId=module['userid']
            markup.row(telebot.types.InlineKeyboardButton(moduleName, callback_data=f'repeat_module_{userId}_{moduleId}'))
        
        return markup