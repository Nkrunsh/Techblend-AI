"""
Implementación de un chatbot utilizando el modelo de lenguaje de OpenAI. 
El chatbot utiliza una ConversationChain para generar respuestas en base a la 
entrada de un usuario. El código incluye un método de prueba que permite al 
usuario interactuar con el chatbot. El bucle principal permite al usuario ingresar 
mensajes y obtiene una respuesta generada por el chatbot utilizando el modelo de 
lenguaje de OpenAI. Además, se muestra el historial de mensajes guardado por el chatbot.
"""

import config
import json
from ChatbotConversationChain import ChatBotChain
from DataParser import HistoryExtractor
from langchain.llms import OpenAI
from langchain.memory import ConversationBufferMemory


class ChatBotAI:

    #Modelo
    _llm = OpenAI(tiktoken_model_name="text-davinci-003", openai_api_key=config.OPENAI_API_KEY, temperature=0.7)
    _bot_memory = ConversationBufferMemory()
    # ChatBot IA 
    _sandraAI = ChatBotChain(llm =_llm, verbose=False, memory=_bot_memory)
    _extractor = HistoryExtractor(_llm)
    _user_data: json

    def __init__(self) -> None:
        pass

    def test(self) -> None:
        human_input = ''       
        #Condicion de salida del bucle --
        while human_input != '--': 
            human_input = input("Human:")
            
            # Filtra comando --
            if human_input != '--':    
                print('\n AI WORKING...')
                response = self._sandraAI.predict(input = human_input)
                data = self._extractor.get_relevant_data(self._bot_memory)
                print( f'{response} \n\n PRINT DATA { data}')


        
        print('\n\n PRINTING HISTORY MESSAGE \n\n')

        
        print(self._user_data)

if __name__ == '__main__':
    bot = ChatBotAI()
    bot.test()
