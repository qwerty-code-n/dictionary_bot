#in this module connections to mondoDB is defined
import json
from bson.objectid import ObjectId

import pymongo
import jsonpickle
from telebot import types
import logging
import os
from datetime import datetime



# в этом модуле определяется класс по взаимодействию с базой данных MongoDB


class noMessagesToSend(Exception):
    def __str__(self):
        return 'fileTooBigError'


class noRecommendationsForThisQuestionaire(Exception):
    def __str__(self):
        return 'noRecommendationsForThisQuestionaire'

#Creating class for DB connection
class Database:
    
    standardMessages=[]
    

    def __init__(self, URL=os.environ.get('DB_STRING'), database='Database'):
        self.URL=URL
        self.databaseName=database
        

    def openConnection(self):
        self.client = pymongo.MongoClient(self.URL)
        database = self.client[self.databaseName]
        self.users= database['TG_Users']
        self.user_state= database['TG_User_State']
        self.standard_messages= database['TG_Standard_Messages']
        self.flash_cards=database['TG_Flash_Cards']
        self.modules=database['TG_Modules']
        self.cards_to_repeat=database['TG_Cards_To_Repeat']
        cursor = self.standard_messages.find()
        self.standardMessages = cursor[0]

        
    def closeConnection(self):
        self.client.close()

#check have this user used bot or not
    def isExistingUser(self, userId):
        
        filter_user = {'id': userId}
        if self.users.count_documents(filter_user)==0:   
            return False
        else:
            return True

    def getStandardMessages(self):
        cursor = self.standard_messages.find()
        return cursor[0]
    
    def getAllUserCards(self, userId):
        filter_user = {'userid': userId}
        
        if self.flash_cards.find(filter_user) is not None:
            return self.flash_cards.find(filter_user)
        else:   
            pass

    def getAllUserModules(self, userId):
        filter_user = {'userid': userId}
        
        if self.modules.find(filter_user) is not None:
            return self.modules.find(filter_user)
        else:   
            pass


    def getAllUserModuleCards(self, userId, moduleId):
        filter = {
            'userid': userId,
            'moduleId': ObjectId(moduleId)
            }
        
        return self.flash_cards.find(filter)

    
    def getModuleNameById(self, moduleId):
        filter = {
            '_id': ObjectId(moduleId)
            }
        
        return self.modules.find_one(filter)['module_name']

    def moveCard(self, cardId, moduleId):
        filter = {
            '_id': ObjectId(cardId)
            }
        
        self.flash_cards.update_one(filter,{ "$set":{'moduleId': ObjectId(moduleId)}})

    def putFlashCard(self, userId, sourceLangCode, sourceVersion, targetVersion):
        
        moduleFilter = {
            'userid': userId,
            'module_name': 'General'
        }
        generalModuleId = self.modules.find_one(moduleFilter)['_id']

        if sourceLangCode=='ru':
            flashCard={
                'userid': userId,
                'russian': sourceVersion,
                'english': targetVersion,
                'moduleId': generalModuleId
            }
        else:
            flashCard={
                'userid': userId,
                'russian': targetVersion,
                'english': sourceVersion,
                'moduleId': generalModuleId
            }
        
        filter=flashCard
        self.flash_cards.replace_one(filter, flashCard, upsert=True)

    def isRepeatMode(self, userId):
        filter_user = {'userid': userId}

        if self.user_state.find_one(filter_user) is not None:
            return self.user_state.find(filter_user)[0]['is_repeat_mode']
        else:   
            pass
    
    def isRequestNewModuleNameMode(self, userId):
        filter_user = {'userid': userId}

        if self.user_state.find_one(filter_user) is not None:
            return self.user_state.find(filter_user)[0]['is_request_model_name_mode']
        else:   
            pass
    
    def createNewModule(self, userId, moduleName):
        module = {
                'userid': userId,
                'module_name': moduleName,
            }
        self.modules.replace_one(module,module, upsert=True)


    def setRepeatMode(self, userId):

        filter_user = {
            'userid': userId
            }
        if self.user_state.find_one(filter_user) is not None:
            self.user_state.update_one(filter_user,{ "$set":{'is_repeat_mode': True}})    
        else:   
            pass

    def setModuleNameRequestMode(self, userId):

        filter_user = {
            'userid': userId
            }
        if self.user_state.find_one(filter_user) is not None:
            self.user_state.update_one(filter_user,{ "$set":{'is_request_model_name_mode': True}})    
        else:   
            pass

    def putCardToRepeat(self, card):
        filter=card

        self.cards_to_repeat.replace_one(filter, card, upsert=True)

    
    def getNumberOfCards(self, userId):
        filter_user = {'userid': userId}
        return self.flash_cards.count_documents(filter_user)

    def getCard(self, cardId):
        filter= {
            '_id': ObjectId(cardId)
            }
        return self.flash_cards.find_one(filter)
    
    def getNumberOfModules(self, userId):
        filter_user = {'userid': userId}
        return self.modules.count_documents(filter_user)
    
    def getNumberOfCardsInModule(self, userId, moduleId):
        filter = {
            'userid': userId,
            'moduleId': ObjectId(moduleId)
            }
        return self.flash_cards.count_documents(filter)
    
    def getNextCardToRepeat(self, userId):

        filter_user = {'userid': userId}
        if self.cards_to_repeat.find_one(filter_user) is not None:
            return self.cards_to_repeat.find_one(filter_user)
        else:
            return False
    
    def getCardToCompare(self,userId):
        filter_user = {'userid': userId}
        if self.user_state.find_one(filter_user) is not None:
            
            return self.user_state.find_one(filter_user)['current_card'] 
        else:   
            pass

    def setCurrentCard(self, userId, card):
        filter_user = {'userid': userId}
        self.user_state.update_one(filter_user, { "$set":{'current_card': card}})
            
    def deleteCardFromQueue(self, userId, Russian, English):
        flashCard={
                'userid': userId,
                'russian': Russian,
                'english': English
            }
        self.cards_to_repeat.delete_many(flashCard)

    def deleteCard(self, cardId):
        filter={
                '_id': ObjectId(cardId)
            }
        self.flash_cards.delete_many(filter)
    
    def deleteModule(self, moduleId, isGeneral):
        filterCards={
                'moduleId': ObjectId(moduleId)
            }
        self.flash_cards.delete_many(filterCards)
        if isGeneral=='False':
            filterModule={
                    '_id': ObjectId(moduleId)
                }
            
            self.modules.delete_many(filterModule)
    
    def getUserModules(self, userId):
        filter={
            'userid': userId
        }

        return self.modules.find(filter)

