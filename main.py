import matplotlib.pyplot as plt

from data_extract import get_dataframe

def plot_data(data_name, datas, labels, title):
    fig, ax = plt.subplots()
    for i, data in enumerate(datas):
        ax.plot(data['Year'].values, data[data_name].values, label=labels[i], marker='o')
    ax.set_xlabel("years")
    ax.set_title(title)
    ax.grid(True)
    plt.legend()

def main():
    # ----- data extract and prepare -----
    df_cmb = get_dataframe("600036_CMB/600036_CMB.xlsx", "600036_CMB/cmb_financials.csv")
    df_cib = get_dataframe("601166_CIB/601166_CIB.xlsx", "601166_CIB/cib_financials.csv")
    df_cncb = get_dataframe("601998_CNCB/601998_CNCB.xlsx", "601998_CNCB/cncb_financials.csv")

    data = [df_cmb, df_cib, df_cncb]
    labels = ["CMB", "CIB", "CNCB"]

    # ----- income and profit -----
    # plot_data("OperatingIncome", data, labels, "Operating Income")
    # plot_data("CoreNetProfit", data, labels, "Core Net Profit")
    # plot_data("DilutedEPS", data, labels, "Diluted EPS")
    # plot_data("CoreEPS", data, labels, "CoreEPS")
    plot_data("ROA", data, labels, "ROA(%)")
    plot_data("CoreROE", data, labels, "Core ROE(%)")
    plot_data("NIS", data, labels, "NIS(%)")
    plot_data("NIM", data, labels, "NIM(%)")
    plot_data("RORWA", data, labels, "RORWA(%)")
    plot_data("NonIIRatio", data, labels, "Non-Interest Income Ratio(%)")
    plot_data("CostIncomeRatio", data, labels, "Cost Income Ratio(%)")

    # ----- assets structure -----
    # plot_data("TotalAssets", data, labels, "Total Assets")
    # plot_data("TotalLiabilities", data, labels, "Total Liabilities")
    # plot_data("Equity", data, labels, "Equity")
    # plot_data("NAVPS", data, labels, "NAVPS")
    # plot_data("TotalCapital", data, labels, "Total Capital")
    # plot_data("CoreTier1Capital", data, labels, "Core Tier 1 Capital")
    plot_data("CET1", data, labels, "CET1 CAR(%)")
    plot_data("Tier1CAR", data, labels, "Tier 1 CAR(%)")
    plot_data("CAR", data, labels, "Capital Adequacy Ratio(%)")

    # ----- deposit structure -----
    # plot_data("TotalDeposits", data, labels, "Total Deposits")
    plot_data("CorpDemandRatio", data, labels, "Corp Demand Deposit Ratio(%)")
    plot_data("CorpTimeRatio", data, labels, "Corp Time Deposit Ratio(%)")
    plot_data("RetailDemandRatio", data, labels, "Retail Demand Deposit Ratio(%)")
    plot_data("RetailTimeRatio", data, labels, "Retail Time Deposit Ratio(%)")

    # ----- loan structure -----
    # plot_data("GrossLoans", data, labels, "Gross Loans")
    # plot_data("NPL", data, labels, "NPL")
    plot_data("NPLRatio", data, labels, "NPL Ratio(%)")
    plot_data("ProvisionCoverage", data, labels, "Provision Coverage(%)")
    # plot_data("LoanLossReserve", data, labels, "Loan Loss Reserve")
    plot_data("NormalMigRate", data, labels, "Normal Mig Rate(%)")
    plot_data("SpecialMigRate", data, labels, "Special Mig Rate(%)")
    plot_data("SubstandardMigRate", data, labels, "Substandard Mig Rate(%)")
    plot_data("DoubtfulMigRate", data, labels, "Doubtful Mig Rate(%)")

    plt.show()

if __name__ == "__main__":
    main()
