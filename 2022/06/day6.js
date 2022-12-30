let fs = require("fs");

function getData(file) {
  return new Promise((resolve) =>
    fs.readFile(file, "utf8", (err, data) => resolve(data))
  );
}

async function getInput(file) {
  let data = await getData(file);
  return data.trim();
}

function allUnique(s) {
  let r = {};
  for (let c of s) {
    r[c] = r[c] ? r[c] + 1 : 1;
  }
  return Object.values(r).every(x=>x==1);

}

function partX(d, n) {
  for (let i = n; i < d.length; i++) {
    if (allUnique(d.slice(i-n, i))) {
      return i;
    }
  }
}

let part1 = (d) => partX(d, 4);
let part2 = (d) => partX(d, 14);

async function main() {
  let input = await getInput("input.txt");

  console.log("Part 1:", part1(input));
  console.log("Part 2:", part2(input));
}

main();
