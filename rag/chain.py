from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from dotenv import load_dotenv

load_dotenv()

llm = ChatGroq(
    model="llama-3.1-8b-instant",
    temperature = 0.3
)

prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
    """You are a professional AI assistant.
        Rules:
        - Answer clearly
        - keep response concise
        - be accurate
        - If unsure, say you do not know
    """
        ),
        ("human", "{question}")
    ]
)

output_parser = StrOutputParser()

chain = prompt | llm | output_parser

def generate_response(user_question):
    
    response = chain.invoke(
        {
            "question": user_question
        }
    )
    
    return response