import requests
import dns.resolver
from src.CustomResolver import CustomResolver

class WebsiteChecker:
    def __init__(self, custom_resolver_path, facebook_access_token):
        self.custom_resolver_path = custom_resolver_path
        self.facebook_access_token = facebook_access_token

    def check_website_status(self, url):
        try:
            response = requests.get(url, timeout=10)
            return response.status_code
        except Exception as e:
            return "Connection Error"

    def get_a_records(self, domain):
        try:
            resolver = CustomResolver(self.custom_resolver_path)
            resolver.lifetime = 5.0
            answers = resolver.resolve(domain, rdtype=dns.rdatatype.A)
            return answers
        except Exception as e:
            return []

    def get_cname_records(self, domain):
        try:
            resolver = CustomResolver(self.custom_resolver_path)
            resolver.lifetime = 5.0
            answers = resolver.resolve(domain, rdtype=dns.rdatatype.CNAME)
            return answers
        except Exception as e:
            return []

    def get_public_ip(self):
        try:
            response = requests.get("https://ipinfo.io", timeout=10)
            data = response.json()
            return data.get("ip", "Unknown"), data.get("org", "Unknown ISP")
        except Exception as e:
            return "Unknown", "Unknown ISP"
    
    def check_facebook_status(self, url):
        latest_graph_api_version = "v18.0"
        api_url = f"https://graph.facebook.com/{latest_graph_api_version}/"
        params = {
            "id": url,
            "scrape": "true",
            "access_token": self.facebook_access_token,
        }
        try:
            response = requests.post(api_url, params=params, timeout=10)
            data = response.json()
            return response.status_code, data
        except Exception as e:
            return "Connection Error", {}