#!/usr/bin/env python3

import requests
from bs4 import BeautifulSoup
import re


def fetch_characters(url):
    """Fetch characters with positions from a Google Doc table."""
    try:
        response = requests.get(url)
        response.raise_for_status()
    except requests.RequestException as e:
        print(f"Request failed: {e}")
        return []

    soup = BeautifulSoup(response.content, "html.parser")
    table = soup.find("table")
    if not table:
        print("No table found in document.")
        return []

    pattern = re.compile(r"(\d+)(\D)(\d+)")
    characters = []

    for row in table.find_all("tr"):
        row_text = "".join(cell.get_text(strip=True) for cell in row.find_all(["td", "th"]))
        match = pattern.match(row_text)
        if match:
            characters.append({
                "x": int(match.group(1)),
                "char": match.group(2),
                "y": int(match.group(3)),
            })

    return characters


def render_grid(characters):
    """Render characters in a 2D grid based on their coordinates."""
    if not characters:
        print("No characters to render.")
        return

    max_x = max(c["x"] for c in characters)
    max_y = max(c["y"] for c in characters)
    grid = [[" "] * (max_x + 1) for _ in range(max_y + 1)]

    for c in characters:
        grid[max_y - c["y"]][c["x"]] = c["char"]

    for row in grid:
        print("".join(row))


if __name__ == "__main__":
    doc_url = "https://docs.google.com/document/d/e/2PACX-1vTMOmshQe8YvaRXi6gEPKKlsC6UpFJSMAk4mQjLm_u1gmHdVVTaeh7nBNFBRlui0sTZ-snGwZM4DBCT/pub"
    chars = fetch_characters(doc_url)
    render_grid(chars)
