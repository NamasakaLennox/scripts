import requests
from bs4 import BeautifulSoup
import re

# Removed List, Dict, Any, and CharPosition type hints as requested

def fetch_url_html(url, timeout=10):
    try:
        response = requests.get(url, timeout=timeout)
        response.raise_for_status()
        return response.text
    except requests.exceptions.RequestException as e:
        # Replaced sys.stderr with a standard print statement
        print(f"Error fetching URL '{url}': {e}")
        return None

def extract_character_positions(html):
    soup = BeautifulSoup(html, 'html.parser')
    positions = []
    
    for row in soup.find_all('tr'):
        cells = row.find_all('td')
        if len(cells) < 3:
            continue

        try:
            x_text = cells[0].get_text(strip=True)
            char = cells[1].get_text(strip=True)
            y_text = cells[2].get_text(strip=True)
            
            # Using re.fullmatch for digit check, since we removed .isdigit() check on string
            # and rely on the int() conversion which handles standard integer strings.
            # However, the original JS check was on the text before conversion.
            # We revert to explicit string check using re.
            
            if (not re.fullmatch(r'\d+', x_text) or 
                not re.fullmatch(r'\d+', y_text) or 
                len(char) != 1 or
                char == ' ' or 
                char == '\n'):
                continue

            x_pos = int(x_text)
            y_pos = int(y_text)
            
            positions.append({'x': x_pos, 'y': y_pos, 'char': char})
            
        except ValueError:
            continue
        except IndexError:
            continue
            
    return positions

def print_character_grid(positions):
    if not positions:
        print("No characters to display.")
        return

    # 1. Calculate grid boundaries
    xs = [p['x'] for p in positions]
    ys = [p['y'] for p in positions]
    min_x, max_x = min(xs), max(xs)
    min_y, max_y = min(ys), max(ys)
    
    width = max_x - min_x + 1
    height = max_y - min_y + 1

    # 2. Create grid (list of lists) filled with spaces
    grid = [[' ' for _ in range(width)] for _ in range(height)]

    # 3. Place characters in grid
    for pos in positions:
        y_index = pos['y'] - min_y
        x_index = pos['x'] - min_x
        
        if 0 <= y_index < height and 0 <= x_index < width:
            grid[y_index][x_index] = pos['char']

    # 4. Print from top to bottom (reverse y-axis)
    for row in reversed(grid):
        print("".join(row))

def fetch_parse_and_render(url):
    html = fetch_url_html(url)
    if html:
        positions = extract_character_positions(html)
        print_character_grid(positions)

if __name__ == '__main__':
    url = "https://docs.google.com/document/d/e/2PACX-1vRPzbNQcx5UriHSbZ-9vmsTow_R6RRe7eyAU60xIF9Dlz-vaHiHNO2TKgDi7jy4ZpTpNqM7EvEcfr_p/pub"
    
    print(f"Fetching and parsing data from: {url}\n")
    fetch_parse_and_render(url)