#put User to default status
#We have tables TG_Users and TG_User_State - in default status it has False for search flag and -1 in account
    def setUserToDefault(self, user):
        
        filter_user = {'userid': user.id}
        user_json = json.loads(jsonpickle.encode(user))

        if self.isExistingUser(user.id):
            self.users.replace_one({'id': user.id}, user_json, upsert=True)
            self.user_state.update_one(filter_user, { "$set":{'is_repeat_mode': False}})
            self.user_state.update_one(filter_user, { "$set":{'is_request_model_name_mode': False}})
            self.user_state.update_one(filter_user, { "$set":{'current_card': []}})
            self.cards_to_repeat.delete_many(filter_user)

        else:
            logging.info(f'Creating new user in DB userid: {user.id}')
            self.users.insert_one(user_json)
            
            defaultUserInfo = { 
                'userid': user.id,
                'name': user.first_name,
                'is_repeat_mode': False,
                'is_request_model_name_mode': False,
                'current_card': []
            }

            defaultModule = {
                'userid': user.id,
                'module_name': 'General',
            }

            self.user_state.insert_one(defaultUserInfo)
            self.modules.replace_one(defaultModule,defaultModule, upsert=True)


    
# # область для тестирования, если нужно проверить как работает тот или иной запрос к БД без запуска бота
if __name__ == "__main__":



    DB =Database(URL = os.environ.get('TRANSLATION_DB_STRING_DEV'),database ='Memory_Cards_Database')
    DB.openConnection()
    
   #test your code

    DB.closeConnection()