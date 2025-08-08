#!/usr/bin/env python3
"""
Generate a complete sitemap.xml for the TbateReader website
"""
import requests
import xml.etree.ElementTree as ET
from datetime import datetime

# Configuration
BASE_URL = "https://mana.dicki.org"
API_URL = "http://localhost:8001"
OUTPUT_PATH = "website/frontend/public/sitemap.xml"

def create_sitemap():
    # Create the root element
    urlset = ET.Element("urlset")
    urlset.set("xmlns", "http://www.sitemaps.org/schemas/sitemap/0.9")
    urlset.set("xmlns:xsi", "http://www.w3.org/2001/XMLSchema-instance")
    urlset.set("xsi:schemaLocation", "http://www.sitemaps.org/schemas/sitemap/0.9 http://www.sitemaps.org/schemas/sitemap/0.9/sitemap.xsd")
    
    today = datetime.now().strftime("%Y-%m-%d")
    
    # Add static pages
    static_pages = [
        {"loc": f"{BASE_URL}/", "priority": "1.0", "changefreq": "daily"},
        {"loc": f"{BASE_URL}/novels", "priority": "0.9", "changefreq": "weekly"},
    ]
    
    for page in static_pages:
        url = ET.SubElement(urlset, "url")
        ET.SubElement(url, "loc").text = page["loc"]
        ET.SubElement(url, "lastmod").text = today
        ET.SubElement(url, "changefreq").text = page["changefreq"]
        ET.SubElement(url, "priority").text = page["priority"]
    
    try:
        # Get novels from API
        response = requests.get(f"{API_URL}/novels")
        if response.status_code == 200:
            novels = response.json()
            
            for novel in novels:
                # Add novel page
                url = ET.SubElement(urlset, "url")
                ET.SubElement(url, "loc").text = f"{BASE_URL}/novels/{novel['id']}"
                ET.SubElement(url, "lastmod").text = today
                ET.SubElement(url, "changefreq").text = "weekly"
                ET.SubElement(url, "priority").text = "0.8"
                
                # Get chapters for this novel
                chapters_response = requests.get(f"{API_URL}/novels/{novel['id']}/chapters")
                if chapters_response.status_code == 200:
                    chapters = chapters_response.json()
                    
                    for chapter in chapters:
                        url = ET.SubElement(urlset, "url")
                        ET.SubElement(url, "loc").text = f"{BASE_URL}/novels/{novel['id']}/chapters/{chapter['number']}"
                        ET.SubElement(url, "lastmod").text = today
                        ET.SubElement(url, "changefreq").text = "monthly"
                        ET.SubElement(url, "priority").text = "0.7"
                        
                    print(f"Added {len(chapters)} chapters for novel: {novel['title']}")
                else:
                    print(f"Failed to fetch chapters for novel {novel['id']}")
        else:
            print(f"Failed to fetch novels: {response.status_code}")
            
    except Exception as e:
        print(f"Error fetching data from API: {e}")
        print("Creating basic sitemap with static pages only")
    
    # Create the XML tree and write to file
    tree = ET.ElementTree(urlset)
    
    # Manual indentation for older Python versions
    def indent(elem, level=0):
        i = "\n" + level * "  "
        if len(elem):
            if not elem.text or not elem.text.strip():
                elem.text = i + "  "
            if not elem.tail or not elem.tail.strip():
                elem.tail = i
            for elem in elem:
                indent(elem, level+1)
            if not elem.tail or not elem.tail.strip():
                elem.tail = i
        else:
            if level and (not elem.tail or not elem.tail.strip()):
                elem.tail = i
    
    indent(urlset)
    
    with open(OUTPUT_PATH, "wb") as f:
        tree.write(f, encoding="utf-8", xml_declaration=True)
    
    print(f"Sitemap generated successfully: {OUTPUT_PATH}")
    print(f"Total URLs: {len(urlset)}")

if __name__ == "__main__":
    create_sitemap()
