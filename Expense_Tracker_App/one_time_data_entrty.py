import pandas as pd
import random
from datetime import datetime, timedelta
from flask import Flask


# Use only categories present in your HTML form
app=Flask(__name__)
@app.route('/')
def d1():
    categories = ['Food', 'Transport', 'Rent', 'Shopping', 'Utilities', 'Other']

    # Amount range per category
    amount_range = {
        'Food': (30, 250),
        'Transport': (20, 150),
        'Rent': (3000, 7000),
        'Shopping': (100, 2000),
        'Utilities': (200, 1000),
        'Other': (50, 500)
    }

    # Generate 50 entries for the last 6–8 months
    entries = []
    start_date = datetime(2024, 11, 1)
    for _ in range(50):
        date = start_date + timedelta(days=random.randint(0, 230))
        category = random.choice(categories)
        amount = round(random.uniform(*amount_range[category]), 2)
        description = f"{category} expense on {date.strftime('%A')}"

        entries.append({
            'Date': date.strftime('%Y-%m-%d'),
            'Category': category,
            'Amount': amount,
            'Description': description
        })

    # Save to Excel
    df = pd.DataFrame(entries)
    df.to_excel('Expense_tracker.xlsx', index=False)

    return " populated with 50 valid entries."

app.run(debug=True)


