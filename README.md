# 🚀 GigShield — AI-Powered Parametric Insurance for Gig Workers

**“From claims to code — GigShield redefines insurance with AI.”**

---

## 📖 Overview

GigShield is an AI-powered parametric insurance platform designed for India’s gig economy workers (Zomato, Swiggy, Blinkit, etc.).

It protects delivery partners from income loss caused by external disruptions such as heavy rainfall, high air pollution (AQI), platform outages, and local restrictions — through **instant, automated payouts with zero manual claims**.

---

## 💡 Problem Statement

Delivery partners depend on daily earnings. However, external disruptions can reduce their income by **20–30%**, including:

- 🌧️ Heavy rainfall  
- 🌫️ High AQI (pollution)  
- ⚙️ Platform outages  
- 🚫 Curfews / zone restrictions  

### ❌ Current Issues
- No income protection system  
- Insurance claims are slow and manual  
- Workers bear full financial risk  

---

## 👤 Target Persona

### Food Delivery Partners (Zomato / Swiggy)

### Why this persona?
- Highly dependent on daily orders  
- Income fluctuates frequently  
- Work affected by weather & disruptions  
- No existing safety net  

### Scenario

Ravi, a delivery partner, logs in during peak hours. Sudden heavy rain reduces orders drastically. He loses his daily income with no backup.

👉 GigShield ensures **automatic compensation** for such losses.

---

## 🚀 Solution

GigShield uses **AI + Parametric Insurance** to:

- Provide weekly subscription-based insurance  
- Monitor real-time disruption data  
- Automatically trigger claims  
- Instantly process payouts  
- Prevent fraud using AI  

---

## ⚙️ Workflow (System Flow)

1. User registers on the platform  
2. Selects a weekly insurance plan  
3. System continuously monitors:
   - Weather conditions  
   - AQI levels  
   - Platform activity  
4. If disruption occurs:
   - Claim is automatically triggered  
5. AI verifies authenticity  
6. Instant payout is processed  

---

## 💰 Payout Model

**Formula:**
Payout = Hours Lost × ₹50

✔ No paperwork  
✔ No manual claims  
✔ Fully automated  

---

## 📊 AI-Based Pricing Model

| Risk Level   | Area Type        | Weekly Premium |
|-------------|----------------|----------------|
| Low Risk    | Safe zones      | ₹20/week       |
| Medium Risk | Moderate zones  | ₹35/week       |
| High Risk   | Flood-prone     | ₹50/week       |

### 🧠 AI Logic
- Uses historical weather + disruption data  
- Predicts probability of income loss  
- Dynamically adjusts premium pricing  

---

## ⚡ Parametric Triggers

Automatic payout when:

- Rainfall ≥ threshold  
- AQI ≥ threshold  
- Orders drop ≥ threshold  
- Flood alerts / curfew issued  

👉 No manual claim required

---

## 🤖 AI/ML Integration

- Risk prediction model  
- Dynamic pricing engine  
- Income estimation model  
- Fraud detection system  
- Disruption prediction  

---

## 🔐 Fraud Detection & Security

### Multi-Layer Protection

- 📍 Multi-source location verification (GPS + network)  
- 📊 Anomaly detection (unusual claim patterns)  
- 🧑‍🤝‍🧑 Fraud ring detection  
- 📱 Device fingerprinting  
- 🔄 Cross-verification with APIs  

### Trust Score System
- Each user gets a reliability score  
- Faster payouts for trusted users  
- Additional checks for suspicious activity  

---

## 🧠 Smart Features

### 🔹 Hyperlocal Risk Mapping
- City divided into risk zones  
- AI identifies high-risk areas  

### 🔹 Income Prediction
- Estimates expected earnings  
- Ensures fair compensation  

### 🔹 Lost Work Hours Calculation
- Calculates actual income loss  

### 🔹 Smart Pause Mode
- Alerts workers during risky conditions  
- Encourages safety  

---

## 📊 Dashboards

### 👷 Worker Dashboard
- Active insurance plan  
- Earnings protection  
- Claim history  
- Risk score  
- Live disruption tracking  

### 🏢 Insurer Dashboard
- Platform analytics  
- Fraud alerts  
- Risk heatmaps  
- Claim monitoring  

---

## 🏗️ Tech Stack

### Frontend
- React (integrated in HTML)  
- JavaScript  
- HTML5, CSS3  
- Chart.js  

### Backend
- Python (Flask)  
- REST APIs  

### Database
- MongoDB  

### Other Tools
- APScheduler (automation)  
- Mock APIs (weather, platform data)  
- Machine Learning (Scikit-learn concepts)  

---

## 🔗 API Endpoints

| Method | Endpoint                 | Description       |
| ------ | ------------------------ | ----------------- |
| POST   | /api/register            | Register user     |
| POST   | /api/login               | Login             |
| GET    | /api/get-risk            | AI risk + premium |
| POST   | /api/create-policy       | Create policy     |
| GET    | /api/get-policy/:user_id | Get policy        |
| POST   | /api/trigger-claim       | Trigger claim     |
| GET    | /api/get-claims/:user_id | Claim history     |

---

## 🌐 Deployment

- Frontend → Netlify  
- Backend → Flask server  

---

## 🎥 Demo Credentials

### Worker
- Email: ravi@demo.com  
- Password: demo123  

### Insurer
- Email: insurer@demo.com  
- Password: admin123  

---

## 🚧 Challenges Faced

- Designing realistic parametric triggers  
- Simulating real-world APIs  
- Fraud detection without real datasets  
- Building dual dashboards  

---

## 📚 What We Learned

- Parametric insurance systems  
- AI-based risk modeling  
- Full-stack development  
- Real-time automation systems  

---

## 🔮 Future Improvements

- Real weather & AQI API integration  
- Payment gateway (Razorpay/UPI)  
- Mobile app version  
- Scalable cloud deployment  
- Multi-language support  

---

## 🌍 Impact

GigShield transforms insurance from a **manual, slow process** into a **fully automated income protection system**, making financial security accessible to millions of gig workers.

---
## ▶️ How to Run Locally

### 🔧 Backend (Flask)

1. Navigate to backend folder:
cd backend

2. Install dependencies:
pip install -r requirements.txt

3. Run the server:
python app.py

Backend will run on:
http://127.0.0.1:5000/

---

### 🌐 Frontend

Simple HTML:
cd frontend
Open index.html or use Live Server (VS Code)

React (if applicable):
npm install
npm start

---

### 🔗 Connect Frontend & Backend

Ensure API calls use:
http://127.0.0.1:5000/api/...

---

### ⚠️ Common Issues

CORS Error:
from flask_cors import CORS
CORS(app)

Module not found:
pip install <module-name>

---

### ✅ Steps to Run

1. Start backend  
2. Open frontend  
3. Use the application 🎉

---

## 🏆 Final Note

GigShield bridges the gap between **technology and financial safety**, ensuring gig workers are protected when they need it the most.
