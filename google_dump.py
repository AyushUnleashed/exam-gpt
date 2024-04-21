from bs4 import BeautifulSoup
import requests
import urllib.parse
from readability import Document
domain_preference = ["www.geeksforgeeks.org", "www.tutorialspoint.com", "www.javatpoint.com", "www.redhat.com"]
from collections import Counter

import re

def collapse_empty_lines(text):
    # Use regular expression to replace multiple empty lines with a single empty line
    collapsed_text = re.sub(r'\n\s*\n', '\n\n', text)

    return collapsed_text

def search_and_extract(topic):
    return f"{topic}", ""
    headers = {"User-Agent": "Mozilla/5.0"}
    search_url = "https://www.google.com/search?" + urllib.parse.urlencode({"q": topic})
    print(f"Search URL: {search_url}")
    response = requests.get(search_url, headers=headers)
    print("response:",response)
    soup = BeautifulSoup(response.text, 'html.parser')

    links = soup.find_all('a')
    print(links)
    domain_name = ''
    article_url =None
    # Searching for preferred domain
    for link in links:
        href = link.get('href')
        print(f"Found link: {href}")
        o = urllib.parse.urlparse(href)
        url_params = urllib.parse.parse_qs(o.query)
        try:
            actual_url = url_params['q'][0]
            domain = actual_url.split('//')[-1].split('/')[0]
            print(f"Extracted domain: {domain}")
            if domain in domain_preference:
                domain_name = domain
                article_url = actual_url
                print(f"Matched preferred domain: {domain}")
                break
        except:
            continue

    # Extracting text from preferred domain
    if domain_name:
        # Save the article URL to a text file
        # with open('links.txt', 'a') as file:
        #     file.write(f"q:{topic} : {article_url}" + '\n')
        # return "text", domain_name
        print(f"Fetching article from: {article_url}")
        article_response = requests.get(article_url, headers=headers)
        article_soup = BeautifulSoup(article_response.text, 'html.parser')

        # Use Readability to extract the main text content
        doc = Document(article_soup.prettify())
        google_dump = doc.summary()
        google_dump = BeautifulSoup(google_dump, 'html.parser').get_text()
        # google_dump = article_soup.get_text()
        google_dump = collapse_empty_lines(google_dump)
        info  = (google_dump[:15000] + '..') if len(google_dump) > 15000 else google_dump
        return info, domain_name

    return f"{topic}", ""

if __name__ == "__main__":
    output = search_and_extract("edit-distance")
    print(output)