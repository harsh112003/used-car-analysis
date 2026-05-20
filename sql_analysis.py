import mysql.connector
import pandas as pd

# ── Connect to MySQL ───────────────────────────────────────────────────────────
conn = mysql.connector.connect(
    host='localhost',
    user='root',
    password='root1234',  # replace with your MySQL root password
    database='used_cars'
)

print("Connected to MySQL successfully")
print()

# ── Helper function ────────────────────────────────────────────────────────────
def run_query(title, query):
    print("=" * 60)
    print(title)
    print("=" * 60)
    df = pd.read_sql(query, conn)   #main conn between mysql and pandas
    print(df.to_string(index=False))
    print()
    return df

# ── Query 1: Transmission vs Price ────────────────────────────────────────────
run_query(
    "QUERY 1: Transmission vs Average Price",
    """
    SELECT 
        Transmission,
        COUNT(*) as total_cars,
        ROUND(AVG(CAST(REPLACE(REPLACE(AskPrice, '₹ ', ''), ',', '') 
            AS DECIMAL(10,2))) / 100000, 2) as avg_price_lakh
    FROM cars
    GROUP BY Transmission
    ORDER BY avg_price_lakh DESC
    """
)

# ── Query 2: Top 10 Brands by Volume ──────────────────────────────────────────
run_query(
    "QUERY 2: Top 10 Brands by Market Share",
    """
    SELECT 
        Brand,
        COUNT(*) as total_listings,
        ROUND(COUNT(*) * 100.0 / (SELECT COUNT(*) FROM cars), 1) as market_share_pct
    FROM cars
    GROUP BY Brand
    ORDER BY total_listings DESC
    LIMIT 10
    """
)

# ── Query 3: Fuel Type Depreciation by Age ────────────────────────────────────
run_query(
    "QUERY 3: Diesel vs Petrol Average Price by Age Group",
    """
    SELECT 
        FuelType,
        CASE 
            WHEN Age BETWEEN 0 AND 3 THEN '0-3 yrs'
            WHEN Age BETWEEN 4 AND 6 THEN '4-6 yrs'
            WHEN Age BETWEEN 7 AND 10 THEN '7-10 yrs'
            WHEN Age BETWEEN 11 AND 15 THEN '11-15 yrs'
            ELSE '15+ yrs'
        END as AgeBucket,
        COUNT(*) as total_cars,
        ROUND(AVG(CAST(REPLACE(REPLACE(AskPrice, '₹ ', ''), ',', '') 
            AS DECIMAL(10,2))) / 100000, 2) as avg_price_lakh
    FROM cars
    WHERE FuelType IN ('Petrol', 'Diesel')
    GROUP BY FuelType, AgeBucket
    ORDER BY FuelType, AgeBucket
    """
)

# ── Query 4: Owner Type vs Price ───────────────────────────────────────────────
run_query(
    "QUERY 4: First vs Second Owner Average Price",
    """
    SELECT
        Owner,
        COUNT(*) as total_cars,
        ROUND(AVG(CAST(REPLACE(REPLACE(AskPrice, '₹ ', ''), ',', '') 
            AS DECIMAL(10,2))) / 100000, 2) as avg_price_lakh
    FROM cars
    GROUP BY Owner
    ORDER BY avg_price_lakh DESC
    """
)

# ── Query 5: Brand Health Scorecard ───────────────────────────────────────────
run_query(
    "QUERY 5: Brand Health Scorecard",
    """
    SELECT
        Brand,
        COUNT(*) as total_listings,
        ROUND(AVG(CAST(REPLACE(REPLACE(AskPrice, '₹ ', ''), ',', '') 
            AS DECIMAL(10,2))) / 100000, 1) as avg_price_lakh,
        ROUND(AVG(Age), 1) as avg_age_years,
        ROUND(SUM(CASE WHEN Owner = 'first' THEN 1 ELSE 0 END) 
            * 100.0 / COUNT(*), 0) as first_owner_pct
    FROM cars
    GROUP BY Brand
    HAVING COUNT(*) >= 50
    ORDER BY avg_price_lakh DESC
    """
)

conn.close()
print("Done. Connection closed.")