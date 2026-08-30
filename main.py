import numpy as np
import matplotlib.pyplot as plt

from data_extract import get_dataframe

def plot_data(data_name, datas, labels, title):
    fig, ax = plt.subplots()
    for i, data in enumerate(datas):
        ax.plot(data['Year'].values, data[data_name].values, label=labels[i], marker='o')
    ax.set_xlabel("years")
    ax.set_title(title)
    plt.legend()

# Convert the file and save the CSV
df_cmb = get_dataframe("600036_CMB/600036_CMB.xlsx", "600036_CMB/cmb_financials.csv")
df_cib = get_dataframe("601166_CIB/601166_CIB.xlsx", "601166_CIB/cib_financials.csv")
df_cncb = get_dataframe("601998_CNCB/601998_CNCB.xlsx", "601998_CNCB/cncb_financials.csv")

data = [df_cmb, df_cib, df_cncb]
labels = ["CMB", "CIB", "CNCB"]

plot_data('ROA', data, labels, 'ROA')
plot_data('NonIIRatio', data, labels, 'NonIIRatio')
plot_data('RORWA', data, labels, 'RORWA')
plot_data('TotalDeposits', data, labels, 'TotalDeposits')

fig, axes = plt.subplots(4, 1)
deposit_ratio_names = ['CorpDemandRatio', 'CorpTimeRatio', 'RetailDemandRatio', 'RetailTimeRatio']
for i, ax in enumerate(axes):
    for j, cur_data in enumerate(data):
        ax.plot(cur_data['Year'].values, cur_data[deposit_ratio_names[i]].values, label=labels[j], marker='o')
    ax.set_title(deposit_ratio_names[i])
    ax.legend()
plt.tight_layout()

plot_data('ProvisionCoverage', data, labels, 'ProvisionCoverage')
plot_data('NIS', data, labels, 'NIS')
plot_data('NIM', data, labels, 'NIM')

plt.show()


