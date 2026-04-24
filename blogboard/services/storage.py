import json
import boto3
import os
from datetime import datetime
from typing import Optional, List, Dict, Any
from botocore.exceptions import ClientError
from pydantic import BaseModel

from blogboard.config.settings import app_settings

class R2StorageService:
    """
    A unified, OOP-driven storage service for Cloudflare R2.
    Replaces older, fragmented modules (db.py, storage.py, db_utils.py).
    """

    def __init__(self):
        """Initializes the R2 client or disables it if config is dummy."""
        self.bucket_name = app_settings.r2.BUCKET_NAME.strip(' ="\'')
        
        # 👉 Detect dummy config
        if "dummy" in app_settings.r2.ACCOUNT_ID.lower():
            print("[INFO] R2 storage disabled (dummy config detected)")
            self.client = None
            return

        self.client = boto3.client(
            service_name="s3",
            endpoint_url=f"https://{app_settings.r2.ACCOUNT_ID}.r2.cloudflarestorage.com",
            aws_access_key_id=app_settings.r2.ACCESS_KEY_ID,
            aws_secret_access_key=app_settings.r2.SECRET_ACCESS_KEY,
            region_name="auto"
        )

    def get_object(self, key: str) -> Optional[str]:
        if self.client is None:
            print(f"[INFO] Skipping R2 fetch → {key}")
            return None

        try:
            response = self.client.get_object(Bucket=self.bucket_name, Key=key)
            return response["Body"].read().decode("utf-8")
        except ClientError as e:
            if e.response['Error']['Code'] == 'NoSuchKey':
                return None
            print(f"[ERROR] R2 error in get_object ({key}): {e}")
            return None
        except Exception as e:
            print(f"[ERROR] Unexpected error fetching {key}: {e}")
            return None

    
    


    def put_object(self, key: str, data: str, content_type: str = "text/plain") -> bool:
        if self.client is None:
            # Create output folder
            os.makedirs("output", exist_ok=True)

            # Add timestamp to avoid overwrite
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

            # Clean filename
            filename = key.replace("/", "_")

            # Final path
            local_path = os.path.join("output", f"{timestamp}_{filename}")

            with open(local_path, "w", encoding="utf-8") as f:
                f.write(data)

            print(f"[INFO] Saved locally → {local_path}")
            return True

        try:
            self.client.put_object(
                Bucket=self.bucket_name,
                Key=key,
                Body=data.encode("utf-8"),
                ContentType=content_type
            )
            print(f"  ✅ Uploaded to R2: {self.bucket_name}/{key}")
            return True
        except Exception as e:
            print(f"[ERROR] Failed to upload {key} to R2: {e}")
            return False

    def get_json(self, key: str) -> Optional[List[Dict[str, Any]]]:
        """Fetches and parses JSON from R2."""
        data = self.get_object(key)
        if data:
            try:
                return json.loads(data)
            except json.JSONDecodeError:
                print(f"[WARN] Failed to decode JSON from {key}. Starting fresh start.")
                return []
        return []

    def get_articles_json(self, domain: str) -> List[Dict[str, Any]]:
        """Specific helper to fetch the articles registry for a domain."""
        return self.get_json(f"blogs/{domain}/articles.json") or []

    def save_articles_json(self, domain: str, articles: List[Dict[str, Any]]) -> bool:
        """Specific helper to save the articles registry for a domain."""
        json_str = json.dumps(articles, indent=2, ensure_ascii=False)
        return self.put_object(f"blogs/{domain}/articles.json", json_str, content_type="application/json")

    def get_recent_history(self, domain: str, limit: int = 3) -> List[Dict[str, Any]]:
        """Fetches the N most recent articles for a specific domain to give context."""
        articles = self.get_articles_json(domain)
        sorted_articles = sorted(articles, key=lambda x: x.get("date", ""), reverse=True)
        recent = sorted_articles[:limit]
        
        # Prune heavy data to save on prompt tokens
        return [{
            "title": a.get("title"),
            "topic": a.get("topic"),
            "subtopics": a.get("subtopics", "")
        } for a in recent]

    def get_all_domains_last_updated(self) -> Dict[str, str]:
        """Scans all domains (from config tags) and returns latest update dates."""
        latest_dates = {}
        for domain_slug in app_settings.tags.model_dump().keys(): # e.g. 'ml', 'dl'
            articles = self.get_articles_json(domain_slug)
            if not articles:
                latest_dates[domain_slug] = "Never"
            else:
                sorted_articles = sorted(articles, key=lambda x: x.get("date", ""), reverse=True)
                latest_dates[domain_slug] = sorted_articles[0].get("date", "Unknown")
        return latest_dates
