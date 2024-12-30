import tempfile
import streamlit as st
from embedchain import App

# Define the embedchain_bot function
def embedchain_bot(db_path, huggingface_api_key, groq_api_key):
    return App.from_config(
        config={
            "llm": {
                "provider": "groq",
                "config": {
                    "model": "llama3-groq-70b-8192-tool-use-preview",
                    "temperature": 0.5,
                    "api_key": groq_api_key,
                },
            },
            "vectordb": {
                "provider": "chroma",
                "config": {"dir": db_path},
            },
            "embedder": {
                "provider": "huggingface",
                "config": {
                    "api_key": huggingface_api_key,
                    "model": "sentence-transformers/all-MiniLM-L6-v2",  # Example model
                },
            },
        }
    )

# Create Streamlit app
st.title("Chat with your Gmail Inbox 📧")
st.caption("This app allows you to chat with your Gmail inbox using Groq for the LLM and Hugging Face for embeddings")

# Get API keys from the user
huggingface_api_key = st.text_input("Enter your Hugging Face API Key (for embedding)", type="password")
groq_api_key = st.text_input("Enter your Groq API Key (for querying)", type="password")

# Set the Gmail filter statically
gmail_filter = "to: me label:inbox"

if st.button("Submit"):
    # Add the Gmail data to the knowledge base if API keys are provided
    if huggingface_api_key and groq_api_key:
        # Create a temporary directory to store the database
        db_path = tempfile.mkdtemp()
        # Create an instance of Embedchain App
        app = embedchain_bot(db_path, huggingface_api_key, groq_api_key)
        try:
            app.add(gmail_filter, data_type="gmail")
            st.success(f"Added emails from Inbox to the knowledge base!")
        except Exception as e:
            st.error(f"Error adding Gmail data: {str(e)}")

        # Ask a question about the emails
        prompt = st.text_input("Ask any question about your emails")

        # Chat with the emails
        if prompt:
            try:
                answer = app.query(prompt)
                st.write(answer)
            except Exception as e:
                st.error(f"Error during query: {str(e)}")

# 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