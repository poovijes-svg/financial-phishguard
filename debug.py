# debug.py
test_url = "http://fake-bank-login.xyz?user=test@example.com"

# Let's manually count the characters
print("Manual character count:")
print("URL:", test_url)
print("Length:", len(test_url))

# Let's count each character type
special_chars = test_url.count('@') + test_url.count('?') + test_url.count('=') + test_url.count('-')
print("Special characters (@, ?, =, -):", special_chars)

# Let's print each character with its position
print("\nCharacter by character analysis:")
for i, char in enumerate(test_url):
    print(f"Position {i}: '{char}'")