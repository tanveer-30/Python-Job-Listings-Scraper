import csv
import requests
from bs4 import BeautifulSoup
URL="https://realpython.github.io/fake-jobs/"
op_file="jobs.csv"
fields=["title","company","location","url"]

def fetch_page(url):
    """Download the page and return its HTML text."""
    response=requests.get(url,timeout=10)
    response.raise_for_status()
    return response.text

def get_text(card,selector):
    """Return the stripped text of the first match, or '' if it is missing."""
    element=card.select_one(selector)
    return element.get_text(strip=True) if element else ""

def get_apply_url(card):
     """Return the 'Apply' link (the job detail page), or '' if it is missing."""
     for link in card.select("footer a"):
        if link.get_text(strip=True).lower()=="apply":
            return link.get("href","")
     return ""

def parse_jobs(html):
     """Turn the page HTML into a list of job dictionaries."""
     soup=BeautifulSoup(html,"html.parser")
     jobs=[]
     for card in soup.select("div.card-content"):
        jobs.append({
            "title":get_text(card,"h2.title"),
            "company":get_text(card,"h3.company"),
            "location":get_text(card,"p.location"),
            "url":get_apply_url(card),
        })
     return jobs

def save_to_csv(jobs,filename):
    """Write the job dictionaries to a CSV file with a header row."""
    with open(filename,"w",newline="",encoding="utf-8") as f:
        writer=csv.DictWriter(f,fieldnames=fields)
        writer.writeheader()
        writer.writerows(jobs)

def main():
    html=fetch_page(URL)
    jobs=parse_jobs(html)
    save_to_csv(jobs,op_file)
    print(f"Save {len(jobs)} jobs to {op_file}")

if __name__ == "__main__":
    main()

