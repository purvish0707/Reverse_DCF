"""
CLI Utility to fetch live NSE & BSE company data from yfinance and generate a customized Reverse DCF Excel model.
All units standardized strictly in ₹ Crore (1 Cr = 100 Lakhs = 10,000,000 INR).

Usage:
    python fetch_company.py "GNA Axles"
    python fetch_company.py "Reliance"
    python fetch_company.py "TCS"
    python fetch_company.py "HDFC Bank"
    python fetch_company.py "L&T"
"""

import sys
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

from data_fetcher import extract_company_data
from create_excel_model import create_reverse_dcf_workbook

def main():
    if len(sys.argv) < 2:
        query = input("Enter Indian company name or NSE/BSE ticker (e.g. GNA Axles, Reliance, TCS, HDFC Bank, L&T): ").strip()
    else:
        query = " ".join(sys.argv[1:]).strip()

    if not query:
        print("Error: No company name or ticker provided.")
        return

    print(f"\n[1/3] Searching and extracting live NSE/BSE market data for: '{query}'...")
    try:
        data = extract_company_data(query)
    except Exception as e:
        print(f"Error fetching data: {e}")
        return

    print(f"\n========================================================")
    print(f"  {data['name'].upper()} ({data['ticker']})")
    print(f"  Sector: {data['sector']} | Industry: {data['industry']}")
    print(f"  Units: All figures standardized in ₹ Crore")
    print(f"========================================================")
    print(f"  • Live Market Price:      ₹{data['price']:,.2f} per share")
    print(f"  • Shares Outstanding:     {data['shares_cr']:,.4f} Cr shares")
    print(f"  • Market Capitalization:  ₹{data['market_cap_cr']:,.2f} Cr")
    
    if data['is_financial']:
        print(f"  • Valuation Methodology:  Banking ROE / Excess Return Method")
        print(f"  • Trailing Net Profit:    ₹{data['net_income_cr']:,.2f} Cr")
        print(f"  • Book Value (Net Worth): ₹{data['book_value_cr']:,.2f} Cr")
        print(f"  • 10Y G-Sec Benchmark:    {data['rf']:.2f}%")
        print(f"  • Beta:                   {data['beta']:.2f}")
        print(f"  • Cost of Equity (Ke):    {data['cost_of_equity']:.2f}%")
    else:
        print(f"  • Valuation Methodology:  Non-Financial (FCFF & WACC)")
        print(f"  • Total Debt:             ₹{data['total_debt_cr']:,.2f} Cr")
        print(f"  • Cash & Equivalents:     ₹{data['cash_cr']:,.2f} Cr")
        print(f"  • Net Debt:               ₹{data['net_debt_cr']:,.2f} Cr")
        print(f"  • Trailing FCFF:          ₹{data['trailing_fcff_cr']:,.2f} Cr")
        print(f"  • 10Y G-Sec Benchmark:    {data['rf']:.2f}%")
        print(f"  • Beta:                   {data['beta']:.2f}")
        print(f"  • Domestic Credit Rating: {data['rating']} (Spread: +{data['rating_spread']:.2f}%)")
        print(f"  • Rating-Derived WACC:    {data['wacc']:.2f}% (Eq: {data['weight_equity']}%, Debt: {data['weight_debt']}%)")

    clean_ticker = data['ticker'].replace('/', '_')
    filename = f"Reverse_DCF_{clean_ticker}.xlsx"
    print(f"\n[2/3] Generating customized Indian Excel model: {filename}...")
    create_reverse_dcf_workbook(filename, data)
    # Also update master Reverse_DCF_Model.xlsx
    create_reverse_dcf_workbook("Reverse_DCF_Model.xlsx", data)

    print(f"[3/3] Done! Excel models generated successfully.")
    print(f"  -> {filename}")
    print(f"  -> Reverse_DCF_Model.xlsx")
    print(f"\nGoal Seek Setup in Excel:")
    if data['is_financial']:
        print(f"  Set cell: C30 (Model Price ₹) | To value: {data['price']} | By changing cell: C21 (Implied Sustainable ROE %)")
    else:
        print(f"  Set cell: C29 (Model Price ₹) | To value: {data['price']} | By changing cell: C20 (Implied FCFF CAGR %)")
    print(f"========================================================\n")

if __name__ == "__main__":
    main()
