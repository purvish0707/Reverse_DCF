import os
import requests
from bs4 import BeautifulSoup
import urllib.parse
import concurrent.futures

def resolve_company_url(query, headers):
    print(f"🔍 Searching Screener database for: '{query}'...")
    search_url = f"https://www.screener.in/api/company/search/?q={urllib.parse.quote(query)}"
    response = requests.get(search_url, headers=headers)
    
    if response.status_code == 200 and response.json():
        results = response.json()
        top_match = results[0]
        print(f"🎯 Found match: {top_match['name']}")
        return top_match['url'], top_match['url'].split('/')[2]
    
    return None, None

def download_pdf(task):
    """Helper function to actually download the PDF files"""
    url, filepath = task
    try:
        if url.startswith('/'):
            url = f"https://www.screener.in{url}"
            
        filename = filepath.split('/')[-1]
        
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Referer': 'https://www.screener.in/',
            'Connection': 'keep-alive'
        }
        
        response = requests.get(url, stream=True, headers=headers, timeout=15)
        
        if response.status_code == 200:
            with open(filepath, 'wb') as f:
                for chunk in response.iter_content(1024 * 1024):
                    f.write(chunk)
            print(f"  ✅ Downloaded: {filename}")
        else:
            print(f"  ❌ Failed: {filename} (Status Code: {response.status_code})")
    except Exception as e:
        print(f"  ❌ Failed to download {url}: {e}")

def scrape_screener_documents(query):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    
    company_path, ticker = resolve_company_url(query, headers)
    if not company_path:
        print(f"❌ Could not find any company matching '{query}'. Try a different name.")
        return
        
    url = f"https://www.screener.in{company_path}"
    print(f"🔗 Accessing documents at: {url}")
    
    response = requests.get(url, headers=headers)
    
    if response.status_code != 200:
        print(f"❌ Could not access company page.")
        return

    soup = BeautifulSoup(response.text, 'html.parser')
    
    script_dir = os.path.dirname(os.path.abspath(__file__))
    base_folder = os.path.join(script_dir, f"{ticker.upper()}_Documents")
    
    os.makedirs(f"{base_folder}/Annual_Reports", exist_ok=True)
    os.makedirs(f"{base_folder}/Concalls", exist_ok=True)
    os.makedirs(f"{base_folder}/Presentations", exist_ok=True)
    os.makedirs(f"{base_folder}/Credit_Ratings", exist_ok=True)

    download_tasks = []

    # 1. Annual Reports
    ar_section = soup.select_one('.documents.annual-reports')
    if ar_section:
        ar_links = ar_section.find_all('a', limit=10)
        for link in ar_links:
            title = link.text.strip().replace('/', '-').replace('\\', '-')
            filepath = f"{base_folder}/Annual_Reports/{title}.pdf"
            download_tasks.append((link.get('href'), filepath))

    # Always look for DRHP/RHP as requested
    for link in soup.find_all('a'):
        link_text = link.text.strip().upper()
        if "DRHP" in link_text or "RHP" in link_text or "PROSPECTUS" in link_text:
            title = link_text.replace('/', '-').replace('\\', '-')
            if link.get('href') and title:
                filepath = f"{base_folder}/Annual_Reports/{title}.pdf"
                if not any(t[1] == filepath for t in download_tasks):
                    download_tasks.append((link.get('href'), filepath))
                break  # Only download the first matching prospectus

    # 2. Concalls & Presentations
    concall_section = soup.select_one('.documents.concalls')
    if concall_section:
        concalls_count = 0
        presentations_count = 0
        for link in concall_section.find_all('a'):
            if concalls_count >= 15 and presentations_count >= 15:
                break
            
            title = link.text.strip().replace('\n', ' ').replace('/', '-').replace('\\', '-')
            if not title or not link.get('href'): continue
            
            # Separate PPTs from Audio/Text transcripts
            if 'ppt' in title.lower() or 'presentation' in title.lower():
                if presentations_count < 15:
                    filepath = f"{base_folder}/Presentations/{title}.pdf"
                    download_tasks.append((link.get('href'), filepath))
                    presentations_count += 1
            else:
                if concalls_count < 15:
                    filepath = f"{base_folder}/Concalls/{title}.pdf"
                    download_tasks.append((link.get('href'), filepath))
                    concalls_count += 1

    # 3. Credit Ratings
    ratings_section = soup.select_one('.documents.credit-ratings')
    if ratings_section:
        for link in ratings_section.find_all('a', limit=3):
            title = link.text.strip().replace('/', '-').replace('\\', '-')
            filepath = f"{base_folder}/Credit_Ratings/{title}.pdf"
            download_tasks.append((link.get('href'), filepath))

    print(f"\n🚀 Found {len(download_tasks)} documents. Starting parallel download...\n")
    
    # 4. Execute Parallel Downloads
    with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
        executor.map(download_pdf, download_tasks)
        
    print(f"\n✅ All downloads for {ticker.upper()} are complete! Check the '{base_folder}' folder.")
    return base_folder

if __name__ == "__main__":
    print("===========================================")
    print("  Report's Extractor (Pro Version)")
    print("===========================================")
    user_input = input("Enter the stock name or ticker (e.g., Tata Motors, HDFC Bank, RELIANCE): ")
    scrape_screener_documents(user_input.strip())
