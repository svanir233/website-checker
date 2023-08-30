import requests
import dns.resolver
from CustomResolver import CustomResolver
from telegram import Bot
import asyncio

# Telegram Bot API Token
TELEGRAM_API_TOKEN = "6591582102:AAF_v5S5X1ircq1u3YetDFlj5i7YerB58ss"
# Telegram Group Chat ID
TARGET_GROUP_CHAT_ID = 561085525
# resolv.conf Location
CUSTOM_RESOLVER_PATH = "/data/data/com.termux/files/usr/etc/resolv.conf"
# Facebook Access Token
FACEBOOK_ACCESS_TOKEN = "EAAJFyRQdRMUBOZCjvR0kKxEZBFnP35IVRM2fvldPZCpeXCTe5gp2yjaW03KxuLFcf1fIIgcxWlyAqIwizXRyLFZBBWOjEriWeqiW6f7NSjXLZAzrYOZCueQ9gZAzohofzdIZBZAcpcuLjnPyfe8YUtZBhIjSrwoX2JCunInwJT7dUnTqjOVw699CdahVZAD7nBZBIMSEa02hnx3MXECGGOd7ZB10ZD"

def check_website_status(url):
    try:
        response = requests.get(url,timeout=10)
        return response.status_code
    except requests.ConnectionError:
        return "Connection Error"

def get_a_records(domain):
    try:
        resolver = CustomResolver(CUSTOM_RESOLVER_PATH)
        answers = resolver.resolve(domain, rdtype=dns.rdatatype.A)
        return answers
    except dns.resolver.NXDOMAIN:
        return []

def get_cname_records(domain):
    try:

        resolver = CustomResolver(CUSTOM_RESOLVER_PATH)
        answers = resolver.resolve(domain, rdtype=dns.rdatatype.CNAME)
        return answers
    except dns.resolver.NXDOMAIN:
        return []
    except dns.resolver.NoAnswer:
        return []

def get_public_ip():
    try:
        response = requests.get("https://ipinfo.io",timeout=10)
        data = response.json()
        return data.get("ip", "Unknown"), data.get("org", "Unknown ISP")
    except Exception as e:
        return "Unknown", "Unknown ISP"
    
def check_facebook_status(url):
    latest_graph_api_version = "v17.0"
    api_url = f"https://graph.facebook.com/{latest_graph_api_version}/"
    params = {
        "id": url,
        "scrape": "true",
        "access_token": FACEBOOK_ACCESS_TOKEN,
    }
    try:
            response = requests.post(api_url,params=params,timeout=10)
            data = response.json()
            return response.status_code, data
    except requests.ConnectionError:
            return "Connection Error"

async def send_telegram_message(message):
    bot = Bot(token=TELEGRAM_API_TOKEN)
    await bot.send_message(chat_id=TARGET_GROUP_CHAT_ID, text=message, parse_mode='None')

async def main():

    website_urls = [
    "https://www.bet86.ph",
    "https://www.face-book.net"
    ]
    interval = 60

    while True:
        public_ip, isp = get_public_ip()
        
        for url in website_urls:
            isp_status = check_website_status(url)
            facebook_status, facebook_return = check_facebook_status(url)


            if url.startswith("https://"):
                domain = url[8:]
            else:
                domain = url

            a_records = get_a_records(domain)
            cname_records = get_cname_records(domain)

            if isp_status == 200:
                isp_status_with_emoji = "✅ Pass"
            elif isp_status == 403:
                isp_status_with_emoji = "❌ Failed"
            else:
                isp_status_with_emoji = "❓ Unknown"
            
            if facebook_status == 200:
                facebook_status_with_emoji = "✅ Pass"
            elif facebook_status == 400:
                facebook_status_with_emoji = "❌ Failed"
            else:
                facebook_status_with_emoji = "❓ Unknown"

            message = (
                f"---------- {url} Status: ----------\n\n"
                f"# Facebook Status: {facebook_status_with_emoji} (Code: {facebook_status})\n"
                f"  - API Response: {facebook_return}\n\n"
                f"# ISP Status: {isp_status_with_emoji} (Code: {isp_status})\n"
                f"  - Machine ISP: {isp}\n"
                f"  - Machine IP: {public_ip}\n\n"
                f"# DNS Lookup: \n"
            )
            
            if a_records:
                message += "## A Record:\n"
                for answer in a_records:
                    message += f"  - IP Address: {answer.address}\n"

            if cname_records:
                message += "## CNAME Record:\n"
                for answer in cname_records:
                    message += f"  - CNAME Target: {answer.target}\n"
            else:
                message += "## CNAME Record Not Found\n"

            await send_telegram_message(message)
            print (message)

        await asyncio.sleep(interval)

if __name__ == "__main__":
    asyncio.run(main())
