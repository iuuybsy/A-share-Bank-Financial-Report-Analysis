import pandas as pd
import os

def convert_excel_to_csv(excel_path, csv_output_path=None):
    """
    Convert the CMB financial indicator Excel file to a CSV 2D table (year × indicators).

    Parameters:
        excel_path (str): Path to the input .xlsx file.
        csv_output_path (str, optional): Path for the output CSV file. If not provided,
                                         it will be saved as "original_filename_output.csv"
                                         in the same directory.

    Returns:
        pd.DataFrame: The transformed DataFrame, and the CSV file is saved.
    """
    # ---------- Chinese-to-English mapping dictionary ----------
    MAP = {
        "营业收入": "OperatingIncome",
        "扣非归母净利润": "CoreNetProfit",
        "经现流": "OperatingCF",
        "稀释每股收益": "DilutedEPS",
        "扣非每股收益": "CoreEPS",
        "每股现金流净额": "CFPerShare",
        "平均资产收益率": "ROA",
        "扣非加权平均净资产收益率": "CoreROE",
        "总资产": "TotalAssets",
        "贷款和垫款总额": "GrossLoans",
        "不良贷款": "NPL",
        "贷款损失准备": "LoanLossReserve",
        "总负债": "TotalLiabilities",
        "公司活期存款": "CorpDemandDeposits",
        "公司定期存款": "CorpTimeDeposits",
        "零售活期存款": "RetailDemandDeposits",
        "零售定期存款": "RetailTimeDeposits",
        "股东权益": "Equity",
        "每股净资产": "NAVPS",
        "资本净额": "TotalCapital",
        "核心一级资本净额": "CoreTier1Capital",
        "风险加权资产": "RWA",
        "净利差": "NIS",
        "净利息收益率": "NIM",
        "净利息收入占比": "NIIRatio",
        "非利息收入占比": "NonIIRatio",
        "成本收入比": "CostIncomeRatio",
        "不良贷款率": "NPLRatio",
        "拨备覆盖率": "ProvisionCoverage",
        "信用成本": "CreditCost",
        "核心一级资本充足率": "CET1",
        "一级资本充足率": "Tier1CAR",
        "资本充足率": "CAR",
        "人民币流动性比例": "RMBLiquidityRatio",
        "外币流动性比例": "FCLiquidityRatio",
        "流动性覆盖率": "LCR",
        "正常类贷款迁徙率": "NormalMigRate",
        "关注类贷款迁徙率": "SpecialMigRate",
        "次级类贷款迁徙率": "SubstandardMigRate",
        "可疑类贷款迁徙率": "DoubtfulMigRate",
    }

    # ---------- Read all worksheets ----------
    xl = pd.ExcelFile(excel_path)
    data_by_year = {}

    for sheet_name in xl.sheet_names:
        # The sheet name is the year (e.g., "2025")
        try:
            year = int(sheet_name)
        except ValueError:
            continue  # Skip sheets not named with a numeric year

        df = pd.read_excel(excel_path, sheet_name=sheet_name, header=None)
        # First column: metric name (Chinese), second column: value
        metric_dict = {}
        for _, row in df.iterrows():
            chinese = row[0]
            value = row[1]
            if pd.isna(chinese) or pd.isna(value):
                continue
            eng = MAP.get(chinese, chinese)  # fallback to original if not mapped
            metric_dict[eng] = value
        data_by_year[year] = metric_dict

    # ---------- Collect the union of all metric columns ----------
    all_metrics = set()
    for d in data_by_year.values():
        all_metrics.update(d.keys())
    all_metrics = sorted(all_metrics)

    # ---------- Build DataFrame ----------
    rows = []
    for year in sorted(data_by_year.keys()):
        row = {"Year": year}
        row.update({m: data_by_year[year].get(m) for m in all_metrics})
        rows.append(row)

    df_out = pd.DataFrame(rows)

    # ---------- Output CSV ----------
    if csv_output_path is None:
        base, _ = os.path.splitext(excel_path)
        csv_output_path = base + "_output.csv"

    df_out.to_csv(csv_output_path, index=False, encoding="utf-8-sig")
    return df_out