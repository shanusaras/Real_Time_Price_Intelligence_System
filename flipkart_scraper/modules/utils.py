# utils.py
import logging

# Tries multiple CSS selectors and returns the first matching text as a string

def extract_with_fallback(soup, selectors):
    for selector in selectors:
        elements = soup.select(selector)
        if elements:
            return [e.get_text(strip=True) for e in elements]
    return []  # Return [] instead of None
