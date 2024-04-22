from langchain_openai import OpenAIEmbeddings, OpenAI
from langchain_community.vectorstores import Chroma
from langchain_community.llms import Ollama
from langchain.chains import  RetrievalQA
from langchain_anthropic import ChatAnthropic
claudeModel = ChatAnthropic(model='claude-3-opus-20240229')

import os
from dotenv import load_dotenv

load_dotenv()

os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")
os.environ["LANGCHAIN_TRACING_V2"] = 'true'
os.environ["LANGCHAIN_API_KEY"] = os.getenv("LANGCHAIN_API_KEY")
os.environ["CHATANTROPIC_API_KEY"] = os.getenv("CHATANTROPIC_API_KEY")
claude_api_key = os.getenv("CHATANTROPIC_API_KEY")

vectorDB = Chroma(persist_directory="./chromaDB", embedding_function=OpenAIEmbeddings())
retriever = vectorDB.as_retriever()

def getProcessedOutput(llmSelected, destination, tripType):
    if (llmSelected=="Gemma"):
        llm=Ollama(model="gemma:2b", temperature=0)
    elif (llmSelected=="OpenAI"):
        llm=OpenAI(temperature=0)
    elif (llmSelected=="Claude"):
        claudeModel = ChatAnthropic(temperature=0, api_key = claude_api_key, model_name="claude-3-opus-20240229")
        llm = claudeModel

    qa_chain = RetrievalQA.from_chain_type(llm=llm, 
                                    chain_type="stuff", 
                                    retriever=retriever, 
                                    return_source_documents=True)
    
    query = \
    f"As the travel expert, imagine a user is preparing for a trip and asks you about a specific location and timing. " \
    f"Your task is to provide them with essential information, weather advice, and local recommendations for that location. " \
    f"The result should be in a structured format including 'Essentials, precautions, place to visit, " \
    f"recommended hotel and recommended restaurant'. " \
    f"The Travel location is {destination}." \
    f"Additional Context and Goals:" \
    f"Upon subsequent user queries, ensure to include personal special needs of having a {tripType} trip."

    llm_response = qa_chain.invoke(query)
    return llm_response['result'], llm_response["source_documents"]
