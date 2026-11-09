# Customer Purchase Intelligence

**Dashboard name:** PIGMENT — Customer Purchase Intelligence  
**Project:** Customer Purchase Pattern Analysis Using Apache Pig

## Overview

An interactive retail analytics dashboard. Upload a retail transaction CSV through the website sidebar and explore customer purchasing behaviour, product performance, category revenue, monthly sales, and city-wise revenue.

**No CSV dataset is included in this repository or ZIP.** Users upload their own CSV file directly through the Streamlit website.

## Features

- CSV upload directly in the Streamlit app
- Automatic validation of required columns
- Total revenue, orders, customers, and average order KPIs
- Monthly revenue trend
- Category revenue breakdown
- Top products by revenue
- City-wise revenue comparison
- Searchable transaction table
- Download filtered transactions as CSV

## Required CSV columns

The uploaded CSV must contain these exact column names (capitalization and surrounding spaces are normalized):

```text
transaction_id
customer_id
transaction_date
product_id
product_name
category
quantity
unit_price
total_amount
payment_method
city
```

Example CSV header:

```csv
transaction_id,customer_id,transaction_date,product_id,product_name,category,quantity,unit_price,total_amount,payment_method,city
```

Dates should be parseable by Pandas (for example `2026-05-21`). Quantity, unit_price, and total_amount should be numeric.

## Run locally

```bash
pip install -r requirements.txt
streamlit run app.py
```

Open the local Streamlit URL, then use **Upload your dataset** in the left sidebar to select a CSV file.

## Deploy on Streamlit Community Cloud

1. Push this repository to GitHub.
2. In Streamlit Community Cloud, create a new app and select this repository.
3. Set the main file path to `app.py`.
4. Deploy.
5. Open the deployed website and upload your CSV using the sidebar uploader.

## Apache Pig analysis

The Pig Latin script is provided at `pig/purchase_analysis.pig`.

First upload the same CSV you used in the dashboard to HDFS. For example:

```bash
hdfs dfs -mkdir -p /user/cloudera/purchase/input
hdfs dfs -put -f customer_transactions.csv /user/cloudera/purchase/input/
pig -x mapreduce pig/purchase_analysis.pig
```

The Pig script writes product, customer, category, and city summaries under `/user/cloudera/purchase/output/`. Change the HDFS paths if your Hadoop username or directory differs.

## Repository structure

```text
Customer-Purchase-Insights/
├── app.py
├── requirements.txt
├── README.md
├── .gitignore
├── LICENSE
└── pig/
    └── purchase_analysis.pig
```

## GitHub upload

```bash
git init
git add .
git commit -m "Add CSV upload customer purchase analytics dashboard"
git branch -M main
git remote add origin https://github.com/YOUR-USERNAME/Customer-Purchase-Insights.git
git push -u origin main
```

Replace the remote URL with your own GitHub repository URL.
