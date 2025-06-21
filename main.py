import streamlit as st
from langchain_ollama import OllamaLLM
from langchain_core.prompts import ChatPromptTemplate

# template for how a question should be answered by the bot
template = """
Answer the question below.

Here is the conversation history: {context}

Question: {question}

Answer:
"""

# chooses the ollama model and prompt and chains them together
model = OllamaLLM(model="llama3")
prompt = ChatPromptTemplate.from_template(template)
chain = prompt | model

# streamlit page config
st.set_page_config(page_title="AI Chatbot", layout="wide")

# title
st.title("💬 AI Chatbot")

# initialize session state for history
if "history" not in st.session_state:
  st.session_state.history = [] # list of (user, bot) tuples
  
# sidebar or header instructions
st.sidebar.markdown("Type your message below and hit **Send**.")

# user input
with st.form(key="chart_form", clear_on_submit=True):
  user_msg = st.text_input("You:", "")
  send = st.form_submit_button("Send")

# when user hits send
if send and user_msg:
  # context string
  context = "\n".join(f"User: {u}\nAI: {a}" for u, a in st.session_state.history)
  # get bot's reply
  bot_reply = chain.invoke({"context": context, "question": user_msg})
  # save user and bot messages
  st.session_state.history.append((user_msg, bot_reply))
  
# display chat history
for user_text, bot_text in st.session_state.history:
  st.markdown(f"**You**: {user_text} ")
  st.markdown(f"**Bot**: {bot_text} ")
  
# clear chat button
if st.sidebar.button("Clear chat"):
  st.session_state.history = []