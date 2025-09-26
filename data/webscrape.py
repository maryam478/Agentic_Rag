import requests
from bs4 import BeautifulSoup

# List of websites to scrape
websites = [
    "https://lucidmotors.com/knowledge",
    "https://lucidmotors.com/knowledge/vehicles/air/the-basics/lucid-air-essentials",
    "https://www.wellsfargo.com/help/"
]

# File to save scraped content
output_file = "scraped_data.txt"

def scrape_and_save(urls, filename):
    with open(filename, "w", encoding="utf-8") as f:
        for url in urls:
            try:
                print(f"Scraping {url} ...")
                response = requests.get(url, timeout=10)
                response.raise_for_status()
                
                soup = BeautifulSoup(response.text, "html.parser")
                
                # Extract only visible text (excluding scripts/styles)
                for script in soup(["script", "style"]):
                    script.extract()
                text = soup.get_text(separator="\n", strip=True)
                
                # Write to file
                f.write(f"=== Content from {url} ===\n")
                f.write(text[:2000])  # Limit to first 2000 chars for readability
                f.write("\n\n")
            
            except Exception as e:
                print(f"Error scraping {url}: {e}")

# Run scraper
scrape_and_save(websites, output_file)

print(f"Scraping complete. Data saved in {output_file}")
