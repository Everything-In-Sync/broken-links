import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin





sites_to_check = [
    "yahoo.com",
    "google.com"
]

def check_broken_links(websites):
        for site in websites:
            try:
                response = requests.get(f"https://{site}")
                soup = BeautifulSoup(response.content, 'html.parser')
                links = [link.get('href') for link in soup.find_all('a')]
                broken_links = []
                
                for link in links:
                    if link and not link.startswith(('/cdn-cgi/l/email-protection', 'tel:', 'mailto:')):
                        # Convert relative URL to absolute URL
                        absolute_link = urljoin(f"https://{site}", link)
                        try:
                            link_response = requests.head(absolute_link, timeout=5)
                            if link_response.status_code >= 400:
                                broken_links.append(absolute_link)
                        except requests.RequestException:
                            broken_links.append(absolute_link)  # Add to broken links if there's an error

                print(f"Broken links for {site}: {broken_links}")
            except requests.RequestException as e:
                print(f"Error accessing {site}: {e}")


check_broken_links(sites_to_check)