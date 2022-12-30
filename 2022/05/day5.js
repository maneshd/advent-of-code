let fs = require("fs");

function getData(file) {
  return new Promise((resolve) =>
    fs.readFile(file, "utf8", (err, data) => resolve(data))
  );
}

async function getInput(file) {
  let data = await getData(file);

  let crates = new Array(10).fill(0).map((_) => []);
  let moves = [];

  let [crateLines, moveLines] = data.split("\n\n");

  crateLines
    .split("\n")
    .slice(0, -1)
    .forEach((line) => {
      for (let idx = 1; idx <= 9; idx++) {
        let i = 4 * idx - 3;
        line[i] !== " " && crates[idx].push(line[i]);
      }
    });
  crates.forEach((x) => x.reverse());

  moveLines
    .trim()
    .split("\n")
    .forEach((line) => {
      let [_, a, __, b, ___, c] = line.split(" ");
      moves.push([a, b, c].map(x=>parseInt(x)));
    });

  return [crates, moves];
}

function repeat(times, fn) {
  times > 0 && fn() && repeat(times - 1, fn);
}

function part1([crates, moves]) {
  crates = crates.map((arr) => [...arr]); // clone
  moves.forEach(([n, s, t]) => {
    repeat(n, () => crates[t].push(crates[s].pop()));
  });
  return crates.slice(1).map(arr => arr.at(-1)).join('');
}

function part2([crates, moves]) {
  crates = crates.map((arr) => [...arr]); // clone
  moves.forEach(([n, s, t]) => {
    let tmp = [];
    repeat(n, () => tmp.push(crates[s].pop()));
    repeat(n, () => crates[t].push(tmp.pop()));
  });
  return crates.slice(1).map(arr => arr.at(-1)).join('');
}

async function main() {
  let input = await getInput("input.txt");

  console.log("Part 1:", part1(input));
  console.log("Part 2:", part2(input));
}

main();
