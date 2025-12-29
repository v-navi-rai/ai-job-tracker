from flask import Flask, request, jsonify
import numpy as np
import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import StandardScaler

app = Flask(__name__)

# -----------------------------
# 1. Generate Synthetic Dataset
# -----------------------------
np.random.seed(42)
N = 2000

data = []

for _ in range(N):
    cpi = np.random.uniform(6.0, 10.0)
    skills = np.random.randint(1, 11)
    projects = np.random.randint(0, 7)
    experience_months = np.random.randint(0, 25)
    college_tier = np.random.choice([1, 2, 3], p=[0.4, 0.4, 0.2])
    role_type = np.random.choice([0, 1])        # 1 = tech
    company_type = np.random.choice([0, 1])     # 1 = product

    score = (
        0.35 * cpi +
        0.25 * skills +
        0.15 * projects +
        0.15 * (experience_months / 12) +
        0.1 * (college_tier == 1) +
        0.1 * role_type +
        0.1 * company_type
    )

    shortlisted = 1 if score > 6.5 else 0

    data.append([
        cpi, skills, projects, experience_months,
        college_tier, role_type, company_type, shortlisted
    ])

df = pd.DataFrame(data, columns=[
    "cpi", "skills", "projects", "experience_months",
    "college_tier", "role_type", "company_type", "shortlisted"
])

# -----------------------------
# 2. Train Model
# -----------------------------
X = df.drop("shortlisted", axis=1)
y = df["shortlisted"]

scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

model = LogisticRegression(max_iter=1000)
model.fit(X_scaled, y)

# -----------------------------
# 3. Prediction API
# -----------------------------
@app.route("/predict", methods=["POST"])
def predict():
    data = request.json

    features = np.array([[
        data["cpi"],
        data["skills"],
        data["projects"],
        data["experience_months"],
        data["college_tier"],
        data["role_type"],
        data["company_type"]
    ]])

    features_scaled = scaler.transform(features)
    probability = model.predict_proba(features_scaled)[0][1]

    return jsonify({
        "shortlisting_probability": round(probability * 100, 2)
    })

# -----------------------------
if __name__ == "__main__":
    app.run(port=5000, debug=True)
