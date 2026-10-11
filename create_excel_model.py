import xlsxwriter

def create_reverse_dcf_workbook(filename="Reverse_DCF_Model.xlsx", company_data=None):
    wb = xlsxwriter.Workbook(filename)
    
    currency_sym = "₹"
    
    # Institutional Dark Navy & Emerald Palette
    header_fmt = wb.add_format({
        'bold': True, 'font_size': 13, 'font_name': 'Calibri',
        'font_color': '#FFFFFF', 'bg_color': '#0F172A',
        'align': 'left', 'valign': 'vcenter', 'indent': 1
    })
    
    subhead_fmt = wb.add_format({
        'bold': True, 'font_size': 10, 'font_name': 'Calibri',
        'font_color': '#0F172A', 'bg_color': '#E2E8F0',
        'align': 'left', 'valign': 'vcenter', 'indent': 1
    })
    
    sec_title_fmt = wb.add_format({
        'bold': True, 'font_size': 10, 'font_name': 'Calibri',
        'font_color': '#1E3A8A', 'bg_color': '#DBEAFE',
        'top': 1, 'bottom': 1, 'top_color': '#93C5FD', 'bottom_color': '#93C5FD'
    })
    
    tbl_header = wb.add_format({
        'bold': True, 'font_size': 9, 'font_name': 'Calibri',
        'font_color': '#FFFFFF', 'bg_color': '#334155',
        'align': 'center', 'valign': 'vcenter', 'border': 1, 'border_color': '#64748B'
    })
    
    label_fmt = wb.add_format({'font_name': 'Calibri', 'font_size': 10, 'valign': 'vcenter'})
    label_bold = wb.add_format({'font_name': 'Calibri', 'font_size': 10, 'bold': True, 'valign': 'vcenter'})
    
    curr_fmt_str = f'[$₹-439] #,##0.00'
    cr_fmt_str = f'#,##0.00'
    
    input_price = wb.add_format({
        'font_name': 'Calibri', 'font_size': 10, 'font_color': '#002060', 'bg_color': '#F8FAFC',
        'border': 1, 'border_color': '#CBD5E1', 'num_format': curr_fmt_str, 'align': 'right'
    })
    input_cr = wb.add_format({
        'font_name': 'Calibri', 'font_size': 10, 'font_color': '#002060', 'bg_color': '#F8FAFC',
        'border': 1, 'border_color': '#CBD5E1', 'num_format': cr_fmt_str, 'align': 'right'
    })
    input_shares = wb.add_format({
        'font_name': 'Calibri', 'font_size': 10, 'font_color': '#002060', 'bg_color': '#F8FAFC',
        'border': 1, 'border_color': '#CBD5E1', 'num_format': '#,##0.0000', 'align': 'right'
    })
    input_pct = wb.add_format({
        'font_name': 'Calibri', 'font_size': 10, 'font_color': '#002060', 'bg_color': '#F8FAFC',
        'border': 1, 'border_color': '#CBD5E1', 'num_format': '0.00%', 'align': 'right'
    })
    
    goal_seek_var_pct = wb.add_format({
        'font_name': 'Calibri', 'font_size': 11, 'bold': True, 'font_color': '#7C2D12', 'bg_color': '#FEF3C7',
        'border': 2, 'border_color': '#F59E0B', 'num_format': '0.00%', 'align': 'right'
    })
    
    calc_cr = wb.add_format({
        'font_name': 'Calibri', 'font_size': 10, 'font_color': '#000000',
        'border': 1, 'border_color': '#E2E8F0', 'num_format': cr_fmt_str, 'align': 'right'
    })
    calc_factor = wb.add_format({
        'font_name': 'Calibri', 'font_size': 10, 'font_color': '#000000',
        'border': 1, 'border_color': '#E2E8F0', 'num_format': '0.0000', 'align': 'right'
    })
    
    summary_highlight = wb.add_format({
        'font_name': 'Calibri', 'font_size': 11, 'bold': True, 'font_color': '#0F172A', 'bg_color': '#DCFCE7',
        'border': 2, 'border_color': '#22C55E', 'num_format': curr_fmt_str, 'align': 'right'
    })
    diff_highlight = wb.add_format({
        'font_name': 'Calibri', 'font_size': 11, 'bold': True, 'font_color': '#0F172A', 'bg_color': '#F1F5F9',
        'border': 2, 'border_color': '#94A3B8', 'num_format': curr_fmt_str, 'align': 'right'
    })
    
    note_box_title = wb.add_format({
        'font_name': 'Calibri', 'font_size': 10, 'bold': True, 'font_color': '#92400E', 'bg_color': '#FEF3C7',
        'top': 1, 'left': 1, 'right': 1, 'border_color': '#F59E0B'
    })
    note_box_body = wb.add_format({
        'font_name': 'Calibri', 'font_size': 9, 'font_color': '#78350F', 'bg_color': '#FFFBEB',
        'left': 1, 'right': 1, 'bottom': 1, 'border_color': '#F59E0B', 'text_wrap': True, 'valign': 'top'
    })

    # Default Indian Non-Financial Data (GNA Axles Ltd)
    nf = {
        'ticker': 'GNA.NS', 'name': 'GNA Axles Ltd',
        'price': 554.55, 'shares_cr': 4.2931, 'total_debt_cr': 183.88,
        'cash_cr': 37.95, 'trailing_fcff_cr': 59.19, 'wacc': 10.59, 'term_g': 5.0,
        'rating': 'CRISIL / CARE AA-'
    }
    
    # Default Indian Financial Data (HDFC Bank Ltd)
    fin = {
        'ticker': 'HDFCBANK.NS', 'name': 'HDFC Bank Limited',
        'price': 707.25, 'shares_cr': 1541.8479, 'book_value_cr': 607199.76,
        'net_income_cr': 79012.77, 'cost_of_equity': 11.50, 'retention_ratio': 40.0,
        'term_g': 5.0
    }

    # Override with live company data if provided
    is_fin = False
    if company_data:
        is_fin = bool(company_data.get('is_financial'))
        if is_fin:
            fin.update({
                'ticker': company_data.get('ticker', fin['ticker']),
                'name': company_data.get('name', fin['name']),
                'price': company_data.get('price', fin['price']),
                'shares_cr': company_data.get('shares_cr', company_data.get('shares_m', 0) / 10.0 if 'shares_m' in company_data else fin['shares_cr']),
                'book_value_cr': company_data.get('book_value_cr', company_data.get('book_value_m', 0) / 10.0 if 'book_value_m' in company_data else fin['book_value_cr']),
                'net_income_cr': company_data.get('net_income_cr', company_data.get('net_income_m', 0) / 10.0 if 'net_income_m' in company_data else fin['net_income_cr']),
                'cost_of_equity': company_data.get('cost_of_equity', fin['cost_of_equity']),
                'term_g': company_data.get('term_g', fin['term_g'])
            })
        else:
            nf.update({
                'ticker': company_data.get('ticker', nf['ticker']),
                'name': company_data.get('name', nf['name']),
                'price': company_data.get('price', nf['price']),
                'shares_cr': company_data.get('shares_cr', company_data.get('shares_m', 0) / 10.0 if 'shares_m' in company_data else nf['shares_cr']),
                'total_debt_cr': company_data.get('total_debt_cr', company_data.get('total_debt_m', 0) / 10.0 if 'total_debt_m' in company_data else nf['total_debt_cr']),
                'cash_cr': company_data.get('cash_cr', company_data.get('cash_m', 0) / 10.0 if 'cash_m' in company_data else nf['cash_cr']),
                'trailing_fcff_cr': company_data.get('trailing_fcff_cr', company_data.get('trailing_fcff_m', 0) / 10.0 if 'trailing_fcff_m' in company_data else nf['trailing_fcff_cr']),
                'wacc': company_data.get('wacc', nf['wacc']),
                'term_g': company_data.get('term_g', nf['term_g']),
                'rating': company_data.get('rating', nf['rating'])
            })

    # -------------------------------------------------------------
    # TAB 1: Non-Financial FCFF Model (All figures in ₹ Crore)
    # -------------------------------------------------------------
    ws1 = wb.add_worksheet("Non-Financial (FCFF in ₹ Cr)")
    ws1.set_tab_color('#2563EB')
    ws1.hide_gridlines(0)
    
    ws1.set_column('A:A', 3)
    ws1.set_column('B:B', 40)
    ws1.set_column('C:C', 18)
    ws1.set_column('D:D', 4)
    ws1.set_column('E:N', 13)
    
    ws1.merge_range('B2:N2', f"NSE/BSE REVERSE DCF: {nf['name'].upper()} ({nf['ticker']}) - FCFF METHOD", header_fmt)
    ws1.merge_range('B3:N3', f"Indian Corporate Valuation • Rating: {nf['rating']} • Base FCFF: ₹{nf['trailing_fcff_cr']:,.2f} Cr • Units: ₹ Crore", subhead_fmt)
    ws1.set_row(1, 32)
    ws1.set_row(2, 20)
    
    ws1.merge_range('B5:C5', "1. MARKET & CAPITAL STRUCTURE (₹ Cr)", sec_title_fmt)
    ws1.write('B6', "Current Market Share Price (₹)", label_bold)
    ws1.write('C6', nf['price'], input_price)
    
    ws1.write('B7', "Diluted Shares Outstanding (Cr shares)", label_bold)
    ws1.write('C7', nf['shares_cr'], input_shares)
    
    ws1.write('B8', "Current Market Capitalization (₹ Cr)", label_fmt)
    ws1.write_formula('C8', '=C6*C7', calc_cr)
    
    ws1.write('B9', "Total Debt / Borrowings (₹ Cr)", label_fmt)
    ws1.write('C9', nf['total_debt_cr'], input_cr)
    
    ws1.write('B10', "Less: Cash & Liquid Balances (₹ Cr)", label_fmt)
    ws1.write('C10', nf['cash_cr'], input_cr)
    
    ws1.write('B11', "Net Debt (₹ Cr)", label_bold)
    ws1.write_formula('C11', '=C9-C10', calc_cr)
    
    ws1.write('B12', "Current Enterprise Value (₹ Cr)", label_bold)
    ws1.write_formula('C12', '=C8+C11', calc_cr)
    
    ws1.merge_range('B14:C14', "2. VALUATION PARAMETERS", sec_title_fmt)
    ws1.write('B15', "Discount Rate (Rating-Derived WACC)", label_bold)
    ws1.write('C15', nf['wacc'] / 100.0, input_pct)
    
    ws1.write('B16', "Terminal Growth Rate (g)", label_bold)
    ws1.write('C16', nf['term_g'] / 100.0, input_pct)
    
    ws1.write('B17', "Normalized Base Year FCFF (₹ Cr)", label_bold)
    ws1.write('C17', nf['trailing_fcff_cr'], input_cr)
    
    ws1.merge_range('B19:C19', "3. GOAL SEEK VARIABLE (IMPLIED GROWTH)", sec_title_fmt)
    ws1.write('B20', "Implied 10-Yr FCFF CAGR (%) [CHANGING CELL]", label_bold)
    ws1.write('C20', 0.1600, goal_seek_var_pct)
    
    ws1.merge_range('B22:C22', "4. VALUATION RECONCILIATION", sec_title_fmt)
    ws1.write('B23', "PV of 10-Year Discrete Cash Flows (₹ Cr)", label_fmt)
    ws1.write_formula('C23', '=SUM(E9:N9)', calc_cr)
    
    ws1.write('B24', "Terminal Value at Year 10 (₹ Cr)", label_fmt)
    ws1.write_formula('C24', '=N7*(1+C16)/(C15-C16)', calc_cr)
    
    ws1.write('B25', "PV of Terminal Value (₹ Cr)", label_fmt)
    ws1.write_formula('C25', '=C24/(1+C15)^10', calc_cr)
    
    ws1.write('B26', "Model Enterprise Value (₹ Cr)", label_bold)
    ws1.write_formula('C26', '=C23+C25', calc_cr)
    
    ws1.write('B27', "Less: Net Debt (₹ Cr)", label_fmt)
    ws1.write_formula('C27', '=C11', calc_cr)
    
    ws1.write('B28', "Model Equity Value (₹ Cr)", label_bold)
    ws1.write_formula('C28', '=C26-C27', calc_cr)
    
    ws1.write('B29', "Model Share Price (₹) [TARGET CELL]", label_bold)
    ws1.write_formula('C29', '=C28/C7', summary_highlight)
    
    ws1.write('B30', "Variance vs Market Price (₹)", label_bold)
    ws1.write_formula('C30', '=C29-C6', diff_highlight)
    
    headers = ["Yr 1", "Yr 2", "Yr 3", "Yr 4", "Yr 5", "Yr 6", "Yr 7", "Yr 8", "Yr 9", "Yr 10"]
    for idx, yr in enumerate(headers):
        col_letter = chr(ord('E') + idx)
        ws1.write(f"{col_letter}5", yr, tbl_header)
        
    ws1.write('D6', "Year", tbl_header)
    ws1.write('D7', "FCFF (₹ Cr)", tbl_header)
    ws1.write('D8', "Discount Factor", tbl_header)
    ws1.write('D9', "PV of FCFF (₹ Cr)", tbl_header)
    
    for idx in range(10):
        col_letter = chr(ord('E') + idx)
        t = idx + 1
        ws1.write(f"{col_letter}6", t, calc_cr)
        ws1.write_formula(f"{col_letter}7", f'=C17*(1+C20)^{t}', calc_cr)
        ws1.write_formula(f"{col_letter}8", f'=1/(1+$C$15)^{t}', calc_factor)
        ws1.write_formula(f"{col_letter}9", f'={col_letter}7*{col_letter}8', calc_cr)
        
    ws1.merge_range('E12:N12', f"📌 EXCEL GOAL SEEK INSTRUCTIONS FOR {nf['ticker']}", note_box_title)
    instructions_text = (
        "1. Open Goal Seek: Press Alt + A + W + G (Data tab > What-If Analysis > Goal Seek).\n"
        f"2. Set cell: C29  (Model Share Price in ₹)\n"
        f"   To value: {nf['price']}  (Current Market Price)\n"
        "   By changing cell: C20  (Implied FCFF CAGR %)\n"
        "3. Click OK to instantly solve the market-implied growth rate!"
    )
    ws1.merge_range('E13:N18', instructions_text, note_box_body)

    # -------------------------------------------------------------
    # TAB 2: Financials (FCFE & Excess Return Model in ₹ Cr)
    # -------------------------------------------------------------
    ws2 = wb.add_worksheet("Financials (ROE in ₹ Cr)")
    ws2.set_tab_color('#059669')
    ws2.hide_gridlines(0)
    
    ws2.set_column('A:A', 3)
    ws2.set_column('B:B', 40)
    ws2.set_column('C:C', 18)
    ws2.set_column('D:D', 4)
    ws2.set_column('E:N', 13)
    
    ws2.merge_range('B2:N2', f"NSE/BSE REVERSE DCF: {fin['name'].upper()} ({fin['ticker']}) - BANK ROE METHOD", header_fmt)
    ws2.merge_range('B3:N3', f"Indian Banking & NBFC Valuation • Trailing Net Income: ₹{fin['net_income_cr']:,.2f} Cr • Cost of Equity: {fin['cost_of_equity']:.2f}%", subhead_fmt)
    ws2.set_row(1, 32)
    ws2.set_row(2, 20)
    
    ws2.merge_range('B5:C5', "1. BANK / FINANCIAL PROFILE (₹ Cr)", sec_title_fmt)
    ws2.write('B6', "Current Share Price (₹)", label_bold)
    ws2.write('C6', fin['price'], input_price)
    
    ws2.write('B7', "Diluted Shares Outstanding (Cr shares)", label_bold)
    ws2.write('C7', fin['shares_cr'], input_shares)
    
    ws2.write('B8', "Market Capitalization (₹ Cr)", label_fmt)
    ws2.write_formula('C8', '=C6*C7', calc_cr)
    
    ws2.write('B9', "Current Net Worth / Book Value (₹ Cr)", label_bold)
    ws2.write('C9', fin['book_value_cr'], input_cr)
    
    ws2.write('B10', "Current Price-to-Book (P/B Multiple)", label_fmt)
    ws2.write_formula('C10', '=C8/C9', calc_factor)
    
    ws2.write('B11', "Trailing Net Income / PAT (₹ Cr)", label_bold)
    ws2.write('C11', fin['net_income_cr'], input_cr)
    
    ws2.write('B12', "Current ROE (PAT / Net Worth)", label_fmt)
    ws2.write_formula('C12', '=C11/C9', input_pct)
    
    ws2.merge_range('B14:C14', "2. VALUATION PARAMETERS", sec_title_fmt)
    ws2.write('B15', "Cost of Equity (Ke) [NOT WACC]", label_bold)
    ws2.write('C15', fin['cost_of_equity'] / 100.0, input_pct)
    
    ws2.write('B16', "Terminal Growth Rate (g)", label_bold)
    ws2.write('C16', fin['term_g'] / 100.0, input_pct)
    
    ws2.write('B17', "Capital Retention Ratio (b)", label_fmt)
    ws2.write('C17', fin['retention_ratio'] / 100.0, input_pct)
    
    ws2.write('B18', "Base Year FCFE (₹ Cr) [PAT*(1-b)]", label_bold)
    ws2.write_formula('C18', '=C11*(1-C17)', calc_cr)
    
    ws2.merge_range('B20:C20', "3. GOAL SEEK VARIABLE", sec_title_fmt)
    ws2.write('B21', "Implied Sustainable ROE (%) [VARIABLE A]", label_bold)
    ws2.write('C21', 0.1650, goal_seek_var_pct)
    
    ws2.write('B22', "Implied FCFE CAGR (%) [VARIABLE B]", label_bold)
    ws2.write('C22', 0.1000, goal_seek_var_pct)
    
    ws2.merge_range('B24:C24', "4. EXCESS RETURN VALUATION", sec_title_fmt)
    ws2.write('B25', "Starting Net Worth (₹ Cr)", label_fmt)
    ws2.write_formula('C25', '=C9', calc_cr)
    
    ws2.write('B26', "PV of 10-Year Excess Returns (₹ Cr)", label_fmt)
    ws2.write_formula('C26', '=SUM(E10:N10)', calc_cr)
    
    ws2.write('B27', "Terminal Excess Return (₹ Cr)", label_fmt)
    ws2.write_formula('C27', '=(N7*(C21-C15))/(C15-C16)', calc_cr)
    
    ws2.write('B28', "PV of Terminal Excess Return (₹ Cr)", label_fmt)
    ws2.write_formula('C28', '=C27/(1+C15)^10', calc_cr)
    
    ws2.write('B29', "Model Equity Value (₹ Cr)", label_bold)
    ws2.write_formula('C29', '=C25+C26+C28', calc_cr)
    
    ws2.write('B30', "Model Share Price (₹) [TARGET CELL]", label_bold)
    ws2.write_formula('C30', '=C29/C7', summary_highlight)
    
    ws2.write('B31', "Variance vs Market Price (₹)", label_bold)
    ws2.write_formula('C31', '=C30-C6', diff_highlight)

    for idx, yr in enumerate(headers):
        col_letter = chr(ord('E') + idx)
        ws2.write(f"{col_letter}5", yr, tbl_header)
        
    ws2.write('D6', "Year", tbl_header)
    ws2.write('D7', "Book Value (₹ Cr)", tbl_header)
    ws2.write('D8', "Net Income (₹ Cr)", tbl_header)
    ws2.write('D9', "Equity Charge (₹ Cr)", tbl_header)
    ws2.write('D10', "PV Excess Return (₹ Cr)", tbl_header)
    
    for idx in range(10):
        col_letter = chr(ord('E') + idx)
        t = idx + 1
        ws2.write(f"{col_letter}6", t, calc_cr)
        
        if idx == 0:
            ws2.write_formula(f"{col_letter}7", '=C9*(1+C17*C21)', calc_cr)
            ws2.write_formula(f"{col_letter}8", '=$C$9*$C$21', calc_cr)
            ws2.write_formula(f"{col_letter}9", '=$C$9*$C$15', calc_cr)
        else:
            prev_col = chr(ord('E') + idx - 1)
            ws2.write_formula(f"{col_letter}7", f'={prev_col}7*(1+$C$17*$C$21)', calc_cr)
            ws2.write_formula(f"{col_letter}8", f'={prev_col}7*$C$21', calc_cr)
            ws2.write_formula(f"{col_letter}9", f'={prev_col}7*$C$15', calc_cr)
            
        ws2.write_formula(f"{col_letter}10", f'=({col_letter}8-{col_letter}9)/(1+$C$15)^{t}', calc_cr)
        
    ws2.merge_range('E13:N13', f"📌 BANK GOAL SEEK INSTRUCTIONS FOR {fin['ticker']}", note_box_title)
    bank_instr = (
        "1. Open Goal Seek: Alt + A + W + G\n"
        f"2. Set cell: C30  (Model Share Price in ₹)\n"
        f"   To value: {fin['price']}  (Target Bank Share Price)\n"
        "   By changing cell: C21  (Implied Sustainable ROE %)\n"
        "3. Click OK to solve the sustainable Return on Equity priced in by the Indian market!"
    )
    ws2.merge_range('E14:N19', bank_instr, note_box_body)

    # -------------------------------------------------------------
    # TAB 3: Indian Valuation Methodology & Guidelines
    # -------------------------------------------------------------
    ws3 = wb.add_worksheet("India Valuation Guidelines")
    ws3.set_tab_color('#64748B')
    ws3.hide_gridlines(0)
    ws3.set_column('A:A', 3)
    ws3.set_column('B:B', 30)
    ws3.set_column('C:C', 85)
    
    ws3.merge_range('B2:C2', "INDIAN CORPORATE VALUATION METHODOLOGY (NSE & BSE)", header_fmt)
    ws3.merge_range('B3:C3', "Theoretical Foundation, Mathematical Formulations, and Ind AS / RBI Standards", subhead_fmt)
    ws3.set_row(1, 32)
    ws3.set_row(2, 20)
    
    guide_rows = [
        ("Core Philosophy", "Reverse DCF asks: 'What operational trajectory must this Indian company achieve to justify its current market price?' rather than projecting subjective growth."),
        ("Standard Indian Units", "All figures are standardized strictly in ₹ Crore (1 Crore = 100 Lakhs = 10,000,000 INR). Diluted share counts are in Crore shares, so Share Price (₹) = Equity Value (₹ Cr) / Shares (Cr)."),
        ("India Risk-Free Rate", "Benchmarked against the 10-Year Government of India (G-Sec) bond yield (~7.00% p.a.), monitored via RBI / CCIL."),
        ("India Equity Risk Premium", "Total ERP is set at 7.00%, incorporating mature market ERP (5.00%) plus India Sovereign Country Risk Premium (2.00%) per Damodaran's emerging market datasets."),
        ("Corporate Tax Regime", "Statutory tax rate is modeled at 25.17% (Section 115BAA: 22% base tax + 10% surcharge + 4% cess)."),
        ("Rating Agencies Spread", "Credit default spreads reflect domestic Indian credit rating scales (CRISIL / CARE / ICRA / India Ratings) from AAA down to BBB."),
        ("Financial Institutions (Banks/NBFCs)", "Indian banks (HDFC Bank, ICICI Bank, SBI) cannot use FCFF because debt is raw operational material. Valued via Excess Return over Book Value discounted at Ke.")
    ]
    
    for idx, (title, desc) in enumerate(guide_rows):
        r = 5 + idx * 2
        ws3.write(f'B{r}', title, label_bold)
        ws3.write(f'C{r}', desc, wb.add_format({'font_name': 'Calibri', 'font_size': 10, 'text_wrap': True, 'valign': 'top'}))
        ws3.set_row(r - 1, 28)
        
    if is_fin:
        ws2.activate()
    else:
        ws1.activate()
        
    wb.close()
    return filename

if __name__ == "__main__":
    create_reverse_dcf_workbook()
