import os
import sys
import csv

# Set UTF-8 encoding
sys.stdout.reconfigure(encoding='utf-8')

# Financial Data Extracted Directly from Official BSE Annual Reports
# Conversion: Original units are in `Rs. Lacs`.
# Converted units: `Rs. Crore` (1 Crore = 100 Lacs, so Value in Crore = Value in Lacs / 100)

data = {
    'FY26': {
        'doc': 'GNA_Axles_Annual_Report_2025-26.pdf',
        'p_pl': 134,
        'p_bs': 133,
        'p_cf': 135,
        'revenue_ops': 147841.83 / 100,
        'other_operating_income': 3397.30 / 100,
        'sale_of_products': 144444.53 / 100,
        'other_income': 299.00 / 100,
        'total_revenue': 148140.83 / 100,
        'cost_materials': 92494.87 / 100,
        'stock_changes': -2005.93 / 100,
        'employee_cost': 8720.58 / 100,
        'other_expenses': 24837.36 / 100,
        'ebitda': (147841.83 + 299.00 - (92494.87 - 2005.93 + 8720.58 + 24837.36)) / 100,
        'dna': 7003.82 / 100,
        'finance_cost_pl': 1325.30 / 100,
        'pbt': 15764.83 / 100,
        'tax_expense': 4069.74 / 100,
        'pat': 11695.09 / 100,
        'cfo': 21391.26 / 100,
        'purchase_ppe': 15815.42 / 100,
        'sale_ppe': 69.60 / 100,
        'net_capex': (15815.42 - 69.60) / 100,
        'interest_paid_cf': 1245.42 / 100,
        'tax_paid_cf': 4150.00 / 100,
        'inventories': 24774.06 / 100,
        'trade_rec': 61090.30 / 100,
        'trade_pay': (647.95 + 26583.43) / 100,
        'cash_and_bank': (51.44 + 3743.66) / 100,
        'borrowings_non_current': 9563.92 / 100,
        'borrowings_current': 8823.79 / 100,
        'total_debt': (9563.92 + 8823.79) / 100,
        'wc_inv_adj': -5409.83 / 100,
        'wc_rec_adj': -1940.30 / 100,
        'wc_pay_adj': 9155.60 / 100,
        'cf_wc_change': ((-5409.83) + (-1940.30) + 9155.60) / 100 # +18.05 Cr cash generated from WC
    },
    'FY25': {
        'doc': 'GNA_Axles_Annual_Report_2025-26.pdf',
        'p_pl': 134,
        'p_bs': 133,
        'p_cf': 135,
        'revenue_ops': 153974.07 / 100,
        'other_operating_income': 2732.92 / 100,
        'sale_of_products': 151241.15 / 100,
        'other_income': 261.05 / 100,
        'total_revenue': 154235.12 / 100,
        'cost_materials': 101747.79 / 100,
        'stock_changes': -904.40 / 100,
        'employee_cost': 7642.23 / 100,
        'other_expenses': 24429.24 / 100,
        'ebitda': (153974.07 + 261.05 - (101747.79 - 904.40 + 7642.23 + 24429.24)) / 100,
        'dna': 5710.03 / 100,
        'finance_cost_pl': 1186.13 / 100,
        'pbt': 14424.10 / 100,
        'tax_expense': 3714.61 / 100,
        'pat': 10709.49 / 100,
        'cfo': 9207.90 / 100,
        'purchase_ppe': 11091.07 / 100,
        'sale_ppe': 108.17 / 100,
        'net_capex': (11091.07 - 108.17) / 100,
        'interest_paid_cf': 1056.27 / 100,
        'tax_paid_cf': 3750.00 / 100,
        'inventories': 19364.23 / 100,
        'trade_rec': 63833.98 / 100,
        'trade_pay': (331.32 + 18062.61) / 100,
        'cash_and_bank': (752.18 + 2469.93) / 100,
        'borrowings_non_current': 10060.21 / 100,
        'borrowings_current': 14320.71 / 100,
        'total_debt': (10060.21 + 14320.71) / 100,
        'wc_inv_adj': 395.93 / 100,
        'wc_rec_adj': -8637.17 / 100,
        'wc_pay_adj': 280.41 / 100,
        'cf_wc_change': (395.93 + (-8637.17) + 280.41) / 100 # -79.61 Cr cash tied up in WC
    },
    'FY24': {
        'doc': 'GNA_Axles_Annual_Report_2023-24.pdf',
        'p_pl': 132,
        'p_bs': 131,
        'p_cf': 133,
        'revenue_ops': 150626.18 / 100,
        'other_operating_income': 1572.30 / 100,
        'sale_of_products': 149053.88 / 100,
        'other_income': 240.39 / 100,
        'total_revenue': 150866.57 / 100,
        'cost_materials': 101121.06 / 100,
        'stock_changes': -1240.55 / 100,
        'employee_cost': 7089.73 / 100,
        'other_expenses': 23929.05 / 100,
        'ebitda': (150626.18 + 240.39 - (101121.06 - 1240.55 + 7089.73 + 23929.05)) / 100,
        'dna': 5333.71 / 100,
        'finance_cost_pl': 1154.90 / 100,
        'pbt': 13478.67 / 100,
        'tax_expense': 3482.27 / 100,
        'pat': 9996.40 / 100,
        'cfo': 9840.94 / 100,
        'purchase_ppe': 8867.66 / 100,
        'sale_ppe': 16.88 / 100,
        'net_capex': (8867.66 - 16.88) / 100,
        'interest_paid_cf': 1021.89 / 100,
        'tax_paid_cf': 3560.00 / 100,
        'inventories': 19760.16 / 100,
        'trade_rec': 57127.19 / 100,
        'trade_pay': (893.56 + 17261.29) / 100,
        'cash_and_bank': (25.35 + 3233.93) / 100,
        'borrowings_non_current': 2911.95 / 100,
        'borrowings_current': 16005.14 / 100,
        'total_debt': (2911.95 + 16005.14) / 100,
        'wc_inv_adj': -935.28 / 100,
        'wc_rec_adj': -329.20 / 100,
        'wc_pay_adj': -4919.68 / 100,
        'cf_wc_change': ((-935.28) + (-329.20) + (-4919.68)) / 100 # -61.84 Cr
    },
    'FY23': {
        'doc': 'GNA_Axles_Annual_Report_2023-24.pdf',
        'p_pl': 132,
        'p_bs': 131,
        'p_cf': 133,
        'revenue_ops': 158293.37 / 100,
        'other_operating_income': 2336.06 / 100,
        'sale_of_products': 155957.31 / 100,
        'other_income': 142.58 / 100,
        'total_revenue': 158435.95 / 100,
        'cost_materials': 105476.25 / 100,
        'stock_changes': -472.78 / 100,
        'employee_cost': 6637.10 / 100,
        'other_expenses': 23385.35 / 100,
        'ebitda': (158293.37 + 142.58 - (105476.25 - 472.78 + 6637.10 + 23385.35)) / 100,
        'dna': 4851.25 / 100,
        'finance_cost_pl': 1096.93 / 100,
        'pbt': 17461.85 / 100,
        'tax_expense': 4441.06 / 100,
        'pat': 13020.79 / 100,
        'cfo': 10542.56 / 100,
        'purchase_ppe': 7544.27 / 100,
        'sale_ppe': 15.00 / 100,
        'net_capex': (7544.27 - 15.00) / 100,
        'interest_paid_cf': 950.73 / 100,
        'tax_paid_cf': 4600.00 / 100,
        'inventories': 18824.88 / 100,
        'trade_rec': 56093.74 / 100,
        'trade_pay': (325.21 + 22222.85) / 100,
        'cash_and_bank': (33.34 + 2688.38) / 100,
        'borrowings_non_current': 3005.60 / 100,
        'borrowings_current': 15592.38 / 100,
        'total_debt': (3005.60 + 15592.38) / 100,
        'wc_inv_adj': -24.31 / 100,
        'wc_rec_adj': -10742.14 / 100,
        'wc_pay_adj': 2798.10 / 100,
        'cf_wc_change': ((-24.31) + (-10742.14) + 2798.10) / 100 # -79.68 Cr
    },
    'FY22': {
        'doc': 'GNA_Axles_Annual_Report_2021-22.pdf',
        'p_pl': 109,
        'p_bs': 108,
        'p_cf': 110,
        'revenue_ops': 127047.36 / 100,
        'other_operating_income': 2768.70 / 100,
        'sale_of_products': 124278.66 / 100,
        'other_income': 55.56 / 100,
        'total_revenue': 127102.92 / 100,
        'cost_materials': 86834.25 / 100,
        'stock_changes': -3582.58 / 100,
        'employee_cost': 5856.10 / 100,
        'other_expenses': 19845.14 / 100,
        'ebitda': (127047.36 + 55.56 - (86834.25 - 3582.58 + 5856.10 + 19845.14)) / 100,
        'dna': 4970.90 / 100,
        'finance_cost_pl': 1123.11 / 100,
        'pbt': 12056.00 / 100,
        'tax_expense': 3179.95 / 100,
        'pat': 8876.05 / 100,
        'cfo': 4137.52 / 100,
        'purchase_ppe': 4556.66 / 100,
        'sale_ppe': 2.10 / 100,
        'net_capex': (4556.66 - 2.10) / 100,
        'interest_paid_cf': 972.85 / 100,
        'tax_paid_cf': 3300.00 / 100,
        'inventories': 18800.58 / 100,
        'trade_rec': 47427.92 / 100,
        'trade_pay': (343.83 + 19818.14) / 100,
        'cash_and_bank': (25.56 + 462.40) / 100,
        'borrowings_non_current': 4728.83 / 100,
        'borrowings_current': 15985.93 / 100,
        'total_debt': (4728.83 + 15985.93) / 100,
        'wc_inv_adj': -3536.05 / 100,
        'wc_rec_adj': -5077.48 / 100,
        'wc_pay_adj': -1980.75 / 100,
        'cf_wc_change': ((-3536.05) + (-5077.48) + (-1980.75)) / 100 # -105.94 Cr
    }
}

