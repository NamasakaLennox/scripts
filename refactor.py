#!/usr/bin/env python3

import requests
from bs4 import BeautifulSoup
import re

import requests
from bs4 import BeautifulSoup
import re

import requests
from bs4 import BeautifulSoup
import re

def get_document_table_rows(url):
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        tables = soup.find_all('table')
        if tables:
            return tables[0].find_all('tr')
    return []

def extract_coordinates_from_row(row):
    text_content = ''.join([td.get_text(strip=True) for td in row.find_all(['td', 'th'])])
    pattern = re.search(r'(\d+)(\D)(\d+)', text_content)
    if pattern:
        return {
            'horizontal': int(pattern.group(1)),
            'character': pattern.group(2),
            'vertical': int(pattern.group(3))
        }
    return None

def create_and_display_grid(coordinate_entries):
    if not coordinate_entries:
        print("No valid coordinates to display.")
        return
    
    max_horizontal = max(entry['horizontal'] for entry in coordinate_entries)
    max_vertical = max(entry['vertical'] for entry in coordinate_entries)
    
    visualization = [[' ' for _ in range(max_horizontal + 1)] for _ in range(max_vertical + 1)]
    
    for entry in coordinate_entries:
        row_position = max_vertical - entry['vertical']
        col_position = entry['horizontal']
        visualization[row_position][col_position] = entry['character']
    
    for visual_row in visualization:
        print(''.join(visual_row))

def execute_coordinate_extraction():
    document_url = 'https://docs.google.com/document/d/e/2PACX-1vRPzbNQcx5UriHSbZ-9vmsTow_R6RRe7eyAU60xIF9Dlz-vaHiHNO2TKgDi7jy4ZpTpNqM7EvEcfr_p/pub'
    
    table_rows = get_document_table_rows(document_url)
    
    coordinates = []
    for table_row in table_rows:
        extracted = extract_coordinates_from_row(table_row)
        if extracted:
            coordinates.append(extracted)
    
    create_and_display_grid(coordinates)

if __name__ == "__main__":
    execute_coordinate_extraction()