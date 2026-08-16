# 🚀 Enterprise Decision Intelligence Platform (EDIP)

> An end-to-end **Business Intelligence & Decision Support Platform** built with **FastAPI, PostgreSQL, React, SQLAlchemy, Docker, Redis and Recharts** for executive analytics, root-cause intelligence, and AI-driven business decision support.

---

# 📌 Overview

Enterprise Decision Intelligence Platform (EDIP) transforms raw sales and operational data into actionable executive insights. The platform performs KPI analytics, profitability analysis, regional intelligence, discount impact analysis, root-cause detection, and strategic business recommendations through an interactive dashboard.

It combines modern backend engineering with analytical workflows to help organizations make faster, data-driven decisions.

---

# ✨ Features

- Executive KPI Dashboard
- Business Filters (Category, Region, Segment, Priority)
- Monthly Revenue & Profit Analytics
- Product Root Cause Intelligence
- Discount Impact Intelligence
- Category & Regional Intelligence
- Decision Recommendation Engine
- Business Alerts System
- PDF Executive Report Export
- FastAPI REST APIs
- PostgreSQL Data Warehouse
- React Interactive Dashboard
- Docker Ready Architecture

---

# 🛠 Tech Stack

| Category | Technologies |
|----------|-------------|
| Frontend | React, Vite, Recharts |
| Backend | FastAPI, Python |
| Database | PostgreSQL |
| ORM | SQLAlchemy |
| Analytics | Pandas, NumPy |
| Visualization | Recharts |
| Cache | Redis |
| Deployment | Docker, Docker Compose |

---

# 🏗 System Architecture

```mermaid
flowchart LR

A[CSV Dataset] --> B[ETL Pipeline]
B --> C[PostgreSQL]
C --> D[FastAPI]
D --> E[Decision Engine]
E --> F[React Dashboard]
F --> G[Executive Insights]
```

---

# 📂 Project Structure

```text
Enterprise-Decision-Intelligence-Platform/
│
├── backend/
│   ├── app/
│   │   ├── api/
│   │   ├── analytics/
│   │   ├── decision_engine/
│   │   ├── models/
│   │   └── core/
│   ├── database/
│   └── requirements.txt
│
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   ├── api.js
│   │   └── App.jsx
│   └── package.json
│
├── datasets/
├── docker-compose.yml
└── README.md
```

---

# 🚀 Quick Start

```bash
git clone https://github.com/gavneet0030/Enterprise-Decision-Intelligence-Platform.git

cd Enterprise-Decision-Intelligence-Platform
```

## Backend

```bash
cd backend
pip install -r requirements.txt
uvicorn app.main:app --reload
```

## Frontend

```bash
cd frontend
npm install
npm run dev
```

### Swagger API

```text
http://127.0.0.1:8000/docs
```

---

# 📡 API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/v1/dashboard` | Executive dashboard |
| GET | `/api/v1/growth` | Revenue growth analytics |
| GET | `/api/v1/product` | Root cause analysis |
| GET | `/api/v1/discount` | Discount intelligence |
| GET | `/api/v1/region` | Regional intelligence |
| GET | `/api/v1/decisions` | Decision recommendations |
| GET | `/api/v1/export/pdf` | Executive PDF report |
| GET | `/docs` | Swagger Documentation |

---

# 📖 About the Project

## ✅ 1. What was the problem?

Large enterprises generate thousands of sales transactions across multiple regions, customer segments, and product categories. Decision-makers often rely on static reports that do not explain **why profit is declining**, **which products are responsible**, or **where corrective actions should be taken**.

EDIP solves this by creating a centralized decision intelligence system that converts operational data into executive-level business insights.

---

## 📊 2. How was the data?

The platform uses the **Superstore retail dataset** containing historical business transactions.

### Dataset Includes

- Orders
- Sales
- Profit
- Discount
- Quantity
- Customer Segment
- Region & State
- Product Category
- Order Date

The raw data is cleaned through an ETL pipeline before being loaded into PostgreSQL for analytical querying.

---

## 📈 3. What analysis did you do?

The platform performs multiple business intelligence analyses:

### Executive KPI Analysis

- Revenue
- Profit
- Orders
- Units Sold
- Profit Margin

### Financial Trend Analysis

- Monthly Revenue
- Monthly Profit
- Growth Rate
- Profit Margin Trend

### Root Cause Intelligence

- Loss-making products
- High discount impact
- Negative profitability detection

### Business Intelligence

- Regional comparison
- Category profitability
- Customer segment performance
- Decision prioritization

---

## 💡 4. What insights did that yield?

The analytical engine generates actionable executive recommendations instead of raw numbers.

### Example Insights

- Technology category contributes the highest enterprise profit.
- Furniture has strong revenue but significantly lower profit margin.
- Products with 40–50% discount consistently generate losses.
- Eastern region shows higher profitability than several other regions.
- High-priority products are automatically flagged for management action.

These insights help executives optimize pricing, discount strategy, inventory, and regional business performance.

---

# 🔄 Workflow

```text
Business Transactions
        │
        ▼
CSV Dataset
        │
        ▼
ETL Pipeline
        │
        ▼
PostgreSQL Warehouse
        │
        ▼
FastAPI Analytics APIs
        │
        ▼
Decision Intelligence Engine
        │
        ▼
React Executive Dashboard
        │
        ▼
Business Recommendations
```

---

# 🎯 Key Functionalities

- Executive KPI Dashboard
- Financial Performance Analytics
- Product Root Cause Detection
- Discount Impact Intelligence
- Regional Intelligence
- Category Profitability Analysis
- Business Alerts
- Decision Recommendation Engine
- Interactive Filtering
- PDF Report Generation

---

# 🌍 Real-World Applications

EDIP can be adopted by:

- Retail Enterprises
- E-commerce Companies
- FMCG Organizations
- Supply Chain Teams
- Business Intelligence Departments
- Financial Analytics Teams
- Executive Leadership

---

# 📈 Business Benefits

- Faster executive decision-making
- Reduced manual reporting effort
- Profitability optimization
- Intelligent discount strategy
- Early identification of loss-making products
- Regional performance benchmarking

---

# 🧠 Technical Highlights

- Modular FastAPI architecture
- SQLAlchemy ORM
- PostgreSQL analytical warehouse
- ETL data pipeline
- React + Recharts visualization
- RESTful API design
- PDF export system
- Docker-ready deployment

---

# 🚀 Future Enhancements

- CI/CD with GitHub Actions
- AWS Deployment
- Kubernetes
- Redis Background Jobs
- ML-based Sales Forecasting
- SHAP Explainable AI
- Real-time Streaming Analytics
- Role-Based Access Control (RBAC)

---

# 👨‍💻 Author

**Gavneet Singh**

- GitHub: https://github.com/gavneet0030
- LinkedIn: https://www.linkedin.com/in/gavneetsingh/

---

⭐ If you found this project useful, consider giving it a **Star** on GitHub.
