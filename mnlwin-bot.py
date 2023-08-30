import requests
import dns.resolver
from telegram import Bot
import websites
import asyncio

# 你的Telegram Bot的API Token
TELEGRAM_API_TOKEN = "6591582102:AAF_v5S5X1ircq1u3YetDFlj5i7YerB58ss"
# 目标Telegram群组的Chat ID
TARGET_GROUP_CHAT_ID = 561085525  # 替换为你的群组Chat ID

def check_website_status(url):
    try:
        response = requests.get(url,timeout=10)
        if response.status_code == 200:
            return "正常"
        elif response.status_code == 403:
            return "被封禁"
        else:
            return "未知状态"
    except requests.ConnectionError:
        return "连接错误"

def get_a_records(domain):
    try:
        resolver = dns.resolver.Resolver()
        answers = resolver.resolve(domain, rdtype=dns.rdatatype.A)
        return answers
    except dns.resolver.NXDOMAIN:
        return []

def get_cname_records(domain):
    try:
        resolver = dns.resolver.Resolver()
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
    
def check_if_blocked(url):
    debug_url = f"https://developers.facebook.com/tools/debug/echo/?q={url}"
    response = requests.get(debug_url,timeout=10)
    if "This Page Isn't Available" in response.text:
        return True  # Page is likely blocked
    else:
        return False  # Page is accessible

async def send_telegram_message(message):
    bot = Bot(token=TELEGRAM_API_TOKEN)
    await bot.send_message(chat_id=TARGET_GROUP_CHAT_ID, text=message, parse_mode='Markdown')

async def main():
    website_urls = [
    "https://www.bet86.ph",
    "https://www.bet86.online",
    "https://www.bet86.games",
    ]
    interval = 60

    while True:
        public_ip, isp = get_public_ip()
        
        for url in website_urls:
            response = requests.get(url,timeout=10)
            status_code = response.status_code
            is_blocked_on_facebook = check_if_blocked(url)

            if url.startswith("https://"):
                domain = url[8:]
            else:
                domain = url

            a_records = get_a_records(domain)
            cname_records = get_cname_records(domain)

            if status_code == 200:
                status_with_emoji = "✅ 正常"
            elif status_code == 403:
                status_with_emoji = "❌ 被封禁"
            else:
                status_with_emoji = "❓ 未知状态"
            if is_blocked_on_facebook:
                facebook_status = "❌ 封禁"
            else:
                facebook_status = "✅ 正常"

            print(f"\n{url} 的状态：{status_with_emoji}（状态码：{status_code}）")

            message = (
                f"# {url} 的状态：\n\n"
                f"Facebook 封禁状态：{facebook_status}\n\n"
                f"ISP 封禁状态：{status_with_emoji}（状态码：{status_code}）\n"
                f"  - 本机运营商：{isp}\n"
                f"  - 本机公共 IP：{public_ip}\n\n"
                f"## DNS 信息：\n"
            )
            
            if a_records:
                message += "### A 记录:\n"
                for answer in a_records:
                    message += f"  - IP address: {answer.address}\n"

            if cname_records:
                message += "### CNAME 记录:\n"
                for answer in cname_records:
                    message += f"  - CNAME target: {answer.target}\n"
            else:
                message += "### 没有 CNAME 记录\n"

            await send_telegram_message(message)

        await asyncio.sleep(interval)

if __name__ == "__main__":
    asyncio.run(main())