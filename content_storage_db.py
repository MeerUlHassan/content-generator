from langchain.text_splitter import CharacterTextSplitter
from langchain_community.embeddings import HuggingFaceEmbeddings
from pinecone import Pinecone as pp
from langchain_community.vectorstores.pinecone import Pinecone
import streamlit as st





def text_splitter_and_store_in_db(data_to_store):
    for content_topic, dict_content_details in data_to_store.items():
        content_text=dict_content_details["content_text"]
        text_splitter = CharacterTextSplitter(separator="\n\n\n\n\n\n",chunk_size=1000, chunk_overlap=0)
        document = text_splitter.create_documents(texts=[content_text], metadatas=[{"content_topic":content_topic,"content_type":dict_content_details["content_type"],"content_language":dict_content_details["language"],"focus_market":dict_content_details["focus_market"],"audience_type":dict_content_details["audience_type"],"content_length":dict_content_details["content_length"]}])
        content_docs = text_splitter.split_documents(document)
        response = store_data_in_pinecone(content_docs)
        return response


def store_data_in_pinecone(document):
    index_name = 'generated-content-storage'
    embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
    pp(api_key=st.secrets["PINECONE_API_KEY"])
    Pinecone.from_documents(document, embeddings, index_name=index_name)
    return "Successfully Uploaded"
def search_similar_topics(topic_text):
    index_name = 'generated-content-storage'
    embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
    docsearch = Pinecone.from_existing_index(index_name, embeddings)
    query = topic_text
    docs = docsearch.similarity_search(query, k=5)
    if len(docs)>=5:
        list_of_5_similiar_topic=[]
        for doc in docs:
            topic_name=doc.metadata["content_topic"]
            list_of_5_similiar_topic.append(topic_name)
        return list_of_5_similiar_topic
    else :
        return None    

def search_similar():
    index_name = 'generated-content-storage'
    embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
    docsearch = Pinecone.from_existing_index(index_name, embeddings)
    query = "https://www.ongraph.com/market-research-software-tools-for-survey-creation/"
    docs = docsearch.similarity_search(query, k=1)


def process_to_store_data(content_topic,content_text,content_type,language,focus_market,audience_type,content_length):
    data_to_store={content_topic:{"content_text":content_text,"content_type":content_type,"language":language,"focus_market":focus_market,"audience_type":audience_type,"content_length":content_length}}
    response = text_splitter_and_store_in_db(data_to_store)
    return response
    


def get_content_from_database(content_topic,content_type,focus_market,content_language,audience_type,content_length):
    try:
        query = content_topic
        index_name = 'generated-content-storage'
        embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
        docsearch = Pinecone.from_existing_index(index_name, embeddings)
        docs = docsearch.similarity_search(query, k=1)
        if (docs[0].metadata["content_topic"] == query and
        docs[0].metadata["content_type"] == content_type and
        docs[0].metadata["content_language"] == content_language and
        docs[0].metadata["focus_market"] == focus_market and
        docs[0].metadata["audience_type"] == audience_type and
        docs[0].metadata["content_length"] == content_length):
            print("geting from database")
            return docs[0].page_content
        else:
            st.session_state.spinner_status = "Sorry not find anything in Database .. wait "
            return None
    except Exception as e:
        return None
        

