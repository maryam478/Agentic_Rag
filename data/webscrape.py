import requests
from bs4 import BeautifulSoup
import os

url = "https://retailservices.wellsfargo.com/customer/faqs.html"
output_file = "scraped_data.txt"

headers = {"User-Agent": "Mozilla/5.0 (compatible; MyScraper/1.0)"}

def scrape_h3_faq(url, filename):
    try:
        print(f"Scraping {url} ...")
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, "html.parser")
        faqs = []

        # Find all <h3> tags (questions)
        for h3 in soup.find_all("h3"):
            question = h3.get_text(" ", strip=True)
            answers = []

            # Collect <p> siblings until next h3/h2
            for sibling in h3.find_all_next():
                if sibling.name in ["h2", "h3"]:
                    break
                if sibling.name == "p":
                    answers.append(sibling.get_text(" ", strip=True))

            if question and answers:
                faqs.append((question, " ".join(answers)))

        # Save results
        with open(filename, "w", encoding="utf-8") as f:
            for q, a in faqs:
                f.write(f"Q: {q}\n")
                f.write(f"A: {a}\n\n")

        print(f"✅ Scraping complete. {len(faqs)} Q&A saved at: {os.path.abspath(filename)}")

    except Exception as e:
        print(f"Error scraping {url}: {e}")

scrape_h3_faq(url, output_file)
