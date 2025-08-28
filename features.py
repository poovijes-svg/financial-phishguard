# features.py
from urllib.parse import urlparse
import re


def get_features(url):
    features = {}

    # Basic URL features
    features['url_length'] = len(url)

    try:
        parsed_url = urlparse(url)
        hostname = parsed_url.hostname
        is_ip = 1 if (hostname and re.match(r"^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$", hostname)) else 0
        features['has_ip'] = is_ip
    except:
        features['has_ip'] = 0

    features['num_special_chars'] = url.count('@') + url.count('?') + url.count('=') + url.count('-')

    return features