# GenVest: AI-Powered Investment Reports

GenVest is a full-stack web application that generates intelligent investment reports using AI, real-time financial data, and machine learning models. It provides users with:

- Real-time stock price data
- News summarization
- SWOT analysis
- AI-based investment recommendations
- Forecast charts with ML-predicted stock prices
- Downloadable PDF reports

---

## 🚀 Tech Stack

### Frontend
- React with Tailwind CSS
- Vite for fast development

### Backend
- Python + Flask
- OpenAI API (GPT)
- Serper.dev for news search
- yFinance for stock data
- XGBoost for stock price forecasting
- ReportLab for PDF generation

---

## 🔧 Folder Structure

```
GenVest/
├── backend/
│   ├── app/
│   │   ├── routes/              # Flask API endpoints
│   │   ├── services/            # External API integrations (OpenAI, Serper, Yahoo)
│   │   ├── utils/               # Helpers (charts, PDF, etc)
│   ├── ml/                      # Machine Learning scripts
│   │   ├── train.py             # Train XGBoost model per ticker
│   │   ├── predict.py           # Load and use models for forecast
│   │   └── models/              # Stored .pkl models
│   ├── run.py                  # Main Flask entrypoint
│
├── frontend/
│   ├── src/
│   │   ├── components/          # React components (ReportViewer, InputForm, etc)
│   │   ├── utils/api.js         # API calls to backend
│   │   ├── App.jsx, main.jsx
│   └── index.html
```

---

## 🧠 How It Works

1. User inputs stock ticker, OpenAI API key, and Serper key.
2. Frontend sends request to backend `/api/report`.
3. Backend:
   - Fetches stock metadata from yFinance
   - Searches news via Serper.dev and summarizes it via OpenAI
   - Generates SWOT analysis and recommendations using GPT
   - Loads/Trains a stock price prediction model (XGBoost)
   - Generates a price forecast chart
   - Returns full report to frontend
4. User views the results and can download the PDF

---

## 🧪 Model Training (XGBoost)
- Forecasts next 30 days of stock price based on last 180 days
- Features used:
  - 10 lagged prices
  - 3-day rolling mean
  - 5-day rolling std
- MAE (Mean Absolute Error) is shown in the UI for transparency

---

## 📝 How to Use

### 1. Clone Repository
```bash
git clone https://github.com/AnaRecio/GenVest.git
cd genvest
```

### 2. Backend Setup
```bash
cd backend
python -m venv env
source env/bin/activate  # or env\Scripts\activate on Windows
pip install -r requirements.txt
python run.py
```

### 3. Frontend Setup
```bash
cd frontend
npm install
npm run dev
```

### 4. Train Initial Model
```bash
cd backend
python ml/train.py  # trains for AAPL by default
```

---

## 🔐 API Keys Required

| Service     | Use                     | How to get it                        |
|-------------|--------------------------|--------------------------------------|
| OpenAI      | News summary, SWOT, GPT | https://platform.openai.com/account/api-keys |
| Serper.dev  | News search             | https://serper.dev                    |

---

## 📦 Example Report Output

- Company metadata (price, market cap, sector)
- Price forecast chart
- 7/14/30 day forecasted prices and % change
- Mean Absolute Error (MAE)
- News summary
- SWOT analysis
- AI investment recommendation
- PDF download

---

## ✅ To-Do / Improvements
- Add ticker autocomplete from backend
- Display confidence intervals on chart
- Deploy to Vercel + Render/Heroku
- Optional: User auth and saved reports

---

## 📄 License
MIT License

---

## ✨ Author
Built by Ana Recio

