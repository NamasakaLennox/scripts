#!/usr/bin/env node

const cheerio = require('cheerio');

async function fetchUrlHtml(url, timeout = 10000) {
    try {
        const controller = new AbortController();
        const timeoutId = setTimeout(() => controller.abort(), timeout);

        const response = await fetch(url, { signal: controller.signal });
        clearTimeout(timeoutId);

        if (!response.ok) {
            throw new Error(`HTTP error! Status: ${response.status}`);
        }

        return await response.text();
    } catch (error) {
        console.error(`Error fetching URL '${url}': ${error.message}`);
        return null;
    }
}

function extractCharacterPositions(html) {
    const $ = cheerio.load(html);
    const positions = [];
    
    // Google Docs specific parsing
    $('table tbody tr').each((i, row) => {
        const cells = $(row).find('td');
        if (cells.length < 3) return;

        try {
            const xPos = parseInt($(cells[0]).text().trim(), 10);
            const char = $(cells[1]).text().trim();
            const yPos = parseInt($(cells[2]).text().trim(), 10);
            
            if (!isNaN(xPos) && 
                !isNaN(yPos) && 
                char.length === 1 && 
                char !== ' ' && 
                char !== '\n') {
                positions.push({ x: xPos, y: yPos, char });
            }
        } catch {
            // Skip invalid rows
        }
    });
    
    return positions;
}

function printCharacterGrid(positions) {
    if (positions.length === 0) {
        console.log("No characters to display.");
        return;
    }

    // Calculate grid boundaries
    const xs = positions.map(p => p.x);
    const ys = positions.map(p => p.y);
    const minX = Math.min(...xs);
    const maxX = Math.max(...xs);
    const minY = Math.min(...ys);
    const maxY = Math.max(...ys);

    // Create grid filled with spaces
    const grid = [];
    for (let y = minY; y <= maxY; y++) {
        grid[y - minY] = Array(maxX - minX + 1).fill(' ');
    }

    // Place characters in grid
    positions.forEach(pos => {
        const yIndex = pos.y - minY;
        const xIndex = pos.x - minX;
        if (grid[yIndex] && xIndex >= 0 && xIndex < grid[yIndex].length) {
            grid[yIndex][xIndex] = pos.char;
        }
    });

    // Print from top to bottom (reverse y-axis)
    for (let i = grid.length - 1; i >= 0; i--) {
        console.log(grid[i].join(''));
    }
}

async function fetchParseAndRender(url) {
    const html = await fetchUrlHtml(url);
    if (html) {
        const positions = extractCharacterPositions(html);
        printCharacterGrid(positions);
    }
}

// Example usage
const url = "https://docs.google.com/document/u/0/d/e/2PACX-1vTMOmshQe8YvaRXi6gEPKKlsC6UpFJSMAk4mQjLm_u1gmHdVVTaeh7nBNFBRlui0sTZ-snGwZM4DBCT/pub?pli=1&hl=en-us"
fetchParseAndRender(url);
