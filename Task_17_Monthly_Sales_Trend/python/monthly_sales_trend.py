"""
Task 17: Monthly Sales Trend
Tools: Python, pandas, matplotlib
Dataset: ../data/retail_sales.csv (sample Superstore-style retail dataset)
Run from the project folder:
    python python/monthly_sales_trend.py
"""
from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt

PROJECT_DIR = Path(__file__).resolve().parents[1]
DATA_PATH = PROJECT_DIR / "data" / "retail_sales.csv"
OUTPUT_DIR = PROJECT_DIR / "output"
OUTPUT_DIR.mkdir(exist_ok=True)

df = pd.read_csv(DATA_PATH)
df["Order Date"] = pd.to_datetime(df["Order Date"], errors="coerce")
df["Sales"] = pd.to_numeric(df["Sales"], errors="coerce")
df = df.dropna(subset=["Order Date", "Sales"])

# Group by month and sort chronologically
monthly_sales = (
    df.assign(Month=df["Order Date"].dt.to_period("M").dt.to_timestamp())
      .groupby("Month", as_index=False)["Sales"]
      .sum()
      .sort_values("Month")
)
monthly_sales["Sales"] = monthly_sales["Sales"].round(2)
monthly_sales.to_csv(OUTPUT_DIR / "monthly_sales_summary.csv", index=False)

plt.figure(figsize=(12, 6))
plt.plot(monthly_sales["Month"], monthly_sales["Sales"], marker="o")
plt.title("Monthly Sales Trend")
plt.xlabel("Month")
plt.ylabel("Total Sales (₹)")
plt.grid(True, alpha=0.3)
plt.xticks(rotation=45, ha="right")
plt.tight_layout()
plt.savefig(OUTPUT_DIR / "monthly_sales_trend.png", dpi=160)
plt.show()

print("Monthly sales summary:")
print(monthly_sales.to_string(index=False))
print(f"\nSaved summary to: {OUTPUT_DIR / 'monthly_sales_summary.csv'}")
print(f"Saved chart to: {OUTPUT_DIR / 'monthly_sales_trend.png'}")
