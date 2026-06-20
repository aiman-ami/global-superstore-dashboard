# Global Superstore Business Dashboard

An interactive business intelligence dashboard built with Streamlit for analyzing sales, profit, and segment-wise performance across global retail operations.

## Objective

Retail businesses generate large volumes of transactional data across regions, product categories, and customer segments. This project transforms raw order data into an interactive dashboard that allows stakeholders to monitor KPIs, compare performance across filters, and identify high value customers without writing a single line of code.

## Dataset

Global Superstore Dataset containing three tables:

**Orders** : 51,290 transactions from 2011 to 2014 across 13 regions and 3 product categories

**Returns** :  Order IDs of all returned orders used to calculate return rate

**People** : Regional manager assignments per region

## Approach

1. Loaded and merged all three sheets from the Excel file
2. Cleaned missing values and engineered new features including Order Year, Profit Margin, and Returned flag
3. Built an interactive Streamlit dashboard with five sidebar filters
4. Displayed KPIs and six chart types covering sales trends, category performance, segment distribution, regional analysis, sub-category breakdown, and top customers

## Dashboard Features

- Sidebar filters for Region, Category, Sub-Category, Year, and Regional Manager
- Five KPI cards showing Total Sales, Total Profit, Average Order Value, Total Orders, and Returns
- Sales and Profit trend over time
- Sales and Profit by Category
- Sales by Regional Manager
- Top 10 Sub-Categories by Sales
- Sales distribution by Customer Segment
- Top 5 Customers by Sales table
- Full filterable data table

## Visuals

![Sales and Profit Trend](visuals/sales_and_profit_trend.png)
![Sales by Category](visuals/total_sales_and_profit.png)
![Sales by Segment](visuals/sales_distribution_by_segment.png)
![Top 8 Regions](visuals/top_8.png)

## Key Findings

- Total sales of $12.6M and total profit of $1.47M across the four year period
- Technology is the most profitable category with a 14% profit margin
- Furniture generates high sales volume but has the weakest profit margin, indicating excessive discounting
- The Consumer segment accounts for 51.5% of all revenue
- Sales grew consistently year over year from 2011 to 2014
- The Central region leads all regions in total sales by a significant margin
- Top customer Tom Ashbrook generated over $40,000 in sales alone

## Results

| Metric | Value |
|---|---|
| Total Sales | $12,642,501 |
| Total Profit | $1,467,457 |
| Total Orders | 25,035 |
| Top Category | Technology |
| Top Segment | Consumer (51.5%) |
| Top Region | Central |

## Tech Stack

- Python 3.12
- Streamlit
- Pandas
- Matplotlib
- xlrd
