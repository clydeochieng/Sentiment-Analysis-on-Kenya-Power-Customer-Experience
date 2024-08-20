import streamlit as st
from tensorflow.keras.models import load_model
import numpy as np
import pickle
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences
from nltk.sentiment.vader import SentimentIntensityAnalyzer

# Set page config for the app
st.set_page_config(
    page_title="KPLC Dashboard",
    page_icon="⚡",
    layout="centered",
    initial_sidebar_state="expanded"
)

# Load the saved tokenizer and model
model = load_model('categorization_model.h5')
with open('tokenizer.pkl', 'rb') as f:
    tokenizer = pickle.load(f)

# Title and Subheader
st.title("⚡ KPLC Customer Support ")
st.markdown(" 🤖 Ask me anything about Kenya Power services")
st.subheader("Get instant responses to your queries")

st.markdown("""
    **Key Features:**
    - 🧠 Intelligent Query Categorization
    - 📋 Custom Responses
    - 💬 Real-Time Interaction

    """)

# Sidebar
st.sidebar.header("Navigation")
st.sidebar.write("For more information, visit [KPLC's website](https://www.kplc.co.ke/)")

# Add a button that redirects to the customer feedback page
if st.button("Give Feedback"):
    feedback_url = "https://www.kplc.co.ke/content/item/1764/customer-feedback"
    st.markdown(f"[Click here to provide feedback]({feedback_url})", unsafe_allow_html=True)

# Custom responses for each category
responses = {
    2: "Hello, apologies, kindly share your account details, exact location and phone number for assistance.",
    3: "Hello, apologies for the delay kindly DM us your meter/account number . You can also check the last 3 token transactions you have made using *977#.",
    4: "Hi. Apologies for the inconvenience. It is a faulty transformer issue affecting the area. We are working to resolve the issue. ",
    0: "Send an email to customercare@kplc.co.ke indicating your account details, exact location and phone number and request for your bill statement",
    1: "If you have a complaint, we're here to listen. Please provide more details so we can assist you better.",
}


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


user_input = st.text_input("Enter your query here:")

if st.button("Submit"):
    category, response = predict_category(user_input)
    st.write(response)

# About Us and Contact Us sections side by side
col1, col2 = st.columns(2)

with col1:
    st.header("About Us")
    st.write("""
    Kenya Power and Lighting Company (KPLC) is committed to providing reliable and high-quality electricity services to all Kenyans. 
    We understand the importance of electricity in your daily life, and we are here to support you with any issues you may encounter.
    Our mission is to deliver safe, affordable, and sustainable electricity to every home and business across Kenya.
    """)

with col2:
    st.header("Contact Us")
    st.write("""
    If you need to get in touch with us, please reach out via the following channels:
    - **Email:** customercare@kplc.co.ke
    - **Phone:** +254 20 3201000
    - **Website:** [KPLC Website](https://www.kplc.co.ke)
    - **Social Media:** Follow us on [Twitter](https://twitter.com/KenyaPower_Care), [Facebook](https://www.facebook.com/KenyaPowerLtd/)
    """)

st.markdown(
    """
    <style>
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

# Footer
st.markdown("""
    <div class="footer">
        <p>© 2024 KPLC | Powered by Streamlit</p>
    </div>
    """, unsafe_allow_html=True)