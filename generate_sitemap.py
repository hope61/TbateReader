#!/usr/bin/env python3
"""
Generate a single consolidated sitemap for the site.
"""
import os
import requests
import xml.etree.ElementTree as ET
from datetime import datetime, timezone

# Configuration
BASE_URL = "https://mana.dicki.org"
API_URL = "https://manaapi.dicki.org"
OUTPUT_DIR = "website/frontend/public"
INDEX_PATH = os.path.join(OUTPUT_DIR, "sitemap.xml")

# Limits
MAX_URLS_PER_SITEMAP = 50000  # Google's limit for a single sitemap


def ensure_dirs():
    os.makedirs(OUTPUT_DIR, exist_ok=True)


def iso_date_today() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%d")


def new_urlset():
    urlset = ET.Element("urlset")
    urlset.set("xmlns", "http://www.sitemaps.org/schemas/sitemap/0.9")
    return urlset


def write_xml(elem: ET.Element, path: str):
    def indent(e, level=0):
        i = "\n" + level * "  "
        if len(e):
            if not e.text or not e.text.strip():
                e.text = i + "  "
            for child in e:
                indent(child, level + 1)
            if not e.tail or not e.tail.strip():
                e.tail = i
        else:
            if level and (not e.tail or not e.tail.strip()):
                e.tail = i

    indent(elem)
    tree = ET.ElementTree(elem)
    with open(path, "wb") as f:
        tree.write(f, encoding="utf-8", xml_declaration=True)


def add_url(urlset: ET.Element, loc: str, lastmod: str):
    url = ET.SubElement(urlset, "url")
    ET.SubElement(url, "loc").text = loc
    ET.SubElement(url, "lastmod").text = lastmod


def create_consolidated_sitemap():
    ensure_dirs()
    today = iso_date_today()

    # Create single urlset for all URLs
    urlset = new_urlset()

    # Add static pages
    static_urls = [
        (f"{BASE_URL}/", today),
        (f"{BASE_URL}/contact", today),
    ]
    
    for loc, lastmod in static_urls:
        add_url(urlset, loc, lastmod)

    # Fetch novels and add only novel list pages (not individual chapters)
    try:
        resp = requests.get(f"{API_URL}/novels", timeout=30)
        resp.raise_for_status()
        novels = resp.json()
        
        for novel in novels:
            novel_id = novel["id"]
            
            # Only add novel list pages - skip individual chapter pages
            novel_url = f"{BASE_URL}/novels/{novel_id}"
            add_url(urlset, novel_url, today)
                
    except Exception as e:
        print(f"Error fetching data from API: {e}")

    # Check if we exceed the single sitemap limit
    total_urls = len(urlset.findall("url"))
    if total_urls > MAX_URLS_PER_SITEMAP:
        print(f"Warning: {total_urls} URLs exceed the single sitemap limit of {MAX_URLS_PER_SITEMAP}")
        print("Consider splitting into multiple sitemaps or reducing content")
    
    # Write the consolidated sitemap
    write_xml(urlset, INDEX_PATH)
    print(f"Wrote consolidated sitemap: {INDEX_PATH}")
    print(f"Total URLs: {total_urls}")


if __name__ == "__main__":
    create_consolidated_sitemap()
