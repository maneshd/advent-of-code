let fs = require("fs");

function getData(file) {
  return new Promise((resolve) =>
    fs.readFile(file, "utf8", (err, data) => resolve(data))
  );
}

async function getInput(file) {
  let data = await getData(file);
  return data
    .trim()
    .split("\n")
    .map((line) => [...line].map((ch) => parseInt(ch)));
}

function part1(input) {
  // 1=visible; 0=not (or not yet known)
  let visible = input.map((line) => new Array(line.length).fill(0));

  input.forEach((line, i) => {
    // LTR
    let max = -1;
    line.forEach((n, j) => {
      if (n > max) visible[i][j] = 1;
      max = Math.max(max, n);
    });
    // RTL
    max = -1;
    line
      .slice()
      .reverse()
      .forEach((n, j) => {
        if (n > max) visible[i][line.length - 1 - j] = 1;
        max = Math.max(max, n);
      });
  });

  // top-down
  let maxs = new Array(input.length).fill(-1);
  input.forEach((line, i) => {
    line.forEach((n, j) => {
      if (n > maxs[j]) visible[i][j] = 1;
      maxs[j] = Math.max(maxs[j], n);
    });
  });
  // bottom-up
  maxs = new Array(input.length).fill(-1);
  input
    .slice()
    .reverse()
    .forEach((line, iRev) => {
      let i = input.length - 1 - iRev;
      line.forEach((n, j) => {
        if (n > maxs[j]) visible[i][j] = 1;
        maxs[j] = Math.max(maxs[j], n);
      });
    });

  let sum = (a, b) => a + b;
  return visible.reduce((prev, line) => prev + line.reduce(sum, 0), 0);
}

function part2(inp) {
  let outOfBounds = (i, j) =>
    i < 0 || j < 0 || i >= inp.length || j >= inp[0].length;
  let dirs = [
    [-1, 0],
    [1, 0],
    [0, 1],
    [0, -1],
  ];
  let getDist = (i, j, [di, dj]) => {
    let n = inp[i][j];
    let res = 0;
    while (true) {
      [i, j] = [i + di, j + dj];
      if (outOfBounds(i, j)) return res;
      res += 1;
      if (inp[i][j] >= n) return res;
    }
  };

  let mul = (a, b) => a * b;
  let maxScore = 0;
  inp.forEach((line, i) => {
    line.forEach((_, j) => {
      let score = dirs.map((dir) => getDist(i, j, dir)).reduce(mul, 1);
      maxScore = Math.max(maxScore, score);
    });
  });
  return maxScore;
}

async function main() {
  let input = await getInput("input.txt");

  console.log("Part 1:", part1(input));
  console.log("Part 2:", part2(input));
}

main();
