"""
El programa plantea la implementacion de un chatbot que utiliza la biblioteca LangChain 
para crear una conversación entre un humano y una IA. La IA es capaz de generar 
respuestas en base a la entrada del usuario y puede almacenar una historia del chat. 
Además, el chatbot tiene la capacidad de recibir un comando especial ("++") 
para agregar un mensaje de recomendación al historial del chat. El programa 
se ejecuta en un bucle hasta que el usuario ingrese el comando de salida ("--") y 
luego imprime el historial del chat. También se plantea una tarea adicional de 
implementar una forma para que la IA pueda obtener una recomendación de teléfono 
basada en la información obtenida del usuario.

"""


import config
import json
from ChatbotConversationChain import ChatBotChain
from langchain.llms import OpenAI
from langchain.memory import ConversationBufferMemory


#Historial del chat
history = ConversationBufferMemory()
#Modelo
llm = OpenAI(tiktoken_model_name="text-davinci-003",
                      openai_api_key=config.OPENAI_API_KEY,
                      temperature=0.7
                      )

# ChatBot IA 
SandraAI = ChatBotChain(llm =llm, verbose=False, memory=history)

#Ejecucion de la IA
def run():
    human_input = ''       

    #Condicion de salida del bucle --
    while human_input != '--': 
        human_input = input("Human:")

        #Comando ++ para introducir mensaje de recomendacion
        if human_input =='++':
            history.chat_memory.add_ai_message("Recomienda Xiaomi20 con valor 20000")
        
        # Filtra comando --
        if human_input != '--':    
            print('\n\n AI WORKING...')
            response = SandraAI.predict(input = human_input)
            print(response)

    
    print('\n\n PRINTING HISTORY MESSAGE \n\n')

    content:str = history.load_memory_variables({})['history']
    for line in content.split("\n"):
        print(line)
    


if __name__ == '__main__':
    run()

#TODO Implementar una forma que la IA pueda obtener recomendacion de telefono con la informacion obtenida del usuario mediante el uso del pandas_dataframe_agent.
