import fs from 'fs';
import path from 'path';

const workspaceRoot = process.cwd();
const projectsDir = path.join(workspaceRoot, 'src/app/work/projects');
const publicDir = path.join(workspaceRoot, 'public');
const SIMILARITY_THRESHOLD = 0.8;

const args = process.argv.slice(2);
const shouldApply = args.includes('--apply');
const verbose = args.includes('--verbose');

const warnMessages = [];
const renameOperations = [];
const folderCache = new Map();

const sanitizeBase = (filePath, extOverride = null) => {
  const ext = ((extOverride !== null && extOverride !== undefined ? extOverride : path.extname(filePath))).toLowerCase();
  return path.basename(filePath, ext).toLowerCase();
};

const levenshtein = (a, b) => {
  const rows = a.length + 1;
  const cols = b.length + 1;
  const dp = Array.from({ length: rows }, () => Array(cols).fill(0));

  for (let i = 0; i < rows; i += 1) dp[i][0] = i;
  for (let j = 0; j < cols; j += 1) dp[0][j] = j;

  for (let i = 1; i < rows; i += 1) {
    for (let j = 1; j < cols; j += 1) {
      if (a[i - 1] === b[j - 1]) {
        dp[i][j] = dp[i - 1][j - 1];
      } else {
        dp[i][j] = Math.min(dp[i - 1][j], dp[i][j - 1], dp[i - 1][j - 1]) + 1;
      }
    }
  }

  return dp[rows - 1][cols - 1];
};

const similarity = (a, b) => {
  if (!a.length && !b.length) return 1;
  const distance = levenshtein(a, b);
  const longest = Math.max(a.length, b.length, 1);
  return 1 - distance / longest;
};

const getFolderState = (folderPath) => {
  if (!folderCache.has(folderPath)) {
    if (!fs.existsSync(folderPath)) {
      folderCache.set(folderPath, { files: [], used: new Set() });
    } else {
      const files = fs
        .readdirSync(folderPath)
        .filter((file) => file !== 'README.md' && !file.startsWith('.'))
        .map((file) => path.join(folderPath, file));
      folderCache.set(folderPath, { files, used: new Set() });
    }
  }
  return folderCache.get(folderPath);
};

const extractImageRefs = (fileContent) => {
  const regex = /\/images\/projects\/[^\s"'`)>}\]]+/g;
  const matches = fileContent.match(regex) || [];
  return Array.from(new Set(matches.map((match) => match.trim())));
};

const ensureProjectsDir = () => {
  if (!fs.existsSync(projectsDir)) {
    throw new Error(`Projects directory not found at ${projectsDir}`);
  }
};

const planRenames = () => {
  ensureProjectsDir();
  const mdxFiles = fs
    .readdirSync(projectsDir)
    .filter((file) => file.endsWith('.mdx'));

  mdxFiles.forEach((file) => {
    const mdxPath = path.join(projectsDir, file);
    const fileContent = fs.readFileSync(mdxPath, 'utf8');
    const imageRefs = extractImageRefs(fileContent);

    if (!imageRefs.length && verbose) {
      console.log(`No project image references found in ${path.relative(workspaceRoot, mdxPath)}`);
      return;
    }

    imageRefs.forEach((reference) => {
      if (!reference.startsWith('/images/projects/')) {
        return;
      }

      const relativePath = reference.replace(/^\/+/, '');
      const targetPath = path.join(publicDir, relativePath);

      if (fs.existsSync(targetPath)) {
        return;
      }

      const folderPath = path.dirname(targetPath);
      if (!fs.existsSync(folderPath)) {
        warnMessages.push(
          `Folder missing for reference ${reference} (defined in ${path.relative(workspaceRoot, mdxPath)})`
        );
        return;
      }

      const folderState = getFolderState(folderPath);
      const available = folderState.files.filter((filePath) => !folderState.used.has(filePath));

      if (!available.length) {
        warnMessages.push(
          `No unused files available in ${path.relative(workspaceRoot, folderPath)} to satisfy ${reference}`
        );
        return;
      }

      const targetExt = path.extname(targetPath).toLowerCase();
      const targetBase = sanitizeBase(targetPath, targetExt);

      const extensionMismatch = folderState.files.find((filePath) => {
        const ext = path.extname(filePath).toLowerCase();
        return sanitizeBase(filePath, ext) === targetBase && ext !== targetExt;
      });

      if (extensionMismatch) {
        warnMessages.push(
          `Reference ${reference} expects ${targetExt || 'no'} extension but available file ${path.relative(
            workspaceRoot,
            extensionMismatch
          )} is ${path.extname(extensionMismatch)}. Update the MDX path instead of renaming.`
        );
        return;
      }

      const scoredCandidates = available
        .filter((filePath) => path.extname(filePath).toLowerCase() === targetExt)
        .map((filePath) => ({
          filePath,
          score: similarity(sanitizeBase(filePath), targetBase),
        }));

      if (!scoredCandidates.length) {
        warnMessages.push(
          `No file with extension ${targetExt || '[none]'} available in ${path.relative(
            workspaceRoot,
            folderPath
          )} for ${reference}. Update the MDX to use the actual filename.`
        );
        return;
      }

      const bestCandidate = scoredCandidates.reduce((best, current) =>
        current.score > best.score ? current : best,
      { filePath: null, score: -1 });

      if (!bestCandidate.filePath || bestCandidate.score < SIMILARITY_THRESHOLD) {
        warnMessages.push(
          `No sufficiently similar file found in ${path.relative(workspaceRoot, folderPath)} for ${reference}.` +
            ' Rename manually or update the MDX.'
        );
        return;
      }

      folderState.used.add(bestCandidate.filePath);
      renameOperations.push({
        source: bestCandidate.filePath,
        target: targetPath,
        reference,
        mdx: path.relative(workspaceRoot, mdxPath),
        score: bestCandidate.score.toFixed(2),
      });
    });
  });
};

const applyRenames = () => {
  renameOperations.sort((a, b) => a.target.localeCompare(b.target));
  renameOperations.forEach(({ source, target }) => {
    const targetDir = path.dirname(target);
    fs.mkdirSync(targetDir, { recursive: true });

    if (fs.existsSync(target)) {
      throw new Error(`Cannot rename ${source} because ${target} already exists.`);
    }

    fs.renameSync(source, target);
  });
};

const main = () => {
  planRenames();

  if (!renameOperations.length) {
    console.log('All project image references are satisfied. No renames required.');
  } else {
    console.log(`Planned ${renameOperations.length} rename(s):`);
    renameOperations.forEach(({ source, target, mdx, reference, score }) => {
      console.log(
        `- ${path.relative(workspaceRoot, source)} -> ${path.relative(workspaceRoot, target)} ` +
          `(${reference} in ${mdx}, similarity ${score})`
      );
    });

    if (shouldApply) {
      applyRenames();
      console.log('\nRenames applied successfully.');
    } else {
      console.log('\nRun again with --apply to perform these renames.');
    }
  }

  if (warnMessages.length) {
    console.warn('\nWarnings:');
    warnMessages.forEach((message) => console.warn(`- ${message}`));
  }
};

main();
