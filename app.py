import os
from dotenv import load_dotenv
import streamlit as st
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain_pinecone import PineconeVectorStore
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.messages import HumanMessage, AIMessage
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser

load_dotenv()

# ── Setup ──────────────────────────────────────────────────
@st.cache_resource
def load_components():
    embeddings = OpenAIEmbeddings(
        model="text-embedding-3-small",
        api_key=os.getenv("OPENAI_API_KEY")
    )
    vectorstore = PineconeVectorStore(
        index_name=os.getenv("PINECONE_INDEX_NAME"),
        embedding=embeddings
    )
    llm = ChatOpenAI(
        model="gpt-4o",
        temperature=0,
        api_key=os.getenv("OPENAI_API_KEY")
    )
    retriever = vectorstore.as_retriever(search_kwargs={"k": 3})
    return llm, retriever

def format_docs(docs):
    return "\n\n".join(doc.page_content for doc in docs)

def format_history(chat_history):
    lines = []
    for msg in chat_history:
        if isinstance(msg, HumanMessage):
            lines.append(f"Human: {msg.content}")
        else:
            lines.append(f"Assistant: {msg.content}")
    return "\n".join(lines)

def get_answer(llm, retriever, question, chat_history):
    # Step 1: Rewrite question to be standalone
    if chat_history:
        condense_prompt = ChatPromptTemplate.from_messages([
            ("system", "Given the conversation history and follow up question, "
                      "rewrite the question to be standalone. "
                      "Return ONLY the rewritten question, nothing else."),
            ("human", "History:\n{history}\n\nFollow up question: {question}")
        ])
        condense_chain = condense_prompt | llm | StrOutputParser()
        standalone_question = condense_chain.invoke({
            "history": format_history(chat_history),
            "question": question
        })
    else:
        standalone_question = question

    # Step 2: Retrieve relevant chunks
    docs = retriever.invoke(standalone_question)

    # Step 3: Answer using retrieved chunks
    answer_prompt = ChatPromptTemplate.from_messages([
        ("system", "You are a helpful assistant. Answer the question "
                   "using only the context below. "
                   "If you don't know, say you don't know.\n\n"
                   "Context:\n{context}"),
        ("human", "{question}")
    ])
    answer_chain = answer_prompt | llm | StrOutputParser()
    answer = answer_chain.invoke({
        "context": format_docs(docs),
        "question": standalone_question
    })
    return answer, docs

# Password protection
def check_password():
    if "authenticated" not in st.session_state:
        st.session_state.authenticated = False

    if not st.session_state.authenticated:
        st.title("🤖 RAG Document Chatbot")
        password = st.text_input("Enter demo password", type="password")
        if st.button("Login"):
            if password == "demo2026":
                st.session_state.authenticated = True
                st.rerun()
            else:
                st.error("Incorrect password")
        st.stop()

check_password()

# ── UI ─────────────────────────────────────────────────────
st.set_page_config(page_title="RAG Chatbot", page_icon="🤖")
st.title("🤖 RAG Document Chatbot")
st.caption("Ask anything about your uploaded documents")

st.info("""
📄 **This demo is loaded with Alphabet's Q1 2026 Earnings Report**

Try asking:
- "What was Alphabet's total revenue in Q1 2026?"
- "What did the CEO say about AI?"
- "How did Google Cloud perform?"
- "What was the net income?"
""")

if "messages" not in st.session_state:
    st.session_state.messages = []
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# Display chat history
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# Chat input
if prompt := st.chat_input("Ask a question about your documents..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            llm, retriever = load_components()
            answer, sources = get_answer(
                llm, retriever, prompt,
                st.session_state.chat_history
            )
            st.markdown(answer)

            if sources:
                with st.expander("📄 Sources"):
                    for i, doc in enumerate(sources):
                        page = doc.metadata.get("page", "?")
                        st.markdown(f"**Chunk {i+1} — Page {page}:**")
                        st.caption(doc.page_content[:300] + "...")

    st.session_state.messages.append({"role": "assistant", "content": answer})
    st.session_state.chat_history.extend([
        HumanMessage(content=prompt),
        AIMessage(content=answer)
    ])
