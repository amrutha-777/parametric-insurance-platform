# Vayurox — AI Parametric Insurance Platform

> Income protection for India's food delivery partners (Zomato, Swiggy, Blinkit, Zepto)

---

## 🚀 Quick Demo

Open `frontend/index.html` directly in your browser — it runs fully in demo/mock mode with no backend required.

**Demo Credentials:**
- Worker: `ravi@demo.com` / `demo123`
- Insurer: `insurer@demo.com` / `admin123`

---

## 🏗 Project Structure

```
vayurox/
├── backend/
│   ├── app.py              # Flask REST API (all AI models)
│   ├── requirements.txt
│   └── render.yaml         # Render.com deployment config
└── frontend/
    ├── index.html          # Complete React app (single file)
    └── vercel.json         # Vercel deployment config
```

---

## 🔗 API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/register` | Register worker or insurer |
| POST | `/api/login` | Login + role-based routing |
| GET | `/api/get-risk?user_id=...` | AI risk score + live weather |
| POST | `/api/create-policy` | Create weekly policy |
| GET | `/api/get-policy/:user_id` | Get active policy |
| POST | `/api/trigger-claim` | Submit or auto-trigger claim |
| GET | `/api/get-claims/:user_id` | Get all claims |
| GET | `/api/analytics/:user_id` | Worker analytics |
| GET | `/api/insurer/overview` | Platform overview |
| GET | `/api/insurer/disruptions` | Live disruption events |
| GET | `/api/insurer/fraud-dashboard` | Fraud cases |
| POST | `/api/insurer/approve-claim/:id` | Override approve |
| POST | `/api/insurer/reject-claim/:id` | Override reject |

---

## 🤖 AI Models Implemented

### 1. Risk Score Model
```python
score = weather_risk * 0.60 + aqi_risk * 0.25 + platform_risk * 0.15 - tenure_bonus
# Output: 0.0 - 1.0 with grade (LOW/MEDIUM/HIGH) + text drivers
```

### 2. Dynamic Pricing Model
```python
weekly_premium = base_premium * city_factor + rain_adj + aqi_adj - loyalty_disc - ml_disc
# Range: ₹20 - ₹250/week
```

### 3. Fraud Detection Model
- Hours lost > 12 → flag
- Duplicate claim same day + type → reject
- Claim velocity > 3/week → flag
- ML anomaly score > 0.92 → flag

### 4. Prediction Model
- City risk factors → next-day disruption probability
- Recommended working hours output

---

## ⚡ Parametric Triggers

| Trigger | Threshold | Payout |
|---------|-----------|--------|
| Heavy Rain | ≥ 25mm/hr | ₹50/hour lost |
| High AQI | AQI ≥ 150 | ₹50/hour lost |
| Platform Drop | ≥ 35% order drop | ₹50/hour lost |
| Extreme Heat | ≥ 42°C | ₹50/hour lost (Pro only) |
| Curfew/Strike | Civic alert issued | ₹50/hour lost |

**Payout formula:** `payout = hours_lost × ₹50` (capped at weekly coverage limit)

---

## 🚀 Deployment

### Backend → Render.com
```bash
cd backend
pip install -r requirements.txt
python app.py  # local dev

# Production: connect GitHub repo to Render
# Build: pip install -r requirements.txt
# Start: gunicorn app:app
```

### Frontend → Vercel
```bash
cd frontend
# Option 1: Drag-drop index.html to vercel.com/new
# Option 2: vercel --prod

# After deploying backend, update API_BASE in index.html:
# const API_BASE = 'https://YOUR-APP.onrender.com/api';
# Set MOCK_MODE = false;
```

### For Production: MongoDB Atlas
Replace the in-memory `DB` dict in `app.py` with:
```python
from pymongo import MongoClient
client = MongoClient(os.environ['MONGODB_URI'])
db = client['gigshield']
```

---

## 🎥 Demo Flow

1. **Worker Demo:**
   - Login as `ravi@demo.com`
   - Overview → see active policy + live weather ticker
   - AI Risk Profile → see risk score breakdown
   - Live Triggers → see parametric monitoring
   - Click "⚡ Simulate Auto-Claim" → watch zero-touch payout flow
   - Claims → see fraud detection + claim history

2. **Insurer Demo:**
   - Login as `insurer@demo.com`
   - Platform Overview → 12,847 workers, disruption events
   - Risk Engine → city heatmap
   - Fraud Dashboard → approve/reject overrides
   - Pricing Control → adjust base premium + multipliers

---

## 📋 Coverage Rules

- ✅ **ONLY income loss** — zero-touch payouts for lost working hours
- ❌ NO health insurance
- ❌ NO vehicle repair
- ❌ NO accident/medical
- ✅ Weekly pricing cycle aligned with gig worker earnings
- ✅ Auto-renew each Sunday

---

## 🔑 Key Features

| Feature | Description |
|---------|-------------|
| Zero-Touch Claims | Parametric triggers auto-initiate claims |
| Dynamic Pricing | ML adjusts weekly premium based on risk factors |
| Fraud Detection | 4-layer AI fraud detection (GPS, velocity, duplication, anomaly) |
| Predictive Alerts | 24-48hr disruption forecast + safe hours recommendation |
| Income Shield Score | 0-100 composite protection score |
| Role-Based Routing | Worker dashboard vs Insurer dashboard |
| Community Risk Map | City-level risk heatmap for insurers |
