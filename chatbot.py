from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate , MessagesPlaceholder
from langchain_core.output_parsers import StrOutputParser
from dotenv import load_dotenv
import streamlit as st
import os
load_dotenv()


Groq_Api_key = os.getenv('Groq_Api')

# --- CONFIGURATION & HIGH-END UI STYLING ---
st.set_page_config(
    page_title="NavTrip.AI - Your Ultimate Travel Companion", 
    page_icon="✈️", 
    layout="centered"
)

# Premium Global Design Overrides with CSS Keyframe Animations
# FIXED: Changed unsafe_html=True to unsafe_allow_html=True
st.markdown("""
<style>
    /* Global Background & Smooth Typography */
    .stApp {
        background: linear-gradient(135deg, #f4f7f6 0%, #e9eff1 100%);
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
    }
    
    /* Elegant Title Header Animation Card */
    .header-container {
        background: linear-gradient(135deg, #1e3c72 0%, #2a5298 100%);
        padding: 2.5rem;
        border-radius: 20px;
        color: white;
        text-align: center;
        box-shadow: 0 10px 30px rgba(42, 82, 152, 0.15);
        margin-bottom: 2rem;
        animation: slideDown 0.8s cubic-bezier(0.16, 1, 0.3, 1);
    }
    
    .header-container h1 {
        color: #ffffff !important;
        font-weight: 800 !important;
        letter-spacing: -0.5px;
        margin-bottom: 0.5rem;
    }

    /* Animated Loading/Thinking State */
    .travel-loader {
        display: inline-flex;
        align-items: center;
        gap: 6px;
        padding: 12px 20px;
        background: white;
        border-radius: 16px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.05);
        border: 1px solid #e2e8f0;
        animation: pulseFade 1.5s infinite ease-in-out;
    }
    
    .dot {
        width: 8px;
        height: 8px;
        background: #2a5298;
        border-radius: 50%;
        animation: jump 1.2s infinite ease-in-out;
    }
    .dot:nth-child(2) { animation-delay: 0.2s; }
    .dot:nth-child(3) { animation-delay: 0.4s; }

    /* CSS Keyframes Rules */
    @keyframes slideDown {
        from { transform: translateY(-30px); opacity: 0; }
        to { transform: translateY(0); opacity: 1; }
    }
    @keyframes pulseFade {
        0%, 100% { opacity: 0.8; }
        50% { opacity: 1; transform: scale(1.01); }
    }
    @keyframes jump {
        0%, 100% { transform: translateY(0); }
        50% { transform: translateY(-8px); }
    }
</style>
""", unsafe_allow_html=True)

# Render Beautiful Interactive Title Header Box
# FIXED: Changed unsafe_html=True to unsafe_allow_html=True
st.markdown("""
<div class="header-container">
    <h1>✈️ NavTrip.AI</h1>
    <p style="font-size: 1.1rem; opacity: 0.9; font-weight: 400; margin: 0;">Your Ultimate Intelligent Travel Companion</p>
</div>
""", unsafe_allow_html=True)

st.write('Ask for any Questions related to travel and get the best answer from NavTrip.AI')

if not Groq_Api_key:
    st.error("Please set the Groq API key in the .env file.")
    st.stop()

@st.cache_resource
def build_chatbot():
    model = ChatGroq(
        model = 'llama-3.3-70b-versatile',
        api_key=Groq_Api_key,
    )
    
    response = ChatPromptTemplate.from_messages([
        (
        "system",
        """
You are an expert, enthusiastic, and helpful travel assistant called NavTrip AI Tour.

Your mission is to help users plan incredible trips, discover hidden local gems, and provide personalized travel recommendations based on their preferences and interests.

Guidelines for your responses:

- Answer in a detailed, engaging, and user-friendly manner.
- Use highly readable formatting such as:
  - Bold text
  - Bullet points
  - Numbering
  - Emojis
  - Tables
  - Code blocks (when needed)
- Suggest a mix of:
  - Iconic landmarks
  - Hidden gems loved by locals
- Provide practical travel information for each recommendation, including:
  - Best time to visit
  - How to get there
  - Entry fees
  - Opening hours
  - Local tips
- Always provide the source of your information whenever possible.
- Maintain a friendly, professional, and travel-expert tone throughout the conversation.
"""
    ),
    MessagesPlaceholder(variable_name="chat_history"),
    ])
    
    chain = response | model | StrOutputParser() 
    return chain

if __name__ == "__main__":
    
    if not Groq_Api_key:
        raise ValueError("Please set the Groq API key in the .env file.")
    
    bot_chain = build_chatbot()
    
    if 'message_history' not in st.session_state:
        st.session_state.message_history = []
        
    for msg in st.session_state.message_history:
       with st.chat_message(msg["role"]):
            st.markdown(msg["content"])
            
    if user_query := st.chat_input("Ask your travel question here..."):
        st.session_state.message_history.append({"role": "user", "content": user_query})
        with st.chat_message("user"):
            st.markdown(user_query)
            
        # response = bot_chain.invoke({"chat_history": st.session_state.message_history})
        # st.session_state.message_history.append({"role": "assistant", "content": response})
        # with st.chat_message("assistant"):
        #     st.markdown(response)
    
        formated_history = []
        for msg in st.session_state.message_history:
            role = 'human' if msg['role'] == 'user' else 'ai'
            formated_history.append((role , msg['content'])) 
        
        with st.chat_message('assistant'):
            with st.spinner(text=""):
                # FIXED: Changed unsafe_html=True to unsafe_allow_html=True
                st.markdown("""
                <div class="travel-loader">
                    <span style="font-size: 14px; font-weight: 500; color: #4a5568; margin-right: 4px;">Mapping your route</span>
                    <div class="dot"></div>
                    <div class="dot"></div>
                    <div class="dot"></div>
                </div>
                """, unsafe_allow_html=True)
                
                response = bot_chain.invoke({"chat_history": formated_history , 'user_query': user_query})
            st.markdown(response)
        
        st.session_state.message_history.append({"role": "assistant", "content": response})
        
        st.rerun()

    # print('NavTrip.AI bot has Started Its working ! ask you question ( or type) esc to exit \n')
    # while True:
    #     user_query = input("You: ")
    #     if user_query.lower() == 'esc':
    #         print("Exciting NavTrip.AI. Safe travels!")
    #         break
        
        # print("NavTrip.AI is thinking...")
        
        # response = bot_chain.invoke({"chat_history": formated_history + [("user", user_query)]})
        # formated_history.append(("user", user_query))
        # formated_history.append(("assistant", response))
        # print('NavTrip.AI', response)