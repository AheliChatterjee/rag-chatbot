from rag.loader import load_pdf
from rag.splitter import split_documents
from rag.vectorstore import create_vector_store

documents = load_pdf("data/NIPS-2017-attention-is-all-you-need-Paper.pdf")

chunks = split_documents(documents)

create_vector_store(chunks)

print("ChromaDB created successfully!")