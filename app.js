/**
 * REVERSE DCF INDIA TERMINAL
 * Institutional Valuation Engine for NSE & BSE Listed Companies
 * Units: All capital structure & cash flow values in ₹ Crore (1 Cr = 10 Million INR)
 * Supports:
 *  1. Indian Non-Financial Corporates: FCFF, CRISIL/CARE Rating WACC, Net Debt Bridge
 *  2. Indian Financial Institutions (Banks/NBFCs): Excess Return (ROE) & FCFE, Cost of Equity (Ke)
 */

// Application State
const state = {
  mode: 'non-financial', // 'non-financial' or 'financial'
  currentPreset: 'GNA.NS',
  companyName: 'GNA Axles Ltd',
  ticker: 'GNA.NS',
  currency: '₹',
  currencyCode: 'INR',
  unit: '₹ Crore',
  sector: 'Auto Parts',
  rating: 'CRISIL / CARE AA-',
  chartInstance: null,
  horizon: 10, // Projection horizon runway (10 or 20 years)
  
  // Non-financial inputs (Values in ₹ Crore, Shares in Crore shares)
  nonFinancial: {
    sharePrice: 554.55,       // ₹ per share
    shares_cr: 4.2931,        // Crore shares (42.93 M shares)
    totalDebt_cr: 183.88,     // ₹ Crore
    cash_cr: 37.95,           // ₹ Crore
    baseFCFF_cr: 59.19,       // ₹ Crore (Normalized Mid-Cycle 10.7% margin, 50% reinvestment)
    wacc: 10.59,              // % (7.0% Rf + 0.57 Beta * 7.0% ERP)
    termG: 5.0,               // % (India long-term nominal terminal rate)
  },

  // Financial institutions inputs (Values in ₹ Crore, Shares in Crore shares)
  financial: {
    sharePrice: 707.25,       // ₹ per share
    shares_cr: 1541.85,       // Crore shares
    bookValue_cr: 607200.0,   // ₹ Crore (Net Worth)
    netIncome_cr: 79012.0,    // ₹ Crore (Trailing PAT)
    retentionRatio: 40.0,     // % retained for regulatory Tier-1 capital
    costOfEquity: 11.50,      // % Ke
    termG: 5.0,               // %
  }
};

// Pure Indian NSE & BSE Preset Profiles (Values in ₹ Crore, Shares in Cr shares)
const PRESETS = {
  'non-financial': [
    { 
      ticker: 'GNA.NS', 
      name: 'GNA Axles Ltd', 
      price: 554.55, 
      shares_cr: 4.2931, 
      totalDebt_cr: 183.88, 
      cash_cr: 37.95, 
      baseFCFF_cr: 59.19, 
      wacc: 10.59, 
      termG: 5.0, 
      sector: 'Auto Parts & Components', 
      rating: 'CRISIL / CARE AA-' 
    },
    { 
      ticker: 'RELIANCE.NS', 
      name: 'Reliance Industries Limited', 
      price: 1170.30, 
      shares_cr: 1353.25, 
      totalDebt_cr: 313000.0, 
      cash_cr: 182000.0, 
      baseFCFF_cr: 63348.0, 
      wacc: 8.50, 
      termG: 5.0, 
      sector: 'Energy, Retail & Telecom', 
      rating: 'CRISIL AAA' 
    },
    { 
      ticker: 'TCS.NS', 
      name: 'Tata Consultancy Services', 
      price: 2156.00, 
      shares_cr: 361.81, 
      totalDebt_cr: 0.0, 
      cash_cr: 42832.0, 
      baseFCFF_cr: 43319.0, 
      wacc: 8.24, 
      termG: 5.0, 
      sector: 'IT Services & Consulting', 
      rating: 'CRISIL AAA' 
    },
    { 
      ticker: 'TMCV.NS', 
      name: 'Tata Motors Commercial Vehicles', 
      price: 382.50, 
      shares_cr: 368.00, 
      totalDebt_cr: 45000.0, 
      cash_cr: 28000.0, 
      baseFCFF_cr: 14500.0, 
      wacc: 11.20, 
      termG: 5.0, 
      sector: 'Automobile (Commercial Vehicles)', 
      rating: 'CRISIL AA+' 
    },
    { 
      ticker: 'LT.NS', 
      name: 'Larsen & Toubro Ltd', 
      price: 3703.30, 
      shares_cr: 137.52, 
      totalDebt_cr: 118000.0, 
      cash_cr: 45000.0, 
      baseFCFF_cr: 18200.0, 
      wacc: 9.80, 
      termG: 5.0, 
      sector: 'Infrastructure & EPC', 
      rating: 'CRISIL AAA' 
    },
    { 
      ticker: 'INFY.NS', 
      name: 'Infosys Limited', 
      price: 1023.40, 
      shares_cr: 415.20, 
      totalDebt_cr: 0.0, 
      cash_cr: 18500.0, 
      baseFCFF_cr: 23400.0, 
      wacc: 8.50, 
      termG: 5.0, 
      sector: 'IT & Digital Services', 
      rating: 'CRISIL AAA' 
    }
  ],
  'financial': [
    { 
      ticker: 'HDFCBANK.NS', 
      name: 'HDFC Bank Limited', 
      price: 707.25, 
      shares_cr: 1541.85, 
      bookValue_cr: 607200.0, 
      netIncome_cr: 79012.0, 
      retentionRatio: 40.0, 
      costOfEquity: 11.50, 
      termG: 5.0, 
      sector: 'Private Sector Bank' 
    },
    { 
      ticker: 'ICICIBANK.NS', 
      name: 'ICICI Bank Limited', 
      price: 1355.00, 
      shares_cr: 705.50, 
      bookValue_cr: 265000.0, 
      netIncome_cr: 48500.0, 
      retentionRatio: 35.0, 
      costOfEquity: 11.20, 
      termG: 5.0, 
      sector: 'Private Sector Bank' 
    },
    { 
      ticker: 'SBIN.NS', 
      name: 'State Bank of India', 
      price: 959.10, 
      shares_cr: 892.46, 
      bookValue_cr: 412000.0, 
      netIncome_cr: 67000.0, 
      retentionRatio: 45.0, 
      costOfEquity: 12.00, 
      termG: 5.0, 
      sector: 'Public Sector Bank' 
    },
    { 
      ticker: 'BAJFINANCE.NS', 
      name: 'Bajaj Finance Limited', 
      price: 960.00, 
      shares_cr: 618.50, 
      bookValue_cr: 86000.0, 
      netIncome_cr: 16500.0, 
      retentionRatio: 40.0, 
      costOfEquity: 12.50, 
      termG: 5.0, 
      sector: 'Consumer NBFC' 
    },
    { 
      ticker: 'KOTAKBANK.NS', 
      name: 'Kotak Mahindra Bank', 
      price: 1845.00, 
      shares_cr: 198.80, 
      bookValue_cr: 132000.0, 
      netIncome_cr: 17800.0, 
      retentionRatio: 40.0, 
      costOfEquity: 11.50, 
      termG: 5.0, 
      sector: 'Private Sector Bank' 
    }
  ]
};

// ============================================================================
// VALUATION MATH ENGINES (NUMERICAL ROOT FINDING IN ₹ CRORE)
// ============================================================================

/**
 * Calculates Model Enterprise Value given a trial FCFF growth rate (g)
 * All values in ₹ Crore
 */
