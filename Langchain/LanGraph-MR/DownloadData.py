#!/usr/bin/env python3
"""
Sitemap Page Downloader

This script downloads a sitemap.xml file from a URL and then downloads all pages
listed in it, saving each page as a separate HTML file.
"""

import xml.etree.ElementTree as ET
import requests
import os
import re
import time
from urllib.parse import urlparse, unquote
from pathlib import Path

from langchain_community.document_loaders import WebBaseLoader


def sanitize_filename(url):
    """Convert URL to a safe filename"""
    # Parse the URL
    parsed = urlparse(url)

    # Create filename from domain and path
    domain = parsed.netloc.replace('www.', '')
    path = parsed.path.strip('/')

    if not path:
        filename = f"{domain}_homepage"
    else:
        # Replace path separators and special characters
        path = path.replace('/', '_').replace('\\', '_')
        filename = f"{domain}_{path}"

    # Remove or replace invalid filename characters
    filename = re.sub(r'[<>:"/\\|?*]', '_', filename)
    filename = re.sub(r'[^\w\-_.]', '_', filename)
    filename = re.sub(r'_+', '_', filename)  # Replace multiple underscores

    # Ensure filename isn't too long (limit to 200 chars)
    if len(filename) > 200:
        filename = filename[:200]

    return filename + '.html'


def parse_sitemap(sitemap_url, session):
    """Download and parse sitemap.xml from URL and extract all URLs"""
    urls = []

    try:
        print(f"Downloading sitemap from: {sitemap_url}")
        response = session.get(sitemap_url,  timeout=30)
        response.raise_for_status()

        # Parse XML from response content
        root = ET.fromstring(response.content)

        # Handle namespace if present
        namespace = ''
        if root.tag.startswith('{'):
            namespace = root.tag.split('}')[0] + '}'

        # Find all URL elements
        url_elements = root.findall(f'.//{namespace}url')

        for url_elem in url_elements:
            loc_elem = url_elem.find(f'{namespace}loc')
            if loc_elem is not None and loc_elem.text:
                urls.append(loc_elem.text.strip())

        # If no URLs found with standard sitemap format, try simple XML structure
        if not urls:
            for elem in root.iter():
                if elem.text and (elem.text.startswith('http://') or elem.text.startswith('https://')):
                    urls.append(elem.text.strip())

    except ET.ParseError as e:
        print(f"Error parsing XML: {e}")
        return []
    except requests.exceptions.RequestException as e:
        print(f"Error downloading sitemap: {e}")
        return []
    except Exception as e:
        print(f"Unexpected error: {e}")
        return []

    return urls


def download_page(url, output_dir, session, delay=1):
    """Download a single page and save it to a file"""
    try:
        print(f"Downloading: {url}")
        response = session.get(url, timeout=30)
        response.raise_for_status()

        # Generate filename
        filename = sanitize_filename(url)
        filepath = os.path.join(output_dir, filename)

        # Ensure unique filename if file already exists
        counter = 1
        original_filepath = filepath
        while os.path.exists(filepath):
            name, ext = os.path.splitext(original_filepath)
            filepath = f"{name}_{counter}{ext}"
            counter += 1

        # Save the content
        with open(filepath, 'w', encoding='utf-8', errors='ignore') as f:
            f.write(response.text)

        print(f"Saved: {filename}")

        # Add delay to be respectful to the server
        time.sleep(delay)

        return True

    except requests.exceptions.RequestException as e:
        print(f"Error downloading {url}: {e}")
        return False
    except Exception as e:
        print(f"Unexpected error downloading {url}: {e}")
        return False


def main():
    """Main function to orchestrate the download process"""
    # Configuration
    sitemap_url = 'https://mountainreview.com/review-sitemap.xml'  # Sitemap URL to download
    output_directory = 'downloaded_pages'  # Directory to save downloaded pages
    delay_between_requests = 1  # Seconds to wait between requests

    print("Sitemap Page Downloader")
    print("=" * 50)

    # Create output directory
    Path(output_directory).mkdir(exist_ok=True)

    # Create session for connection reuse
    session = requests.Session()

    # Parse sitemap
    print(f"Fetching sitemap from: {sitemap_url}")
    urls = parse_sitemap(sitemap_url, session)

    if not urls:
        print("No URLs found in sitemap!")
        return

    print(f"Found {len(urls)} URLs to download")
    print(f"Output directory: {output_directory}")
    print("-" * 50)

    # Download pages
    successful_downloads = 0
    failed_downloads = 0

    for i, url in enumerate(urls, 1):
        print(f"[{i}/{len(urls)}] ", end="")

        if download_page(url, output_directory, session, delay_between_requests):
            successful_downloads += 1
        else:
            failed_downloads += 1

    # Summary
    print("-" * 50)
    print(f"Download completed!")
    print(f"Successful downloads: {successful_downloads}")
    print(f"Failed downloads: {failed_downloads}")
    print(f"Total URLs processed: {len(urls)}")
    print(f"Files saved to: {output_directory}")


from langchain_community.document_loaders import WebBaseLoader

page_url = "https://mountainreview.com/it/recensione/guscio-vaude-larice-25l-jacket-ii/"

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3",
    "language" : "it-IT,it;q=0.9,en-US;q=0.8,en;q=0.7"
    }

loader = WebBaseLoader(web_paths=[page_url],header_template=headers)
docs = []
for doc in loader.lazy_load():
    docs.append(doc)

print(docs[0])

