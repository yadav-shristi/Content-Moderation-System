import streamlit as st
import json
import os
import hashlib
import time
import pickle
import numpy as np

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
model_path = os.path.join(BASE_DIR, "toxicity_model.pkl")
tfidf_path = os.path.join(BASE_DIR, "tfidf_vectorizer.pkl")
st.write("Current Directory:", BASE_DIR)
st.write("Files here:", os.listdir(BASE_DIR))

with open(model_path, "rb") as f:
    model = pickle.load(f)

with open(tfidf_path, "rb") as f:
    tfidf = pickle.load(f)

labels = [
    'toxic',
    'severe_toxic',
    'obscene',
    'threat',
    'insult',
    'identity_hate'
]

USER_FILE = os.path.join(BASE_DIR, "users.json")

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def load_users():
    if os.path.exists(USER_FILE):
        with open(USER_FILE, "r") as f:
            return json.load(f)
    return {}

def save_users(users):
    with open(USER_FILE, "w") as f:
        json.dump(users, f, indent=4)

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "username" not in st.session_state:
    st.session_state.username = ""

if "last_text" not in st.session_state:
    st.session_state.last_text = ""

def login_signup():

    st.title("Moderation System")

    menu = st.radio("Select Option", ["Login", "Signup"])

    users = load_users()

    if menu == "Signup":
        st.subheader("Create Account")

        new_user = st.text_input("Username")
        new_pass = st.text_input("Password", type="password")

        if st.button("Signup"):
            if new_user in users:
                st.warning("User already exists")
            elif new_user == "" or new_pass == "":
                st.warning("Fields cannot be empty")
            else:
                users[new_user] = hash_password(new_pass)
                save_users(users)
                st.success("Account created successfully")

    elif menu == "Login":
        st.subheader("Login")

        username = st.text_input("Username")
        password = st.text_input("Password", type="password")

        if st.button("Login"):
            if username in users and users[username] == hash_password(password):
                st.session_state.logged_in = True
                st.session_state.username = username
                st.success(f"Welcome {username}")
                st.rerun()
            else:
                st.error("Invalid credentials")

def main_app():

    st.sidebar.title(f"{st.session_state.username}")

    menu = st.sidebar.radio("Navigation", ["Live Moderation", "Logout"])

    if menu == "Logout":
        st.session_state.logged_in = False
        st.session_state.username = ""
        st.rerun()

    elif menu == "Live Moderation":

        st.title("Content Moderation")
        st.write("Type text below to see real-time toxicity detection")

        user_input = st.text_area("Type here...", key="live_input")

        if user_input != st.session_state.last_text:

            st.session_state.last_text = user_input

            if len(user_input.strip()) > 5:

                time.sleep(0.5)

                with st.spinner("Analyzing..."):

                    text_vec = tfidf.transform([user_input])
                    prediction = model.predict_proba(text_vec)[0]

                    st.subheader("📊 Live Results")

                    for label, prob in zip(labels, prediction):
                        st.write(f"{label}: {round(prob*100,2)}%")

                    overall_score = np.mean(prediction) * 100

                    st.subheader("⚡ Overall Score")
                    st.write(f"{round(overall_score,2)} / 100")

                    if overall_score > 60:
                        st.error("🚨 High Risk - Content Blocked")
                        st.markdown(
                            f"<div style='background-color:#ffcccc;padding:10px;border-radius:5px'>{user_input}</div>",
                            unsafe_allow_html=True
                        )

                    elif overall_score > 30:
                        st.warning("⚠ Moderate Risk - Be Careful")

                    else:
                        st.success("Safe Content")

            elif user_input.strip() != "":
                st.info("Keep typing... (minimum 5 characters for analysis)")

if not st.session_state.logged_in:
    login_signup()
else:
    main_app()
