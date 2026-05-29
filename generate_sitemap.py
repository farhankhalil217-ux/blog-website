import os
import json
from datetime import datetime

DOMAIN = "https://solarmetrix.app"

# Remove the '../main-site/' prefix so it runs directly in the repo root
NEWS_INDEX = "posts/news_index.json"
EVERGREEN_INDEX = "posts/evergreen_index.json"
SITEMAP_PATH = "sitemap.xml"

def generate_sitemap():
    urls = []
    
    # 1. Main Pages
    today = datetime.utcnow().strftime('%Y-%m-%d')
    urls.append({"loc": f"{DOMAIN}/", "lastmod": today, "changefreq": "daily", "priority": "1.0"})
    urls.append({"loc": f"{DOMAIN}/post", "lastmod": today, "changefreq": "daily", "priority": "0.8"})

    # 2. News Articles
    if os.path.exists(NEWS_INDEX):
        with open(NEWS_INDEX, 'r', encoding='utf-8') as f:
            news_data = json.load(f)
            for item in news_data:
                # SEO Hack: Bypassing the original publish date to force a complete Google recrawl
                urls.append({"loc": f"{DOMAIN}/blog/{item['slug']}", "lastmod": today, "changefreq": "never", "priority": "0.7"})

    # 3. Evergreen Articles
    if os.path.exists(EVERGREEN_INDEX):
        with open(EVERGREEN_INDEX, 'r', encoding='utf-8') as f:
            evergreen_data = json.load(f)
            for item in evergreen_data:
                # SEO Hack: Bypassing the original publish date to force a complete Google recrawl
                urls.append({"loc": f"{DOMAIN}/blog/{item['slug']}", "lastmod": today, "changefreq": "monthly", "priority": "0.9"})

    # Build XML
    xml = ['<?xml version="1.0" encoding="UTF-8"?>']
    xml.append('<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">')
    for u in urls:
        xml.append(f'  <url>\n    <loc>{u["loc"]}</loc>\n    <lastmod>{u["lastmod"]}</lastmod>\n    <changefreq>{u["changefreq"]}</changefreq>\n    <priority>{u["priority"]}</priority>\n  </url>')
    xml.append('</urlset>')

    with open(SITEMAP_PATH, 'w', encoding='utf-8') as f:
        f.write('\n'.join(xml))
    print("✅ Sitemap generated successfully with forced update timestamps.")

if __name__ == "__main__":
    generate_sitemap()
