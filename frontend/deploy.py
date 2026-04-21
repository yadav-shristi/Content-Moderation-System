import streamlit as st
import pickle
import numpy as np
import os
import hashlib
import json
import time

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

model_path = os.path.join(BASE_DIR, "toxicity_model.pkl")
tfidf_path = os.path.join(BASE_DIR, "tfidf_vectorizer.pkl")

with open(model_path, "rb") as f:
    model = pickle.load(f)

with open(tfidf_path, "rb") as f:
    tfidf = pickle.load(f)

labels = ['toxic','severe_toxic','obscene','threat','insult','identity_hate']

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
        json.dump(users, f)

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "username" not in st.session_state:
    st.session_state.username = ""

if "last_text" not in st.session_state:
    st.session_state.last_text = ""

def login_signup():
    st.title("Content Moderation System")
    menu = st.radio("Select Option", ["Login", "Signup"])

    users = load_users()

    if menu == "Signup":
        new_user = st.text_input("Username")
        new_pass = st.text_input("Password", type="password")

        if st.button("Signup"):
            if new_user in users:
                st.warning("User exists")
            else:
                users[new_user] = hash_password(new_pass)
                save_users(users)
                st.success("Account created")

    elif menu == "Login":
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")

        if st.button("Login"):
            if username in users and users[username] == hash_password(password):
                st.session_state.logged_in = True
                st.session_state.username = username
                st.rerun()
            else:
                st.error("Invalid login")

def main_app():
    st.sidebar.title(st.session_state.username)

    if st.sidebar.button("Logout"):
        st.session_state.logged_in = False
        st.rerun()

    st.title("Content Moderation")

    text = st.text_area("Enter text")

    if text:
        with st.spinner("Analyzing..."):
            vec = tfidf.transform([text])
            pred = model.predict_proba(vec)[0]

            for l, p in zip(labels, pred):
                st.write(f"{l}: {round(p*100,2)}%")

            score = np.mean(pred)*100

            if score > 60:
                st.error("High Risk")
            elif score > 30:
                st.warning("Moderate Risk")
            else:
                st.success("Safe")

if not st.session_state.logged_in:
    login_signup()
else:
    main_app()
