from langchain.llms.base import BaseLLM
from langchain.schema import HumanMessage
from langchain import PromptTemplate 

from langchain.memory import ConversationBufferMemory
class HistoryExtractor:
    _llm:BaseLLM

    _template="""Tu funcion es identificar la siguiente informacion de un hisotrial de chat de asistencia en ventas entre Usuario e IA:
    -Nombre de usuario: Solo si el usuario lo menciona
    -Tipo de producto: Si es telefono, plan o TP (telefono y plan)
    -Presupuesto: Puede estar expresado en pesos o lucas
    -Caracterisitcas del dispositivo: Una descripcion resumida del producto buscado
    -Modelo: Solo si el usuario entrega un nombre en particular de telefono
    -Marca: Solo si el usuario nombra alguna marca
    
Historial:
{chat}

Formato de Salida: La informacion debe ser entregada en un formato json, si no se encuentra infromacion, competa con un 'nan'.
"""
    

    def __init__(self, llm:BaseLLM) -> None:
        self._llm=llm

    def get_relevant_data(self, content:ConversationBufferMemory):
        chat_content=''
        messages =content.chat_memory.messages 
        for message in messages:
            if type(message) == HumanMessage:
                chat_content += 'Human: '+message.content+'\n'
            else:
                chat_content += 'AI: '+message.content+'\n'
        prompt = PromptTemplate(input_variables=["chat"], template=self._template)
        answer = self._llm.predict(prompt.format(chat=chat_content))
        return answer
    
   