function calculateEVFromGrowth(g, baseFCFF_cr, wacc, termG, nYears = 10) {
  let pvDiscrete = 0;
  let currFCFF = baseFCFF_cr;
  
  for (let t = 1; t <= nYears; t++) {
    currFCFF *= (1 + g);
    const df = Math.pow(1 + wacc, -t);
    pvDiscrete += currFCFF * df;
  }
  
  // Terminal Value (Gordon Growth)
  const terminalFCFF = currFCFF * (1 + termG);
  const tv = terminalFCFF / (wacc - termG);
  const pvTV = tv * Math.pow(1 + wacc, -nYears);
  
  return {
    ev: pvDiscrete + pvTV,
    pvDiscrete: pvDiscrete,
    pvTV: pvTV,
    finalFCFF: currFCFF
  };
}

/**
 * Solves for Implied FCFF CAGR that matches Market Enterprise Value (in ₹ Crore)
 */
function solveImpliedFCFFCAGR(targetEV_cr, baseFCFF_cr, wacc, termG, nYears = 10) {
  let low = -0.50;  // -50% CAGR
  let high = 1.50;  // +150% CAGR
  const tolerance = 0.0001;
  const maxIter = 100;
  
  for (let i = 0; i < maxIter; i++) {
    const mid = (low + high) / 2;
    const calc = calculateEVFromGrowth(mid, baseFCFF_cr, wacc, termG, nYears);
    const diff = calc.ev - targetEV_cr;
    
    if (Math.abs(diff) < tolerance || Math.abs(high - low) < tolerance) {
      return mid;
    }
    
    if (calc.ev < targetEV_cr) {
      low = mid;
    } else {
      high = mid;
    }
  }
  return (low + high) / 2;
}

/**
 * Financial Institutions: Excess Return Model (All values in ₹ Crore)
 */
function calculateBankEquityFromROE(roe, bookValue_cr, costOfEquity, retentionRatio, termG, nYears = 10) {
  let pvExcess = 0;
  let currBV = bookValue_cr;
  
  for (let t = 1; t <= nYears; t++) {
    const netIncome = currBV * roe;
    const equityCharge = currBV * costOfEquity;
    const excessReturn = netIncome - equityCharge;
    const df = Math.pow(1 + costOfEquity, -t);
    pvExcess += excessReturn * df;
    
    currBV += netIncome * retentionRatio;
  }
  
  // Terminal Excess Return
  const terminalExcess = (currBV * (roe - costOfEquity)) / (costOfEquity - termG);
  const pvTerminalExcess = terminalExcess * Math.pow(1 + costOfEquity, -nYears);
  
  const intrinsicEquity = bookValue_cr + pvExcess + pvTerminalExcess;
  return {
    equityValue: intrinsicEquity,
    pvExcess: pvExcess,
    pvTerminalExcess: pvTerminalExcess,
    finalBV: currBV
  };
}

/**
 * Solves for Implied Sustainable ROE for Indian Banks & NBFCs
 */
function solveImpliedROE(targetMarketCap_cr, bookValue_cr, costOfEquity, retentionRatio, termG, nYears = 10) {
  let low = 0.01;   // 1% ROE
  let high = 0.80;  // 80% ROE
  const tolerance = 0.0001;
  const maxIter = 100;
  
  for (let i = 0; i < maxIter; i++) {
    const mid = (low + high) / 2;
    const calc = calculateBankEquityFromROE(mid, bookValue_cr, costOfEquity, retentionRatio, termG, nYears);
    const diff = calc.equityValue - targetMarketCap_cr;
    
    if (Math.abs(diff) < tolerance || Math.abs(high - low) < tolerance) {
      return mid;
    }
    
    if (calc.equityValue < targetMarketCap_cr) {
      low = mid;
    } else {
      high = mid;
    }
  }
  return (low + high) / 2;
}

// ============================================================================
// UI CONTROLLER & EVENT LISTENERS
// ============================================================================

function init() {
  setupNavigationTabs();
  setupCompanySearch();
  setupAnalysisSubTabs();
  setupModal();
  setupDownloadButton();
  
  renderPresetButtons();
  loadPreset(state.currentPreset);
}

function setupNavigationTabs() {
  const tabNF = document.getElementById('tabNonFinancial');
  const tabF = document.getElementById('tabFinancial');

  tabNF.addEventListener('click', () => switchMode('non-financial'));
  tabF.addEventListener('click', () => switchMode('financial'));
}

function setupAnalysisSubTabs() {
  const tabs = document.querySelectorAll('.sub-tab');
  tabs.forEach(tab => {
    tab.addEventListener('click', () => {
      tabs.forEach(t => t.classList.remove('active'));
      tab.classList.add('active');

      const view = tab.getAttribute('data-view');
      const chartEl = document.getElementById('viewChart');
      const sensEl = document.getElementById('viewSensitivity');
      const schedEl = document.getElementById('viewSchedule');

      if (chartEl) chartEl.classList.toggle('active', view === 'chart');
      if (sensEl) sensEl.classList.toggle('active', view === 'sensitivity');
      if (schedEl) schedEl.classList.toggle('active', view === 'schedule');

      if (view === 'chart' && state.chartInstance) {
        state.chartInstance.resize();
      }
    });
  });

  const h10 = document.getElementById('btnHorizon10');
  const h20 = document.getElementById('btnHorizon20');
  if (h10 && h20) {
    h10.addEventListener('click', () => {
      state.horizon = 10;
      h10.classList.add('active');
      h20.classList.remove('active');
      calculateAndRender();
    });
    h20.addEventListener('click', () => {
      state.horizon = 20;
      h20.classList.add('active');
      h10.classList.remove('active');
      calculateAndRender();
    });
  }
}

function setupCompanySearch() {
  const searchForm = document.getElementById('searchCompanyForm');
  const searchInput = document.getElementById('companySearchInput');
  const searchBtn = document.getElementById('fetchCompanyBtn');
  const clearBtn = document.getElementById('clearSearchBtn');

  if (searchInput) {
    searchInput.addEventListener('input', () => {
      clearBtn.style.display = searchInput.value ? 'block' : 'none';
    });
  }
  if (clearBtn) {
    clearBtn.addEventListener('click', () => {
      searchInput.value = '';
      clearBtn.style.display = 'none';
      searchInput.focus();
    });
  }

  if (searchForm) {
    searchForm.addEventListener('submit', async (e) => {
      e.preventDefault();
      const query = searchInput.value.trim();
      if (!query) return;

      const btnText = searchBtn.querySelector('.btn-text');
      const btnSpinner = searchBtn.querySelector('.btn-spinner');
      
      btnText.style.display = 'none';
      btnSpinner.style.display = 'inline-flex';
      searchBtn.disabled = true;

      try {
        const res = await fetch(`/api/fetch?query=${encodeURIComponent(query)}`);
        if (!res.ok) throw new Error(`HTTP ${res.status}`);
        const json = await res.json();
        
        if (!json.success) {
          alert(`Could not extract NSE/BSE data for "${query}": ${json.error || 'Unknown error'}`);
          return;
        }

        const data = json.data;
        applyFetchedCompanyData(data);
      } catch (err) {
        console.warn('Backend API fetch unavailable or failed, attempting preset lookup:', err);
        const q = query.toLowerCase();
        const nonFinMatch = PRESETS['non-financial'].find(p => 
          p.ticker.toLowerCase().includes(q) || 
          p.name.toLowerCase().includes(q) ||
          q.includes(p.ticker.toLowerCase().replace('.ns', '').replace('.bo', ''))
        );
        const finMatch = PRESETS['financial'].find(p => 
          p.ticker.toLowerCase().includes(q) || 
          p.name.toLowerCase().includes(q) ||
          q.includes(p.ticker.toLowerCase().replace('.ns', '').replace('.bo', ''))
        );

        if (nonFinMatch) {
          if (state.mode !== 'non-financial') switchMode('non-financial');
          loadPreset(nonFinMatch.ticker);
        } else if (finMatch) {
          if (state.mode !== 'financial') switchMode('financial');
          loadPreset(finMatch.ticker);
        } else {
          alert(`Note: Real-time NSE/BSE extraction for "${query}" requires the local Python server (python server.py).\n\nOn static Netlify deployment, please click any of the preset companies (Reliance, TCS, HDFC Bank, GNA Axles, Tata Motors, L&T, Infosys, ICICI Bank, SBI, Bajaj Finance) or test locally.`);
        }
      } finally {
        btnText.style.display = 'inline-flex';
        btnSpinner.style.display = 'none';
        searchBtn.disabled = false;
      }
    });
  }
}

