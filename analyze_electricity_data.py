#!/usr/bin/env python3
"""
PGE Electricity Data Analysis: 2025
Analyzes monthly comparisons and identifies above-average usage days
"""

import pandas as pd
import numpy as np
from datetime import datetime

# Read the data
file_path = "/Users/aishwarya/Documents/PGE/pge_electric_usage_2025_10_to_12.csv"

# Skip the header rows (first 6 rows contain account info)
df = pd.read_csv(file_path, skiprows=6)

# Clean the data
df['DATE'] = pd.to_datetime(df['DATE'])
df['USAGE (kWh)'] = pd.to_numeric(df['USAGE (kWh)'], errors='coerce')
df['COST'] = df['COST'].str.replace('$', '').astype(float)

# Extract month for grouping
df['Month'] = df['DATE'].dt.month
df['Month_Name'] = df['DATE'].dt.strftime('%B')

# Aggregate by date
daily_data = df.groupby('DATE').agg({
    'USAGE (kWh)': 'sum',
    'COST': 'sum',
    'Month': 'first',
    'Month_Name': 'first'
}).reset_index()

daily_data.columns = ['Date', 'Usage_kWh', 'Cost_USD', 'Month', 'Month_Name']

# Monthly totals
monthly_totals = daily_data.groupby(['Month', 'Month_Name']).agg({
    'Cost_USD': 'sum',
    'Usage_kWh': 'sum'
}).reset_index()

print("=" * 80)
print("PGE ELECTRICITY ANALYSIS: October - December 2025")
print("=" * 80)
print()

# SECTION 1: Monthly Comparison
print("=" * 80)
print("MONTHLY COMPARISON")
print("=" * 80)
print()

print("TOTAL COST PER MONTH:")
print("-" * 40)
for _, row in monthly_totals.iterrows():
    print(f"{row['Month_Name']:12s}: ${row['Cost_USD']:8.2f}")
print()

print("TOTAL USAGE PER MONTH:")
print("-" * 40)
for _, row in monthly_totals.iterrows():
    print(f"{row['Month_Name']:12s}: {row['Usage_kWh']:8.2f} kWh")
print()

print("MONTH-OVER-MONTH TRENDS:")
print("-" * 40)
# Calculate month-over-month changes
for i in range(1, len(monthly_totals)):
    prev_month = monthly_totals.iloc[i-1]
    curr_month = monthly_totals.iloc[i]

    cost_change = curr_month['Cost_USD'] - prev_month['Cost_USD']
    cost_pct_change = (cost_change / prev_month['Cost_USD']) * 100

    usage_change = curr_month['Usage_kWh'] - prev_month['Usage_kWh']
    usage_pct_change = (usage_change / prev_month['Usage_kWh']) * 100

    print(f"{prev_month['Month_Name']} to {curr_month['Month_Name']}:")
    print(f"  Cost:  ${cost_change:+8.2f} ({cost_pct_change:+6.2f}%)")
    print(f"  Usage: {usage_change:+8.2f} kWh ({usage_pct_change:+6.2f}%)")
    print()

# SECTION 2: Above-Average Days Analysis (per month)
print("=" * 80)
print("ABOVE-AVERAGE DAYS ANALYSIS (BY MONTH)")
print("=" * 80)
print()

for month_num in sorted(daily_data['Month'].unique()):
    month_data = daily_data[daily_data['Month'] == month_num]
    month_name = month_data.iloc[0]['Month_Name']

    # Calculate averages for this month
    avg_cost = month_data['Cost_USD'].mean()
    avg_usage = month_data['Usage_kWh'].mean()

    # Find above-average days
    above_avg_cost_days = month_data[month_data['Cost_USD'] > avg_cost].sort_values('Cost_USD', ascending=False)
    above_avg_usage_days = month_data[month_data['Usage_kWh'] > avg_usage].sort_values('Usage_kWh', ascending=False)

    print(f"{month_name.upper()} 2025")
    print("-" * 80)
    print(f"Average Daily Cost:  ${avg_cost:.2f}")
    print(f"Average Daily Usage: {avg_usage:.2f} kWh")
    print()

    # Above-average cost days
    print(f"Days with ABOVE-AVERAGE Cost (>{avg_cost:.2f}):")
    print(f"{'Date':<15} {'Day':<10} {'Cost':<12} {'Usage (kWh)':<12}")
    print("-" * 50)
    for _, row in above_avg_cost_days.iterrows():
        day_name = row['Date'].strftime('%A')
        print(f"{row['Date'].strftime('%Y-%m-%d'):<15} {day_name:<10} ${row['Cost_USD']:<11.2f} {row['Usage_kWh']:<12.2f}")
    print()

    # Above-average usage days
    print(f"Days with ABOVE-AVERAGE Usage (>{avg_usage:.2f} kWh):")
    print(f"{'Date':<15} {'Day':<10} {'Usage (kWh)':<12} {'Cost':<12}")
    print("-" * 50)
    for _, row in above_avg_usage_days.iterrows():
        day_name = row['Date'].strftime('%A')
        print(f"{row['Date'].strftime('%Y-%m-%d'):<15} {day_name:<10} {row['Usage_kWh']:<12.2f} ${row['Cost_USD']:<11.2f}")
    print()
    print()

# SUMMARY STATISTICS
print("=" * 80)
print("OVERALL SUMMARY (2025)")
print("=" * 80)
print(f"Total Period Cost:        ${monthly_totals['Cost_USD'].sum():.2f}")
print(f"Total Period Usage:       {monthly_totals['Usage_kWh'].sum():.2f} kWh")
print(f"Average Daily Cost:       ${daily_data['Cost_USD'].mean():.2f}")
print(f"Average Daily Usage:      {daily_data['Usage_kWh'].mean():.2f} kWh")
print(f"Highest Single Day Cost:  ${daily_data['Cost_USD'].max():.2f} on {daily_data.loc[daily_data['Cost_USD'].idxmax(), 'Date'].strftime('%Y-%m-%d')}")
print(f"Highest Single Day Usage: {daily_data['Usage_kWh'].max():.2f} kWh on {daily_data.loc[daily_data['Usage_kWh'].idxmax(), 'Date'].strftime('%Y-%m-%d')}")
print()
