import streamlit as st
from keras.models import load_model
import numpy as np
import pickle
from keras.preprocessing.text import Tokenizer
from keras.preprocessing.sequence import pad_sequences

# Set page config for the app
st.set_page_config(page_title="KPLC Chatbot", page_icon="⚡", layout="centered")

# Load the saved model
model = load_model('categorization_model.h5')

# Custom CSS for black background and blue accents
st.markdown(
    """
    <style>
    .stApp {
        background-color: #000000;
        background-image: linear-gradient(180deg, #000000 0%, #0d47a1 100%);
        color: white;
    }
    .stTextInput, .stButton {
        background-color: #0d47a1;
        color: white;
    }
    h1, h2, h3, h4, h5, h6 {
        color: #2196f3;
    }
    .stTextInput > div > input {
        background-color: #1c1c1c;
        color: white;
    }
    .stButton > button {
        background-color: #1c1c1c;
        color: white;
        border: 2px solid #2196f3;
    }
    .stButton > button:hover {
        background-color: #2196f3;
        color: white;
    }
    .footer {
        position: fixed;
        left: 0;
        bottom: 0;
        width: 100%;
        background-color: #000000;
        color: #2196f3;
        text-align: center;
        padding: 10px;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Title and Subheader
st.title("⚡ KPLC Customer Support Chatbot")
st.subheader("Get instant responses to your queries")

# Custom responses for each category
responses = {
    2: "Hello, apologies, kindly share your account details, exact location and phone number for assistance.",
    3: "Hello, apologies for the delay kindly DM us your meter/account number . You can also check the last 3 token transactions you have made using *977#.",
    4: "Hi. Apologies for the inconvenience. It is a faulty transformer issue affecting the area. We are working to resolve the issue. ",
    0: "Send an email to customercare@kplc.co.ke indicating your account details, exact location and phone number and request for your bill statement",
    1: "If you have a complaint, we're here to listen. Please provide more details so we can assist you better.",
}

# Load the saved tokenizer
with open('tokenizer.pkl', 'rb') as f:
    tokenizer = pickle.load(f)

# Function to preprocess text using Tokenizer and pad_sequences
def preprocess_text(text):
    # Convert text to sequences
    seq = tokenizer.texts_to_sequences([text])
    # Pad sequences
    padded = pad_sequences(seq, maxlen=50)
    return padded

# Function to predict category
def predict_category(text):
    processed_text = preprocess_text(text)
    prediction = model.predict(processed_text)
    category = np.argmax(prediction, axis=1)[0]
    response = responses.get(category, "Sorry, I couldn't understand your request. Please try again.")
    return category, response

# Streamlit interface with black background and blue accents
user_input = st.text_input("Enter your query here:")

if st.button("Submit"):
    category, response = predict_category(user_input)
    st.write(response)

# Footer
st.markdown("""
    <div class="footer">
        <p>© 2024 KPLC | Powered by Streamlit</p>
    </div>
    """, unsafe_allow_html=True)