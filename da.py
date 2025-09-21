#!/usr/bin/env python3

import requests
from bs4 import BeautifulSoup

def fetch_url_html(url, timeout=10):
    try:
        response = requests.get(url, timeout=timeout)
        response.raise_for_status()
        return response.text
    except requests.RequestException as e:
        print(f"Error fetching URL '{url}': {e}")
        return None

def extract_character_positions(html):
    soup = BeautifulSoup(html, "html.parser")
    positions = []

    # Google Docs specific parsing
    for row in soup.select("table tbody tr"):
        cells = row.find_all("td")
        if len(cells) < 3:
            continue

        try:
            x_pos = int(cells[0].get_text(strip=True))
            char = cells[1].get_text(strip=True)
            y_pos = int(cells[2].get_text(strip=True))

            if (
                char 
                and len(char) == 1 
                and not char.isspace()
            ):
                positions.append({"x": x_pos, "y": y_pos, "char": char})
        except ValueError:
            # Skip invalid rows
            continue

    return positions

def print_character_grid(positions):
    if not positions:
        print("No characters to display.")
        return

    # Calculate grid boundaries
    xs = [p["x"] for p in positions]
    ys = [p["y"] for p in positions]
    min_x, max_x = min(xs), max(xs)
    min_y, max_y = min(ys), max(ys)

    # Create grid filled with spaces
    width = max_x - min_x + 1
    height = max_y - min_y + 1
    grid = [[" " for _ in range(width)] for _ in range(height)]

    # Place characters in grid
    for pos in positions:
        y_index = pos["y"] - min_y
        x_index = pos["x"] - min_x
        if 0 <= y_index < height and 0 <= x_index < width:
            grid[y_index][x_index] = pos["char"]

    # Print from top to bottom (reverse y-axis)
    for row in reversed(grid):
        print("".join(row))

def fetch_parse_and_render(url):
    html = fetch_url_html(url)
    if html:
        positions = extract_character_positions(html)
        print_character_grid(positions)

# Example usage
url = ""
fetch_parse_and_render(url)
