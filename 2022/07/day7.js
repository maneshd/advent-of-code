let fs = require("fs");

function getData(file) {
  return new Promise((resolve) =>
    fs.readFile(file, "utf8", (err, data) => resolve(data))
  );
}

async function getInput(file) {
  let data = await getData(file);
  return data.trim().split("\n");
}

let makeDir = (parent) => ({ dirs: {}, files: {}, parent });

function makeTree(lines) {
  let root = makeDir(null);

  let current = root;
  lines.forEach((line, idx) => {
    if (line[0] === "$") {
      if (line === "$ ls") return;
      let [_, cmd, dirName] = line.split(" ");
      if (dirName === "/") {
        current = root;
      } else if (dirName === "..") {
        current = current.parent;
      } else {
        current = current.dirs[dirName];
      }
      return;
    }
    // listing contents of directory
    let [L, R] = line.split(" ");
    if (L === "dir") {
      if (current.dirs[R]) return;
      current.dirs[R] = makeDir(current);
    } else {
      if (current.files[R]) return;
      current.files[R] = parseInt(L);
    }
  });
  return root;
}

let add = (a, b) => a + b;

function getSize(dir) {
  if (dir.size !== undefined) return dir.size;
  dir.size =
    0 +
    Object.values(dir.files).reduce(add, 0) +
    Object.values(dir.dirs)
      .map((d) => getSize(d))
      .reduce(add, 0);
  return dir.size;
}

function part1(root) {
  return (
    (getSize(root) <= 100000 ? getSize(root) : 0) +
    Object.values(root.dirs)
      .map((d) => part1(d))
      .reduce(add, 0)
  );
}

function part2(root) {
  let freeSpace = 70000000 - getSize(root);
  let needSpace = 30000000;

  let candidates = [];
  let getCandidates = (root) => {
    if (freeSpace + getSize(root) >= needSpace) {
      candidates.push(getSize(root));
    }
    Object.values(root.dirs).forEach(d => getCandidates(d));
  };
  getCandidates(root);
  return candidates.reduce((a, b) => a < b ? a : b, 1e10);
}

async function main() {
  let input = await getInput("input.txt");
  let tree = makeTree(input);

  console.log("Part 1:", part1(tree));
  console.log("Part 2:", part2(tree));
}

main();
