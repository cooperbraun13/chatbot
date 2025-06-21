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

def handle_conversation():
  context = ""
  print("Welcome to the AI ChatBot, type 'exit' to quite.")
  while True:
    user_input = input("You: ")
    if user_input.lower() == "exit":
      break
    
    result = chain.invoke({"context": "", "question": user_input})
    print("Bot: ", result)
    context += f"\nUser: {user_input}\nAI: {result}"
    
if __name__ == "__main__":
  handle_conversation()