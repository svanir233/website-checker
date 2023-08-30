import requests
import dns.resolver
from CustomResolver import CustomResolver
from bs4 import BeautifulSoup
from telegram import Bot
import asyncio

# 你的Telegram Bot的API Token
TELEGRAM_API_TOKEN = "6591582102:AAF_v5S5X1ircq1u3YetDFlj5i7YerB58ss"
# 目标Telegram群组的Chat ID
TARGET_GROUP_CHAT_ID = 561085525  # 替换为你的群组Chat ID
# 目标resolv.conf的位置
CUSTOM_RESOLVER_PATH = '/data/data/com.termux/files/usr/etc/resolv.conf'

def check_website_status(url):
    try:
        response = requests.get(url,timeout=10)
        return response.status_code
    except requests.ConnectionError:
        return "连接错误"

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
        return data.get("ip", "未知"), data.get("org", "未知运营商")
    except Exception as e:
        return "未知", "未知运营商"
    
def check_facebook_status(url):
    latest_graph_api_version = "v17.0"  # 替换为最新的 Graph API 版本
    user_access_token = "EAAJFyRQdRMUBOZCqZAJgmYZClkUqMwqPPjl0AQhhAnIAfNv3KLZAU7Kk1kuYUIiI3EkxkGstk5rvZADu1cg9WGf4yFbCDNku4e2joiZBOtZAl8Cowuxnzb29UroQwiBWYem4FYkPXL7u5lZBKnzQAKGaGjQuOfmqVbLnrGOop29ZBgbaSY3OIUvofZATTRbMha5nDdog1GFXyTAMcZCw2L1DgZDZD"  # 替换为你的用户访问令牌

    api_url = f"https://graph.facebook.com/{latest_graph_api_version}/"
    params = {
        "id": url,
        "scrape": "true",
        "access_token": user_access_token,
    }
    try:
            response = requests.post(api_url,params=params,timeout=10)
            data = response.json()
            return response.status_code, data
    except requests.ConnectionError:
            return "连接错误"

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
                isp_status_with_emoji = "✅ 正常"
            elif isp_status == 403:
                isp_status_with_emoji = "❌ 被封禁"
            else:
                isp_status_with_emoji = "❓ 未知状态"
            
            if facebook_status == 200:
                facebook_status_with_emoji = "✅ 正常"
            elif facebook_status == 400:
                facebook_status_with_emoji = "❌ 被封禁"
            else:
                facebook_status_with_emoji = "❓ 未知状态"

            message = (
                f"---------- {url} 的状态：----------\n\n"
                f"# Facebook 封禁状态：{facebook_status_with_emoji}（状态码：{facebook_status}）\n"
                f"  - API 返回值：{facebook_return}\n\n"
                f"# ISP 封禁状态：{isp_status_with_emoji}（状态码：{isp_status}）\n"
                f"  - 本机运营商：{isp}\n"
                f"  - 本机公共 IP：{public_ip}\n\n"
                f"# DNS 信息：\n"
            )
            
            if a_records:
                message += "## A 记录:\n"
                for answer in a_records:
                    message += f"  - IP address: {answer.address}\n"

            if cname_records:
                message += "## CNAME 记录:\n"
                for answer in cname_records:
                    message += f"  - CNAME target: {answer.target}\n"
            else:
                message += "## 没有 CNAME 记录\n"

            await send_telegram_message(message)
            print (message)

        await asyncio.sleep(interval)

if __name__ == "__main__":
    asyncio.run(main())
