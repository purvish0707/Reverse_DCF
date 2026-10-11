# Reverse DCF India Terminal (NSE & BSE Equities)

An institutional-grade **Reverse DCF (Discounted Cash Flow)** model and web terminal built specifically for the **Indian Stock Market (NSE & BSE listed companies)**, adhering strictly to Aswath Damodaran's valuation methodology and Indian accounting/regulatory standards:

1. **Standard Financial Units**: All financial line items (Market Cap, Net Debt, FCFF, Net Profit, Net Worth) are standardized strictly in **₹ Crore** ($1\text{ Crore} = 100\text{ Lakhs} = 10,000,000\text{ INR}$). Share counts are in **Crore shares**, ensuring that:
   $$\text{Share Price (₹)} = \frac{\text{Equity Value (₹ Crore)}}{\text{Shares (Crore shares)}}$$
2. **Non-Financial Corporates**: Uses **FCFF (Free Cash Flow to Firm)**, **Domestic Rating-Derived WACC (CRISIL/CARE/ICRA spreads)**, and an **Enterprise Value Bridge** ($\text{Net Debt} = \text{Total Debt} - \text{Cash}$).
3. **Financial Institutions (Banks, NBFCs, Insurance)**: Uses **Excess Return / Sustainable ROE** and **FCFE** discounted at the **Cost of Equity ($K_e$)**, recognizing that debt is raw operating inventory and capital retention is governed by RBI Tier-1 regulatory capital requirements.

---

## 🚀 1-Click NSE/BSE Live Data Extractor

Input **any Indian company name or ticker** (e.g. *"GNA Axles"*, *"Reliance"*, *"TCS"*, *"Tata Motors"*, *"L&T"*, *"HDFC Bank"*, *"ICICI Bank"*, *"SBI"*, *"Bajaj Finance"*):
* **Live Market Price (₹)**: Extracted in real time via live NSE/BSE feeds.
* **Diluted Shares (Cr shares)**: Converted to Crores.
* **Trailing / Normalized FCFF (₹ Cr)**: Clean cash flow calculation in ₹ Crore.
* **Rating-Derived WACC for India**:
  * **10-Year Benchmark Risk-Free Rate ($R_f$)**: **7.00%** (RBI / CCIL 10-Year Government of India G-Sec yield).
  * **Equity Risk Premium (ERP)**: **7.00%** (Damodaran India Total ERP: 5.0% mature market + 2.0% India sovereign country risk premium).
  * **Domestic Credit Rating Spread**: CRISIL, CARE, ICRA default spreads over G-Sec.
  * **Indian Statutory Tax Rate ($t$)**: **25.17%** (Corporate tax under Section 115BAA).
  * **Terminal Growth Rate ($g_{\text{term}}$)**: **5.00%** (Indian long-term sustainable nominal GDP ceiling).
* **Auto-Classification**: Automatically detects whether the Indian company is a **Bank/NBFC** or **Corporate**, and switches between the FCFF model and the Excess Return / ROE model.
* **Synchronized Excel Generation**: Dynamically outputs `Reverse_DCF_<TICKER>.xlsx` pre-filled with the company's metrics and live Excel Goal Seek formulas.

---

## 1. Web Terminal ([http://localhost:8080](http://localhost:8080))

The web terminal is served locally by `server.py`:
1. Open **[http://localhost:8080](http://localhost:8080)** in your browser.
2. In the top search bar, type any Indian company name (e.g. *"GNA Axles"*, *"Reliance"*, *"TCS"*, or *"HDFC Bank"*) or click any preset chip.
3. The terminal instantly:
   * Populates share price (₹), market cap (₹ Cr), net debt (₹ Cr), and cash flow (₹ Cr).
   * Calculates the rating-derived WACC and credit profile.
   * Solves the market-implied 10-year FCFF growth rate (or implied sustainable ROE for banks).
   * Renders the 10-year cash flow projection chart, 2D sensitivity heatmap, and reality check gauge calibrated against Indian nominal GDP (~10.5% - 11.5%).
4. Click **Download Excel Model (.xlsx)** to download that exact company's workbook.

---

## 2. CLI Tool (`fetch_company.py`)

Run from the command line to fetch data and generate dedicated workbooks directly:

```bash
# Fetch any Indian company by name or NSE/BSE ticker
python fetch_company.py "GNA Axles"
python fetch_company.py "Reliance"
python fetch_company.py "TCS"
python fetch_company.py "HDFC Bank"
python fetch_company.py "L&T"
```

This will print the extracted metrics in ₹ Crore and generate a tailored workbook:
`Reverse_DCF_<TICKER>.xlsx` and update `Reverse_DCF_Model.xlsx`.

---

## 3. How Goal Seek Works in Excel

### Non-Financial Corporates (Tab 1: `Non-Financial (FCFF in ₹ Cr)`)
* **Set Cell**: `C29` (Model Share Price in ₹)
* **To Value**: Current Market Price (e.g. `554.55`)
* **By Changing Cell**: `C20` (Implied FCFF CAGR %)
* **Shortcut**: <kbd>Alt</kbd> + <kbd>A</kbd> + <kbd>W</kbd> + <kbd>G</kbd>

### Financial Institutions (Tab 2: `Financials (ROE in ₹ Cr)`)
* **Set Cell**: `C30` (Model Share Price in ₹)
* **To Value**: Target Bank Share Price (e.g. `707.25`)
* **By Changing Cell**: `C21` (Implied Sustainable ROE %)
* **Shortcut**: <kbd>Alt</kbd> + <kbd>A</kbd> + <kbd>W</kbd> + <kbd>G</kbd>
