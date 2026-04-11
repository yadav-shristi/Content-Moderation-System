Content Moderation System

Overview:
The project is a machine learning-based web application that detects toxic, abusive, or harmful text content.
It uses Natural Language Processing (NLP) techniques and a multi-label classification model to analyze user input in real time.
This system is designed to simulate how modern social media platforms moderate user-generated content.

Objectives:
Detect harmful and toxic content automatically.
Classify text into multiple categories.

Features:
User Login
Multi-label Classification into categories:
1. Toxic
2. Severe Toxic
3. Obscene
4. Threat
5. Insult
6. Identity Hate

Workflow:
1. User enters text in the Streamlit UI
2. Text is sent to FastAPI via API request
3. Backend processes text using TF-IDF
4. Model predicts toxicity probabilities
5. Results are returned to frontend
6. Output is displayed

Tech Stack:
Programming: Python
Machine Learning:
1) Scikit-learn
2) TF-IDF Vectorizer
3) Logistic Regression
Data Processing:
Pandas
NumPy
Web Frameworks:
Streamlit (Frontend)
FastAPI (Backend)
Visualization:
Matplotlib

Project Structure
ai-moderation-system/
│
├── backend/
│   ├── api.py
│
├── frontend/
│   ├── deploy.py
│   └── dashboard.py
│-data/
| |- sample_submissions
| |- labeled_data
| |- cyberbullying_tweets
|
├── requirements.txt
├── README.md


Installation & Setup:
pip install -r requirements.txt

Run Backend (FastAPI):
cd backend
uvicorn api:app --reload
Open: http://127.0.0.1:8000/docs

Run Frontend (Streamlit):
cd frontend
streamlit run deploy.py

Run Dashboard:
streamlit run dashboard.py

Real-World Application:
1. Social media content moderation
2. Online gaming chat filtering
3. Comment section monitoring
4. Cyberbullying detection systems

Future Improvements:
1. Deep Learning models (BERT, LSTM)
2. Multilingual support
3. Real-time streaming using WebSockets
4. Cloud deployment with database integration

Conclusion:
This project demonstrates how machine learning and NLP can be used to build scalable and real-time content moderation systems, similar to those used by platforms.

Note: 

This project is developed for educational purposes and demonstrates the application of AI in content moderation systems.