# Create Data Register CSV
register_rows = []
header = ['item', 'value', 'unit', 'fiscal year/date', 'source document', 'page or table/section', 'exact line item label', 'status']

for yr, d in data.items():
    doc_name = d['doc']
    p_pl = d['p_pl']
    p_bs = d['p_bs']
    p_cf = d['p_cf']
    
    # Revenue
    register_rows.append(['Revenue from Operations', f"{d['revenue_ops']:.2f}", 'Rs. Crore', yr, doc_name, f"Page {p_pl}, Statement of Profit and Loss", "Revenue from Operations / Total Income from Operations", "EXTRACTED"])
    register_rows.append(['Other Income', f"{d['other_income']:.2f}", 'Rs. Crore', yr, doc_name, f"Page {p_pl}, Statement of Profit and Loss", "Other Income", "EXTRACTED"])
    register_rows.append(['Operating EBITDA', f"{d['ebitda']:.2f}", 'Rs. Crore', yr, doc_name, f"Page {p_pl}, P&L Derived", "Revenue - Operating Expenses (excl D&A, Finance Cost)", "DERIVED"])
    register_rows.append(['Depreciation & Amortisation', f"{d['dna']:.2f}", 'Rs. Crore', yr, doc_name, f"Page {p_pl}, Statement of Profit and Loss", "Depreciation, Impairment and Amortisation Expenses", "EXTRACTED"])
    register_rows.append(['Finance Cost (P&L)', f"{d['finance_cost_pl']:.2f}", 'Rs. Crore', yr, doc_name, f"Page {p_pl}, Statement of Profit and Loss", "Financial Costs", "EXTRACTED"])
    register_rows.append(['Profit Before Tax (PBT)', f"{d['pbt']:.2f}", 'Rs. Crore', yr, doc_name, f"Page {p_pl}, Statement of Profit and Loss", "Profit from continuing operations before Tax", "EXTRACTED"])
    
    ebit_val = d['pbt'] + d['finance_cost_pl']
    register_rows.append(['EBIT (PBT + Finance Cost)', f"{ebit_val:.2f}", 'Rs. Crore', yr, doc_name, f"Page {p_pl}, P&L Derived", "PBT + Financial Costs", "DERIVED"])
    register_rows.append(['Tax Expense', f"{d['tax_expense']:.2f}", 'Rs. Crore', yr, doc_name, f"Page {p_pl}, Statement of Profit and Loss", "Tax Expense (Current & Deferred Tax)", "EXTRACTED"])
    
    t_rate = d['tax_expense'] / d['pbt']
    register_rows.append(['Effective Tax Rate (t)', f"{t_rate*100:.2f}%", 'Percentage', yr, doc_name, f"Page {p_pl}, Derived", "Tax Expense / PBT", "DERIVED"])
    register_rows.append(['Profit After Tax (PAT)', f"{d['pat']:.2f}", 'Rs. Crore', yr, doc_name, f"Page {p_pl}, Statement of Profit and Loss", "Profit for the year", "EXTRACTED"])
    
    # Cash Flow
    register_rows.append(['Cash Flow from Operations (CFO)', f"{d['cfo']:.2f}", 'Rs. Crore', yr, doc_name, f"Page {p_cf}, Cash Flow Statement", "Net cash from operating activities", "EXTRACTED"])
    register_rows.append(['Purchase of PPE / Fixed Assets', f"{d['purchase_ppe']:.2f}", 'Rs. Crore', yr, doc_name, f"Page {p_cf}, Cash Flow Statement", "Increase in Fixed assets/Capital Work in Progress / Purchase of Fixed assets", "EXTRACTED"])
    register_rows.append(['Sale Proceeds of Fixed Assets', f"{d['sale_ppe']:.2f}", 'Rs. Crore', yr, doc_name, f"Page {p_cf}, Cash Flow Statement", "Sale of fixed assets", "EXTRACTED"])
    register_rows.append(['Net Capex', f"{d['net_capex']:.2f}", 'Rs. Crore', yr, doc_name, f"Page {p_cf}, Derived", "Purchase of Fixed Assets - Sale of Fixed Assets", "DERIVED"])
    register_rows.append(['Interest Paid (Cash Flow)', f"{d['interest_paid_cf']:.2f}", 'Rs. Crore', yr, doc_name, f"Page {p_cf}, Cash Flow Statement", "Interest paid", "EXTRACTED"])
    register_rows.append(['Income Tax Paid (Cash Flow)', f"{d['tax_paid_cf']:.2f}", 'Rs. Crore', yr, doc_name, f"Page {p_cf}, Cash Flow Statement", "Income Tax Paid", "EXTRACTED"])
    
    # Balance Sheet
    register_rows.append(['Inventories', f"{d['inventories']:.2f}", 'Rs. Crore', yr, doc_name, f"Page {p_bs}, Balance Sheet", "Inventories", "EXTRACTED"])
    register_rows.append(['Trade Receivables', f"{d['trade_rec']:.2f}", 'Rs. Crore', yr, doc_name, f"Page {p_bs}, Balance Sheet", "Trade Receivables", "EXTRACTED"])
    register_rows.append(['Trade Payables', f"{d['trade_pay']:.2f}", 'Rs. Crore', yr, doc_name, f"Page {p_bs}, Balance Sheet", "Trade Payable (Micro & Small + Other)", "EXTRACTED"])
    register_rows.append(['Cash & Bank Balances', f"{d['cash_and_bank']:.2f}", 'Rs. Crore', yr, doc_name, f"Page {p_bs}, Balance Sheet", "Cash & Cash Equivalents + Other Bank Balances", "EXTRACTED"])
    register_rows.append(['Total Borrowings (Debt)', f"{d['total_debt']:.2f}", 'Rs. Crore', yr, doc_name, f"Page {p_bs}, Balance Sheet", "Non-Current Borrowings + Current Borrowings", "EXTRACTED"])
    
    # FCFF calculations
    # Method (a): CFO + Finance Cost * (1 - t) - Net Capex
    fcff_a = d['cfo'] + (d['finance_cost_pl'] * (1 - t_rate)) - d['net_capex']
    # Method (b): EBIT * (1 - t) + D&A - Net Capex - delta NWC
    # NWC change: note that in CF statement, positive CF adjustment means decrease in NWC (source of cash)
    delta_nwc = -d['cf_wc_change'] # increase in NWC is cash outflow
    fcff_b = (ebit_val * (1 - t_rate)) + d['dna'] - d['net_capex'] - delta_nwc
    
    register_rows.append(['FCFF Method (a)', f"{fcff_a:.2f}", 'Rs. Crore', yr, doc_name, "Derived via Method (a)", "CFO + Finance Cost*(1-t) - Net Capex", "DERIVED"])
    register_rows.append(['FCFF Method (b)', f"{fcff_b:.2f}", 'Rs. Crore', yr, doc_name, "Derived via Method (b)", "EBIT*(1-t) + D&A - Net Capex - Change in NWC", "DERIVED"])

