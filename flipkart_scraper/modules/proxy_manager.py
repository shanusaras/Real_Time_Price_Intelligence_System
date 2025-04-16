import requests
import random
import logging
from bs4 import BeautifulSoup

class ProxyManager:
    def __init__(self):
        self.proxies = [
            # List of reliable public HTTPS proxies
            'http://157.245.27.9:3128',
            'http://157.245.207.190:8080',
            'http://167.71.5.83:8080',
            'http://159.65.77.168:8080',
            'http://206.189.59.223:8080',
            'http://165.22.36.75:8080',
            'http://159.89.49.60:3128',
            'http://142.93.168.69:8080',
            # Add more proxies here
        ]
        self.current_proxy = None
        logging.info(f"Initialized with {len(self.proxies)} proxies")
    
    def refresh_proxies(self):
        """Refresh the list of proxies by testing them"""
        working_proxies = []
        for proxy in self.proxies:
            try:
                response = requests.get(
                    'https://www.google.com',
                    proxies={'http': proxy, 'https': proxy},
                    timeout=5
                )
                if response.status_code == 200:
                    working_proxies.append(proxy)
                    logging.info(f"Proxy {proxy} is working")
            except:
                logging.warning(f"Proxy {proxy} failed test")
                continue
        
        self.proxies = working_proxies
        logging.info(f"Refreshed proxy list. {len(self.proxies)} working proxies found")
    
    def get_proxy(self):
        """Get a random working proxy"""
        if not self.proxies:
            self.refresh_proxies()
        
        if not self.proxies:
            logging.warning("No proxies available")
            return None
        
        # Select a random proxy
        self.current_proxy = random.choice(self.proxies)
        return {
            'http': self.current_proxy,
            'https': self.current_proxy
        }
    
    def remove_current_proxy(self):
        """Remove the current proxy from the list if it's not working"""
        if self.current_proxy and self.current_proxy in self.proxies:
            self.proxies.remove(self.current_proxy)
            logging.info(f"Removed proxy {self.current_proxy}. {len(self.proxies)} remaining")
            self.current_proxy = None
