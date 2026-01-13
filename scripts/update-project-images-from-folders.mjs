import fs from 'fs';
import path from 'path';

const workspaceRoot = process.cwd();
const projectsDir = path.join(workspaceRoot, 'src/app/work/projects');
const publicProjectsDir = path.join(workspaceRoot, 'public/images/projects');

const allowedExtensions = new Set(['.png', '.jpg', '.jpeg', '.gif', '.webp', '.svg', '.avif']);

const mdxFiles = fs
  .readdirSync(projectsDir)
  .filter((file) => file.endsWith('.mdx'))
  .sort((a, b) => a.localeCompare(b));

const updated = [];
const skipped = [];

const getFrontmatter = (raw) => {
  if (!raw.startsWith('---')) return null;
  const endIndex = raw.indexOf('\n---', 3);
  if (endIndex === -1) return null;
  const frontmatter = raw.slice(4, endIndex);
  const body = raw.slice(endIndex + 4);
  return { frontmatter, body };
};

const getImagesBlock = (frontmatter) => {
  const regex = /(^images:\s*\n(?:^[ \t]+-.*\n?)*)/m;
  const match = frontmatter.match(regex);
  return match ? match[0] : null;
};

const extractImageRefs = (imagesBlock) => {
  const refs = [];
  const lineRegex = /^[ \t]*-\s*"?([^"\n]+)"?/gm;
  let match;
  while ((match = lineRegex.exec(imagesBlock)) !== null) {
    const value = match[1].trim();
    if (value.startsWith('/images/projects/')) {
      refs.push(value);
    }
  }
  return refs;
};

const getFoldersFromRefs = (refs) => {
  const folders = new Set();
  refs.forEach((ref) => {
    const parts = ref.replace(/^\/+/, '').split('/');
    if (parts.length >= 3) {
      folders.add(parts[2]);
    }
  });
  return Array.from(folders);
};

const buildImageList = (folder) => {
  const folderPath = path.join(publicProjectsDir, folder);
  if (!fs.existsSync(folderPath)) {
    return null;
  }
  const files = fs
    .readdirSync(folderPath)
    .filter((file) => {
      if (file === 'README.md' || file.startsWith('.')) {
        return false;
      }
      const fullPath = path.join(folderPath, file);
      if (!fs.statSync(fullPath).isFile()) {
        return false;
      }
      const ext = path.extname(file).toLowerCase();
      return allowedExtensions.has(ext);
    })
    .sort((a, b) => a.localeCompare(b));

  return files.map((file) => `/images/projects/${folder}/${file}`);
};

const buildImagesBlock = (images) => {
  if (!images.length) return 'images:\n  - ""';
  return ['images:', ...images.map((img) => `  - "${img}"`)].join('\n');
};

mdxFiles.forEach((file) => {
  const mdxPath = path.join(projectsDir, file);
  const raw = fs.readFileSync(mdxPath, 'utf8');
  const fm = getFrontmatter(raw);

  if (!fm) {
    skipped.push({ file, reason: 'Missing frontmatter' });
    return;
  }

  const imagesBlock = getImagesBlock(fm.frontmatter);
  if (!imagesBlock) {
    skipped.push({ file, reason: 'Missing images block' });
    return;
  }

  const imageRefs = extractImageRefs(imagesBlock);
  if (!imageRefs.length) {
    skipped.push({ file, reason: 'No image references' });
    return;
  }

  const folders = getFoldersFromRefs(imageRefs);
  if (!folders.length) {
    skipped.push({ file, reason: 'No project folders detected' });
    return;
  }

  let newImages = [];
  folders.forEach((folder) => {
    const list = buildImageList(folder);
    if (list && list.length) {
      newImages = newImages.concat(list);
    }
  });

  if (!newImages.length) {
    skipped.push({ file, reason: 'Referenced folders have no allowed assets' });
    return;
  }

  const uniqueImages = Array.from(new Set(newImages));
  const replacement = `${buildImagesBlock(uniqueImages)}\n`;
  const nextFrontmatter = fm.frontmatter.replace(imagesBlock, replacement);
  const needsLeadingNewline = fm.body.startsWith('\n') ? '' : '\n';
  const nextContent = `---\n${nextFrontmatter}\n---${needsLeadingNewline}${fm.body}`;
  if (nextContent !== raw) {
    fs.writeFileSync(mdxPath, nextContent);
    updated.push({ file, folders: folders.join(', '), count: uniqueImages.length });
  } else {
    skipped.push({ file, reason: 'Already normalized' });
  }
});

if (updated.length) {
  console.log('Updated image references for:');
  updated.forEach(({ file, folders, count }) => {
    console.log(`- ${file} (${count} image(s) from ${folders})`);
  });
} else {
  console.log('No MDX files required image updates.');
}

if (skipped.length) {
  console.log('\nSkipped:');
  skipped.forEach(({ file, reason }) => {
    console.log(`- ${file}: ${reason}`);
  });
}
