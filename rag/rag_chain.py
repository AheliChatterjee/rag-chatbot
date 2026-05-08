from dotenv import load_dotenv
import streamlit as st
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

from rag.retriever import get_retriever

# Load environment variables
load_dotenv()

# Initialize LLM
llm = ChatGroq(
    api_key=st.secrets["GROQ_API_KEY"],
    model="llama-3.1-8b-instant",
    temperature=0.3
)
# Prompt template
prompt = ChatPromptTemplate.from_template(
    """
     You are a helpful AI research assistant.

    Answer the user's question ONLY using the provided context.

    Rules:
    - If the answer is not present in the context, say:
      "I could not find this information in the uploaded document."
    - Do NOT use outside knowledge.
    - Keep answers accurate and concise.

    Context:
    {context}

    Question:
    {question}
    """
)

# Output parser
output_parser = StrOutputParser()


def generate_rag_response(question):

    retriever = get_retriever()

    retrieved_docs = retriever.invoke(question)

    context = "\n\n".join(
        [doc.page_content for doc in retrieved_docs]
    )

    chain = prompt | llm | output_parser

    response = chain.invoke(
        {
            "context": context,
            "question": question
        }
    )

    return response