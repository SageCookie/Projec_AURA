import asyncio
import json
from datetime import datetime
from crawl4ai import AsyncWebCrawler, BrowserConfig, CrawlerRunConfig, RateLimiter, CacheMode
from crawl4ai.async_dispatcher import MemoryAdaptiveDispatcher
from datetime import datetime, timezone

# Mapping User Requirements to Config
def get_user_run_config(requirements: dict):
    return CrawlerRunConfig(
        # Asset Filtering
        exclude_external_images=not requirements.get("include_images", False),
        # Noise Removal
        excluded_tags=requirements.get("exclude_tags", ["nav", "footer", "header", "aside"]),
        word_count_threshold=requirements.get("min_word_count", 20),
        # Dynamic Content
        scan_full_page=requirements.get("deep_scan", True),
        scroll_delay=0.8 if requirements.get("deep_scan") else 0,
        # Cache & Error Handling
        cache_mode=CacheMode.BYPASS,
        stream=True
    )

async def automated_collector(urls: list[str], user_prefs: dict):
    # Browser setup for "Staying under the radar"
    browser_cfg = BrowserConfig(
        browser_type="chromium",
        headless=True,
        enable_stealth=True,  # Crucial for anti-bot
        headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/120.0.0.0 Safari/537.36"}
    )

    # Dispatcher setup for "16GB RAM Optimization"
    dispatcher = MemoryAdaptiveDispatcher(
        memory_threshold_percent=80.0, # Slow down if RAM > 12.8GB
        max_session_permit=5,          # Limit tabs to 5
        rate_limiter=RateLimiter(base_delay=(3.0, 7.0)) # Randomize timing
    )

    results = []

    async with AsyncWebCrawler(config=browser_cfg) as crawler:
        run_config = get_user_run_config(user_prefs)
        
        # Batch process URLs
        async for result in await crawler.arun_many(
            urls=urls,
            config=run_config,
            dispatcher=dispatcher
        ) :
            # Detailed Error Reporting
            error_info = ""
            status = result.status_code if result.status_code else "UNKNOWN"
            
            if not result.success:
                # Capture why it failed
                error_info = f"[CRAWL_FAILED] Status: {status} | Reason: {result.error_message}"
            
            # Construct the exact JSON format requested
            data_packet = {
                "title": result.metadata.get("title", "No Title") if result.success else f"Error: {result.url}",
                "url": result.url,
                "raw_content": result.markdown if result.success else error_info,
                "summary": "Pending LLM processing...", 
                "tech_score": 0,
                "category": "Pending...",
                "timestamp": datetime.now(timezone.utcoffset).isoformat()
            }
            results.append(data_packet)

    return results

# Example simulation of a User Request
if __name__ == "__main__":
    user_urls = [
        "https://intellipaat.com/blog/how-to-determine-the-url-that-a-local-git-repository-was-originally-cloned-from/", 
        "https://invalid-url-test.xyz", # To test error handling
        "https://www.python.org/static/files/pubkeys.txt" # Non-HTML example
    ]
    
    # Requirements defined by the User in your future UI
    requirements = {
        "include_images": False,
        "deep_scan": True,
        "exclude_tags": ["nav", "footer", "script", "style"]
    }

    # Final logic would be:
    print("🚀 AURA Collector starting...")
    final_output = asyncio.run(automated_collector(user_urls, requirements))
    print(json.dumps(final_output, indent=2))
    print("\n✅ Scraping Complete.")