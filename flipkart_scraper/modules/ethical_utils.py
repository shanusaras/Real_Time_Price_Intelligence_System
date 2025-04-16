"""
Ethical utilities for web scraping
Implements rate limiting, robots.txt checking, and other ethical safeguards
"""
import time
import logging
import urllib.robotparser
from urllib.parse import urlparse, urljoin
import requests
from functools import wraps
import json
import os
from datetime import datetime, timedelta

logger = logging.getLogger(__name__)

class EthicalScraperConfig:
    def __init__(self):
        self.RATE_LIMIT = 1  # Minimum seconds between requests
        self.MAX_REQUESTS_PER_HOUR = 100
        self.CACHE_DURATION = timedelta(hours=6)
        self.USER_AGENT = "Educational_PriceIntelligenceBot/1.0 (Educational Project; Contact: your@email.com)"
        self.CACHE_DIR = "cache"
        
        # Create cache directory if it doesn't exist
        if not os.path.exists(self.CACHE_DIR):
            os.makedirs(self.CACHE_DIR)
        
        # Initialize request tracking
        self.last_request_time = 0
        self.request_count = 0
        self.request_reset_time = datetime.now()

config = EthicalScraperConfig()

def check_robots_txt(url):
    """Check if URL is allowed by robots.txt"""
    logger.debug(f"[robots.txt] Checking robots.txt for URL: {url}")
    if not url or not isinstance(url, str) or url.strip() == '' or url.startswith('/'):
        logger.error(f"[robots.txt] Invalid URL for robots.txt check: {url}")
        return False
    try:
        rp = urllib.robotparser.RobotFileParser()
        domain = str(urlparse(url).scheme) + "://" + str(urlparse(url).netloc)
        robots_url = urljoin(domain, "/robots.txt")
        if isinstance(robots_url, bytes):
            robots_url = robots_url.decode('utf-8')
        rp.set_url(str(robots_url))
        rp.read()
        return rp.can_fetch(str(config.USER_AGENT), str(url))
    except Exception as e:
        logger.warning(f"Could not check robots.txt: {e}")
        return True  # Fail open but log the error


def get_cache_key(url, params=None):
    """Generate a cache key from URL and parameters"""
    if url is None:
        key = "no_url"
    else:
        key = url
    if params:
        key += "_" + json.dumps(params, sort_keys=True)
    return key.replace("/", "_").replace(":", "_")


def get_cached_response(cache_key):
    """Get cached response if it exists and is not expired"""
    cache_file = os.path.join(config.CACHE_DIR, f"{cache_key}.json")
    if os.path.exists(cache_file):
        with open(cache_file, 'r') as f:
            cache_data = json.load(f)
        cached_time = datetime.fromisoformat(cache_data['timestamp'])
        if datetime.now() - cached_time < config.CACHE_DURATION:
            return cache_data['content']
    return None

def cache_response(cache_key, content):
    """Cache response content"""
    cache_file = os.path.join(config.CACHE_DIR, f"{cache_key}.json")
    cache_data = {
        'timestamp': datetime.now().isoformat(),
        'content': content
    }
    with open(cache_file, 'w') as f:
        json.dump(cache_data, f)

def ethical_scraping_decorator(func):
    """Decorator to enforce ethical scraping practices (URL must be passed explicitly as a keyword argument)"""
    @wraps(func)
    def wrapper(*args, **kwargs):
        url = kwargs.get('url', None)
        logger.debug(f"[decorator] Entered decorator for {func.__name__}, url={url}")
        if not url or not isinstance(url, str) or url.strip() == '' or url.startswith('/'):
            logger.error(f"[decorator] Invalid or missing URL for {func.__name__}: {url}")
            return None
        logger.debug(f"[decorator] Checking robots.txt for url={url}")
        if not check_robots_txt(url):
            logger.error(f"URL {url} is not allowed by robots.txt")
            return None
        # Rate limiting
        current_time = time.time()
        time_since_last_request = current_time - config.last_request_time
        if time_since_last_request < config.RATE_LIMIT:
            logger.debug(f"[decorator] Rate limit hit, sleeping for {config.RATE_LIMIT - time_since_last_request:.2f}s")
            time.sleep(config.RATE_LIMIT - time_since_last_request)
        # Hourly limit
        if datetime.now() - config.request_reset_time > timedelta(hours=1):
            config.request_count = 0
            config.request_reset_time = datetime.now()
        if config.request_count >= config.MAX_REQUESTS_PER_HOUR:
            logger.error("Hourly request limit reached")
            return None
        config.last_request_time = time.time()
        config.request_count += 1
        # Caching
        logger.debug(f"[decorator] Checking cache for url={url}")
        cache_key = get_cache_key(url, kwargs.get('params'))
        cached_response = get_cached_response(cache_key)
        if cached_response:
            logger.info(f"Using cached response for {url}")
            return cached_response
        logger.debug(f"[decorator] Calling wrapped function {func.__name__} with url={url}")
        response = func(*args, **kwargs)
        if response:
            cache_response(cache_key, response)
            logger.debug(f"[decorator] Cached response for url={url}")
        return response
    return wrapper
