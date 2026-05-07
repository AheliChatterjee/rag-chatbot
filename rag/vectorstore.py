from langchain_chroma import Chroma

from rag.embeddings import get_embedding_model


CHROMA_PATH = "chroma_db"


def create_vector_store(chunks):

    embedding_model = get_embedding_model()

    vector_store = Chroma.from_documents(

        documents=chunks,

        embedding=embedding_model,

        persist_directory=CHROMA_PATH
    )

    return vector_store


def load_vector_store():

    embedding_model = get_embedding_model()

    vector_store = Chroma(

        persist_directory=CHROMA_PATH,

        embedding_function=embedding_model
    )

    return vector_store