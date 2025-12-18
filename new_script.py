#!/usr/bin/env python3

import requests
from bs4 import BeautifulSoup
import re

def fetch_table_rows(doc_url):
    """Retrieve table rows from the specified Google Doc URL."""
    try:
        page_content = requests.get(doc_url).content
        document = BeautifulSoup(page_content, 'html.parser')
        first_table = document.select_one('table')
        
        if first_table is None:
            return None
        
        return first_table.find_all('tr')
    except requests.RequestException as e:
        print(f"Network error: {e}")
        return None

def parse_coordinate_data(row):
    """Extract coordinate information from a table row if it matches the expected pattern."""
    cell_text = ''.join(td.get_text(strip=True) for td in row.find_all(['td', 'th']))
    
    # Look for pattern: numbers + single character + numbers
    coord_match = re.search(r'(\d+)([^\d\s])(\d+)', cell_text)
    
    if coord_match:
        return {
            'x': int(coord_match.group(1)),
            'character': coord_match.group(2),
            'y': int(coord_match.group(3))
        }
    return None

def build_coordinate_grid(coord_list):
    """Convert list of coordinates into a display grid."""
    if not coord_list:
        print("No coordinate data available.")
        return
    
    # Determine grid boundaries
    x_bound = max(entry['x'] for entry in coord_list)
    y_bound = max(entry['y'] for entry in coord_list)
    
    # Initialize empty grid
    display_grid = [[' '] * (x_bound + 1) for _ in range(y_bound + 1)]
    
    # Populate grid with characters
    for entry in coord_list:
        display_grid[y_bound - entry['y']][entry['x']] = entry['character']
    
    # Render the grid
    for line in display_grid:
        print(''.join(line))

def main(doc_url):    
    table_rows = fetch_table_rows(doc_url)
    if not table_rows:
        return
    
    coordinate_data = []
    for row in table_rows:
        parsed_entry = parse_coordinate_data(row)
        if parsed_entry:
            coordinate_data.append(parsed_entry)
    
    build_coordinate_grid(coordinate_data)

if __name__ == "__main__":
    doc_url = 'https://docs.google.com/document/d/e/2PACX-1vRPzbNQcx5UriHSbZ-9vmsTow_R6RRe7eyAU60xIF9Dlz-vaHiHNO2TKgDi7jy4ZpTpNqM7EvEcfr_p/pub'
    main(doc_url)
