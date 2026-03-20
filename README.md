# AI-Powered Parametric Insurance for Gig Delivery Workers

---

## Problem Statement

Delivery partners in India’s gig economy often face income loss due to external disruptions such as heavy rain, floods, pollution, or curfews.

These workers depend on daily earnings, and when such disruptions occur, they lose 20–30% of their income. Currently, there is no system that protects their income during these uncontrollable situations.

---

## Persona Focus (Mandatory Requirement)

We focus specifically on:

### Food Delivery Partners (Swiggy/Zomato)

### Why this persona?
- Highly dependent on daily orders  
- Work is heavily affected by weather conditions  
- Income fluctuates frequently  
- No existing income protection system  

### Persona Scenario

Ravi is a Swiggy delivery partner.  
He logs in to work during peak hours, but suddenly heavy rain starts. Orders drop and deliveries stop. Ravi loses his daily earnings with no backup support.

Our solution ensures Ravi receives automatic compensation for lost income.

---

## Proposed Solution

We propose an AI-powered parametric insurance platform that:

- Provides weekly subscription-based insurance  
- Automatically detects disruptions using real-time data  
- Instantly compensates workers  
- Uses AI-driven fraud detection  

---

## Workflow (How the System Works)

1. User registers on the platform  
2. Selects a weekly insurance plan  
3. System monitors:
   - Weather conditions  
   - Location activity  
4. If a disruption occurs:
   - Claim is automatically triggered  
5. AI verifies authenticity  
6. Instant payout is processed  

---

## Weekly Pricing Model (AI-Based)

| Risk Level | Area Type | Weekly Premium |
|-----------|----------|----------------|
| Low Risk  | Safe zones | ₹20/week |
| Medium Risk | Moderate zones | ₹35/week |
| High Risk | Flood-prone zones | ₹50/week |

### AI Logic
- Uses historical weather data  
- Predicts disruption probability  
- Dynamically adjusts pricing  

---

## Parametric Triggers

Automatic payout when:

- Rainfall > 50mm  
- AQI > 300  
- Flood alerts issued  
- Curfew or zone closure  

No manual claims are required.

---

## AI/ML Integration

- Risk prediction  
- Dynamic pricing  
- Income estimation  
- Fraud detection  

---

## Adversarial Defense and Anti-Spoofing Strategy

### Multi-Source Location Verification
- Compare GPS, network location, and movement patterns  
- Detect sudden location jumps  

### Anomaly Detection
- Identify unusual claim frequency  
- Flag abnormal behavior  

### Fraud Ring Detection
- Detect multiple users claiming from the same area at the same time  
- Identify coordinated fraud patterns  

### Device Fingerprinting
- Track device IDs  
- Prevent multiple accounts from the same device  

### Cross-Verification
- Validate claims using weather APIs and traffic data  

### Fairness for Honest Users
- Use a trust score system  
- Faster payouts for reliable users  
- Additional verification for suspicious users  

---

## Parametric Automation

- Real-time disruption monitoring  
- Automatic claim initiation  
- Instant payout processing  

---

## Integration Capabilities

- Weather APIs  
- Traffic data (mock or simulated)  
- Platform APIs (simulated)  
- Payment systems (Razorpay or UPI sandbox)  

---

## Innovation and Unique Features

### Trust Score System
- Reliability-based scoring  
- Faster claims for trusted users  

### Hyperlocal Risk Mapping
- City divided into risk zones  
- AI identifies high-risk areas  

### Income Prediction Model
- Estimates expected earnings  
- Ensures fair payouts  

### Lost Work Hours Calculation
- Calculates actual hours lost  
- Improves accuracy of payouts  

### Smart Pause Mode
- Alerts workers during high-risk conditions  
- Encourages safety  

### Dashboard

Worker Dashboard:
- Earnings protected  
- Active plan  
- Claim history  

Admin Dashboard:
- Fraud alerts  
- Risk analytics  
- Claim patterns  

---

## Tech Stack

- Frontend: React or Streamlit  
- Backend: Python (Flask or Django)  
- Database: MongoDB  
- APIs: Weather API  
- AI/ML: Scikit-learn  
- Payments: Razorpay or UPI sandbox  

---

## Development Plan

Phase 1:
- Idea design and documentation  

Phase 2:
- Registration system  
- Pricing model  
- Claims system  

Phase 3:
- Fraud detection  
- Dashboard  
- Payment simulation  

---

## Conclusion

This platform provides a simple, automated, and AI-driven insurance system for gig workers by protecting their income during disruptions, using intelligent risk modeling, and preventing fraud with strong detection mechanisms.

The goal is to ensure financial stability and build trust among delivery workers.
