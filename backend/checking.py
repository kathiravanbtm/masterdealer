import pandas as pd

data = {
    "id": [1, 2, 3, 4, 5],
    "gstin": ["22AAAAA0000A1Z5", "33BBBBB1111B2Z6", "44CCCCC2222C3Z7", "55DDDDD3333D4Z8", "66EEEEE4444E5Z9"],
    "trade_name": ["Alpha Traders", "Beta Enterprises", "Gamma Stores", "Delta Supplies", "Epsilon Goods"],
    "email": ["alpha@example.com", "beta@example.com", "gamma@example.com", "delta@example.com", "epsilon@example.com"],
    "mobile": ["9876543210", "8765432109", "7654321098", "6543210987", "5432109876"],
    "assigned_to": ["Officer1", "Officer2", "Officer1", "Officer3", "Officer2"],
    "reg_date": ["2020-01-01", "2019-05-10", "2021-07-15", "2018-03-20", "2022-11-30"],
    "suspension_date": [None, None, None, None, None],
    "taxpayer_type": ["Regular", "Composition", "Regular", "Regular", "Composition"],
    "constitution": ["Proprietorship", "Partnership", "LLP", "Private Ltd", "Public Ltd"],
    "is_migrated": [1, 0, 1, 1, 0],
    "jurisdiction": ["Jurisdiction1", "Jurisdiction2", "Jurisdiction1", "Jurisdiction3", "Jurisdiction2"],
    "hsn_code": ["1001", "1002", "1003", "1004", "1005"],
    "principal_address": ["Street 1", "Street 2", "Street 3", "Street 4", "Street 5"],
    "created_at": ["2020-01-01", "2019-05-10", "2021-07-15", "2018-03-20", "2022-11-30"],
    "updated_at": ["2023-01-01", "2023-02-10", "2023-03-15", "2023-04-20", "2023-05-30"],
}

df = pd.DataFrame(data)
df.to_excel("dealers_dummy_data.xlsx", index=False)
print("Excel file created: dealers_dummy_data.xlsx")
