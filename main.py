from SEOOptimizer import topic_generator, content_generator
import streamlit as st
from streamlit_option_menu import option_menu


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

with st.sidebar:
    st.write('Enter OpenAI API key below')
    OPEN_AI_API = st.text_input(
        'OpenAI API Key 🔑' ,placeholder='Paste your key(🔑) here',type="password")
    if not OPEN_AI_API:
        st.warning(
            body='Kindly enter you API 🔑 in the side bar to chat with us' ,icon='⚠️')


Ribbon = option_menu(None, ["Topic Generator", "Generate Content", "Content Response"],
                     icons=['house', 'list-task', "list-task"],
                     menu_icon="cast", default_index=0, orientation="horizontal",
                     styles={
    "container": {"padding": "0!important", "background-color": "#fafafa"},
    "icon": {"color": "orange", "font-size": "25px"},
    "nav-link": {"font-size": "25px", "text-align": "left", "margin": "0px", "--hover-color": "#eee"},
    "nav-link-selected": {"background-color": "grey"},
})


def function_to_generate(Ribbon):

    if Ribbon == "Topic Generator":

        st.session_state.topic_selected = None
        st.session_state.topic_response_for_generate_content = []
        
        topic_type = st.radio('**Select Content Type**', [
                              'Blog Post', 'Article', 'Email Newsletter', 'Story'], horizontal=True, key="topic_radiobutton")
        temp_option = st.radio('Select how mainstream or wild you want the idea to be ?', [
                               'Mainstream idea', 'Different Ideas', 'Out Of Ordinary Ideas', 'Wild Idea'], horizontal=True)
        topic_language = st.selectbox('**Select a language**', ['English', 'Hindi', 'Spanish', 'French', 'German', 'Mandarin Chinese', 'Arabic',
                                                                'Portuguese', 'Russian', 'Japanese', 'Italian', 'Turkish', 'Korean',
                                                                'Dutch', 'Swedish', 'Polish', 'Vietnamese', 'Hebrew', 'Thai', 'Greek',
                                                                'Czech', 'Romanian', 'Hungarian', 'Malay', 'Swahili', 'Finnish',
                                                                'Icelandic', 'Danish', 'Norwegian', 'Filipino', 'Indonesian'], key="topic_language")
        text = st.text_input(
            'Input some text to generate Topics..', key="topic_text")
        if text:
            if st.button("Generate Topics"):
                response = topic_generator(
                    text, temp_option, topic_language, topic_type, OPEN_AI_API)
                st.session_state.topic_response.append(response)

            print(st.session_state.topic_response)
            if st.session_state.topic_response:
                topic = st.radio('Recommended Topics',
                                 st.session_state.topic_response[-1],)
                # if topic:
                #     if st.button('Copy'):
                #         pyperclip.copy(topic)
                #         st.success('Text copied successfully!')


if Ribbon == 'Generate Content':
    st.session_state.topic_response = []

    if "disabled" not in st.session_state:
        st.session_state.disabled = False

    content_type = st.radio('**Select Content Type**',
                            ['Blog Post', 'Article', 'Email Newsletter', 'Story'], horizontal=True)
    content_length = st.radio(
        '**Select Content Length**', ['Short', 'Medium', 'Large'], horizontal=True)

    content_language = st.selectbox('**Select a language**', ['English', 'Hindi', 'Spanish', 'French', 'German', 'Mandarin Chinese', 'Arabic',
                                                              'Portuguese', 'Russian', 'Japanese', 'Italian', 'Turkish', 'Korean',
                                                              'Dutch', 'Swedish', 'Polish', 'Vietnamese', 'Hebrew', 'Thai', 'Greek',
                                                              'Czech', 'Romanian', 'Hungarian', 'Malay', 'Swahili', 'Finnish',
                                                              'Icelandic', 'Danish', 'Norwegian', 'Filipino', 'Indonesian'])
    focus_market = st.selectbox('**Focus Market**', ['India', 'Brazil', 'France ', 'USA', 'Germany', 'China', 'Saudi Arabia',
                                                     'Mexico', 'Russia', 'Japan', 'Italy', 'Turkey', 'South Korea',
                                                     'Netherlands', 'Sweden', 'Poland', 'Vietnam', 'Israel', 'Thailand', 'Greece',
                                                     'Czech Republic', 'Romania', 'Hungary', 'Malaysia', 'Kenya', 'Finland',

                                                     'Iceland', 'Denmark', 'Norway', 'Philippines', 'United States'])
    audience_type = st.radio(
        '**Audience Type**', ['Neutral', 'Professional', 'Funny', 'Friendly'], horizontal=True)

    content_topic = st.text_input(
        'Input some text to generate Topics..', key="content_topic_key")
    st.session_state.content_topic=content_topic
    if st.session_state.content_topic:
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
                st.write(f"Topic is {st.session_state.topic_selected}")

    if st.session_state.topic_selected:
        if st.button("Generate Content", disabled=st.session_state.disabled,on_click=hider,key="contentgenerator"):
            content_topic=""
            with st.spinner("Generating Content Wait ..."):
                content_response = content_generator(
                    st.session_state.topic_selected, content_type, content_length, focus_market, content_language, audience_type, OPEN_AI_API)
                st.session_state.topic_selected = None
            if content_response:
                st.session_state.content_response.append(content_response)
                st.text_area(label="Content Generated...",
                             height=1000, value=content_response)


if Ribbon == 'Content Response':
    st.session_state.topic_selected = None
    st.session_state.topic_response_for_generate_content = []
    if st.session_state.content_response:
        st.text_area(label=" Here the response of your Search",
                     height=1000, value=st.session_state.content_response[-1])


if __name__ == "__main__":
    function_to_generate(Ribbon)
