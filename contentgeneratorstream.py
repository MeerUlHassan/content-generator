import streamlit as st
from langchain.schema import HumanMessage, SystemMessage
from streamlit_option_menu import option_menu
from openai import OpenAI
from langchain_openai import ChatOpenAI
from content_storage_db import process_to_store_data,get_content_from_database
import time

def disable():
    """This function Disables the button
    """
    st.session_state.disabled = True
    
def hider():
    st.session_state["content_topic_key"] = ""
    st.session_state.content_topic=None
    st.session_state.topic_response_for_generate_content = []

def hider2():
    st.session_state.topic_selected = None

def initilize_openai(OPEN_AI_API):
    open_ai = OpenAI(api_key=OPEN_AI_API)
    return open_ai


if "content_length" not in st.session_state:
    st.session_state.content_length=None
if "audience_type" not in st.session_state:
    st.session_state.audience_type=None
if "focus_market" not in st.session_state:
    st.session_state.focus_market = None
if "content_language" not in st.session_state:
    st.session_state.content_language = None
if "content_type" not in st.session_state:
    st.session_state.content_type = None
if "content_topic" not in st.session_state:
    st.session_state.content_topic = None
if "content_response" not in st.session_state:
    st.session_state.content_response = []
if "topic_response_for_generate_content" not in st.session_state:
    st.session_state.topic_response_for_generate_content = []
if "topic_selected" not in st.session_state:
    st.session_state.topic_selected = None
if "topic_response" not in st.session_state:
    st.session_state.topic_response = []

     
     
def convert_temperature_from_string_to_int(temperature_value):
    temperature_for_openai=0.0
    if temperature_value =="Different Ideas":
        temperature_for_openai=0.3
    elif temperature_value=="Out Of Ordinary Ideas":
        temperature_for_openai=0.6
    elif temperature_value=="Wild Idea":
        temperature_for_openai=0.9
    return  temperature_for_openai

        
  
def topic_generator(input_text,temperature_value,topic_language,topic_type,OPEN_AI_API):
    open_ai = initilize_openai(OPEN_AI_API)
    temperature_value_in_number=convert_temperature_from_string_to_int(temperature_value)
    prompt = f"""topic text is {input_text},topic output language is {topic_language} and this topic will be used for {topic_type}
""" 
    messages=[
    {"role": "system", "content": "You are a helpful assistant who will give 5 SEO optimized Topic about given topic text by using given information."},
    {"role": "user", "content": prompt}]
    response=open_ai.chat.completions.create(
            model="gpt-3.5-turbo",
            temperature=temperature_value_in_number,messages=messages)
    
    res=response.choices[0].message.content.split("\n")
    while("" in res):
        res.remove("")
    for i in range(len(res)):
        res[i] = res[i].replace('"', '')
    return res


def content_generator_using_chatopenai(content_topic,content_type,content_length,focus_market,content_language,audience_type,OPEN_AI_API):
    instruction_system="You are a helpful assistant who will create  a content for a given type by following given instructions."
    user_data = f"""content topic is {content_topic},Content type is {content_type} and content length is {content_length},main focused market is of {focus_market} country,type of audience {audience_type},output response will be in {content_language}language.
"""  
    messages = [
    SystemMessage(
        content=instruction_system
    ),
    HumanMessage(
        content=user_data
    )]
    chat = ChatOpenAI(streaming=True,temperature=0.0,api_key=OPEN_AI_API)
    response=chat.stream(messages)
    return response
    
    
 

with st.sidebar:
    OPEN_AI_API = st.text_input(
        'OpenAI API Key 🔑' ,placeholder='Paste your key(🔑) here',type="password")
    if not OPEN_AI_API:
        st.warning(
            body='Kindly enter you API 🔑 here' ,icon='⚠️')

st.title("CONTENT GENERATOR")
Option_Selected = option_menu(None, ["Generate Content","Save Content"],
                     icons=['list-task', "list-task"],
                     menu_icon="cast", default_index=0, orientation="horizontal",
                     styles={
    "container": {"padding": "0!important", "background-color": "black"},
    "icon": {"color": "orange", "font-size": "20px"},
    "nav-link": {"font-size": "20px", "text-align": "left", "margin": "0px", "--hover-color": "#eee"},
    "nav-link-selected": {"background-color": "grey"},
})


