import streamlit as st
from dotenv import load_dotenv
import qdrant_client

from langchain.chat_models import ChatOpenAI
from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationalRetrievalChain
from htmlTemplates import css, bot_template, user_template
from langchain.vectorstores import Qdrant
from langchain.embeddings.openai import OpenAIEmbeddings

import os

def get_vectorstore():
    client = qdrant_client.QdrantClient(
        os.getenv("QDRANT_HOST"),
        api_key=os.getenv("QDRANT_API_KEY")
    )
        
    embeddings = OpenAIEmbeddings()

    vector_store = Qdrant(
        client=client,
        collection_name=os.getenv("QDRANT_COLLECTION_NAME"),
        embeddings=embeddings,
    )

    # vector_store2 = Qdrant(
    #     client=client,
    #     collection_name="QDRANT_COLLECTION_NAME2",
    #     embeddings=embeddings,
    # )

    # # Concatenate the two vector stores
    # vector_store = vector_store1.concat(vector_store2)

    return vector_store



# def get_vectorstore2():
#   """
#   Gets a vector store for multiple collections.

#   Returns:
#     A list of Qdrant objects, one for each collection.
#   """

#   client = qdrant_client.QdrantClient(
#       os.getenv("QDRANT_HOST"),
#       api_key=os.getenv("QDRANT_API_KEY")
#   )

#   embeddings = OpenAIEmbeddings()

#   # Get the list of collection names
#   collection_names = os.getenv("QDRANT_COLLECTION_NAMES").split(",")

#   from langchain.vectorstores import LangChainVectorStore

#   vector_store = LangChainVectorStore(
#         embeddings=OpenAIEmbeddings(),
#     )

#   # Iterate over the list of collection names and create a Qdrant object for each collection
#   for collection_name in collection_names:
#     vector_store.append(Qdrant(
#         client=client,
#         collection_name=collection_name,
#         embeddings=embeddings,
#     ))

#   # Return the list of Qdrant objects
#   return vector_store

def get_conversation_chain(vectorstore):
    llm = ChatOpenAI(temperature=0.6)
    memory = ConversationBufferMemory(memory_key='chat_history', return_messages=True)
    conversation_chain = ConversationalRetrievalChain.from_llm(
        llm=llm,
        retriever=vectorstore.as_retriever(),
        memory=memory
    )
    return conversation_chain

def handle_userinput(user_question):
    response = st.session_state.conversation({'question': user_question})
    st.session_state.chat_history = response.get('chat_history', [])

    for i, message in enumerate(st.session_state.chat_history):
        if i % 2 == 0:
            # content_after_pipe = message.content[16:].strip()
            st.write(user_template.replace("{{MSG}}", message.content), unsafe_allow_html=True)
        else:
            
            st.write(bot_template.replace("{{MSG}}", message.content), unsafe_allow_html=True)

def main():
    load_dotenv()
    st.set_page_config(page_title="CurBot", page_icon="images/CurBot chatbot.png")
    st.write(css, unsafe_allow_html=True)

    if "conversation" not in st.session_state:
        st.session_state.conversation = None
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = None

    st.header("Curriculum Bot")
    user_question = st.text_input("ECNG 1009 Edition")

    if user_question:
        handle_userinput(user_question)

    

    vectorstore = get_vectorstore()

    # create conversation chain
    if st.session_state.conversation is None:
        st.session_state.conversation = get_conversation_chain(vectorstore)

if __name__ == '__main__':
    main()