function applyFetchedCompanyData(data) {
  state.companyName = data.name;
  state.ticker = data.ticker;
  state.sector = data.sector || 'Indian Corporate';
  state.rating = data.rating || 'CRISIL / CARE AA';

  if (data.is_financial) {
    state.mode = 'financial';
    state.financial.sharePrice = data.price;
    state.financial.shares_cr = data.shares_cr || (data.shares_m / 10.0);
    state.financial.bookValue_cr = data.book_value_cr || (data.book_value_m / 10.0);
    state.financial.netIncome_cr = data.net_income_cr || (data.net_income_m / 10.0);
    state.financial.costOfEquity = data.cost_of_equity;
    state.financial.retentionRatio = data.retention_ratio || 40.0;
    state.financial.termG = data.term_g || 5.0;
  } else {
    state.mode = 'non-financial';
    state.nonFinancial.sharePrice = data.price;
    state.nonFinancial.shares_cr = data.shares_cr || (data.shares_m / 10.0);
    state.nonFinancial.totalDebt_cr = data.total_debt_cr || (data.total_debt_m / 10.0);
    state.nonFinancial.cash_cr = data.cash_cr || (data.cash_m / 10.0);
    state.nonFinancial.baseFCFF_cr = data.trailing_fcff_cr || (data.trailing_fcff_m / 10.0);
    state.nonFinancial.wacc = data.wacc;
    state.nonFinancial.termG = data.term_g || 5.0;
  }

  // Update tabs UI
  document.getElementById('tabNonFinancial').classList.toggle('active', !data.is_financial);
  document.getElementById('tabFinancial').classList.toggle('active', data.is_financial);
  
  const badge = document.getElementById('modelMethodBadge');
  if (!data.is_financial) {
    badge.textContent = 'FCFF Method (₹ Cr)';
    badge.className = 'badge badge-info';
    badge.style.background = '';
    badge.style.border = '';
  } else {
    badge.textContent = 'Excess Return ROE (₹ Cr)';
    badge.className = 'badge text-emerald';
    badge.style.background = 'rgba(16, 185, 129, 0.15)';
    badge.style.border = '1px solid rgba(16, 185, 129, 0.3)';
  }

  // Display Extraction Status Bar
  const bar = document.getElementById('extractionStatusBar');
  if (bar) {
    bar.style.display = 'flex';
    document.getElementById('extCompName').textContent = `${data.name} (${data.ticker})`;
    document.getElementById('extSector').textContent = `${data.sector}`;
    document.getElementById('extPrice').textContent = `₹${data.price.toFixed(2)} (Live NSE/BSE)`;

    if (!data.is_financial) {
      document.getElementById('extWaccLabel').textContent = 'Rating & WACC:';
      document.getElementById('extWacc').textContent = `${data.rating} • WACC: ${data.wacc.toFixed(2)}% (10Y G-Sec: ${data.rf}%, Spread: +${data.rating_spread}%)`;
      document.getElementById('extCashflowLabel').textContent = 'Base FCFF:';
      document.getElementById('extCashflow').textContent = `₹${state.nonFinancial.baseFCFF_cr.toLocaleString(undefined, {maximumFractionDigits: 2})} Cr`;
    } else {
      document.getElementById('extWaccLabel').textContent = 'Cost of Equity (Ke):';
      document.getElementById('extWacc').textContent = `${data.cost_of_equity.toFixed(2)}% (Beta: ${data.beta}, G-Sec Rf: ${data.rf}%)`;
      document.getElementById('extCashflowLabel').textContent = 'Net Income (PAT):';
      document.getElementById('extCashflow').textContent = `₹${state.financial.netIncome_cr.toLocaleString(undefined, {maximumFractionDigits: 1})} Cr (Net Worth: ₹${state.financial.bookValue_cr.toLocaleString(undefined, {maximumFractionDigits: 1})} Cr)`;
    }
  }

  // Clear active preset buttons
  document.querySelectorAll('.preset-chip').forEach(c => c.classList.remove('active'));

  updateDownloadButtonLabel();
  renderInputs();
  calculateAndRender();
}

function updateDownloadButtonLabel() {
  const btnText = document.getElementById('downloadBtnText');
  if (btnText) {
    btnText.textContent = `Download Excel Model (${state.ticker}.xlsx)`;
  }
}

function setupDownloadButton() {
  const btn = document.getElementById('downloadExcelBtn');
  if (!btn) return;

  btn.addEventListener('click', async (e) => {
    e.preventDefault();
    
    const payload = {
      is_financial: state.mode === 'financial',
      ticker: state.ticker,
      name: state.companyName,
      currency: 'INR',
      currency_symbol: '₹',
      unit: '₹ Crore',
      ...(state.mode === 'financial' ? {
        price: state.financial.sharePrice,
        shares_cr: state.financial.shares_cr,
        book_value_cr: state.financial.bookValue_cr,
        net_income_cr: state.financial.netIncome_cr,
        cost_of_equity: state.financial.costOfEquity,
        retention_ratio: state.financial.retentionRatio,
        term_g: state.financial.termG
      } : {
        price: state.nonFinancial.sharePrice,
        shares_cr: state.nonFinancial.shares_cr,
        total_debt_cr: state.nonFinancial.totalDebt_cr,
        cash_cr: state.nonFinancial.cash_cr,
        trailing_fcff_cr: state.nonFinancial.baseFCFF_cr,
        wacc: state.nonFinancial.wacc,
        term_g: state.nonFinancial.termG,
        rating: state.rating || 'CRISIL AA'
      })
    };

    try {
      const resp = await fetch('/api/export', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(payload)
      });
      if (!resp.ok) throw new Error('Export error');
      const blob = await resp.blob();
      const url = window.URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = url;
      a.download = `Reverse_DCF_${state.ticker.replace('/', '_')}.xlsx`;
      document.body.appendChild(a);
      a.click();
      a.remove();
      window.URL.revokeObjectURL(url);
    } catch (err) {
      console.warn('Fallback to direct model file download:', err);
      window.location.href = 'Reverse_DCF_Model.xlsx';
    }
  });
}

function switchMode(newMode) {
  if (state.mode === newMode) return;
  state.mode = newMode;
  
  document.getElementById('tabNonFinancial').classList.toggle('active', newMode === 'non-financial');
  document.getElementById('tabFinancial').classList.toggle('active', newMode === 'financial');
  
  const badge = document.getElementById('modelMethodBadge');
  if (newMode === 'non-financial') {
    badge.textContent = 'FCFF Method (₹ Cr)';
    badge.className = 'badge badge-info';
    badge.style.background = '';
    badge.style.border = '';
    state.currentPreset = PRESETS['non-financial'][0].ticker;
  } else {
    badge.textContent = 'Excess Return ROE (₹ Cr)';
    badge.className = 'badge text-emerald';
    badge.style.background = 'rgba(16, 185, 129, 0.15)';
    badge.style.border = '1px solid rgba(16, 185, 129, 0.3)';
    state.currentPreset = PRESETS['financial'][0].ticker;
  }
  
  renderPresetButtons();
  loadPreset(state.currentPreset);
}

