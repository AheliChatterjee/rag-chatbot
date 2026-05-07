from rag.vectorstore import load_vector_store


def get_retriever():

    vector_store = load_vector_store()

    retriever = vector_store.as_retriever(

        search_type="similarity",

        search_kwargs={"k": 5}
    )

    return retriever