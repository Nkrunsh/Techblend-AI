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