function renderPresetButtons() {
  const container = document.getElementById('presetButtons');
  container.innerHTML = '';
  const list = PRESETS[state.mode];
  
  list.forEach(p => {
    const btn = document.createElement('button');
    btn.className = `preset-chip ${p.ticker === state.currentPreset ? 'active' : ''}`;
    btn.textContent = `${p.ticker.replace('.NS', '')} (${p.name})`;
    btn.addEventListener('click', () => loadPreset(p.ticker));
    container.appendChild(btn);
  });
}

function loadPreset(ticker) {
  state.currentPreset = ticker;
  document.querySelectorAll('.preset-chip').forEach(btn => {
    btn.classList.toggle('active', btn.textContent.startsWith(ticker.replace('.NS', '')));
  });

  const preset = PRESETS[state.mode].find(p => p.ticker === ticker);
  if (!preset) return;

  state.companyName = preset.name;
  state.ticker = preset.ticker;
  state.sector = preset.sector || 'Indian Corporate';
  state.rating = preset.rating || 'CRISIL / CARE AA';

  if (state.mode === 'non-financial') {
    state.nonFinancial.sharePrice = preset.price;
    state.nonFinancial.shares_cr = preset.shares_cr;
    state.nonFinancial.totalDebt_cr = preset.totalDebt_cr;
    state.nonFinancial.cash_cr = preset.cash_cr;
    state.nonFinancial.baseFCFF_cr = preset.baseFCFF_cr;
    state.nonFinancial.wacc = preset.wacc;
    state.nonFinancial.termG = preset.termG;
  } else {
    state.financial.sharePrice = preset.price;
    state.financial.shares_cr = preset.shares_cr;
    state.financial.bookValue_cr = preset.bookValue_cr;
    state.financial.netIncome_cr = preset.netIncome_cr;
    state.financial.retentionRatio = preset.retentionRatio;
    state.financial.costOfEquity = preset.costOfEquity;
    state.financial.termG = preset.termG;
  }

  // Update status bar
  const bar = document.getElementById('extractionStatusBar');
  if (bar) {
    bar.style.display = 'flex';
    document.getElementById('extCompName').textContent = `${preset.name} (${preset.ticker})`;
    document.getElementById('extSector').textContent = preset.sector;
    document.getElementById('extPrice').textContent = `₹${preset.price.toFixed(2)}`;

    if (state.mode === 'non-financial') {
      document.getElementById('extWaccLabel').textContent = 'Rating & WACC:';
      document.getElementById('extWacc').textContent = `${preset.rating} • WACC: ${preset.wacc.toFixed(2)}% (10Y G-Sec: 7.00%)`;
      document.getElementById('extCashflowLabel').textContent = 'Base FCFF:';
      document.getElementById('extCashflow').textContent = `₹${preset.baseFCFF_cr.toLocaleString(undefined, {maximumFractionDigits: 1})} Cr`;
    } else {
      document.getElementById('extWaccLabel').textContent = 'Cost of Equity (Ke):';
      document.getElementById('extWacc').textContent = `${preset.costOfEquity.toFixed(2)}% (10Y G-Sec: 7.00%)`;
      document.getElementById('extCashflowLabel').textContent = 'Net Income (PAT):';
      document.getElementById('extCashflow').textContent = `₹${preset.netIncome_cr.toLocaleString(undefined, {maximumFractionDigits: 1})} Cr (Net Worth: ₹${preset.bookValue_cr.toLocaleString(undefined, {maximumFractionDigits: 1})} Cr)`;
    }
  }

  updateDownloadButtonLabel();
  renderInputs();
  calculateAndRender();
}

