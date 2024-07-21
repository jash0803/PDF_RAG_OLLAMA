import os
from langchain_community.document_loaders import UnstructuredFileLoader
from langchain_community.vectorstores import FAISS
# Below converts text to vector embeddings
from langchain_community.embeddings import HuggingFaceBgeEmbeddings
# Converts to smaller chunks and then apply vector embeddings
from langchain.text_splitter import CharacterTextSplitter
# Conversational retrieval
from langchain.chains import retrieval_qa
from langchain_community.llms import Ollama

working_dir = os.path.dirname(os.path.abspath(__file__))

# Correctly instantiate the Ollama object
llm = Ollama(
    model="llama3:latest",
    temperature=0  # Very less random answer and for 1 it gives creative answers
)
embedding = HuggingFaceBgeEmbeddings()

def get_answer(file_name, query):
    file_path = f"{working_dir}/{file_name}"
    # Loading the document
    loader = UnstructuredFileLoader(file_path)
    documents = loader.load()

    # Create text chunks & overlap is done so context is not missed
    text_splitter = CharacterTextSplitter(separator="\n", chunk_size=1000, chunk_overlap=200)

    text_chunks = text_splitter.split_documents(documents)

    # Vector embeddings from text chunks USE CHROMEDB
    knowledge_base = FAISS.from_documents(text_chunks, embedding)

    # QA chain is invoked by the query user has given via response
    # The user's query is converted into vector embedding and mapped with the text chunks (which are in the form of vector embedding)
    qa_chain = retrieval_qa.from_chain_type(
        llm,
        retriever=knowledge_base.as_retriever()
    )
    response = qa_chain.invoke({"query": query})
    return response["result"]
