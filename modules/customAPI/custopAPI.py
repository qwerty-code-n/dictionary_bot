import requests
import logging
from datetime import datetime

class sendCustomRequest():
    @staticmethod
    def send_message(token, chat_id, text):

        method_url = r'sendMessage'
        payload = {
            'chat_id': str(chat_id), 
            'text': text,
            'parse_mode': 'HTML',
            'protect_content': True
            }
       
        request_url = "https://api.telegram.org/bot{0}/{1}".format(token, method_url)
        params = payload
        
        response = requests.post(request_url, params=params)
        
        return response


    @staticmethod
    def send_photo(token, chat_id, text, photo):

        method_url = r'sendPhoto'
        payload = {
            'chat_id': str(chat_id), 
            'text': text,
            'parse_mode': 'HTML',
            'protect_content': True
            }
        files={
            'photo': photo
        }
        request_url = "https://api.telegram.org/bot{0}/{1}".format(token, method_url)
        params = payload
        
        response = requests.post(request_url, params=params,files=files)
        
        return response

    @staticmethod
    def check_user_belogs_to_chat(token, chat_id, user_id):

        method_url = r'getChatMember'
        payload = {
            'chat_id': str(chat_id), 
            'user_id': int(user_id)
            }
       
        request_url = "https://api.telegram.org/bot{0}/{1}".format(token, method_url)
       
        response = requests.get(request_url, params=payload)
        
        return response
