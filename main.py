from data_extract import convert_excel_to_csv

# Convert the file and save the CSV
df_cmb = convert_excel_to_csv("600036_CMB/600036_CMB.xlsx", "600036_CMB/cmb_financials.csv")
df_cib = convert_excel_to_csv("601166_CIB/601166_CIB.xlsx", "601166_CIB/cib_financials.csv")
df_cncb = convert_excel_to_csv("601998_CNCB/601998_CNCB.xlsx", "601998_CNCB/cncb_financials.csv")

print(df_cmb)
print(df_cib)
print(df_cncb)

