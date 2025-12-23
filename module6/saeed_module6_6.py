pip install streamlit pydantic langchain langchain-openai
import streamlit as st
import sqlite3
from datetime import datetime
from pydantic import BaseModel, root_validator, ValidationError
from langchain_openai import ChatOpenAI
import os


DB_FILE = "chat_metadata.db"
MODEL_NAME = "gpt-4o-mini"

st.set_page_config(page_title="LLM Chat with Metadata", layout="centered")
st.title("💬 LLM Chat with Metadata Storage")


conn = sqlite3.connect(DB_FILE, check_same_thread=False)
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS chat_history (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    question TEXT,
    answer TEXT,
    name TEXT,
    time TEXT,
    number TEXT,
    timestamp TEXT
)
""")
conn.commit()


class Metadata(BaseModel):
    name: str = None
    time: str = None
    number: str = None

    @root_validator
    def check_at_least_one(cls, values):
        if not any(values.values()):
            raise ValueError("At least one of 'name', 'time', or 'number' must be provided")
        return values


llm = ChatOpenAI(
    model=MODEL_NAME,
    temperature=0,
    api_key=os.getenv("OPENAI_API_KEY")
)


def load_history():
    cursor.execute("SELECT question, answer, name, time, number, timestamp FROM chat_history ORDER BY id")
    return cursor.fetchall()

history = load_history()

for q, a, name, time_, number, ts in history:
    st.markdown(f"**Q ({ts})**: {q}")
    st.markdown(f"**A**: {a}")
    meta = ", ".join(f"{k}: {v}" for k, v in [("name", name), ("time", time_), ("number", number)] if v)
    if meta:
        st.markdown(f"**Metadata**: {meta}")
    st.markdown("---")


with st.form(key="chat_form"):
    user_question = st.text_input("Enter your question")
    name = st.text_input("Name (optional)")
    time_input = st.text_input("Time (optional)")
    number = st.text_input("Number (optional)")
    submit = st.form_submit_button("Send")

if submit:
    
    try:
        metadata = Metadata(name=name or None, time=time_input or None, number=number or None)
    except ValidationError as e:
        st.error(f"Validation Error: {e}")
        st.stop()

  
    st.markdown(f"**You:** {user_question}")

    
    answer = llm.invoke(user_question).content
    st.markdown(f"**LLM Answer:** {answer}")

    
    cursor.execute("""
        INSERT INTO chat_history (question, answer, name, time, number, timestamp)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (user_question, answer, metadata.name, metadata.time, metadata.number, datetime.now().isoformat()))
    conn.commit()
    st.success("Saved successfully!")

   
    st.experimental_rerun()
