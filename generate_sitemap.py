#!/usr/bin/env python3
"""
Generate sitemap index and split sitemaps for the site.
"""
import os
import math
from typing import List, Tuple
import requests
import xml.etree.ElementTree as ET
from datetime import datetime

# Configuration
BASE_URL = "https://mana.dicki.org"
API_URL = "https://manaapi.dicki.org"
OUTPUT_DIR = "website/frontend/public"
SITEMAPS_DIR = os.path.join(OUTPUT_DIR, "sitemaps")
INDEX_PATH = os.path.join(OUTPUT_DIR, "sitemap.xml")  # keep existing path as index

# Limits
URLS_PER_SITEMAP = 5000  # safe chunking well below 50k limit


def ensure_dirs():
    os.makedirs(SITEMAPS_DIR, exist_ok=True)


def iso_date_today() -> str:
    return datetime.utcnow().strftime("%Y-%m-%d")


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


def write_sitemap_chunk(urls: List[Tuple[str, str]], filename: str):
    urlset = new_urlset()
    for loc, lastmod in urls:
        add_url(urlset, loc, lastmod)
    path = os.path.join(SITEMAPS_DIR, filename)
    write_xml(urlset, path)
    return path


def new_sitemapindex():
    idx = ET.Element("sitemapindex")
    idx.set("xmlns", "http://www.sitemaps.org/schemas/sitemap/0.9")
    return idx


def add_sitemap(index: ET.Element, loc: str, lastmod: str):
    sm = ET.SubElement(index, "sitemap")
    ET.SubElement(sm, "loc").text = loc
    ET.SubElement(sm, "lastmod").text = lastmod


def slugify(value: str) -> str:
    return "".join(c if c.isalnum() or c in ("-", "_") else "_" for c in value)


def create_sitemap_index():
    ensure_dirs()
    today = iso_date_today()

    # Collect URLs grouped per novel for chunking
    groups: List[Tuple[str, List[Tuple[str, str]]]] = []  # (group_name, [(loc,lastmod)])

    # Static pages group (routes defined in router)
    static_urls = [
        (f"{BASE_URL}/", today),
        (f"{BASE_URL}/contact", today),
    ]
    groups.append(("static", static_urls))

    # Fetch novels and chapters
    try:
        resp = requests.get(f"{API_URL}/novels", timeout=30)
        resp.raise_for_status()
        novels = resp.json()
        for novel in novels:
            novel_id = novel["id"]
            novel_title = novel.get("title", f"novel_{novel_id}")
            novel_slug = slugify(str(novel_title))

            # Novel page
            novel_urls = [(f"{BASE_URL}/novels/{novel_id}", today)]

            # Chapters
            ch_resp = requests.get(f"{API_URL}/novels/{novel_id}/chapters", timeout=60)
            if ch_resp.status_code == 200:
                chapters = ch_resp.json()
                for ch in chapters:
                    number = ch.get("number")
                    if number is None:
                        continue
                    loc = f"{BASE_URL}/novels/{novel_id}/chapters/{number}"
                    novel_urls.append((loc, today))
            else:
                print(f"Warn: chapters fetch failed for novel {novel_id}: {ch_resp.status_code}")

            groups.append((f"novel_{novel_slug}", novel_urls))
    except Exception as e:
        print(f"Error fetching data from API: {e}")

    # Write child sitemaps and index
    index = new_sitemapindex()
    child_files = []
    for group_name, urls in groups:
        if not urls:
            continue
        chunks = [urls[i : i + URLS_PER_SITEMAP] for i in range(0, len(urls), URLS_PER_SITEMAP)]
        for ci, chunk in enumerate(chunks, start=1):
            fname = f"{group_name}-{ci}.xml"
            child_path = write_sitemap_chunk(chunk, fname)
            child_url = f"{BASE_URL}/sitemaps/{fname}"
            add_sitemap(index, child_url, today)
            child_files.append(child_path)

    write_xml(index, INDEX_PATH)
    print(f"Wrote sitemap index: {INDEX_PATH}")
    for p in child_files:
        print(f"Wrote child sitemap: {p}")


if __name__ == "__main__":
    create_sitemap_index()
