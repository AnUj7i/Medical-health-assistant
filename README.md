 # 🩺 Medical Research Assistant (RAG)
 <img width="1024" height="1024" alt="874ac6ca-d769-4597-b605-afaac9ab3f5f" src="https://github.com/user-attachments/assets/07692fb3-74e2-4e78-8d0b-5ee8a61419ee" />

 An intelligent AI-powered medical assistant built with Streamlit and Google Gemini (Generative AI) and RAG (Retrieval-Augmented Generation).  
It helps users get medical research insights, upload and query PDF-based knowledge, and even view analytics on the most common queries — all in one interactive dashboard.


## 🚀 Features

✅ **AI Medical Chatbot** — Ask health-related questions, and Gemini 2.5 Pro provides factual and empathetic responses.  
✅ **Retrieval-Augmented Generation (RAG)** — Upload medical research PDFs and let the assistant use them as context.  
✅ **Offline Fallback** — Works even when Gemini is unavailable (predefined local responses).  
✅ Firebase Integration** — Stores user details and chat logs securely.  
✅ Analytics Dashboard** — Visualizes the most common medical queries using interactive charts.  
✅ **Emergency Section** — Quick access to important helpline numbers in India.  
✅ **Modern UI** — Clean, responsive, and professional design built with Streamlit and Plotly.


## 🧠 Tech Stack

| Component | Technology |
|------------|-------------|
| Frontend | Streamlit |
| Backend | Python |
| AI Model | Google Gemini 2.5 Pro |
| Embedding & RAG | Sentence Transformers (`all-MiniLM-L6-v2`) |
| Data Storage | Firebase Firestore |
| Visualization | Plotly |
| PDF Processing | PyMuPDF |
| Environment | Python-dotenv |
| ML Framework | TensorFlow + tf-keras |


## Project Demo 

✅FIRST <img width="1815" height="1027" alt="Screenshot 2025-11-05 141707" src="https://github.com/user-attachments/assets/5d8c8b84-6137-4939-af85-ca71ef050d53" />

✅SECOND <img width="1888" height="1025" alt="Screenshot 2025-11-05 142526" src="https://github.com/user-attachments/assets/0107bd09-30a8-4915-8798-6a4ee00f2b05" />

✅THIRD <img width="1689" height="729" alt="Screenshot 2025-11-05 143139" src="https://github.com/user-attachments/assets/d0639b7c-61bd-4bb5-b63f-b28163b23333" />

✅FOURTH <img width="1492" height="950" alt="Screenshot 2025-11-05 143800" src="https://github.com/user-attachments/assets/2c9775bd-859c-4a05-a822-16364f2d3f1e" />

 ✅Video Demo
 
 https://github.com/user-attachments/assets/3c1605be-f787-4049-9ccf-9216fa0b1329

## Setup

### 1️⃣ Clone the Repository
```bash
git clone https://github.com/AnUj7i/medical-research-assistant.git
cd medical
```
### 2️⃣ Create an Virtual Environment
```bash
python -m venv venv
venv\Scripts\activate
```
3️⃣ Install Dependencies

```bash
pip install -r requirements.txt
```

4️⃣  Environment Variables for your secrete keys

```bash
GEMINI_API_KEY=your_real_gemini_api_key_here

```

5️⃣ Add Firebase Config (you could download it from the firebase service account )

```bash
firebase_config.json

```

▶️ Run the App 

```bash
streamlit run app.py

```





