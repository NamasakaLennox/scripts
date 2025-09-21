const fs = require("fs")

let text = fs.readFileSync("./trim", "utf8");
console.log(text)

text = text.replace(/\s+/g, " ");

fs.writeFileSync("out", text, "utf8");