# Write to data_register.csv
with open('data_register.csv', 'w', newline='', encoding='utf-8') as f:
    writer = csv.writer(f)
    writer.writerow(header)
    writer.writerows(register_rows)

print(f"data_register.csv created successfully with {len(register_rows)} logged items.")

# Print Summary Table
print("\n" + "="*125)
print("  GNA AXLES LIMITED: HISTORICAL 5-YEAR FINANCIALS & TWO-WAY FCFF RECONCILIATION (Rs. Crore)")
print("="*125)

metrics = [
    ('Revenue from Operations', lambda d: d['revenue_ops']),
    ('Other Operating Income', lambda d: d['other_operating_income']),
    ('Other Income', lambda d: d['other_income']),
    ('Operating EBITDA', lambda d: d['ebitda']),
    ('EBITDA Margin (%)', lambda d: (d['ebitda'] / d['revenue_ops']) * 100),
    ('Depreciation & Amortisation (D&A)', lambda d: d['dna']),
    ('Finance Costs (P&L)', lambda d: d['finance_cost_pl']),
    ('Profit Before Tax (PBT)', lambda d: d['pbt']),
    ('EBIT (PBT + Finance Cost)', lambda d: d['pbt'] + d['finance_cost_pl']),
    ('EBIT Margin (%)', lambda d: ((d['pbt'] + d['finance_cost_pl']) / d['revenue_ops']) * 100),
    ('Tax Expense (P&L)', lambda d: d['tax_expense']),
    ('Effective Tax Rate (%)', lambda d: (d['tax_expense'] / d['pbt']) * 100),
    ('Profit After Tax (PAT)', lambda d: d['pat']),
    ('PAT Margin (%)', lambda d: (d['pat'] / d['revenue_ops']) * 100),
    ('--- CASH FLOWS ---', None),
    ('Cash Flow from Operations (CFO)', lambda d: d['cfo']),
    ('Net Capex (Purchase - Sale of PPE)', lambda d: d['net_capex']),
    ('Capex as % of Revenue', lambda d: (d['net_capex'] / d['revenue_ops']) * 100),
    ('Working Capital Impact in CFO', lambda d: d['cf_wc_change']),
    ('--- FCFF METHOD (a) ---', None),
    ('CFO', lambda d: d['cfo']),
    ('Add: After-tax Finance Cost [I*(1-t)]', lambda d: d['finance_cost_pl'] * (1 - (d['tax_expense'] / d['pbt']))),
    ('Less: Net Capex', lambda d: -d['net_capex']),
    ('FCFF - Method (a) [CFO + I*(1-t) - Capex]', lambda d: d['cfo'] + (d['finance_cost_pl'] * (1 - (d['tax_expense'] / d['pbt']))) - d['net_capex']),
    ('--- FCFF METHOD (b) ---', None),
    ('NOPAT [EBIT * (1 - t)]', lambda d: (d['pbt'] + d['finance_cost_pl']) * (1 - (d['tax_expense'] / d['pbt']))),
    ('Add: Depreciation & Amortisation', lambda d: d['dna']),
    ('Less: Net Capex', lambda d: -d['net_capex']),
    ('Less: Change in Non-Cash WC (-Delta NWC)', lambda d: d['cf_wc_change']),
    ('FCFF - Method (b) [NOPAT + D&A - Capex - dNWC]', lambda d: ((d['pbt'] + d['finance_cost_pl']) * (1 - (d['tax_expense'] / d['pbt']))) + d['dna'] - d['net_capex'] + d['cf_wc_change']),
    ('--- RECONCILIATION GAP ---', None),
    ('Variance Gap: Method (a) - Method (b)', lambda d: (d['cfo'] + (d['finance_cost_pl'] * (1 - (d['tax_expense'] / d['pbt']))) - d['net_capex']) - (((d['pbt'] + d['finance_cost_pl']) * (1 - (d['tax_expense'] / d['pbt']))) + d['dna'] - d['net_capex'] + d['cf_wc_change']))
]

header_str = f"{'Financial Metric':<45} | {'FY22':>12} | {'FY23':>12} | {'FY24':>12} | {'FY25':>12} | {'FY26':>12}"
print(header_str)
print("-" * len(header_str))

for label, fn in metrics:
    if fn is None:
        print(f" {label}")
        continue
    row_vals = []
    for yr in ['FY22', 'FY23', 'FY24', 'FY25', 'FY26']:
        val = fn(data[yr])
        if '%' in label:
            row_vals.append(f"{val:>11.2f}%")
        else:
            row_vals.append(f"{val:>12.2f}")
    print(f"{label:<45} | " + " | ".join(row_vals))

print("="*125)
