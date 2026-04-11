import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(page_title="Moderation Dashboard", layout="wide")

st.title("Content Moderation Analytics Dashboard")

try:
    df = pd.read_csv("moderation_log.csv")

    df["timestamp"] = pd.to_datetime(df["timestamp"])

except:
    st.warning("No data available yet")
    st.stop()

st.subheader("Overview")

col1, col2, col3 = st.columns(3)

col1.metric("Total Requests", len(df))
col2.metric("High Risk", len(df[df["action"] == "Block"]))
col3.metric("Safe", len(df[df["action"] == "Allow"]))

st.subheader("Toxicity Trend")

fig, ax = plt.subplots()
ax.plot(df["timestamp"], df["score"])
ax.set_xlabel("Time")
ax.set_ylabel("Score")

st.pyplot(fig)

st.subheader("Category Distribution")

category_cols = ['toxic','severe_toxic','obscene','threat','insult','identity_hate']

st.bar_chart(df[category_cols].mean())

st.subheader("Flagged Content")

flagged = df[df["action"] == "Block"]

if not flagged.empty:
    for i, row in flagged.iterrows():
        with st.expander(f" {row['text'][:60]}..."):
            st.write(f"Score: {row['score']}")
            st.write(f"Time: {row['timestamp']}")
else:
    st.info("No flagged content yet")
