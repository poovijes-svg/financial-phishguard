# features.py
import re
from urllib.parse import urlparse
import whois
from datetime import datetime
import requests
from bs4 import BeautifulSoup
import time


# Function to fetch the HTML content of a page
def get_page_content(url):
    """
    Tries to fetch the HTML content of a URL.
    Returns the BeautifulSoup object if successful, None if it fails.
    """
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    try:
        # Only wait 5 seconds for a response to avoid getting stuck
        response = requests.get(url, headers=headers, timeout=5)
        response.raise_for_status()  # Check if the request was successful
        return BeautifulSoup(response.text, 'html.parser')
    except (requests.RequestException, ConnectionError) as e:
        print(f"Failed to fetch {url}: {e}")
        return None


def get_features(url):
    features = {}

    # 1. Original URL-based Features
    features['url_length'] = len(url)
    try:
        parsed_url = urlparse(url)
        hostname = parsed_url.hostname
        is_ip = 1 if (hostname and re.match(r"^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$", hostname)) else 0
        features['has_ip'] = is_ip
    except:
        features['has_ip'] = 0
    features['num_special_chars'] = url.count('@') + url.count('?') + url.count('=') + url.count('-')
    # features['domain_age_days'] = get_domain_age(url)  # From previous step

    # 2. NEW: HTML-based Features (The Big Upgrade)
    soup = get_page_content(url)

    # Initialize all new features with a default value of 0
    new_features = {
        'num_inputs': 0,  # Number of input fields
        'num_password_inputs': 0,  # Number of password fields
        'num_links': 0,  # Number of links on the page
        'num_images': 0,  # Number of images
        'has_form': 0,  # Does the page have a form?
        'has_login_form': 0  # Does the page have a login form?
    }

    # Only try to extract HTML features if we successfully fetched the page
    if soup is not None:
        try:
            # Count all input fields (phishing sites often have many)
            inputs = soup.find_all('input')
            new_features['num_inputs'] = len(inputs)

            # Count password fields (a huge red flag)
            password_inputs = soup.find_all('input', {'type': 'password'})
            new_features['num_password_inputs'] = len(password_inputs)

            # Count all links and images
            new_features['num_links'] = len(soup.find_all('a'))
            new_features['num_images'] = len(soup.find_all('img'))

            # Check for forms
            forms = soup.find_all('form')
            new_features['has_form'] = 1 if forms else 0

            # Heuristic: If there's a password field in a form, it's likely a login form
            if new_features['num_password_inputs'] > 0 and new_features['has_form'] == 1:
                new_features['has_login_form'] = 1

        except Exception as e:
            print(f"Error parsing HTML for {url}: {e}")

    # Add all the new features to the main features dictionary
    features.update(new_features)

    return features


def get_domain_age(url):
    """ (Keep your existing get_domain_age function here) """
    try:
        parsed_url = urlparse(url)
        domain_name = parsed_url.hostname
        if domain_name and domain_name.startswith('www.'):
            domain_name = domain_name[4:]

        domain_info = whois.whois(domain_name)
        creation_date = domain_info.creation_date
        if isinstance(creation_date, list):
            creation_date = creation_date[0]

        if creation_date:
            today = datetime.now()
            age_in_days = (today - creation_date).days
            return age_in_days
        else:
            return -1
    except Exception as e:
        print(f"WHOIS lookup failed for {url}: {e}")
        return -1


# Test the new function
if __name__ == '__main__':
    test_urls = [
        "https://www.example.com",
        "https://www.github.com/login",
        "http://clearly-a-fake-phishing-site-12345.com",
    ]

    for url in test_urls:
        print(f"\nTesting: {url}")
        features = get_features(url)
        # Print only the new HTML-based features for clarity
        html_features = {k: v for k, v in features.items() if
                         k in ['num_inputs', 'num_password_inputs', 'num_links', 'has_form', 'has_login_form']}
        print(f"New HTML Features: {html_features}")
        time.sleep(2)  # Be polite to servers