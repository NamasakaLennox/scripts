#!/usr/bin/node

const fs = require('fs')

const text = fs.readFileSync('uris.txt');
const json = JSON.parse(text)

const edges = json.data.viewer.records.edges;

const URIs = [];

for (let edge of edges) {

    let URI = edge.node.uris[0]
    URIs.push(URI)
}

console.log(URIs.length)
console.log(URIs)
fs.writeFileSync('out.txt', JSON.stringify(URIs, null, 1))