function renderInputs() {
  const container = document.getElementById('dynamicInputsContainer');
  
  if (state.mode === 'non-financial') {
    const d = state.nonFinancial;
    container.innerHTML = `
      <div class="input-section-title">Market & Capital Structure (₹ Crore)</div>
      <div class="form-group">
        <div class="form-label-row">
          <label class="form-label">Current Share Price</label>
          <span class="form-value-badge" id="lbl_sharePrice">₹${d.sharePrice.toFixed(2)}</span>
        </div>
        <div class="input-container">
          <span class="input-prefix">₹</span>
          <input type="number" step="0.5" class="form-control has-prefix" id="in_sharePrice" value="${d.sharePrice}">
        </div>
      </div>

      <div class="form-group">
        <div class="form-label-row">
          <label class="form-label">Diluted Shares Outstanding (Cr shares)</label>
          <span class="form-value-badge" id="lbl_shares">${d.shares_cr.toFixed(4)} Cr</span>
        </div>
        <input type="number" step="0.1" class="form-control" id="in_shares" value="${d.shares_cr}">
      </div>

      <div class="form-group">
        <div class="form-label-row">
          <label class="form-label">Total Debt / Borrowings (₹ Cr)</label>
          <span class="form-value-badge" id="lbl_debt">₹${d.totalDebt_cr.toLocaleString()} Cr</span>
        </div>
        <input type="number" step="10" class="form-control" id="in_totalDebt" value="${d.totalDebt_cr}">
      </div>

      <div class="form-group">
        <div class="form-label-row">
          <label class="form-label">Cash & Liquid Balances (₹ Cr)</label>
          <span class="form-value-badge" id="lbl_cash">₹${d.cash_cr.toLocaleString()} Cr</span>
        </div>
        <input type="number" step="10" class="form-control" id="in_cash" value="${d.cash_cr}">
      </div>

      <div class="input-section-title">Valuation & Cash Flow Parameters (₹ Crore)</div>
      <div class="form-group">
        <div class="form-label-row">
          <label class="form-label">Normalized Base FCFF (₹ Cr)</label>
          <span class="form-value-badge" id="lbl_fcff">₹${d.baseFCFF_cr.toLocaleString()} Cr</span>
        </div>
        <input type="number" step="5" class="form-control" id="in_baseFCFF" value="${d.baseFCFF_cr}">
      </div>

      <div class="form-group">
        <div class="form-label-row">
          <label class="form-label">Discount Rate (Rating-Derived WACC %)</label>
          <span class="form-value-badge" id="lbl_wacc">${d.wacc.toFixed(2)}%</span>
        </div>
        <div class="slider-container">
          <input type="range" min="6.0" max="18.0" step="0.1" id="sl_wacc" value="${d.wacc}">
          <input type="number" step="0.1" class="form-control has-suffix" style="width: 90px;" id="in_wacc" value="${d.wacc}">
        </div>
        <span class="text-muted" style="font-size: 0.72rem;">Derived: 7.0% G-Sec + Domestic Credit Spread + 7.0% India ERP</span>
      </div>

      <div class="form-group">
        <div class="form-label-row">
          <label class="form-label">Terminal Growth Rate (g %)</label>
          <span class="form-value-badge" id="lbl_termG">${d.termG.toFixed(2)}%</span>
        </div>
        <div class="slider-container">
          <input type="range" min="3.0" max="7.0" step="0.1" id="sl_termG" value="${d.termG}">
          <input type="number" step="0.1" class="form-control has-suffix" style="width: 90px;" id="in_termG" value="${d.termG}">
        </div>
        <span class="text-muted" style="font-size: 0.72rem;">Sustainable long-term nominal GDP growth ceiling</span>
      </div>
    `;

    bindInput('in_sharePrice', (v) => { d.sharePrice = v; document.getElementById('lbl_sharePrice').textContent = `₹${v.toFixed(2)}`; });
    bindInput('in_shares', (v) => { d.shares_cr = v; document.getElementById('lbl_shares').textContent = `${v.toFixed(4)} Cr`; });
    bindInput('in_totalDebt', (v) => { d.totalDebt_cr = v; document.getElementById('lbl_debt').textContent = `₹${v.toLocaleString()} Cr`; });
    bindInput('in_cash', (v) => { d.cash_cr = v; document.getElementById('lbl_cash').textContent = `₹${v.toLocaleString()} Cr`; });
    bindInput('in_baseFCFF', (v) => { d.baseFCFF_cr = v; document.getElementById('lbl_fcff').textContent = `₹${v.toLocaleString()} Cr`; });
    
    bindSliderAndInput('sl_wacc', 'in_wacc', (v) => { d.wacc = v; document.getElementById('lbl_wacc').textContent = `${v.toFixed(2)}%`; });
    bindSliderAndInput('sl_termG', 'in_termG', (v) => { d.termG = v; document.getElementById('lbl_termG').textContent = `${v.toFixed(2)}%`; });

  } else {
    // Financial Institutions Inputs (Excess Return / ROE in ₹ Cr)
    const d = state.financial;
    container.innerHTML = `
      <div class="input-section-title">Bank / NBFC Capital Profile (₹ Crore)</div>
      <div class="form-group">
        <div class="form-label-row">
          <label class="form-label">Current Share Price</label>
          <span class="form-value-badge" id="lbl_sharePrice">₹${d.sharePrice.toFixed(2)}</span>
        </div>
        <div class="input-container">
          <span class="input-prefix">₹</span>
          <input type="number" step="0.5" class="form-control has-prefix" id="in_sharePrice" value="${d.sharePrice}">
        </div>
      </div>

      <div class="form-group">
        <div class="form-label-row">
          <label class="form-label">Diluted Shares Outstanding (Cr shares)</label>
          <span class="form-value-badge" id="lbl_shares">${d.shares_cr.toFixed(2)} Cr</span>
        </div>
        <input type="number" step="1" class="form-control" id="in_shares" value="${d.shares_cr}">
      </div>

      <div class="form-group">
        <div class="form-label-row">
          <label class="form-label">Net Worth / Book Value of Equity (₹ Cr)</label>
          <span class="form-value-badge" id="lbl_bv">₹${d.bookValue_cr.toLocaleString()} Cr</span>
        </div>
        <input type="number" step="100" class="form-control" id="in_bookValue" value="${d.bookValue_cr}">
      </div>

      <div class="form-group">
        <div class="form-label-row">
          <label class="form-label">Base Year Net Profit / PAT (₹ Cr)</label>
          <span class="form-value-badge" id="lbl_ni">₹${d.netIncome_cr.toLocaleString()} Cr</span>
        </div>
        <input type="number" step="100" class="form-control" id="in_netIncome" value="${d.netIncome_cr}">
      </div>

      <div class="input-section-title">Cost of Equity & Capital Parameters</div>
      <div class="form-group">
        <div class="form-label-row">
          <label class="form-label">Cost of Equity (Ke %) [NOT WACC]</label>
          <span class="form-value-badge" id="lbl_ke">${d.costOfEquity.toFixed(2)}%</span>
        </div>
        <div class="slider-container">
          <input type="range" min="8.0" max="20.0" step="0.1" id="sl_ke" value="${d.costOfEquity}">
          <input type="number" step="0.1" class="form-control has-suffix" style="width: 90px;" id="in_ke" value="${d.costOfEquity}">
        </div>
      </div>

      <div class="form-group">
        <div class="form-label-row">
          <label class="form-label">Capital Retention Ratio (%)</label>
          <span class="form-value-badge" id="lbl_retention">${d.retentionRatio.toFixed(1)}%</span>
        </div>
        <div class="slider-container">
          <input type="range" min="10.0" max="75.0" step="1.0" id="sl_retention" value="${d.retentionRatio}">
          <input type="number" step="1.0" class="form-control has-suffix" style="width: 90px;" id="in_retention" value="${d.retentionRatio}">
        </div>
        <span class="text-muted" style="font-size: 0.72rem;">Retained to meet RBI Tier-1 regulatory capital requirements</span>
      </div>

      <div class="form-group">
        <div class="form-label-row">
          <label class="form-label">Terminal Growth Rate (g %)</label>
          <span class="form-value-badge" id="lbl_termG">${d.termG.toFixed(2)}%</span>
        </div>
        <div class="slider-container">
          <input type="range" min="3.0" max="7.0" step="0.1" id="sl_termG" value="${d.termG}">
          <input type="number" step="0.1" class="form-control has-suffix" style="width: 90px;" id="in_termG" value="${d.termG}">
        </div>
      </div>
    `;

    bindInput('in_sharePrice', (v) => { d.sharePrice = v; document.getElementById('lbl_sharePrice').textContent = `₹${v.toFixed(2)}`; });
    bindInput('in_shares', (v) => { d.shares_cr = v; document.getElementById('lbl_shares').textContent = `${v.toFixed(2)} Cr`; });
    bindInput('in_bookValue', (v) => { d.bookValue_cr = v; document.getElementById('lbl_bv').textContent = `₹${v.toLocaleString()} Cr`; });
    bindInput('in_netIncome', (v) => { d.netIncome_cr = v; document.getElementById('lbl_ni').textContent = `₹${v.toLocaleString()} Cr`; });

    bindSliderAndInput('sl_ke', 'in_ke', (v) => { d.costOfEquity = v; document.getElementById('lbl_ke').textContent = `${v.toFixed(2)}%`; });
    bindSliderAndInput('sl_retention', 'in_retention', (v) => { d.retentionRatio = v; document.getElementById('lbl_retention').textContent = `${v.toFixed(1)}%`; });
    bindSliderAndInput('sl_termG', 'in_termG', (v) => { d.termG = v; document.getElementById('lbl_termG').textContent = `${v.toFixed(2)}%`; });
  }
}

function bindInput(id, updater) {
  const el = document.getElementById(id);
  if (!el) return;
  el.addEventListener('input', (e) => {
    const val = parseFloat(e.target.value);
    if (!isNaN(val)) {
      updater(val);
      calculateAndRender();
    }
  });
}

function bindSliderAndInput(sliderId, inputId, updater) {
  const slider = document.getElementById(sliderId);
  const input = document.getElementById(inputId);
  if (!slider || !input) return;

  slider.addEventListener('input', (e) => {
    const val = parseFloat(e.target.value);
    input.value = val;
    updater(val);
    calculateAndRender();
  });

  input.addEventListener('input', (e) => {
    const val = parseFloat(e.target.value);
    if (!isNaN(val)) {
      slider.value = val;
      updater(val);
      calculateAndRender();
    }
  });
}

// ============================================================================
// REAL-TIME SOLVER & PRESENTATION UPDATE (IN ₹ CRORE)
// ============================================================================

function calculateAndRender() {
  if (state.mode === 'non-financial') {
    calculateNonFinancial();
  } else {
    calculateFinancial();
  }
}

