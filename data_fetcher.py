import sys
import yfinance as yf
import traceback

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

# Known NSE / BSE Ticker Aliases & Popular Indian Stocks
KNOWN_ALIASES = {
    'GNAAXLES': 'GNA.NS',
    'GNAAXLES.NS': 'GNA.NS',
    'GNA AXLES': 'GNA.NS',
    'GNA': 'GNA.NS',
    'RELIANCE': 'RELIANCE.NS',
    'RIL': 'RELIANCE.NS',
    'HDFCBANK': 'HDFCBANK.NS',
    'HDFC': 'HDFCBANK.NS',
    'TCS': 'TCS.NS',
    'INFY': 'INFY.NS',
    'INFOSYS': 'INFY.NS',
    'TATAMOTORS': 'TATAMOTORS.NS',
    'TATA MOTORS': 'TATAMOTORS.NS',
    'ICICIBANK': 'ICICIBANK.NS',
    'ICICI': 'ICICIBANK.NS',
    'SBIN': 'SBIN.NS',
    'SBI': 'SBIN.NS',
    'BHARTIARTL': 'BHARTIARTL.NS',
    'AIRTEL': 'BHARTIARTL.NS',
    'ITC': 'ITC.NS',
    'LT': 'LT.NS',
    'L&T': 'LT.NS',
    'LARSEN': 'LT.NS',
    'BAJFINANCE': 'BAJFINANCE.NS',
    'BAJAJ FINANCE': 'BAJFINANCE.NS',
    'KOTAKBANK': 'KOTAKBANK.NS',
    'KOTAK': 'KOTAKBANK.NS',
    'MARUTI': 'MARUTI.NS',
    'WIPRO': 'WIPRO.NS',
    'HINDUNILVR': 'HINDUNILVR.NS',
    'HUL': 'HINDUNILVR.NS',
    'ASIANPAINT': 'ASIANPAINT.NS',
    'SUNPHARMA': 'SUNPHARMA.NS',
    'TITAN': 'TITAN.NS',
    'AXISBANK': 'AXISBANK.NS'
}

def resolve_indian_ticker(query):
    query_clean = query.strip()
    q_upper = query_clean.upper()
    q_no_space = q_upper.replace(' ', '')
    
    if q_no_space in KNOWN_ALIASES:
        return KNOWN_ALIASES[q_no_space]
    if q_upper in KNOWN_ALIASES:
        return KNOWN_ALIASES[q_upper]
        
    # If user explicitly entered an exchange suffix (.NS or .BO)
    if q_upper.endswith('.NS') or q_upper.endswith('.BO'):
        return q_upper
        
    # Search via yfinance prioritizing Indian tickers
    try:
        search = yf.Search(f"{query_clean} India", max_results=8)
        if search.quotes and len(search.quotes) > 0:
            for q in search.quotes:
                sym = q.get('symbol', '')
                if sym.endswith('.NS') or sym.endswith('.BO'):
                    return sym
    except Exception as e:
        print(f"yFinance search error: {e}")
        
    # Second search attempt without suffix
    try:
        search2 = yf.Search(query_clean, max_results=8)
        if search2.quotes and len(search2.quotes) > 0:
            for q in search2.quotes:
                sym = q.get('symbol', '')
                if sym.endswith('.NS') or sym.endswith('.BO'):
                    return sym
            # If no Indian ticker found in quotes, return first equity
            for q in search2.quotes:
                if q.get('quoteType') == 'EQUITY':
                    return q.get('symbol')
    except Exception:
        pass
        
    # Fallback to appending .NS
    return f"{q_upper}.NS"

