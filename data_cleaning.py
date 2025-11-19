import pandas as pd
import numpy as np

def clean_retail_dataset(path):
    print("Loading dataset...")
    df = pd.read_excel(path)

    # -----------------------------------------------------------
    # 1. Basic Cleaning
    # -----------------------------------------------------------
    print("Removing duplicates...")
    df = df.drop_duplicates()

    # -----------------------------------------------------------
    # 2. Convert data types
    # -----------------------------------------------------------
    print("Converting dt to datetime...")
    df['dt'] = pd.to_datetime(df['dt'], errors='coerce')

    print("Converting time column...")
    df['time'] = pd.to_datetime(df['time'], errors='coerce').dt.time

    # -----------------------------------------------------------
    # 3. Drop columns with no useful information
    # -----------------------------------------------------------
    if df['discount'].isna().sum() == len(df):
        print("Dropping completely null column: discount")
        df = df.drop(columns=['discount'])

    # -----------------------------------------------------------
    # 4. Standardize categorical text
    # -----------------------------------------------------------
    print("Standardizing categories and text columns...")
    df['item_desc'] = df['item_desc'].str.strip().str.title()
    df['category'] = df['category'].str.strip().str.title()
    df['store_code'] = df['store_code'].str.strip()
    df['payment_type'] = df['payment_type'].str.strip().str.title()
    df['order_type'] = df['order_type'].str.strip().str.title()

    # -----------------------------------------------------------
    # 5. Handle missing / invalid numeric values
    # -----------------------------------------------------------
    numeric_cols = ['quantity', 'rate', 'tax_percent', 'total', 'cost_price',
                    'speed', 'availability', 'quality', 'hygiene', 'service']

    for col in numeric_cols:
        if df[col].dtype != 'float64' and df[col].dtype != 'int64':
            df[col] = pd.to_numeric(df[col], errors='coerce')
        df[col] = df[col].fillna(df[col].median())

    # -----------------------------------------------------------
    # 6. Derived Columns
    # -----------------------------------------------------------
    print("Creating derived metrics...")

    # Matches expected sale amount
    df['expected_total'] = df['quantity'] * df['rate']
    df['total_mismatch'] = np.where(df['expected_total'] != df['total'], True, False)

    # Profit per unit
    df['profit_per_unit'] = df['rate'] - df['cost_price']

    # Total profit
    df['total_profit'] = df['quantity'] * df['profit_per_unit']

    # Customer satisfaction score
    df['customer_score'] = df[['quality', 'service', 'speed', 'hygiene']].mean(axis=1)

    # -----------------------------------------------------------
    # 7. Remove impossible values
    # -----------------------------------------------------------
    print("Removing negative or zero quantity/total rows...")
    df = df[df['quantity'] > 0]
    df = df[df['total'] > 0]

    # -----------------------------------------------------------
    # 8. Export cleaned dataset
    # -----------------------------------------------------------
    print("Saving cleaned CSV to cleaned_retail_dataset.csv ...")
    df.to_csv("cleaned_retail_dataset.csv", index=False)

    print("Cleaning complete!")
    return df


if __name__ == "__main__":
    clean_retail_dataset("dataset.xlsx")