function calculateNonFinancial() {
  const d = state.nonFinancial;
  const netDebt_cr = d.totalDebt_cr - d.cash_cr;
  const targetEquityVal_cr = d.sharePrice * d.shares_cr; // Price * Cr shares = ₹ Cr
  const targetEV_cr = targetEquityVal_cr + netDebt_cr;    // ₹ Cr
  const wacc = d.wacc / 100;
  const termG = d.termG / 100;
  const horizon = state.horizon || 10;
  
  // Solve for BOTH 10-Yr and 20-Yr Implied Growth Rates
  const impliedCAGR10 = solveImpliedFCFFCAGR(targetEV_cr, d.baseFCFF_cr, wacc, termG, 10);
  const impliedCAGR20 = solveImpliedFCFFCAGR(targetEV_cr, d.baseFCFF_cr, wacc, termG, 20);

  // Active projection according to selected horizon
  const activeCAGR = horizon === 20 ? impliedCAGR20 : impliedCAGR10;
  const dcfOutput = calculateEVFromGrowth(activeCAGR, d.baseFCFF_cr, wacc, termG, horizon);
  const modelEquityVal_cr = dcfOutput.ev - netDebt_cr;
  const modelSharePrice = modelEquityVal_cr / d.shares_cr; // ₹ Cr / Cr shares = ₹ per share
  const convergenceDiff = Math.abs(modelSharePrice - d.sharePrice);

  // Update Top KPIs
  document.getElementById('impliedMetricLabel').textContent = 'Implied 10-Yr FCFF CAGR';
  document.getElementById('impliedMetricValue').textContent = `${(impliedCAGR10 * 100).toFixed(2)}%`;
  document.getElementById('impliedMetricSubtext').textContent = '10-yr high growth';
  
  const kpi20Label = document.getElementById('impliedMetricLabel20');
  const kpi20Val = document.getElementById('impliedMetricValue20');
  const kpi20Sub = document.getElementById('impliedMetricSubtext20');
  if (kpi20Label) kpi20Label.textContent = 'Implied 20-Yr FCFF CAGR';
  if (kpi20Val) kpi20Val.textContent = `${(impliedCAGR20 * 100).toFixed(2)}%`;
  if (kpi20Sub) kpi20Sub.textContent = '20-yr extended runway';

  document.getElementById('dispCurrentPrice').textContent = `₹${d.sharePrice.toFixed(2)}`;
  document.getElementById('dispMarketCap').textContent = `Mkt Cap: ₹${targetEquityVal_cr.toLocaleString(undefined, {maximumFractionDigits: 1})} Cr`;
  
  document.getElementById('dispConvergence').textContent = `₹${convergenceDiff.toFixed(4)} Diff`;
  document.getElementById('valuationAnchorLabel').textContent = 'Implied Enterprise Value';
  document.getElementById('dispAnchorVal').textContent = `₹${targetEV_cr.toLocaleString(undefined, {maximumFractionDigits: 1})} Cr`;
  document.getElementById('dispAnchorMeta').textContent = `PV Cash: ₹${dcfOutput.pvDiscrete.toLocaleString(undefined, {maximumFractionDigits: 1})} Cr | TV: ₹${dcfOutput.pvTV.toLocaleString(undefined, {maximumFractionDigits: 1})} Cr`;

  // Update Modal references for Excel
  const modalSet = document.getElementById('modalSetCell');
  const modalTo = document.getElementById('modalToValue');
  const modalBy = document.getElementById('modalByChanging');
  if (modalSet) modalSet.textContent = 'C29';
  if (modalTo) modalTo.textContent = d.sharePrice.toFixed(2);
  if (modalBy) modalBy.textContent = 'C20 (Implied Growth Rate %)';

  // Build projection data (in ₹ Cr) for the active horizon (10 or 20)
  const years = [];
  const projectedFCFFs = [];
  const discountFactors = [];
  const pvFCFFs = [];
  const cumPVs = [];
  let curr = d.baseFCFF_cr;
  let cumPV = 0;
  
  for (let t = 1; t <= horizon; t++) {
    years.push(`Yr ${t}`);
    curr *= (1 + activeCAGR);
    projectedFCFFs.push(parseFloat(curr.toFixed(2)));
    const df = 1 / Math.pow(1 + wacc, t);
    discountFactors.push(df.toFixed(4));
    const pv = curr * df;
    cumPV += pv;
    pvFCFFs.push(parseFloat(pv.toFixed(2)));
    cumPVs.push(parseFloat(cumPV.toFixed(2)));
  }

  // Update Chart & Tables
  document.getElementById('chartTitle').textContent = `${horizon}-Year FCFF Projection for ${state.companyName}`;
  document.getElementById('chartSubtitle').textContent = `Implied Growth: ${(activeCAGR * 100).toFixed(2)}% CAGR (${horizon}-Yr Runway) | WACC: ${d.wacc.toFixed(2)}% | Units: ₹ Crore`;
  
  renderChart(years, projectedFCFFs, pvFCFFs, `Projected FCFF (₹ Cr)`, `PV of FCFF (₹ Cr)`);
  
  renderScheduleTable(years, [
    { label: 'Projected FCFF (₹ Cr)', data: projectedFCFFs },
    { label: 'Discount Factor', data: discountFactors },
    { label: 'Present Value (₹ Cr)', data: pvFCFFs },
    { label: 'Cumulative PV (₹ Cr)', data: cumPVs }
  ]);

  renderSensitivityMatrix(d.wacc, d.termG, (w, g) => {
    return solveImpliedFCFFCAGR(targetEV_cr, d.baseFCFF_cr, w / 100, g / 100, horizon);
  }, '%', `${horizon}-Yr FCFF CAGR`);

  updateIndianRealityCheck(activeCAGR * 100);
}

