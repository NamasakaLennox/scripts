#!/usr/bin/env node

const axios = require("axios");
const cheerio = require("cheerio");

const DEFAULT_TIMEOUT = 10_000;

/**
 * Fetch raw HTML from a URL
 */
async function fetchHtml(url, timeout = DEFAULT_TIMEOUT) {
  try {
    const { data } = await axios.get(url, { timeout });
    return data;
  } catch (err) {
    console.error(`Failed to fetch "${url}": ${err.message}`);
    return null;
  }
}

/**
 * Extract character positions from a Google Docs–style table
 */
function parseCharacterPositions(html) {
  const $ = cheerio.load(html);
  const positions = [];

  $("table tbody tr").each((_, row) => {
    const cells = $(row).find("td");
    if (cells.length < 3) return;

    const x = Number.parseInt($(cells[0]).text().trim(), 10);
    const char = $(cells[1]).text().trim();
    const y = Number.parseInt($(cells[2]).text().trim(), 10);

    if (
      Number.isNaN(x) ||
      Number.isNaN(y) ||
      char.length !== 1 ||
      char === " " ||
      char === "\n"
    ) {
      return;
    }

    positions.push({ x, y, char });
  });

  return positions;
}

/**
 * Render character positions to a console grid
 */
function renderGrid(positions) {
  if (!positions.length) {
    console.log("No characters to display.");
    return;
  }

  const xs = positions.map((p) => p.x);
  const ys = positions.map((p) => p.y);

  const minX = Math.min(...xs);
  const maxX = Math.max(...xs);
  const minY = Math.min(...ys);
  const maxY = Math.max(...ys);

  const width = maxX - minX + 1;
  const height = maxY - minY + 1;

  const grid = Array.from({ length: height }, () => Array(width).fill(" "));

  for (const { x, y, char } of positions) {
    const row = y - minY;
    const col = x - minX;
    grid[row][col] = char;
  }

  // Print top-to-bottom (invert Y-axis)
  for (let row = grid.length - 1; row >= 0; row--) {
    console.log(grid[row].join(""));
  }
}

/**
 * Fetch, parse, and render characters from a URL
 */
async function fetchParseAndRender(url) {
  const html = await fetchHtml(url);
  if (!html) return;

  const positions = parseCharacterPositions(html);
  renderGrid(positions);
}

/* Example usage */
const url =
  "https://docs.google.com/document/d/e/2PACX-1vRPzbNQcx5UriHSbZ-9vmsTow_R6RRe7eyAU60xIF9Dlz-vaHiHNO2TKgDi7jy4ZpTpNqM7EvEcfr_p/pub";

fetchParseAndRender(url);
