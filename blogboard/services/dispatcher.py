import os
import json
import logging
import requests
from typing import Dict, Any, Optional

logger = logging.getLogger(__name__)

class NotificationDispatcher:
    """
    Dispatcher service for broadcasting new article alerts to Discord, Slack,
    Telegram, and generating local social micro-content (Twitter/LinkedIn).
    """

    def __init__(self):
        self.discord_url = os.getenv("DISCORD_WEBHOOK_URL")
        self.slack_url = os.getenv("SLACK_WEBHOOK_URL")
        self.telegram_token = os.getenv("TELEGRAM_BOT_TOKEN")
        self.telegram_chat_id = os.getenv("TELEGRAM_CHAT_ID")

    def dispatch_all(self, article_data: Dict[str, Any]) -> Dict[str, bool]:
        """
        Dispatches alerts across all configured channels.
        """
        results = {
            "discord": False,
            "slack": False,
            "telegram": False,
            "social": False
        }

        title = article_data.get("title", "New Article")
        domain = article_data.get("domain", "Tech")
        slug = article_data.get("slug", "article")
        read_time = article_data.get("read_time", "5 min")
        
        logger.info(f"[DISPATCHER] Broadcasting new article: '{title}' ({domain})")

        # 1. Discord
        if self.discord_url:
            results["discord"] = self.send_discord(article_data)

        # 2. Slack
        if self.slack_url:
            results["slack"] = self.send_slack(article_data)

        # 3. Telegram
        if self.telegram_token and self.telegram_chat_id:
            results["telegram"] = self.send_telegram(article_data)

        # 4. Social Threads
        results["social"] = self.generate_social_threads(article_data)

        return results

    def send_discord(self, article: Dict[str, Any]) -> bool:
        try:
            payload = {
                "embeds": [
                    {
                        "title": f"🚀 New Article: {article.get('title')}",
                        "description": article.get("description", "Check out our latest published post on BlogBoard!"),
                        "color": 8121079,  # Purple theme
                        "fields": [
                            {"name": "Domain", "value": article.get("domain", "Tech").upper(), "inline": True},
                            {"name": "Read Time", "value": article.get("read_time", "5 min"), "inline": True},
                        ],
                        "footer": {"text": "BlogBoard Autonomous AI Publisher"}
                    }
                ]
            }
            res = requests.post(self.discord_url, json=payload, timeout=5)
            if res.status_code in [200, 204]:
                logger.info("  ✅ Discord notification sent successfully.")
                return True
        except Exception as e:
            logger.warning(f"  ⚠️ Failed to send Discord webhook: {e}")
        return False

    def send_slack(self, article: Dict[str, Any]) -> bool:
        try:
            payload = {
                "text": f"🎉 *New BlogBoard Article Published!*\n*Title:* {article.get('title')}\n*Domain:* {article.get('domain', '').upper()} | *Read Time:* {article.get('read_time')}"
            }
            res = requests.post(self.slack_url, json=payload, timeout=5)
            if res.status_code == 200:
                logger.info("  ✅ Slack notification sent successfully.")
                return True
        except Exception as e:
            logger.warning(f"  ⚠️ Failed to send Slack webhook: {e}")
        return False

    def send_telegram(self, article: Dict[str, Any]) -> bool:
        try:
            url = f"https://api.telegram.org/bot{self.telegram_token}/sendMessage"
            message = (
                f"📢 *New Article Published on BlogBoard*\n\n"
                f"📌 *{article.get('title')}*\n"
                f"🏷️ Category: #{article.get('domain')}\n"
                f"⏱️ Read Time: {article.get('read_time')}\n"
            )
            payload = {
                "chat_id": self.telegram_chat_id,
                "text": message,
                "parse_mode": "Markdown"
            }
            res = requests.post(url, json=payload, timeout=5)
            if res.status_code == 200:
                logger.info("  ✅ Telegram alert sent successfully.")
                return True
        except Exception as e:
            logger.warning(f"  ⚠️ Failed to send Telegram alert: {e}")
        return False

    def generate_social_threads(self, article: Dict[str, Any]) -> bool:
        try:
            os.makedirs("output/social", exist_ok=True)
            slug = article.get("slug", "article")
            title = article.get("title", "Article")
            domain = article.get("domain", "tech")
            
            social_data = {
                "title": title,
                "domain": domain,
                "twitter_thread": [
                    f"🧵 1/4 Excited to share our new article: '{title}'!",
                    f"💡 2/4 In this deep dive, we explore key concepts and practical implementations in #{domain}.",
                    f"📊 3/4 Read time is only {article.get('read_time', '5 min')}. Perfect for your daily learning routine.",
                    f"🔗 4/4 Check out the full article on BlogBoard! #{domain} #AI #Tech"
                ],
                "linkedin_post": (
                    f"🚀 New Publication: {title}\n\n"
                    f"We just published an in-depth article on {title} in the {domain.upper()} domain.\n\n"
                    f"Key Takeaways:\n"
                    f"• In-depth technical breakdown\n"
                    f"• Best practices and code patterns\n"
                    f"• Real-world applications\n\n"
                    f"#MachineLearning #ArtificialIntelligence #{domain.upper()} #TechBlog"
                )
            }
            
            out_file = os.path.join("output", "social", f"{slug}.json")
            with open(out_file, "w", encoding="utf-8") as f:
                json.dump(social_data, f, indent=2)

            logger.info(f"  ✅ Generated social media threads → {out_file}")
            return True
        except Exception as e:
            logger.warning(f"  ⚠️ Failed to generate social media threads: {e}")
            return False

dispatcher = NotificationDispatcher()
