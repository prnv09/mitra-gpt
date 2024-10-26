from openai import OpenAI
import time
import os
from dotenv import load_dotenv
import streamlit as st
load_dotenv()

ASSISTANT_ID = os.getenv('ASSISTANT_ID')
OPENAI_KEY = os.getenv('OPENAI_KEY')

MATH_ASSISTANT_ID = ASSISTANT_ID

client = OpenAI(api_key=OPENAI_KEY)

def submit_message(assistant_id, thread, user_message):
    client.beta.threads.messages.create(
        thread_id=thread.id, role="user", content=user_message,
        file_ids=['file-bMleCcB3btG9JFTx9ZaCzyLL','file-smveIqQRXUJaQEYVwaEkFpSH','file-qMXQ3k8TC979ETJxeqpc917o','file-kJKz9KUi6UE1uDeipJbuVEUy']
    )
    return client.beta.threads.runs.create(
        thread_id=thread.id,
        assistant_id=assistant_id,
    )


def get_response(thread):
    return client.beta.threads.messages.list(thread_id=thread.id, order="asc")

def create_thread_and_run(user_input):
    thread = client.beta.threads.create()
    run = submit_message(MATH_ASSISTANT_ID, thread, user_input)
    return thread, run

def pretty_print(messages):
    print("# Messages")
    for m in messages:
        st.write(f"{m.role}: {m.content[0].text.value}")
    print()

def wait_on_run(run, thread):
    while run.status == "queued" or run.status == "in_progress":
        run = client.beta.threads.runs.retrieve(
            thread_id=thread.id,
            run_id=run.id,
        )
        time.sleep(0.5)
    return run

def run(query):
    thread1, run1 = create_thread_and_run(query)
    run1 = wait_on_run(run1, thread1)
    pretty_print(get_response(thread1))

def main():
    # Emulating concurrent user requests
    st.title("MITRA Chatbot")
    user_question = st.text_input("Ask a question about your documents:")
    if user_question:
        run(user_question)

main()