def extract_company_data(query):
    ticker_symbol = resolve_indian_ticker(query)
    ticker = yf.Ticker(ticker_symbol)
    info = ticker.info or {}
    
    # If info is empty, try falling back between .NS and .BO
    if (not info or ('currentPrice' not in info and 'regularMarketPrice' not in info)) and '.' in ticker_symbol:
        alt_sym = ticker_symbol.replace('.NS', '.BO') if ticker_symbol.endswith('.NS') else ticker_symbol.replace('.BO', '.NS')
        try:
            alt_ticker = yf.Ticker(alt_sym)
            if alt_ticker.info and len(alt_ticker.info) > 10:
                ticker = alt_ticker
                ticker_symbol = alt_sym
                info = ticker.info
        except Exception:
            pass

    # Company Metadata
    company_name = info.get('longName') or info.get('shortName') or ticker_symbol
    sector = info.get('sector', 'Indian Corporate')
    industry = info.get('industry', 'NSE/BSE Listed')
    currency = 'INR'
    currency_sym = '₹'
    
    is_financial = (
        sector.lower() in ['financial services', 'financials'] or 
        'bank' in industry.lower() or 
        'insurance' in industry.lower() or
        'nbfc' in industry.lower() or
        'capital markets' in industry.lower()
    )
    
    # Live Price (₹ per share)
    price = info.get('currentPrice') or info.get('regularMarketPrice') or info.get('previousClose')
    if not price:
        try:
            fast_info = getattr(ticker, 'fast_info', {})
            price = fast_info.get('lastPrice')
        except Exception:
            pass
            
    if not price:
        try:
            hist = ticker.history(period='5d')
            if not hist.empty:
                price = float(hist['Close'].iloc[-1])
        except Exception:
            pass
            
    if not price:
        raise ValueError(f"Could not retrieve live price for {ticker_symbol}. Please verify NSE/BSE symbol.")
        
    # Diluted Shares Outstanding (in Crores: 1 Crore = 10,000,000 shares)
    shares_raw = info.get('sharesOutstanding')
    if not shares_raw:
        try:
            fast_info = getattr(ticker, 'fast_info', {})
            shares_raw = fast_info.get('shares')
        except Exception:
            pass
    if not shares_raw:
        mcap_raw = info.get('marketCap')
        if mcap_raw and price:
            shares_raw = mcap_raw / price
        else:
            shares_raw = 100000000 # default 10 Cr shares
            
    shares_cr = shares_raw / 1e7 # Converted to Crores
    mkt_cap_cr = price * shares_cr # In ₹ Crore
    
    # Currency & FX Handling for Financial Statements
    fin_curr = info.get('financialCurrency', 'INR')
    fx_multiplier = 1.0
    if fin_curr == 'USD':
        try:
            usd_inr = yf.Ticker('USDINR=X').fast_info.get('lastPrice')
            fx_multiplier = float(usd_inr) if usd_inr and usd_inr > 50 else 86.5
        except Exception:
            fx_multiplier = 86.5

    total_debt_cr = ((info.get('totalDebt') or 0) * fx_multiplier) / 1e7 # In ₹ Crore
    cash_cr = ((info.get('totalCash') or 0) * fx_multiplier) / 1e7 # In ₹ Crore
    net_debt_cr = total_debt_cr - cash_cr
    
    # Beta
    beta = info.get('beta')
    if beta is None or beta <= 0:
        beta = 0.95
        
    # Indian Valuation Parameters
    rf = 0.0700      # 7.00% India 10-Yr G-Sec Benchmark Yield
    erp = 0.0700     # 7.00% Damodaran Total ERP for India (Mature 5.0% + Country Risk Premium 2.0%)
    tax_rate = 0.2517 # 25.17% Statutory Corporate Tax Rate under Section 115BAA
    ke = rf + beta * erp
    
    if is_financial:
        book_value_per_share = info.get('bookValue')
        if book_value_per_share and book_value_per_share > 0:
            total_book_value_cr = (book_value_per_share * fx_multiplier) * shares_cr
        else:
            total_book_value_cr = mkt_cap_cr * 0.70
            
        net_income_raw = info.get('netIncomeToCommon')
        if net_income_raw:
            net_income_cr = (net_income_raw * fx_multiplier) / 1e7
        else:
            net_income_cr = total_book_value_cr * 0.14 # 14% ROE default
            
        return {
            'ticker': ticker_symbol,
            'name': company_name,
            'sector': sector,
            'industry': industry,
            'currency': 'INR',
            'currency_symbol': '₹',
            'unit': '₹ Crore',
            'is_financial': True,
            'price': round(float(price), 2),
            'shares_cr': round(float(shares_cr), 4),
            'market_cap_cr': round(float(mkt_cap_cr), 2),
            'book_value_cr': round(float(total_book_value_cr), 2),
            'net_income_cr': round(float(net_income_cr), 2),
            'rf': round(rf * 100, 2),
            'beta': round(float(beta), 2),
            'cost_of_equity': round(ke * 100, 2),
            'retention_ratio': 40.0,
            'term_g': 5.0 # 5.0% India long-term nominal terminal rate
        }
    else:
        # Non-Financial Corporate Profile
        ebitda_cr = ((info.get('ebitda') or 0) * fx_multiplier) / 1e7
        
        # Trailing FCFF derivation (in ₹ Crore)
        trailing_fcf_raw = info.get('freeCashflow')
        ocf_raw = info.get('operatingCashflow') or 0
        
        if trailing_fcf_raw:
            trailing_fcf_raw = trailing_fcf_raw * fx_multiplier
        if ocf_raw:
            ocf_raw = ocf_raw * fx_multiplier
            
        if trailing_fcf_raw and trailing_fcf_raw > 0:
            # Check for capex anomalies in automated feeds
            if ocf_raw > 0 and (trailing_fcf_raw / ocf_raw < 0.10):
                trailing_fcf_raw = ocf_raw * 0.35
        else:
            if ocf_raw > 0:
                trailing_fcf_raw = ocf_raw * 0.60
            else:
                trailing_fcf_raw = (mkt_cap_cr * 1e7) * 0.04
                
        trailing_fcff_cr = trailing_fcf_raw / 1e7
        
        # Credit Rating derivation for Indian Corporates
        if ebitda_cr > 0:
            leverage = net_debt_cr / ebitda_cr
        else:
            leverage = total_debt_cr / mkt_cap_cr if mkt_cap_cr > 0 else 0
            
        if net_debt_cr <= 0 or leverage < 0.5:
            rating = 'CRISIL / CARE AAA'
            spread = 0.0065
        elif leverage < 1.5:
            rating = 'CRISIL / CARE AA+'
            spread = 0.0085
        elif leverage < 2.5:
            rating = 'CRISIL / CARE AA / AA-'
            spread = 0.0115
        elif leverage < 3.5:
            rating = 'CRISIL / CARE A+'
            spread = 0.0160
        elif leverage < 4.5:
            rating = 'CRISIL / CARE A / BBB+'
            spread = 0.0240
        else:
            rating = 'CRISIL / CARE BBB'
            spread = 0.0350
            
        kd_pre = rf + spread
        kd_after = kd_pre * (1 - tax_rate)
        
        tot_capital = mkt_cap_cr + total_debt_cr
        we = mkt_cap_cr / tot_capital if tot_capital > 0 else 1.0
        wd = total_debt_cr / tot_capital if tot_capital > 0 else 0.0
        
        wacc = (we * ke) + (wd * kd_after)
        
        return {
            'ticker': ticker_symbol,
            'name': company_name,
            'sector': sector,
            'industry': industry,
            'currency': 'INR',
            'currency_symbol': '₹',
            'unit': '₹ Crore',
            'is_financial': False,
            'price': round(float(price), 2),
            'shares_cr': round(float(shares_cr), 4),
            'market_cap_cr': round(float(mkt_cap_cr), 2),
            'total_debt_cr': round(float(total_debt_cr), 2),
            'cash_cr': round(float(cash_cr), 2),
            'net_debt_cr': round(float(net_debt_cr), 2),
            'trailing_fcff_cr': round(float(trailing_fcff_cr), 2),
            'rf': round(rf * 100, 2),
            'beta': round(float(beta), 2),
            'rating': rating,
            'rating_spread': round(spread * 100, 2),
            'cost_of_debt_after_tax': round(kd_after * 100, 2),
            'cost_of_equity': round(ke * 100, 2),
            'wacc': round(wacc * 100, 2),
            'weight_equity': round(we * 100, 1),
            'weight_debt': round(wd * 100, 1),
            'term_g': 5.0 # 5.0% India long-term nominal terminal rate
        }

if __name__ == '__main__':
    for test in ['GNA Axles', 'GNAAXLES', 'Reliance', 'TCS', 'HDFC Bank', 'Tata Motors', 'ICICI Bank']:
        print(f"\n--- Testing Indian Extraction: {test} ---")
        res = extract_company_data(test)
        print(f"Ticker: {res['ticker']} | {res['name']}")
        print(f"Price: ₹{res['price']} | Shares: {res['shares_cr']} Cr shares | Market Cap: ₹{res['market_cap_cr']} Cr")
        if res['is_financial']:
            print(f"Method: Banking ROE | Net Income: ₹{res['net_income_cr']} Cr | Book Value: ₹{res['book_value_cr']} Cr | Ke: {res['cost_of_equity']}%")
        else:
            print(f"Method: FCFF | Net Debt: ₹{res['net_debt_cr']} Cr | FCFF: ₹{res['trailing_fcff_cr']} Cr | WACC: {res['wacc']}% (Rating: {res['rating']})")
