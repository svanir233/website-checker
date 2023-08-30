import asyncio
from ConfigLoader import ConfigLoader
from WebsiteChecker import WebsiteChecker
from TelegramBot import TelegramBot

async def main():
    #LOAD CONFIG
    config = ConfigLoader.load_config('config.json')
    if not config:
        print("No valid config found. Exiting...")
        return

    #INSTANTIATE
    website_checker = WebsiteChecker(config["custom_resolver_path"], config["facebook_access_token"])
    telegram_bot = TelegramBot(config["telegram_api_token"])

    #ALGORITHM
    while True:
        public_ip, isp = website_checker.get_public_ip()
        
        for url in config["website_urls"]:
            isp_status = website_checker.check_website_status(url)
            facebook_status, facebook_return = website_checker.check_facebook_status(url)

            if url.startswith("https://"):
                domain = url[8:]
            else:
                domain = url

            a_records = website_checker.get_a_records(domain)
            cname_records = website_checker.get_cname_records(domain)

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

            await telegram_bot.send_message(config["telegram_chat_id"], message, parse_mode='None')
            print(message)

        await asyncio.sleep(int(config["interval"]))

if __name__ == "__main__":
    asyncio.run(main())
