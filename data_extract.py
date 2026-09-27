# -*- coding: utf-8 -*-
"""
Read multiple sheets (bank codes) from bank_data.xlsx,
reshape them into long format and save as CSV files.
"""

import os
import pandas as pd

# ============ Configuration ============
input_file = "data/bank_data.xlsx"
output_dir = "data"
os.makedirs(output_dir, exist_ok=True)

long_csv = os.path.join(output_dir, "bank_data_long.csv")
wide_csv = os.path.join(output_dir, "bank_data_wide.csv")

# ============ Indicator Chinese-English mapping ============
INDICATOR_MAP = {
    # Profitability / earnings
    "净息差": "NIM",
    "净利差": "NIS",
    "ROA": "ROA",
    "ROE": "ROE",
    "RORWA": "RORWA",
    "成本收入比": "Cost-to-Income Ratio",
    "营业收入增速": "Operating Income Growth Rate",
    "扣非归母净利润增速": "Recurring Net Profit Growth Rate",
    "拨备前利润增速": "Pre-provision Profit Growth Rate",
    "非息收入占比": "NIIR",
    # Asset quality
    "不良贷款率": "NPL",
    "不良生成率": "NPLG",
    "拨备覆盖率": "PCR",
    "拨贷比": "LLR",
    "信贷成本": "Credit Cost",
    # Capital adequacy
    "资本充足率": "CAR",
    "核心一级资本充足率": "CET1 CAR",
    "杠杆率": "LR",
    # Scale / growth
    "总资产增速": "Total Assets Growth Rate",
    "贷款增速": "Loan Growth Rate",
    "存款增速": "Deposit Growth Rate",
    "存款成本率": "Deposit Cost Rate",
    "贷款收益率": "Loan Yield",
    # Per share / dividends
    "EPS": "EPS",
    "BPS": "BPS",
    "股息率": "Dividend Yield",
}

# ============ Bank mapping: sheet name -> (stock code, abbreviation) ============
# Modify this mapping based on the actual sheet names in your data.
BANK_MAP = {
    "招商银行": ("600036", "CMD"),
    "600036": ("600036", "CMD"),
    "工商银行": ("601398", "ICBC"),
    "601398": ("601398", "ICBC"),
    "兴业银行": ("601166", "CIB"),
    "601166": ("601166", "CIB"),
    "中信银行": ("601998", "CITIC"),
    "601998": ("601998", "CITIC"),
    "华夏银行": ("600015", "HXB"),
    "600015": ("600015", "HXB"),
}


def get_indicator_en(name):
    """Convert a Chinese indicator name to its English abbreviation;
    return the original name if it is not in the mapping."""
    return INDICATOR_MAP.get(str(name), str(name))


def get_bank_info(sheet_name):
    """Return (stock code, abbreviation)."""
    name = str(sheet_name)
    if name in BANK_MAP:
        return BANK_MAP[name]
    # If the sheet name is already in "code_abbreviation" format.
    if "_" in name:
        parts = name.split("_", 1)
        return parts[0], parts[1]
    # Fallback: use the name as the code and the first 3 characters as the abbreviation.
    return name, name[:3].upper()


# ============ 1. Read all sheets from the Excel file ============
sheets = pd.read_excel(input_file, sheet_name=None, header=None)

records = []

# ============ 2. Convert to long format ============
for sheet_name, df in sheets.items():
    stock_code, bank_abbr = get_bank_info(sheet_name)
    years = df.iloc[0, 1:].tolist()
    for _, row in df.iloc[1:].iterrows():
        indicator = row.iloc[0]
        if pd.isna(indicator):
            continue
        indicator_en = get_indicator_en(indicator)
        for year, value in zip(years, row.iloc[1:]):
            if pd.isna(year):
                continue
            records.append({
                "BankCode": str(stock_code),
                "BankAbbr": str(bank_abbr),
                "Indicator": indicator_en,
                "Year": int(float(year)),
                "Value": pd.to_numeric(value, errors="coerce")
            })

long_df = pd.DataFrame(records)
long_df = long_df.sort_values(["Indicator", "Year", "BankCode"]).reset_index(drop=True)
long_df.to_csv(long_csv, index=False, encoding="utf-8-sig")

# ============ 3. Save the wide table ============
wide_df = long_df.pivot_table(
    index=["Year", "Indicator"],
    columns="BankCode",
    values="Value"
).reset_index()
wide_df.to_csv(wide_csv, index=False, encoding="utf-8-sig")

print("Long table saved:", long_csv, long_df.shape)
print("Wide table saved:", wide_csv, wide_df.shape)

# ============ 4. Save one CSV per bank ============
# Rows: Year, columns: Indicator.
for bank_code, group in long_df.groupby("BankCode"):
    bank_abbr = group["BankAbbr"].iloc[0]
    pivot = group.pivot_table(
        index="Year",
        columns="Indicator",
        values="Value"
    ).reset_index()
    pivot.columns.name = None
    filename = f"{bank_code}_{bank_abbr}.csv"
    filepath = os.path.join(output_dir, filename)
    pivot.to_csv(filepath, index=False, encoding="utf-8-sig")
    print(f"Bank CSV saved: {filepath}, shape={pivot.shape}")
