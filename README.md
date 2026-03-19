# 🚀 AI Sales Research Agent

An AI-powered B2B sales intelligence system that automates prospect research.
It scrapes company websites, analyzes business models, identifies potential pain points, and generates hyper-personalized sales hooks in seconds.

---

## 🌟 Key Features

* 🔎 **Automated Web Scraping**
  Extracts structured data from company websites using Firecrawl or fallback scraping.

* 🧠 **AI-Powered Insights**
  Uses LLMs (Google Gemini / OpenAI GPT) to generate:

  * Sales insights
  * Pain points
  * Personalization hooks

* 🏢 **Industry Detection**
  Automatically classifies companies based on content heuristics.

* 💬 **Personalized Outreach Hooks**
  Generates tailored ice-breakers for cold emails and outreach.

* 🗄️ **Persistent Storage**
  Stores analyzed reports in MongoDB.

* 🔄 **Modular AI Architecture**
  Easily switch between OpenAI and Gemini models.

* ⚡ **Fast API Backend**
  Built with FastAPI for high performance.

* 📊 **Interactive Dashboard**
  Streamlit UI for real-time analysis and visualization.

---

## 🛠️ Tech Stack

| Layer    | Technology                    |
| -------- | ----------------------------- |
| Backend  | FastAPI (Python)              |
| Frontend | Streamlit                     |
| AI/LLM   | OpenAI GPT / Google Gemini    |
| Scraping | Firecrawl API / BeautifulSoup |
| Database | MongoDB                       |
| DevOps   | Docker (optional)             |

---

## 📂 Project Structure

```text
ai-sales-agent/
├── app/
│   ├── agents/          # Scraper, Processor, Insight Agent
│   ├── main.py          # FastAPI application
│   ├── database.py      # MongoDB connection
│   └── config.py        # Environment config
├── streamlit_app/
│   └── app.py           # Streamlit UI
├── .env                 # Environment variables (not committed)
├── requirements.txt
└── README.md
```

---

## ⚙️ Installation & Setup

### 1️⃣ Clone the Repository

```bash
git clone https://github.com/Songram-Biswas/Ai-sale.git
cd ai-sales-agent
```

---

### 2️⃣ Create Virtual Environment

```bash
python -m venv venv
```

Activate:

* Windows:

```bash
venv\Scripts\activate
```

* Mac/Linux:

```bash
source venv/bin/activate
```

---

### 3️⃣ Install Dependencies

```bash
pip install -r requirements.txt
```

---

### 4️⃣ Configure Environment Variables

Create a `.env` file in the root directory:

```env
OPENAI_API_KEY=your_openai_key
GEMINI_API_KEY=your_gemini_key
MONGO_URI=your_mongodb_uri
FIRECRAWL_API_KEY=your_firecrawl_key
```

---

## 🚀 Running the Application

### ▶️ Start FastAPI Backend

```bash
uvicorn app.main:app --reload
```

Backend will run at:

```
http://127.0.0.1:8000
```

---

### 🎯 Start Streamlit UI

```bash
streamlit run streamlit_app/app.py
```

---

## 🧪 API Usage

### POST `/analyze_company`

Analyze a company website.

#### Request:

```json
{
  "url": "https://example.com"
}
```

#### Response:

```json
{
  "company_info": {
    "title": "Company Name",
    "industry": "Software",
    "description": "..."
  },
  "sales_intelligence": {
    "insights": "...",
    "pain_points": ["...", "..."],
    "personalization_hooks": ["...", "..."]
  }
}
```

---

## 🔄 System Workflow

```text
User Input (URL)
        ↓
Data Collection Agent (Scraping)
        ↓
Data Processing Layer
        ↓
LLM Insight Agent
        ↓
FastAPI Response
        ↓
Streamlit Dashboard
        ↓
MongoDB Storage
```

---

## ⚠️ Error Handling

* Graceful fallback if AI API fails
* Database failures do not crash the system
* Network errors handled during scraping

---

## 🐳 Docker (Optional)

Build and run:

```bash
docker-compose up --build
```

---

## 📌 Future Improvements

* 🔁 Redis caching layer
* ⚡ Async scraping pipeline
* 📈 Advanced analytics dashboard
* 🔐 Authentication system
* 🌐 Deployment (AWS / Render / GCP)

---

## 🤝 Contributing

Contributions are welcome!

```bash
fork → branch → commit → pull request
```

---

## 📄 License

This project is open-source and available under the MIT License.

---

## 💡 Author

Built by **Songram Biswas**
AI & Machine Learning Enthusiast 🚀
