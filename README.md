# 📊 Sales Analytics API

A RESTful Sales Analytics API built using **FastAPI**, **SQLModel**, and **PostgreSQL (Supabase)**.

This project was developed as **Capstone 1** during my internship at **Emami**. The API exposes sales analytics endpoints and a complete Product CRUD system over a PostgreSQL database.

---

## Features

### Sales Analytics

- Total KPIs
- Sales Trend (Daily / Weekly / Monthly / Yearly)
- Sales by Region
- Sales by Category
- Top Selling Products

### Product Management

- Create Product
- Read Products
- Read Single Product
- Update Product
- Delete Product

### Other Features

- PostgreSQL (Supabase)
- SQLModel ORM
- Auto-generated Swagger Documentation
- Request Validation using Pydantic
- Error Handling (404, 422)
- RESTful API Design

---

## Tech Stack

| Technology | Purpose |
|------------|---------|
| FastAPI | REST API Framework |
| SQLModel | ORM |
| SQLAlchemy | Database Engine |
| PostgreSQL (Supabase) | Database |
| Pandas | CSV Import |
| Uvicorn | ASGI Server |
| Pydantic | Data Validation |

---

## Project Structure

```text
SalesAnalyticsAPI
│
├── app
│   ├── database.py
│   ├── main.py
│   ├── models.py
│   ├── schemas.py
│   └── routers
│       ├── analytics.py
│       └── products.py
│
├── data
│   ├── FMCG_2022_2024.csv
│   └── Products.csv
│
├── scripts
│   ├── importSales_csv.py
│   ├── importProducts.py
│   └── exploreProducts.ipynb
│
├── requirements.txt
├── README.md
└── .env
```

---

## Installation

Clone the repository

```bash
git clone https://github.com/parthsingh23/SalesAnalyticsAPI.git
cd SalesAnalyticsAPI
```

Create a virtual environment

```bash
python -m venv cap1Env
```

Activate it

### Windows

```bash
cap1Env\Scripts\activate
```

Install dependencies

```bash
pip install -r requirements.txt
```

---

## Environment Variables

Create a `.env` file

```env
DATABASE_URL=your_supabase_database_url
```

---

## Run the API

```bash
uvicorn app.main:app --reload
```

The API will be available at

```
http://127.0.0.1:8000
```

Swagger Documentation

```
http://127.0.0.1:8000/docs
```

---

## API Endpoints

### Analytics

| Method | Endpoint |
|---------|----------|
| GET | /analytics/kpis |
| GET | /analytics/sales/trend |
| GET | /analytics/sales/by-region |
| GET | /analytics/sales/by-category |

### Products

| Method | Endpoint |
|---------|----------|
| GET | /products |
| GET | /products/{id} |
| POST | /products |
| PUT | /products/{id} |
| DELETE | /products/{id} |
| GET | /products/top |

---

## Database

- PostgreSQL
- Hosted on Supabase
- Imported sales dataset (~190k records)
- Imported products dataset (~4548 records)

---

## Author

**Parth Singh**

B.Tech CSE, Techno India University

IIT Madras BS Degree (Data Science)

GitHub: https://github.com/parthsingh23

---

## License

This project was developed for educational and internship purposes.