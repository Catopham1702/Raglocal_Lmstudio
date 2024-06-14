from langchain.vectorstores.chroma import Chroma
from langchain_community.embeddings import HuggingFaceInstructEmbeddings
from langchain_core.messages import AIMessage, HumanMessage
from langchain.prompts import ChatPromptTemplate
from openai import OpenAI
import streamlit as st

CHROMA_PATH = "chroma"

PROMPT_TEMPLATE = """
Answer the user's question based on the below context:
{context}
This is the question:
{question}
"""

# Prepare the DB.
embedding_function = HuggingFaceInstructEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
db = Chroma(persist_directory=CHROMA_PATH, embedding_function=embedding_function)

# Point to the local server
client = OpenAI(base_url="http://localhost:1234/v1", api_key="not-needed")

def chat_with_gpt(prompt):
    response = client.chat.completions.create(
        model="local-model",
        messages=[
            {"role": "user", "content": str(prompt)}
        ],
        temperature=0.7,
    )
    return response.choices[0].message.content

def main():
    st.set_page_config(page_title="RAG example", page_icon="🤖")
    st.title("RAG example")

    # Initialize chat history
    if "messages" not in st.session_state:
        st.session_state.messages = []

    if "local-model" not in st.session_state:
        st.session_state["local-model"] = "local-model"

    # Display initial assistant message
    if not st.session_state.messages:
        st.session_state.messages.append({"role": "assistant", "content": "I'm ready, waiting for questions."})

    # Display chat messages from history on app rerun
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Get user query
    if query := st.chat_input("Question:"):
        with st.chat_message("user"):
            st.markdown(query)

        # Search the DB
        results = db.similarity_search_with_relevance_scores(query, k=3)
        context_text = " ".join([doc.page_content for doc, _ in results])
        prompt_template = ChatPromptTemplate.from_template(PROMPT_TEMPLATE)
        prompt = prompt_template.format(context=context_text, question=query)

        st.session_state.messages.append({"role": "user", "content": query})

        # Get assistant response
        response = chat_with_gpt(prompt)
        st.session_state.messages.append({"role": "assistant", "content": response})

        with st.chat_message("assistant"):
            st.markdown(response)

if __name__ == "__main__":
    main()
