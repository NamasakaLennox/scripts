#!/usr/bin/env python3

import requests
from bs4 import BeautifulSoup
import re

def get_characters_from_google_doc(url):
    try:
        r = requests.get(url)
        r.raise_for_status()
    except requests.RequestException as e:
        print(f"Error: {e}")
        return

    soup = BeautifulSoup(r.content, 'html.parser')
    table = soup.find('table')
    if not table:
        print("No table found.")
        return

    pattern = re.compile(r'(\d+)(\D)(\d+)')
    chars = []

    for row in table.find_all('tr'):
        text = ''.join(cell.get_text(strip=True) for cell in row.find_all(['td', 'th']))
        if m := pattern.match(text):
            chars.append({'x': int(m[1]), 'y': int(m[3]), 'char': m[2]})

    display_grid(chars)

def display_grid(chars):
    if not chars:
        print("No characters.")
        return

    max_x = max(c['x'] for c in chars)
    max_y = max(c['y'] for c in chars)
    grid = [[' '] * (max_x + 1) for _ in range(max_y + 1)]

    for c in chars:
        grid[max_y - c['y']][c['x']] = c['char']

    print('\n'.join(''.join(row) for row in grid))


# # Run
doc_url = 'https://docs.google.com/document/d/e/2PACX-1vQGUck9HIFCyezsrBSnmENk5ieJuYwpt7YHYEzeNJkIb9OSDdx-ov2nRNReKQyey-cwJOoEKUhLmN9z/pub'
get_characters_from_google_doc(doc_url)
