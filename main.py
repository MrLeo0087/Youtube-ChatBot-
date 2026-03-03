import streamlit as st
from caption_generator import transcript_generator


st.set_page_config(
    page_title="Youtube Video Summarizer",
    page_icon="📄")

# ------- SESSION ---------
if 'transcript' not in st.session_state:
    st.session_state.transcript = "" 

if 'page' not in st.session_state:
    st.session_state.page = 'home'

if 'gemini_api' not in st.session_state:
    st.session_state.gemini_api = ""

if 'groq_api' not in st.session_state:
    st.session_state.groq_api = ""

if 'llm_type' not in st.session_state:
    st.session_state.llm_type = "DEFAULT"

if 'url' not in st.session_state:
    st.session_state.url = ""

if 'summary' not in st.session_state:
    st.session_state.summary = ""


# ----- SIDEBAR -------
with st.sidebar:
    st.markdown("""
        <div>
        <h2 style="font-family: Verdana, Geneva, Tahoma, sans-serif;font-size: 28px;text-align: center;">
                    SETTING⚙️
                    </h2>         
        </div>  
    """,unsafe_allow_html=True)
    st.divider()
    URL = st.text_input("Video URL",placeholder="Paste your link here",key="URL")
    st.session_state.url = URL
    st.divider()

    # BUTTON
    if st.button("GET TRANSCRIPT",type='primary',use_container_width=True):
        if st.session_state.url:
            transcript = transcript_generator(URL)
            full = ""
            for i in transcript:
                full+=i
            st.session_state.transcript = full
    if st.button('HOME🏡',use_container_width=True):
        st.session_state.page = "home"
        
    if st.button('SUMMARY📝',use_container_width=True):
        st.session_state.page = "summary"

    if st.button('CHAT💬',use_container_width=True):
        st.session_state.page = "chat"

    if st.button('NOTE🗒️',use_container_width=True):
        st.session_state.page = "note"


if st.session_state.page == 'home':
    st.title("Youtube Video Summarizer")
    st.subheader("By Darshan")

    st.divider()


    model_type = st.selectbox('Select LLM',['DEFAULT','GEMINI','GROQ','OLLAMA (LOCAL)'])

    if model_type == "DEFAULT":
        st.session_state.llm_type = "DEFAULT"

        st.text_input("API KEY (GEMINI)", type="password", key="gemini_api")
        st.text_input("API KEY (GROQ)", type="password", key="groq_api")

        if st.session_state.gemini_api and st.session_state.groq_api:
            st.success("""\n
                        Summarize Model -> meta-llama/llama-4-scout-17b-16e-instruct \n 
                        Chat Model -> gemini-2.5-flash-lite \n
                        Note Model -> gemini-2.5-flash""")

    if model_type == "GEMINI":
        st.session_state.llm_type = "GEMINI"
        st.text_input("API KEY (GEMINI)", type="password", key="gemini_api")
        if st.session_state.gemini_api:
            st.success("""\n
                    Summarize Model -> gemini-2.5-flash \n 
                    Chat Model -> gemini-2.5-flash-lite \n
                    Note Model -> gemini-2.5-flash""")
        
    elif model_type == "GROQ":
        st.session_state.llm_type = "GROQ"
        st.text_input("API KEY (GROQ)", type="password", key="groq_api")
        if st.session_state.groq_api:
            st.success("""\n
                    Summarize Model -> llama-3.1-8b-instant \n 
                    Chat Model -> meta-llama/llama-4-maverick-17b-128e-instruct \n
                    Note Model -> meta-llama/llama-4-scout-17b-16e-instruct""")
            
    elif model_type == 'OLLAMA (LOCAL)':
        st.success("""\n
                    Summarize Model -> qwen2.5:3b \n 
                    Chat Model -> Phi-4-Mini \n
                    Note Model -> Phi-4-Mini""")
    if st.session_state.transcript:
        st.text_area('Transcript',value=st.session_state.transcript)
        
    

        
if st.session_state.page == 'summary':
    st.title("📝 Video Summary")
    st.divider()

    if not st.session_state.transcript:
        st.warning("⚠️ No transcript found. Please go to the sidebar and click 'GET TRANSCRIPT' first.")
    
    elif not st.session_state.groq_api:
        st.warning("⚠️ Groq API Key is missing. Please enter it on the Home page.")

    else:
        if not st.session_state.summary:
            with st.spinner("Llama is reading the transcript... please wait..."):
                try:
                    from model_choice.default import summary
                    result = summary(st.session_state.groq_api, st.session_state.transcript)
                    st.session_state.summary = result
                    st.success("Summary Generated!")
                except Exception as e:
                    st.error(f"Error generating summary: {e}")

        st.warning("Final Summary")
        st.markdown(st.session_state.summary) 

        with st.expander("Edit Summary"):
            st.text_area(
                'Edit the markdown below:', 
                height=400, 
                key='summary'
            )

        st.divider()

        if st.button("🔄 Regenerate Summary"):
            st.session_state.summary = ""
            st.rerun()



if st.session_state.page == 'chat':
    pass
    # if st.session_state.llm_type == "DEFAULT":
    #     if st.session_state.transcript and st.session_state.gemini_api:
    #         from model_choice.default import chat
    #         result = chat(st.session_state.gemini_api,st.session_state.transcript)
    #         st.session_state.summary = result

    #         st.text_area('Summary',value=st.session_state.summary)

    #     else:
    #         st.warning("SOME ERROR ... CHECK API AND TRANSCRIPT")


if st.session_state.page == 'note':
    st.markdown('Note')
