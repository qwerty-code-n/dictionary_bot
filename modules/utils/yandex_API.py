import requests
import os 
import logging

class YandexAPI:


    def __init__(self, APIkey=os.environ.get('YANDEX_TRANSLATION_API_KEY')):

        self.APIkey=APIkey

#определение языка присланного сообщения
    def detectLanguage(self, message):
        header = {'Authorization': 'Api-Key {}'.format(self.APIkey)}
        POST = "https://translate.api.cloud.yandex.net/translate/v2/detect"


        body = {
                
                "languageCodeHints":["ru", "en"],
                "text": message
            }
        
        req = requests.post(POST, headers=header, json=body)
        data = req.json()

   
        langCode = data['languageCode']
        return langCode


#перевод сообщения
    def translate(self, message, targetLanguage):
        header = {'Authorization': 'Api-Key {}'.format(self.APIkey)}
        POST = "https://translate.api.cloud.yandex.net/translate/v2/translate"


        body = {
                
                "texts": [message],
                "targetLanguageCode":  targetLanguage
            }
        
        req = requests.post(POST, headers=header, json=body)
        data = req.json()

        translation = data['translations'][0]['text']
        return translation

#проверка на опечатки
    def spellCheck(self, message, language):

        

        url= f'https://speller.yandex.net/services/spellservice.json/checkText?text={message};lang={language}'

        req = requests.get(url)
        data = req.json()

        return(data)
    
#синтез голосового сообщения
    def voiceSynthesis(self, message, language):

        if language=='en':
            langCode='en-US'
        elif language=='ru':
            langCode='ru-RU'

        header = {'Authorization': 'Api-Key {}'.format(self.APIkey)}
        url = "https://tts.api.cloud.yandex.net/speech/v1/tts:synthesize"


        body = {
               
                "text": message,
                "lang":  langCode,

            }
        
        with requests.post(url, headers=header, data=body, stream=True) as resp:
                
            if resp.status_code != 200:
                logging.error('cannot make synthesis')
            
            for chunk in resp.iter_content(chunk_size=None):
                yield chunk
