"""
GigShield Backend - AI Parametric Insurance Platform
Flask REST API with in-memory database (replace with MongoDB Atlas in production)
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
import uuid
import random
import math
from datetime import datetime, timedelta
import hashlib
import json

app = Flask(__name__)
CORS(app, origins="*")

# ──────────────────────────────────────────────
# IN-MEMORY DATABASE (replace with MongoDB Atlas)
# ──────────────────────────────────────────────
DB = {
    "users": {},
    "policies": {},
    "claims": {},
    "fraud_logs": {},
    "disruptions": {}
}

# Seed demo accounts
DEMO_WORKER = {
    "id": "usr_worker_demo",
    "name": "Ravi Kumar",
    "email": "ravi@demo.com",
    "password_hash": hashlib.md5("demo123".encode()).hexdigest(),
    "role": "worker",
    "city": "Mumbai",
    "zone": "Andheri West",
    "platform": "Zomato",
    "avg_weekly_earnings": 4200,
    "work_hours_per_day": 8,
    "tenure_months": 6,
    "created_at": datetime.now().isoformat()
}

DEMO_INSURER = {
    "id": "usr_insurer_demo",
    "name": "Priya Sharma",
    "email": "insurer@demo.com",
    "password_hash": hashlib.md5("admin123".encode()).hexdigest(),
    "role": "insurer",
    "company": "GigShield Insurance Ltd.",
    "created_at": datetime.now().isoformat()
}

DB["users"][DEMO_WORKER["id"]] = DEMO_WORKER
DB["users"][DEMO_INSURER["id"]] = DEMO_INSURER

# ──────────────────────────────────────────────
# CITY RISK DATA (simulated hyper-local data)
# ──────────────────────────────────────────────
CITY_RISK = {
    "Mumbai":    {"rain": 0.85, "aqi": 0.40, "flood": 0.75, "platform": 0.20},
    "Delhi NCR": {"rain": 0.45, "aqi": 0.90, "flood": 0.30, "platform": 0.15},
    "Bengaluru": {"rain": 0.55, "aqi": 0.35, "flood": 0.25, "platform": 0.30},
    "Hyderabad": {"rain": 0.50, "aqi": 0.40, "flood": 0.35, "platform": 0.20},
    "Chennai":   {"rain": 0.60, "aqi": 0.35, "flood": 0.50, "platform": 0.15},
    "Pune":      {"rain": 0.65, "aqi": 0.30, "flood": 0.40, "platform": 0.20},
}

ZONE_MULTIPLIERS = {
    "low":    0.80,
    "medium": 1.00,
    "high":   1.35
}

# ──────────────────────────────────────────────
# MOCK WEATHER + AQI + PLATFORM DATA
# ──────────────────────────────────────────────
def get_mock_weather(city):
    """Simulates weather API response"""
    base = CITY_RISK.get(city, {"rain": 0.5, "aqi": 0.5})
    rain_mm = random.uniform(0, 60) * base["rain"]
    aqi = int(random.uniform(50, 250) * base["aqi"])
    temp_c = random.uniform(28, 44)
    return {
        "city": city,
        "rain_mm_per_hr": round(rain_mm, 1),
        "aqi": aqi,
        "temperature_c": round(temp_c, 1),
        "flood_alert": rain_mm > 35,
        "timestamp": datetime.now().isoformat()
    }

def get_mock_platform_data(city):
    """Simulates platform order API"""
    order_drop_pct = random.uniform(0, 55)
    return {
        "city": city,
        "order_drop_pct": round(order_drop_pct, 1),
        "platform_down": order_drop_pct > 40,
        "timestamp": datetime.now().isoformat()
    }

# ──────────────────────────────────────────────
# AI MODELS
# ──────────────────────────────────────────────
def compute_risk_score(user):
    """
    AI Risk Model:
    Inputs: city, weather_risk, aqi_risk, platform_reliability, work_hours, tenure
    Output: risk_score (0.0 - 1.0) + breakdown
    """
    city = user.get("city", "Mumbai")
    risks = CITY_RISK.get(city, {"rain": 0.5, "aqi": 0.5, "flood": 0.5, "platform": 0.2})
    work_hours = user.get("work_hours_per_day", 8)
    tenure = user.get("tenure_months", 1)

    # Weighted risk components
    weather_risk = risks["rain"] * 0.40 + risks["flood"] * 0.20
    aqi_risk = risks["aqi"] * 0.25
    platform_risk = risks["platform"] * 0.15
    hours_risk = min(work_hours / 12, 1.0) * 0.10
    tenure_bonus = min(tenure / 24, 1.0) * 0.10  # longer tenure = lower risk

    raw_score = weather_risk + aqi_risk + platform_risk + hours_risk - tenure_bonus
    score = max(0.05, min(0.99, raw_score))

    # Explanation
    drivers = []
    if risks["rain"] > 0.7:
        drivers.append("High rainfall zone increases income disruption risk")
    if risks["aqi"] > 0.7:
        drivers.append("Severe air pollution affects outdoor delivery hours")
    if risks["platform"] > 0.25:
        drivers.append("Platform outages frequently impact order availability")
    if work_hours > 9:
        drivers.append("Long work hours increase exposure to disruptions")
    if tenure > 12:
        drivers.append("Strong delivery history reduces premium")

    return {
        "score": round(score, 3),
        "grade": "HIGH" if score > 0.65 else "MEDIUM" if score > 0.35 else "LOW",
        "weather_risk": round(weather_risk, 3),
        "aqi_risk": round(aqi_risk, 3),
        "platform_risk": round(platform_risk, 3),
        "drivers": drivers if drivers else ["Risk profile within normal range"]
    }

def compute_weekly_premium(user, risk_data=None):
    """
    Dynamic Pricing Model:
    weekly_premium = base + (risk_score × multiplier) + adjustments
    Range: ₹20 - ₹250/week
    """
    if not risk_data:
        risk_data = compute_risk_score(user)

    base_premium = 80  # ₹80 base
    risk_score = risk_data["score"]
    city = user.get("city", "Mumbai")
    risks = CITY_RISK.get(city, {"rain": 0.5, "aqi": 0.5})
    work_hours = user.get("work_hours_per_day", 8)
    tenure = user.get("tenure_months", 1)

    # Component adjustments
    rain_adj = round(risks["rain"] * 35)
    aqi_adj = round(risks["aqi"] * 20)
    platform_adj = round(risks.get("platform", 0.2) * 15)
    hours_adj = max(0, round((work_hours - 6) * 4))
    loyalty_disc = min(round(tenure * 2.5), 30)
    ml_disc = round(base_premium * max(0, (0.6 - risk_score)) * 0.15)

    total = base_premium + rain_adj + aqi_adj + platform_adj + hours_adj - loyalty_disc - ml_disc
    total = max(20, min(250, total))

    return {
        "weekly_premium": round(total),
        "base": base_premium,
        "rain_adj": rain_adj,
        "aqi_adj": aqi_adj,
        "platform_adj": platform_adj,
        "hours_adj": hours_adj,
        "loyalty_disc": loyalty_disc,
        "ml_disc": ml_disc,
        "coverage_limit": min(total * 18, 4500),
        "payout_rate_per_hour": 50
    }

def fraud_check(claim_data, user_id):
    """
    Fraud Detection Model:
    - Duplicate claim detection
    - Unrealistic hours check
    - Location mismatch
    - Claim velocity check
    """
    flags = []
    is_fraud = False

    hours_lost = claim_data.get("hours_lost", 0)
    claim_type = claim_data.get("claim_type", "")

    # Rule 1: Unrealistic hours
    if hours_lost > 12:
        flags.append("Hours lost exceeds 12 — unrealistic for single disruption event")
        is_fraud = True

    # Rule 2: Duplicate claim same day
    today = datetime.now().date().isoformat()
    user_claims_today = [
        c for c in DB["claims"].values()
        if c["user_id"] == user_id and c["date"][:10] == today and c["claim_type"] == claim_type
    ]
    if user_claims_today:
        flags.append(f"Duplicate claim detected: {claim_type} already claimed today")
        is_fraud = True

    # Rule 3: Claim velocity (>3 claims/week)
    week_ago = (datetime.now() - timedelta(days=7)).isoformat()
    weekly_claims = [
        c for c in DB["claims"].values()
        if c["user_id"] == user_id and c["date"] > week_ago
    ]
    if len(weekly_claims) >= 4:
        flags.append(f"High claim velocity: {len(weekly_claims)} claims in 7 days")
        is_fraud = True

    # Rule 4: Random ML anomaly detection (simplified)
    anomaly_score = random.uniform(0, 1)
    if anomaly_score > 0.92:
        flags.append("ML anomaly: claim pattern deviates significantly from normal")
        is_fraud = True

    return {
        "is_fraud": is_fraud,
        "flags": flags,
        "anomaly_score": round(anomaly_score, 3),
        "verdict": "REJECTED — Suspicious Activity" if is_fraud else "APPROVED — No Anomalies"
    }

def predict_disruptions(city):
    """
    Prediction Model: forecast next 24-48hr disruptions
    """
    risks = CITY_RISK.get(city, {"rain": 0.5, "aqi": 0.5})
    predictions = []
    
    if random.random() < risks["rain"] * 0.8:
        predictions.append({
            "type": "Heavy Rainfall",
            "probability": round(risks["rain"] * 100),
            "window": "Tomorrow 2PM–8PM",
            "recommended_hours": "Work 8AM–1PM or after 9PM",
            "severity": "HIGH" if risks["rain"] > 0.7 else "MEDIUM"
        })
    if random.random() < risks["aqi"] * 0.7:
        predictions.append({
            "type": "Poor Air Quality",
            "probability": round(risks["aqi"] * 85),
            "window": "Tomorrow morning 6AM–11AM",
            "recommended_hours": "Avoid morning routes; work 11AM–4PM",
            "severity": "MEDIUM"
        })
    if not predictions:
        predictions.append({
            "type": "Clear conditions expected",
            "probability": 85,
            "window": "Next 48 hours",
            "recommended_hours": "All hours suitable for deliveries",
            "severity": "LOW"
        })
    return predictions

def compute_income_shield_score(user_id):
    """Bonus: Income Shield Score 0-100"""
    user = DB["users"].get(user_id, {})
    policies = [p for p in DB["policies"].values() if p["user_id"] == user_id]
    claims = [c for c in DB["claims"].values() if c["user_id"] == user_id]
    
    base = 50
    if policies: base += 20
    active_policy = next((p for p in policies if p["status"] == "active"), None)
    if active_policy: base += 15
    tenure = user.get("tenure_months", 0)
    base += min(tenure, 10)
    fraud_claims = [c for c in claims if c.get("fraud_result", {}).get("is_fraud")]
    base -= len(fraud_claims) * 10
    
    return max(0, min(100, base))

# ──────────────────────────────────────────────
# API ROUTES
# ──────────────────────────────────────────────

@app.route("/api/health", methods=["GET"])
def health():
    return jsonify({"status": "ok", "service": "GigShield API", "version": "1.0.0"})

# AUTH
@app.route("/api/register", methods=["POST"])
def register():
    data = request.json
    required = ["name", "email", "password", "role", "city"]
    for f in required:
        if not data.get(f):
            return jsonify({"error": f"Missing field: {f}"}), 400

    # Check duplicate email
    if any(u["email"] == data["email"] for u in DB["users"].values()):
        return jsonify({"error": "Email already registered"}), 409

    user_id = "usr_" + uuid.uuid4().hex[:8]
    user = {
        "id": user_id,
        "name": data["name"],
        "email": data["email"],
        "password_hash": hashlib.md5(data["password"].encode()).hexdigest(),
        "role": data["role"],
        "city": data["city"],
        "zone": data.get("zone", "Central"),
        "platform": data.get("platform", "Zomato"),
        "avg_weekly_earnings": int(data.get("avg_weekly_earnings", 3500)),
        "work_hours_per_day": int(data.get("work_hours_per_day", 8)),
        "tenure_months": int(data.get("tenure_months", 1)),
        "created_at": datetime.now().isoformat()
    }
    DB["users"][user_id] = user
    
    return jsonify({
        "message": "Registration successful",
        "user_id": user_id,
        "role": user["role"],
        "token": f"token_{user_id}"
    }), 201

@app.route("/api/login", methods=["POST"])
def login():
    data = request.json
    email = data.get("email", "").lower().strip()
    password = data.get("password", "")
    password_hash = hashlib.md5(password.encode()).hexdigest()

    user = next((u for u in DB["users"].values() 
                 if u["email"].lower() == email and u["password_hash"] == password_hash), None)
    
    if not user:
        return jsonify({"error": "Invalid email or password"}), 401

    return jsonify({
        "message": "Login successful",
        "token": f"token_{user['id']}",
        "user_id": user["id"],
        "name": user["name"],
        "role": user["role"],
        "city": user.get("city", "Mumbai")
    })

# RISK
@app.route("/api/get-risk", methods=["GET", "POST"])
def get_risk():
    if request.method == "POST":
        user_data = request.json
    else:
        user_id = request.args.get("user_id", "usr_worker_demo")
        user_data = DB["users"].get(user_id, {})
    
    risk = compute_risk_score(user_data)
    premium = compute_weekly_premium(user_data, risk)
    weather = get_mock_weather(user_data.get("city", "Mumbai"))
    platform = get_mock_platform_data(user_data.get("city", "Mumbai"))
    predictions = predict_disruptions(user_data.get("city", "Mumbai"))
    shield_score = compute_income_shield_score(user_data.get("id", ""))
    
    return jsonify({
        "risk": risk,
        "premium": premium,
        "weather": weather,
        "platform": platform,
        "predictions": predictions,
        "shield_score": shield_score
    })

# POLICY
@app.route("/api/create-policy", methods=["POST"])
def create_policy():
    data = request.json
    user_id = data.get("user_id")
    user = DB["users"].get(user_id)
    
    if not user:
        return jsonify({"error": "User not found"}), 404
    
    # Deactivate old policies
    for p in DB["policies"].values():
        if p["user_id"] == user_id and p["status"] == "active":
            p["status"] = "expired"
    
    risk = compute_risk_score(user)
    premium_data = compute_weekly_premium(user, risk)
    
    policy_id = "POL_" + uuid.uuid4().hex[:6].upper()
    now = datetime.now()
    next_week = now + timedelta(days=7)
    
    policy = {
        "id": policy_id,
        "user_id": user_id,
        "plan": data.get("plan", "standard"),
        "status": "active",
        "created_at": now.isoformat(),
        "valid_from": now.isoformat(),
        "valid_until": next_week.isoformat(),
        "next_renewal": next_week.isoformat(),
        "auto_renew": data.get("auto_renew", True),
        "weekly_premium": premium_data["weekly_premium"],
        "coverage_limit": premium_data["coverage_limit"],
        "triggers": data.get("triggers", ["rain", "aqi", "platform", "curfew", "heat"]),
        "risk_score": risk["score"],
        "payout_this_week": 0,
        "premium_breakdown": premium_data
    }
    
    DB["policies"][policy_id] = policy
    return jsonify({"message": "Policy created", "policy": policy}), 201

@app.route("/api/get-policy/<user_id>", methods=["GET"])
def get_policy(user_id):
    policies = [p for p in DB["policies"].values() if p["user_id"] == user_id]
    active = next((p for p in policies if p["status"] == "active"), None)
    return jsonify({
        "active_policy": active,
        "all_policies": sorted(policies, key=lambda x: x["created_at"], reverse=True)
    })

# CLAIMS
@app.route("/api/trigger-claim", methods=["POST"])
def trigger_claim():
    data = request.json
    user_id = data.get("user_id")
    user = DB["users"].get(user_id)
    
    if not user:
        return jsonify({"error": "User not found"}), 404
    
    # Check active policy
    active_policy = next(
        (p for p in DB["policies"].values() 
         if p["user_id"] == user_id and p["status"] == "active"), None
    )
    if not active_policy:
        return jsonify({"error": "No active policy. Please purchase a policy first."}), 400
    
    claim_type = data.get("claim_type", "rain")
    hours_lost = float(data.get("hours_lost", 2))
    
    # Get live trigger data
    weather = get_mock_weather(user.get("city", "Mumbai"))
    platform = get_mock_platform_data(user.get("city", "Mumbai"))
    
    # Validate trigger threshold
    trigger_validated = False
    trigger_value = ""
    
    if claim_type == "rain" and weather["rain_mm_per_hr"] >= 25:
        trigger_validated = True
        trigger_value = f"{weather['rain_mm_per_hr']}mm/hr (threshold: 25mm)"
    elif claim_type == "aqi" and weather["aqi"] >= 150:
        trigger_validated = True
        trigger_value = f"AQI {weather['aqi']} (threshold: 150)"
    elif claim_type == "platform" and platform["order_drop_pct"] >= 35:
        trigger_validated = True
        trigger_value = f"Orders down {platform['order_drop_pct']}% (threshold: 35%)"
    elif claim_type == "curfew":
        trigger_validated = random.random() > 0.3  # mock civic alert
        trigger_value = "Civic disruption alert confirmed"
    elif claim_type == "heat" and weather["temperature_c"] >= 42:
        trigger_validated = True
        trigger_value = f"{weather['temperature_c']}°C (threshold: 42°C)"
    else:
        # For demo: allow manual claims with lower thresholds
        trigger_validated = True
        trigger_value = "Manual claim — threshold met based on reported conditions"
    
    # Fraud detection
    fraud_result = fraud_check({
        "claim_type": claim_type,
        "hours_lost": hours_lost
    }, user_id)
    
    # Calculate payout
    payout = 0
    status = "pending"
    
    if fraud_result["is_fraud"]:
        status = "rejected"
    elif trigger_validated:
        payout = min(hours_lost * 50, active_policy["coverage_limit"] - active_policy["payout_this_week"])
        payout = max(0, payout)
        status = "approved"
        active_policy["payout_this_week"] = active_policy.get("payout_this_week", 0) + payout
    else:
        status = "rejected"
        fraud_result["flags"].append("Parametric threshold not met — disruption not severe enough")
    
    claim_id = "CLM_" + uuid.uuid4().hex[:6].upper()
    claim = {
        "id": claim_id,
        "user_id": user_id,
        "policy_id": active_policy["id"],
        "claim_type": claim_type,
        "hours_lost": hours_lost,
        "payout": round(payout),
        "status": status,
        "trigger_validated": trigger_validated,
        "trigger_value": trigger_value,
        "fraud_result": fraud_result,
        "weather_snapshot": weather,
        "date": datetime.now().isoformat(),
        "auto_triggered": data.get("auto_triggered", False),
        "flow": [
            {"step": "Disruption Detected", "status": "done", "time": datetime.now().strftime("%H:%M:%S")},
            {"step": "Threshold Validated", "status": "done" if trigger_validated else "failed"},
            {"step": "Fraud Check", "status": "done" if not fraud_result["is_fraud"] else "failed"},
            {"step": "Payout Processed", "status": "done" if status == "approved" else "failed",
             "amount": round(payout) if status == "approved" else 0}
        ]
    }
    
    DB["claims"][claim_id] = claim
    
    if fraud_result["is_fraud"]:
        DB["fraud_logs"][claim_id] = {
            "claim_id": claim_id,
            "user_id": user_id,
            "user_name": user.get("name"),
            "flags": fraud_result["flags"],
            "date": datetime.now().isoformat()
        }
    
    return jsonify({
        "claim": claim,
        "message": f"Claim {status.upper()}: ₹{round(payout)} payout" if status == "approved" else f"Claim {status.upper()}"
    })

@app.route("/api/get-claims/<user_id>", methods=["GET"])
def get_claims(user_id):
    claims = sorted(
        [c for c in DB["claims"].values() if c["user_id"] == user_id],
        key=lambda x: x["date"], reverse=True
    )
    return jsonify({"claims": claims})

# INSURER ROUTES
@app.route("/api/insurer/overview", methods=["GET"])
def insurer_overview():
    all_policies = list(DB["policies"].values())
    all_claims = list(DB["claims"].values())
    all_users = list(DB["users"].values())
    
    workers = [u for u in all_users if u["role"] == "worker"]
    active_policies = [p for p in all_policies if p["status"] == "active"]
    approved_claims = [c for c in all_claims if c["status"] == "approved"]
    fraud_cases = list(DB["fraud_logs"].values())
    
    total_payout = sum(c["payout"] for c in approved_claims)
    total_premium = sum(p["weekly_premium"] for p in active_policies)
    
    # City risk heatmap
    city_stats = {}
    for p in all_policies:
        user = DB["users"].get(p["user_id"], {})
        city = user.get("city", "Unknown")
        if city not in city_stats:
            city_stats[city] = {"policies": 0, "claims": 0, "payout": 0, "risk_score": []}
        city_stats[city]["policies"] += 1
        city_stats[city]["risk_score"].append(p.get("risk_score", 0.5))
    
    for city in city_stats:
        scores = city_stats[city]["risk_score"]
        city_stats[city]["avg_risk"] = round(sum(scores) / len(scores), 3) if scores else 0
        city_stats[city].pop("risk_score")
    
    for c in all_claims:
        user = DB["users"].get(c["user_id"], {})
        city = user.get("city", "Unknown")
        if city in city_stats:
            city_stats[city]["claims"] += 1
            city_stats[city]["payout"] += c.get("payout", 0)
    
    return jsonify({
        "total_workers": len(workers),
        "active_policies": len(active_policies),
        "claims_processed": len(approved_claims),
        "fraud_blocked": len(fraud_cases),
        "total_payout": round(total_payout),
        "total_premium": round(total_premium),
        "loss_ratio": round(total_payout / total_premium * 100, 1) if total_premium > 0 else 0,
        "city_heatmap": city_stats
    })

@app.route("/api/insurer/disruptions", methods=["GET"])
def insurer_disruptions():
    """Live disruption events across all cities"""
    events = []
    for city in CITY_RISK:
        weather = get_mock_weather(city)
        platform = get_mock_platform_data(city)
        
        affected = sum(1 for p in DB["policies"].values() 
                      if DB["users"].get(p["user_id"], {}).get("city") == city 
                      and p["status"] == "active")
        
        if weather["rain_mm_per_hr"] > 25:
            events.append({
                "type": "Heavy Rain", "city": city,
                "value": f"{weather['rain_mm_per_hr']}mm/hr",
                "affected_workers": affected,
                "severity": "HIGH" if weather["rain_mm_per_hr"] > 40 else "MEDIUM",
                "triggered": True
            })
        if weather["aqi"] > 150:
            events.append({
                "type": "High AQI", "city": city,
                "value": f"AQI {weather['aqi']}",
                "affected_workers": affected,
                "severity": "HIGH" if weather["aqi"] > 200 else "MEDIUM",
                "triggered": True
            })
        if platform["order_drop_pct"] > 35:
            events.append({
                "type": "Platform Slowdown", "city": city,
                "value": f"Orders ↓{platform['order_drop_pct']}%",
                "affected_workers": affected,
                "severity": "MEDIUM",
                "triggered": True
            })
    
    return jsonify({"events": events, "timestamp": datetime.now().isoformat()})

@app.route("/api/insurer/fraud-dashboard", methods=["GET"])
def fraud_dashboard():
    all_claims = list(DB["claims"].values())
    suspicious = [c for c in all_claims if c.get("fraud_result", {}).get("is_fraud")]
    
    return jsonify({
        "fraud_cases": [
            {
                "claim_id": c["id"],
                "user_id": c["user_id"],
                "user_name": DB["users"].get(c["user_id"], {}).get("name", "Unknown"),
                "claim_type": c["claim_type"],
                "flags": c.get("fraud_result", {}).get("flags", []),
                "date": c["date"],
                "status": c["status"]
            } for c in suspicious
        ],
        "total_fraud": len(suspicious),
        "amount_saved": sum(c["hours_lost"] * 50 for c in suspicious)
    })

@app.route("/api/insurer/approve-claim/<claim_id>", methods=["POST"])
def approve_claim_override(claim_id):
    claim = DB["claims"].get(claim_id)
    if not claim:
        return jsonify({"error": "Claim not found"}), 404
    claim["status"] = "approved"
    claim["fraud_result"]["is_fraud"] = False
    claim["payout"] = claim["hours_lost"] * 50
    return jsonify({"message": "Claim approved", "claim": claim})

@app.route("/api/insurer/reject-claim/<claim_id>", methods=["POST"])
def reject_claim_override(claim_id):
    claim = DB["claims"].get(claim_id)
    if not claim:
        return jsonify({"error": "Claim not found"}), 404
    claim["status"] = "rejected"
    return jsonify({"message": "Claim rejected", "claim": claim})

@app.route("/api/analytics/<user_id>", methods=["GET"])
def worker_analytics(user_id):
    claims = [c for c in DB["claims"].values() if c["user_id"] == user_id]
    policies = [p for p in DB["policies"].values() if p["user_id"] == user_id]
    
    total_saved = sum(c["payout"] for c in claims if c["status"] == "approved")
    by_type = {}
    for c in claims:
        t = c["claim_type"]
        if t not in by_type:
            by_type[t] = {"count": 0, "payout": 0}
        by_type[t]["count"] += 1
        if c["status"] == "approved":
            by_type[t]["payout"] += c["payout"]
    
    weekly = {}
    for c in claims:
        week = c["date"][:10]
        if week not in weekly:
            weekly[week] = {"saved": 0, "claims": 0}
        if c["status"] == "approved":
            weekly[week]["saved"] += c["payout"]
            weekly[week]["claims"] += 1
    
    return jsonify({
        "total_saved": round(total_saved),
        "total_claims": len(claims),
        "approved_claims": len([c for c in claims if c["status"] == "approved"]),
        "by_disruption_type": by_type,
        "weekly_trend": weekly,
        "coverage_utilization": round(
            total_saved / (policies[0]["coverage_limit"] if policies else 1) * 100, 1
        ) if policies else 0
    })

# Seed some demo data
def seed_demo_data():
    # Create a demo policy
    user = DEMO_WORKER
    risk = compute_risk_score(user)
    premium = compute_weekly_premium(user, risk)
    
    pol_id = "POL_DEMO01"
    DB["policies"][pol_id] = {
        "id": pol_id,
        "user_id": user["id"],
        "plan": "standard",
        "status": "active",
        "created_at": (datetime.now() - timedelta(days=3)).isoformat(),
        "valid_from": (datetime.now() - timedelta(days=3)).isoformat(),
        "valid_until": (datetime.now() + timedelta(days=4)).isoformat(),
        "next_renewal": (datetime.now() + timedelta(days=4)).isoformat(),
        "auto_renew": True,
        "weekly_premium": premium["weekly_premium"],
        "coverage_limit": premium["coverage_limit"],
        "triggers": ["rain", "aqi", "platform", "curfew"],
        "risk_score": risk["score"],
        "payout_this_week": 850,
        "premium_breakdown": premium
    }
    
    # Demo claims
    for i, (ctype, hours, status, payout) in enumerate([
        ("rain", 4, "approved", 200),
        ("aqi", 3, "approved", 150),
        ("platform", 2, "approved", 100),
    ]):
        cid = f"CLM_DEMO0{i+1}"
        DB["claims"][cid] = {
            "id": cid,
            "user_id": user["id"],
            "policy_id": pol_id,
            "claim_type": ctype,
            "hours_lost": hours,
            "payout": payout,
            "status": status,
            "trigger_validated": True,
            "trigger_value": "Demo trigger",
            "fraud_result": {"is_fraud": False, "flags": [], "verdict": "APPROVED"},
            "date": (datetime.now() - timedelta(days=i+1)).isoformat(),
            "auto_triggered": True,
            "flow": [
                {"step": "Disruption Detected", "status": "done"},
                {"step": "Threshold Validated", "status": "done"},
                {"step": "Fraud Check", "status": "done"},
                {"step": "Payout Processed", "status": "done", "amount": payout}
            ]
        }

seed_demo_data()

if __name__ == "__main__":
    app.run(debug=True, port=5000, host="0.0.0.0")
