import streamlit as st
from backend import get_vectorstore, generate_assistant_response

# --- CONFIGURATION ---
st.set_page_config(page_title="MIT Course Assistant", page_icon="🎓", layout="wide")

# --- UI ---
st.title("🎓 MIT Agentic Course Planning Assistant")
st.markdown("""
This assistant helps you plan your terms at MIT using the official course catalog. 
It is running **100% locally** using **Llama 3** and **RAG**.
""")

vstore = get_vectorstore()

if vstore is None:
    st.error("Missing Data: Please put your MIT PDFs in the '/data' folder.")
else:
    # Sidebar for Student Profile
    st.sidebar.header("Student Profile")
    student_history = st.sidebar.text_area(
        "Completed Courses & Grades:",
        placeholder="e.g., Completed 6.1200 with an A, 6.1010 with a B+",
        height=150
    )

    # Chat Interface
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # chat history
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # User Input
    if prompt := st.chat_input("Ask about prerequisites or plan your term..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant"):
            with st.spinner("Consulting Catalog..."):
                # backend for response
                answer = generate_assistant_response(vstore, prompt, student_history)
                
                st.markdown(answer)
                st.session_state.messages.append({"role": "assistant", "content": answer})