function calculateFinancial() {
  const d = state.financial;
  const targetEquityVal_cr = d.sharePrice * d.shares_cr;
  const ke = d.costOfEquity / 100;
  const termG = d.termG / 100;
  const retention = d.retentionRatio / 100;
  const horizon = state.horizon || 10;
  
  // Solve for BOTH 10-Yr and 20-Yr Implied Sustainable ROE
  const impliedROE10 = solveImpliedROE(targetEquityVal_cr, d.bookValue_cr, ke, retention, termG, 10);
  const impliedROE20 = solveImpliedROE(targetEquityVal_cr, d.bookValue_cr, ke, retention, termG, 20);

  const activeROE = horizon === 20 ? impliedROE20 : impliedROE10;
  const bankOutput = calculateBankEquityFromROE(activeROE, d.bookValue_cr, ke, retention, termG, horizon);
  const modelSharePrice = bankOutput.equityValue / d.shares_cr;
  const convergenceDiff = Math.abs(modelSharePrice - d.sharePrice);

  // Update Top KPIs
  document.getElementById('impliedMetricLabel').textContent = 'Implied 10-Yr ROE';
  document.getElementById('impliedMetricValue').textContent = `${(impliedROE10 * 100).toFixed(2)}%`;
  document.getElementById('impliedMetricSubtext').textContent = '10-yr horizon';
  
  const kpi20Label = document.getElementById('impliedMetricLabel20');
  const kpi20Val = document.getElementById('impliedMetricValue20');
  const kpi20Sub = document.getElementById('impliedMetricSubtext20');
  if (kpi20Label) kpi20Label.textContent = 'Implied 20-Yr ROE';
  if (kpi20Val) kpi20Val.textContent = `${(impliedROE20 * 100).toFixed(2)}%`;
  if (kpi20Sub) kpi20Sub.textContent = '20-yr extended runway';

  document.getElementById('dispCurrentPrice').textContent = `₹${d.sharePrice.toFixed(2)}`;
  document.getElementById('dispMarketCap').textContent = `Net Worth: ₹${d.bookValue_cr.toLocaleString(undefined, {maximumFractionDigits: 1})} Cr`;
  
  document.getElementById('dispConvergence').textContent = `₹${convergenceDiff.toFixed(4)} Diff`;
  document.getElementById('valuationAnchorLabel').textContent = 'Intrinsic Equity Value';
  document.getElementById('dispAnchorVal').textContent = `₹${bankOutput.equityValue.toLocaleString(undefined, {maximumFractionDigits: 1})} Cr`;
  document.getElementById('dispAnchorMeta').textContent = `Net Worth: ₹${d.bookValue_cr.toLocaleString(undefined, {maximumFractionDigits: 1})} Cr | PV Excess: ₹${bankOutput.pvExcess.toLocaleString(undefined, {maximumFractionDigits: 1})} Cr`;

  // Update Modal references for Excel
  const modalSet = document.getElementById('modalSetCell');
  const modalTo = document.getElementById('modalToValue');
  const modalBy = document.getElementById('modalByChanging');
  if (modalSet) modalSet.textContent = 'C30';
  if (modalTo) modalTo.textContent = d.sharePrice.toFixed(2);
  if (modalBy) modalBy.textContent = 'C21 (Implied ROE %)';

  // Build projection data (in ₹ Cr) for the active horizon
  const years = [];
  const projectedBV = [];
  const netIncomes = [];
  const excessReturns = [];
  const discountFactors = [];
  const pvExcess = [];
  const cumPVExcess = [];
  let currBV = d.bookValue_cr;
  let cumPV = 0;

  for (let t = 1; t <= horizon; t++) {
    years.push(`Yr ${t}`);
    const ni = currBV * activeROE;
    const charge = currBV * ke;
    const excess = ni - charge;
    const df = 1 / Math.pow(1 + ke, t);
    const pv = excess * df;
    cumPV += pv;
    
    projectedBV.push(parseFloat(currBV.toFixed(1)));
    netIncomes.push(parseFloat(ni.toFixed(1)));
    excessReturns.push(parseFloat(excess.toFixed(1)));
    discountFactors.push(df.toFixed(4));
    pvExcess.push(parseFloat(pv.toFixed(1)));
    cumPVExcess.push(parseFloat(cumPV.toFixed(1)));
    
    currBV += ni * retention;
  }

  document.getElementById('chartTitle').textContent = `${horizon}-Year Net Profit & Excess Return for ${state.companyName}`;
  document.getElementById('chartSubtitle').textContent = `Implied ROE: ${(activeROE * 100).toFixed(2)}% (${horizon}-Yr Runway) | Cost of Equity: ${d.costOfEquity.toFixed(2)}% | Units: ₹ Crore`;
  
  renderChart(years, netIncomes, pvExcess, `Net Profit / PAT (₹ Cr)`, `PV of Excess Return (₹ Cr)`);

  renderScheduleTable(years, [
    { label: 'Net Worth / Equity (₹ Cr)', data: projectedBV },
    { label: 'Net Profit / PAT (₹ Cr)', data: netIncomes },
    { label: 'Excess Return (₹ Cr)', data: excessReturns },
    { label: 'Discount Factor', data: discountFactors },
    { label: 'PV Excess Return (₹ Cr)', data: pvExcess },
    { label: 'Cumulative PV Excess (₹ Cr)', data: cumPVExcess }
  ]);

  renderSensitivityMatrix(d.costOfEquity, d.termG, (k, g) => {
    return solveImpliedROE(targetEquityVal_cr, d.bookValue_cr, k / 100, retention, g / 100, horizon);
  }, '%', `${horizon}-Yr ROE`);

  updateBankRealityCheck(activeROE * 100, targetEquityVal_cr / d.bookValue_cr);
}

// ============================================================================
// CHART.JS RENDERER
// ============================================================================

function renderChart(labels, series1, series2, s1Name, s2Name) {
  const canvas = document.getElementById('cashflowChart');
  if (!canvas) return;

  if (state.chartInstance) {
    state.chartInstance.destroy();
  }

  const ctx = canvas.getContext('2d');
  state.chartInstance = new Chart(ctx, {
    type: 'bar',
    data: {
      labels: labels,
      datasets: [
        {
          label: s1Name,
          data: series1,
          backgroundColor: 'rgba(6, 182, 212, 0.45)',
          borderColor: '#06B6D4',
          borderWidth: 1.5,
          borderRadius: 4,
          order: 2
        },
        {
          label: s2Name,
          data: series2,
          type: 'line',
          backgroundColor: 'rgba(16, 185, 129, 0.15)',
          borderColor: '#10B981',
          borderWidth: 2.5,
          pointBackgroundColor: '#34D399',
          pointRadius: 4,
          tension: 0.3,
          order: 1
        }
      ]
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      interaction: {
        mode: 'index',
        intersect: false,
      },
      plugins: {
        legend: {
          position: 'top',
          labels: {
            color: '#94A3B8',
            font: { family: "'JetBrains Mono', monospace", size: 11 }
          }
        },
        tooltip: {
          backgroundColor: '#0F172A',
          titleColor: '#F8FAFC',
          bodyColor: '#94A3B8',
          borderColor: '#334155',
          borderWidth: 1,
          callbacks: {
            label: function(context) {
              return ` ${context.dataset.label}: ₹${context.parsed.y.toLocaleString()} Cr`;
            }
          }
        }
      },
      scales: {
        x: {
          grid: { color: 'rgba(51, 65, 85, 0.25)' },
          ticks: { color: '#94A3B8', font: { family: "'JetBrains Mono', monospace", size: 10 } }
        },
        y: {
          grid: { color: 'rgba(51, 65, 85, 0.25)' },
          ticks: {
            color: '#94A3B8',
            font: { family: "'JetBrains Mono', monospace", size: 10 },
            callback: function(v) { return `₹${v.toLocaleString()} Cr`; }
          }
        }
      }
    }
  });
}

function renderScheduleTable(years, rows) {
  const container = document.getElementById('scheduleTableContainer');
  if (!container) return;

  let html = '<table class="financial-table" id="projectionsTable"><thead><tr><th style="min-width: 220px;">Particulars (₹ Crore)</th>';
  years.forEach(y => html += `<th>${y}</th>`);
  html += '</tr></thead><tbody>';

  rows.forEach(r => {
    html += `<tr><td style="font-weight: 600; color: #F1F5F9;">${r.label}</td>`;
    r.data.forEach(val => {
      const formatted = typeof val === 'number' ? `₹${val.toLocaleString()}` : val;
      html += `<td>${formatted}</td>`;
    });
    html += '</tr>';
  });

  html += '</tbody></table>';
  container.innerHTML = html;
}

