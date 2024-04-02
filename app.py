import streamlit as st
import time
from langchain_core.messages import AIMessage, HumanMessage
from langchain_community.document_loaders.web_base import WebBaseLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores.chroma import Chroma
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain_google_genai import GoogleGenerativeAIEmbeddings, ChatGoogleGenerativeAI
from dotenv import load_dotenv
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.chains.history_aware_retriever import create_history_aware_retriever
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain.chains.retrieval import create_retrieval_chain

# load env variable
load_dotenv()

# Function for creating Vectorstore
def get_vectorstore_from_url(url):
    # get the text in document form
    loader = WebBaseLoader(web_path=url)
    document = loader.load()

    # Splitting the document into chunks
    text_splitter = RecursiveCharacterTextSplitter()
    document_chunks = text_splitter.split_documents(documents=document)

    # Create vectorstore for the chunks
    embeddings = OpenAIEmbeddings()
    vector_store = Chroma.from_documents(documents=document_chunks, embedding=embeddings)

    return vector_store


# Function to modify the initial search query into more refined query and get related documents from the vectorstore
def get_context_retriever_chain(vector_store):
    llm = ChatOpenAI()
    # create retriever
    retriever = vector_store.as_retriever()
    
    prompt = ChatPromptTemplate.from_messages([
      MessagesPlaceholder(variable_name="chat_history"),
      ("user", "{input}"),
      ("user", "Given the above conversation, generate a search query to look up in order to get information relevant to the conversation")
    ])
    
    retriever_chain = create_history_aware_retriever(llm, retriever, prompt)
    
    return retriever_chain


# Function to get the retrievals
def get_conversational_rag_chain(retriever_chain):
    llm = ChatOpenAI()

    prompt = ChatPromptTemplate.from_messages([
        ("system", "Answer the user's questions based on the below context:\n\n{context}"),
        MessagesPlaceholder(variable_name="chat_history"),
        ("user", "{input}")
    ])

    # stuff document chain
    stuff_document_chain = create_stuff_documents_chain(llm=llm, prompt=prompt)
    return create_retrieval_chain(retriever=retriever_chain, combine_docs_chain=stuff_document_chain)


# Function to get the response
def get_response(user_input):
    # Retriever Chain
    retriever_chain = get_context_retriever_chain(st.session_state.vector_store)
    # Conversation chain
    conversation_rag_chain = get_conversational_rag_chain(retriever_chain)

    # Getting the rsponse rag chain
    response = conversation_rag_chain.invoke({
        "chat_history": st.session_state.chat_history,
        "input": user_input
    })

    return response['answer']


# App config
st.set_page_config(page_title="Chat With Websites", page_icon="🤖")
st.markdown("<h1 style='font-family: Arial, sans-serif; color: #ffffff;'>Chat With Websites</h1><p style='font-size: 24px;'>Interact with your website in real-time! 💬🌐</p>", unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    st.header("Settings")
    website_url = st.text_input("Website URL")

# If the user didn't put the URL in the URL box, then show this
if website_url is None or website_url == "":
    st.info("Please enter a website URL")

else:
    # Session state
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = [
            AIMessage(content="Hello, I am a bot. How can I help you?")
        ]
    
    if "vector_store" not in st.session_state:
        st.session_state.vector_store = get_vectorstore_from_url(website_url)
    
    # User input
    user_query = st.chat_input("Type your message here...")
    if user_query is not None and user_query != "":
        response = get_response(user_query)
        # Add user query to the "chat_history"
        st.session_state.chat_history.append(HumanMessage(content=user_query))
        # Add llm response to the "chat_history"
        st.session_state.chat_history.append(AIMessage(content=response))
        
    
    # Conversation
    for message in st.session_state.chat_history:
        if isinstance(message, AIMessage):
            with st.chat_message("AI"):
                st.write(message.content)
        elif isinstance(message, HumanMessage):
            with st.chat_message("Human"):
                st.write(message.content)

