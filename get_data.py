# get_data.py
# This is a list of well-known, legitimate bank websites
good_urls = [
    "https://www.bankofamerica.com",
    "https://www.wellsfargo.com",
    "https://www.chase.com",
    "https://www.citibank.com",
    "https://www.usbank.com",
    "https://www.pnc.com",
    "https://www.capitalone.com",
    "https://www.tdbank.com",
    "https://www.hsbc.com",
    "https://www.americanexpress.com"
]

# This is a list of known phishing URLs. I found these on PhishTank.
# !! WARNING !! - NEVER CLICK ON THESE LINKS. Just copy the text.
# Read the bad URLs from the phish_sample.txt file
with open('phish_sample.txt', 'r') as f:
    bad_urls = [line.strip() for line in f.readlines()]

# Save the good URLs to a file
with open('good_urls.txt', 'w') as f:
    for url in good_urls:
        f.write(url + '\n')

# Save the bad URLs to a file
with open('bad_urls.txt', 'w') as f:
    for url in bad_urls:
        f.write(url + '\n')

print("Saved good and bad URLs!")