function renderSensitivityMatrix(centerDiscount, centerTermG, solverFunc, unit, metricName) {
  const container = document.getElementById('sensitivityMatrixContainer');
  if (!container) return;

  const discountDeltas = [-1.5, -0.75, 0.0, +0.75, +1.5];
  const gDeltas = [-1.0, -0.5, 0.0, +0.5, +1.0];

  const discountVals = discountDeltas.map(d => (centerDiscount + d).toFixed(2));
  const gVals = gDeltas.map(d => (centerTermG + d));
  const discountLabel = state.mode === 'non-financial' ? 'WACC' : 'Cost of Equity';

  const titleEl = document.getElementById('sensLegend');
  if (titleEl) {
    titleEl.textContent = `Sensitivity of ${metricName || 'Implied Rate'} to ${discountLabel} and Terminal Growth Rate (g)`;
  }

  let html = '<table class="sensitivity-table"><thead><tr>';
  html += `<th>${discountLabel} \\ Term g</th>`;
  gVals.forEach(g => {
    html += `<th>g = ${g.toFixed(1)}%</th>`;
  });
  html += '</tr></thead><tbody>';

  discountVals.forEach((dVal, rowIdx) => {
    html += `<tr><td style="background: rgba(30, 41, 59, 0.9); font-weight: 700; color: #94A3B8;">${dVal}%</td>`;
    gVals.forEach((gVal, colIdx) => {
      const isCenter = rowIdx === 2 && colIdx === 2;
      let solved = solverFunc(parseFloat(dVal), parseFloat(gVal.toFixed(1))) * 100;
      let displayVal = `${solved.toFixed(1)}${unit}`;
      
      let cellClass = isCenter ? 'sens-curr-cell' : '';
      let style = '';
      if (solved > 25) {
        style = 'background: rgba(239, 68, 68, 0.25); color: #FCA5A5;';
      } else if (solved > 16) {
        style = 'background: rgba(245, 158, 11, 0.2); color: #FCD34D;';
      } else if (solved > 10) {
        style = 'background: rgba(16, 185, 129, 0.2); color: #6EE7B7;';
      } else if (solved > 0) {
        style = 'background: rgba(59, 130, 246, 0.2); color: #93C5FD;';
      } else {
        style = 'background: rgba(148, 163, 184, 0.15); color: #CBD5E1;';
      }

      html += `<td class="${cellClass}" style="${style}" title="${discountLabel}: ${dVal}%, g: ${gVal.toFixed(1)}%">${displayVal}</td>`;
    });
    html += '</tr>';
  });

  html += '</tbody></table>';
  container.innerHTML = html;
}

// ============================================================================
// REALITY CHECK & BENCHMARKING COMMENTARY (CALIBRATED TO INDIAN NOMINAL GDP)
// ============================================================================

function updateIndianRealityCheck(growthRate) {
  const badge = document.getElementById('realityBadge');
  const verdict = document.getElementById('benchmarkVerdict');
  const commentary = document.getElementById('realityCommentary');
  const bar = document.getElementById('gaugeBar');

  let pct = Math.max(0, Math.min(100, (growthRate + 5) * 3));
  bar.style.left = `${pct}%`;

  if (growthRate < 0) {
    badge.textContent = 'Contraction / Distress Priced In';
    badge.className = 'badge text-rose';
    badge.style.background = 'rgba(244, 63, 94, 0.2)';
    verdict.textContent = '📉 Contrarian Turnaround Opportunity';
    commentary.innerHTML = `<strong>Priced for Decline:</strong> The Indian market is discounting a negative cash flow CAGR of <strong>${growthRate.toFixed(1)}%</strong> for <strong>${state.companyName}</strong>. If operational performance merely remains flat, the stock offers significant re-rating potential.`;
  } else if (growthRate <= 8.0) {
    badge.textContent = 'Sub-GDP Pace / Conservative';
    badge.className = 'badge text-emerald';
    badge.style.background = 'rgba(16, 185, 129, 0.2)';
    verdict.textContent = '🛡️ Modest Expectation Hurdle';
    commentary.innerHTML = `<strong>Conservative Hurdle:</strong> An implied CAGR of <strong>${growthRate.toFixed(1)}%</strong> is below India's nominal GDP growth rate (~10.5%). The company does not need to gain market share or expand operating margins to meet current market expectations.`;
  } else if (growthRate <= 15.0) {
    badge.textContent = 'India GDP Benchmark Pace';
    badge.className = 'badge badge-info';
    verdict.textContent = '⚡ Balanced Growth Hurdle';
    commentary.innerHTML = `<strong>Healthy Expansion:</strong> An implied FCFF CAGR of <strong>${growthRate.toFixed(1)}%</strong> tracks India's economic growth. Achievable through disciplined capital allocation and normalized reinvestment.`;
  } else if (growthRate <= 22.0) {
    badge.textContent = 'High Growth Outperformance';
    badge.className = 'badge';
    badge.style.background = 'rgba(245, 158, 11, 0.2)';
    badge.style.color = '#F59E0B';
    verdict.textContent = '🔥 High Expectation Hurdle';
    commentary.innerHTML = `<strong>Priced for Accelerated Expansion:</strong> The market is pricing in <strong>${growthRate.toFixed(1)}%</strong> annual FCFF growth (~1.5x to 2x nominal GDP). This demands superior capacity utilization, margin defense, and continuous order book execution.`;
  } else {
    badge.textContent = 'Hyper-Optimistic / Price for Perfection';
    badge.className = 'badge';
    badge.style.background = 'rgba(239, 68, 68, 0.25)';
    badge.style.color = '#EF4444';
    verdict.textContent = '⚠️ Extremely Demanding Hurdle';
    commentary.innerHTML = `<strong>Priced for Perfection:</strong> Compounding Free Cash Flow at <strong>${growthRate.toFixed(1)}%</strong> p.a. for a decade leaves virtually zero margin of safety against raw material inflation or demand cycles.`;
  }
}

function updateBankRealityCheck(impliedROE, pbRatio) {
  const badge = document.getElementById('realityBadge');
  const verdict = document.getElementById('benchmarkVerdict');
  const commentary = document.getElementById('realityCommentary');
  const bar = document.getElementById('gaugeBar');

  let pct = Math.max(0, Math.min(100, impliedROE * 4));
  bar.style.left = `${pct}%`;

  if (impliedROE < 11.0) {
    badge.textContent = 'Sub-Cost of Equity ROE';
    badge.className = 'badge';
    badge.style.background = 'rgba(244, 63, 94, 0.2)';
    badge.style.color = '#F43F5E';
    verdict.textContent = '📉 Below Hurdle Rate';
    commentary.innerHTML = `<strong>Discounted Valuation:</strong> At <strong>${pbRatio.toFixed(2)}x P/B</strong>, the market is pricing in an ROE of only <strong>${impliedROE.toFixed(1)}%</strong> for <strong>${state.companyName}</strong>, below the 10Y G-Sec + risk spread. Any NPA recovery or NIM expansion provides strong upside.`;
  } else if (impliedROE <= 16.0) {
    badge.textContent = 'Tier-1 Banking Benchmark';
    badge.className = 'badge badge-info';
    verdict.textContent = '⚖️ Quality Banking Hurdle';
    commentary.innerHTML = `<strong>Standard Indian Banking ROE:</strong> The market expects a sustainable <strong>${impliedROE.toFixed(1)}%</strong> ROE for <strong>${state.companyName}</strong>, in line with premier Indian commercial banks (14% - 16%).`;
  } else {
    badge.textContent = 'Elite Moat Required';
    badge.className = 'badge';
    badge.style.background = 'rgba(245, 158, 11, 0.2)';
    badge.style.color = '#F59E0B';
    verdict.textContent = '🏆 Premium Franchise Multiple';
    commentary.innerHTML = `<strong>Priced for Top-Decile Returns:</strong> At <strong>${pbRatio.toFixed(2)}x P/B</strong>, the market demands an extraordinary sustainable ROE of <strong>${impliedROE.toFixed(1)}%</strong> for <strong>${state.companyName}</strong>, requiring superior credit underwriting and low CASA deposit beta.`;
  }
}

// Modal helper
function setupModal() {
  const btn = document.getElementById('excelGuideBtn');
  const modal = document.getElementById('excelModal');
  const close = document.getElementById('closeModalBtn');

  if (btn && modal) {
    btn.addEventListener('click', () => modal.style.display = 'flex');
  }
  if (close && modal) {
    close.addEventListener('click', () => modal.style.display = 'none');
  }
  if (modal) {
    window.addEventListener('click', (e) => {
      if (e.target === modal) modal.style.display = 'none';
    });
  }
}

// Initialize on DOM load
document.addEventListener('DOMContentLoaded', init);
