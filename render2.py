#!/usr/bin/env python3

import requests
from bs4 import BeautifulSoup
from collections import defaultdict
from typing import List, Dict, Tuple, Optional

def fetch_url_html(url: str, timeout: int = 10) -> Optional[str]:
    """Fetch HTML content from a URL."""
    try:
        response = requests.get(url, timeout=timeout)
        response.raise_for_status()
        return response.text
    except requests.RequestException as error:
        print(f"Error fetching URL '{url}': {error}")
        return None

def extract_character_positions(html: str) -> List[Dict[str, int | str]]:
    """Extract character positions from the first table in the HTML."""
    soup = BeautifulSoup(html, 'html.parser')
    table = soup.find('table')
    if not table:
        print("No table found in the document.")
        return []

    positions = []
    for row in table.find_all('tr'):
        cells = row.find_all(['td', 'th'])
        if len(cells) < 3:
            continue
        try:
            x_pos = int(cells[0].get_text(strip=True))
            character = cells[1].get_text(strip=True)
            y_pos = int(cells[2].get_text(strip=True))
            if len(character) == 1:
                positions.append({"x": x_pos, "y": y_pos, "char": character})
        except (ValueError, IndexError):
            continue
    return positions

def print_character_grid(positions: List[Dict[str, int | str]]) -> None:
    """Print a grid of characters based on their x, y positions."""
    if not positions:
        print("No characters to display.")
        return

    min_x = min(pos["x"] for pos in positions)
    max_x = max(pos["x"] for pos in positions)
    min_y = min(pos["y"] for pos in positions)
    max_y = max(pos["y"] for pos in positions)

    grid: defaultdict[Tuple[int, int], str] = defaultdict(lambda: ' ')
    for pos in positions:
        grid[(pos["x"], pos["y"])] = pos["char"]

    for y in reversed(range(min_y, max_y + 1)):
        row = "".join(grid[(x, y)] for x in range(min_x, max_x + 1))
        print(row)

def fetch_parse_and_render(url: str) -> None:
    """Fetch, parse, and render character data from a document URL."""
    html = fetch_url_html(url)
    if html:
        positions = extract_character_positions(html)
        print_character_grid(positions)

# Example usage:
url = "https://docs.google.com/document/d/e/2PACX-1vQGUck9HIFCyezsrBSnmENk5ieJuYwpt7YHYEzeNJkIb9OSDdx-ov2nRNReKQyey-cwJOoEKUhLmN9z/pub"
fetch_parse_and_render(url)