def function_to_generate(Option_Selected):

    if Option_Selected == 'Generate Content':
        st.session_state.topic_response = []

        if "disabled" not in st.session_state:
            st.session_state.disabled = False

        content_type = st.radio('**CONTENT TYPE**',
                                ['**Blog Post**', '**Article**', '**Email Newsletter**', '**Story**'], horizontal=True)
        st.session_state.content_type=content_type
        content_length = st.radio(
            '**CONTENT LENGTH**', ['**Short**', '**Medium**', '**Large**'], horizontal=True)
        st.session_state.content_length=content_length
        content_language = st.selectbox(':black[**SELECT LANGUAGE**]', ['English', 'Hindi', 'Spanish', 'French', 'German', 'Mandarin Chinese', 'Arabic',
                                                                'Portuguese', 'Russian', 'Japanese', 'Italian', 'Turkish', 'Korean',
                                                                'Dutch', 'Swedish', 'Polish', 'Vietnamese', 'Hebrew', 'Thai', 'Greek',
                                                                'Czech', 'Romanian', 'Hungarian', 'Malay', 'Swahili', 'Finnish',
                                                                'Icelandic', 'Danish', 'Norwegian', 'Filipino', 'Indonesian'])
        st.session_state.content_language=content_language
        focus_market = st.selectbox('**FOCUS MARKET**', ['India', 'Brazil', 'France ', 'USA', 'Germany', 'China', 'Saudi Arabia',
                                                        'Mexico', 'Russia', 'Japan', 'Italy', 'Turkey', 'South Korea',
                                                        'Netherlands', 'Sweden', 'Poland', 'Vietnam', 'Israel', 'Thailand', 'Greece',
                                                        'Czech Republic', 'Romania', 'Hungary', 'Malaysia', 'Kenya', 'Finland',

                                                        'Iceland', 'Denmark', 'Norway', 'Philippines', 'United States'])
        st.session_state.focus_market=focus_market
        audience_type = st.radio(
            '**AUDIENCE TYPE**', ['Neutral', 'Professional', 'Funny', 'Friendly'], horizontal=True)
        st.session_state.audience_type=audience_type
        content_topic = st.text_input(
            'Enter Topic', key="content_topic_key",placeholder="Enter Topic",label_visibility="collapsed")
        st.session_state.content_topic=content_topic
        if content_topic:
            if st.session_state.disabled == False:
                if st.button("Recommend Some Topics",):
                    temperature_value = 0.0
                    with st.spinner("Recommending Topics ..."):
                        topic_response_for_content = topic_generator(
                            content_topic, temperature_value, content_language, content_type, OPEN_AI_API)

                    topic_response_for_content.insert(0, content_topic)
                    st.session_state.topic_response_for_generate_content.append(
                        topic_response_for_content)
            if st.session_state.disabled == False:
                if st.session_state.topic_response_for_generate_content:
                    topic_selected = st.radio(
                        'Recommended Topics', st.session_state.topic_response_for_generate_content[-1])
                    st.session_state.topic_selected = topic_selected

        if st.session_state.topic_selected:
            if st.button("Generate Content",key="content_generator"):
                with st.spinner("processing..."):
                    content_from_db=get_content_from_database(st.session_state.topic_selected,content_type,focus_market,content_language,audience_type,st.session_state.content_length)
                    if content_from_db:
                        message_placeholder = st.empty()
                        full_response = ""
                        for chunk in content_from_db.split():
                            full_response += chunk + " "
                            time.sleep(0.02)
                            message_placeholder.markdown(full_response + "▌")
                        message_placeholder.markdown(content_from_db) 

                    else :
                        response=content_generator_using_chatopenai(st.session_state.topic_selected,content_type,content_length,focus_market,content_language,audience_type,OPEN_AI_API)
                        # time.sleep(0.5)
                        with st.container(border=True):
                            placeholder = st.empty()
                            full_response=""
                            for chunk in response:
                                full_response+=chunk.content
                                if bool(chunk):
                                    time.sleep(0.02)
                                    placeholder.markdown(full_response + "")
                            st.session_state.content_response=full_response
                
            
    if Option_Selected == "Save Content":
        if "store_topic_in_db" not in st.session_state:
            st.session_state.store_topic_in_db=None
        st.session_state.store_topic_in_db=st.session_state.topic_selected
        st.session_state.topic_selected=None
        st.session_state.topic_response_for_generate_content=[]
        if st.session_state.content_response:
            content_text=st.text_area(label=" Here the response of your Search",
                        height=1000, value=st.session_state.content_response)
            if  st.button("Save",key="savebutton"):
                my_bar = st.progress(0, text="uploading ..")
                response=process_to_store_data(st.session_state.store_topic_in_db,content_text,st.session_state.content_type,st.session_state.content_language,st.session_state.focus_market,st.session_state.audience_type,st.session_state.content_length)   
                st.warning(response,icon="⚠️")
        else:
            st.warning("No Content Found !!", icon="⚠️")
        
    

if __name__ == "__main__":
    
    function_to_generate(Option_Selected)
