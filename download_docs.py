import os
import requests
import json
import urllib.parse
from bs4 import BeautifulSoup

def download_file(url, target_path, headers=None):
    if os.path.exists(target_path) and os.path.getsize(target_path) > 1000:
        print(f"  [ALREADY EXISTS] {os.path.basename(target_path)}")
        return True
    if headers is None:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept': '*/*',
            'Referer': 'https://www.bseindia.com/'
        }
    try:
        print(f"  [DOWNLOADING] {os.path.basename(target_path)} from {url}...")
        res = requests.get(url, headers=headers, timeout=30)
        if res.status_code == 200 and len(res.content) > 100:
            with open(target_path, 'wb') as f:
                f.write(res.content)
            print(f"  [SAVED] {os.path.basename(target_path)} ({len(res.content):,} bytes)")
            return True
        else:
            print(f"  [FAILED] {os.path.basename(target_path)} (Status: {res.status_code}, Size: {len(res.content)})")
            return False
    except Exception as e:
        print(f"  [ERROR] {os.path.basename(target_path)}: {e}")
        return False

def main():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    docs_dir = os.path.join(base_dir, "docs")
    
    ar_dir = os.path.join(docs_dir, "Annual_Reports")
    cr_dir = os.path.join(docs_dir, "Credit_Ratings")
    pres_dir = os.path.join(docs_dir, "Presentations_and_Concalls")
    dam_dir = os.path.join(docs_dir, "Damodaran_Datasets")
    
    for d in [ar_dir, cr_dir, pres_dir, dam_dir]:
        os.makedirs(d, exist_ok=True)
        
    print("==================================================")
    print(" DOWNLOADING OFFICIAL FILINGS & DATASETS TO /docs ")
    print("==================================================")
    
    # 1. Official BSE Annual Reports (Last 6 Years)
    ar_files = [
        ("GNA_Axles_Annual_Report_2025-26.pdf", "https://www.bseindia.com/xml-data/corpfiling/AttachHis/d44291ad-cb84-4cc7-a9ff-b931c4133e40.pdf"),
        ("GNA_Axles_Annual_Report_2024-25.pdf", "https://www.bseindia.com/xml-data/corpfiling/AttachHis/bf715587-2da2-42a2-837e-91c45a1ae532.pdf"),
        ("GNA_Axles_Annual_Report_2023-24.pdf", "https://www.bseindia.com/xml-data/corpfiling/AttachHis/f9e16271-cc9e-4bb6-b439-bc6d630f2973.pdf"),
        ("GNA_Axles_Annual_Report_2022-23.pdf", "https://www.bseindia.com/xml-data/corpfiling/AttachHis/496aed0d-0d50-4f86-b1a3-fddbafa7a32c.pdf"),
        ("GNA_Axles_Annual_Report_2021-22.pdf", "https://www.bseindia.com/bseplus/AnnualReport/540124/74736540124_20_09_22.pdf"),
        ("GNA_Axles_Annual_Report_2020-21.pdf", "https://www.bseindia.com/bseplus/AnnualReport/540124/69980540124_31_08_21.pdf"),
        ("GNA_Axles_Annual_Report_2019-20.pdf", "https://www.bseindia.com/bseplus/AnnualReport/540124/64912540124.pdf")
    ]
    
    print("\n--- 1. Official Annual Reports (BSE Filings) ---")
    for fname, url in ar_files:
        download_file(url, os.path.join(ar_dir, fname))
        
    # 2. Official Rating Rationales
    cr_files = [
        ("CARE_Rating_Rationale_GNA_Axles_June_2024.pdf", "https://www.careratings.com/upload/CompanyFiles/PR/202406120614_GNA_Axles_Limited.pdf"),
        ("CARE_Rating_Rationale_GNA_Axles_July_2023.pdf", "https://www.careratings.com/upload/CompanyFiles/PR/202307130721_GNA_Axles_Limited.pdf")
    ]
    print("\n--- 2. Rating Agency Reports (CARE / ICRA) ---")
    for fname, url in cr_files:
        download_file(url, os.path.join(cr_dir, fname))
        
    # 3. Damodaran Datasets
    dam_files = [
        ("Damodaran_Country_Risk_Premium_ctryprem.xlsx", "https://pages.stern.nyu.edu/~adamodar/pc/datasets/ctryprem.xlsx"),
        ("Damodaran_Industry_Unlevered_Betas_betas.xls", "https://pages.stern.nyu.edu/~adamodar/pc/datasets/betas.xls"),
        ("Damodaran_Total_Beta_Sector_totalbeta.xls", "https://pages.stern.nyu.edu/~adamodar/pc/datasets/totalbeta.xls")
    ]
    print("\n--- 3. Damodaran Datasets (pages.stern.nyu.edu) ---")
    for fname, url in dam_files:
        download_file(url, os.path.join(dam_dir, fname), headers={'User-Agent': 'Mozilla/5.0'})
        
    # 4. Check for Investor Presentations / Concalls from BSE / Screener
    print("\n--- 4. Checking Investor Presentations & Concalls ---")
    # Let's inspect Screener or BSE
    try:
        res = requests.get('https://www.screener.in/company/GNA/consolidated/', headers={'User-Agent': 'Mozilla/5.0'})
        soup = BeautifulSoup(res.text, 'html.parser')
        cc_section = soup.select_one('.documents.concalls')
        if cc_section:
            for a in cc_section.find_all('a'):
                href = a.get('href')
                text = a.text.strip().replace('/', '-').replace('\\', '-')
                if href and href.endswith('.pdf'):
                    fname = f"{text}.pdf"
                    download_file(href, os.path.join(pres_dir, fname))
    except Exception as e:
        print(f"Error checking presentations: {e}")

    print("\nAll downloads completed!")

if __name__ == "__main__":
    main()
