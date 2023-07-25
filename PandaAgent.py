from langchain.llms import OpenAI
import pandas as pd
from langchain.agents import create_pandas_dataframe_agent
import config

file = "Documents\cellphones_data.csv"
data = pd.read_csv(file)
data.head(10)
llm = OpenAI(tiktoken_model_name="text-davinci-003", openai_api_key=config.OPENAI_API_KEY, temperature=0.5)

agent = create_pandas_dataframe_agent(llm, data, verbose=True)
query = "¿Cuales son los 3 telefonos con mejor memoria?"
res = agent.run(query)
print(res)