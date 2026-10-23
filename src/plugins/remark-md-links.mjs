import fs from 'node:fs';
import path from 'node:path';
import { visit } from 'unist-util-visit';

// Pages link to each other as relative `*.md` files, which also works on GitHub.
// Rewrite them to the URLs Astro serves.
export function remarkMdLinks({ base, docsDir }) {
  const root = fs.realpathSync(docsDir);
  return (tree, file) => {
    const from = path.dirname(fs.realpathSync(file.path));
    visit(tree, 'link', (node) => {
      const m = /^([^#?]*\.mdx?)(#.*)?$/.exec(node.url);
      if (!m || /^[a-z]+:/i.test(node.url)) return;
      const rel = path
        .relative(root, path.resolve(from, m[1]))
        .replace(/\.mdx?$/, '')
        .replace(/(^|\/)index$/, '');
      node.url = `${base}/${rel}${rel ? '/' : ''}${m[2] ?? ''}`.replace(/\/{2,}/g, '/');
    });
  };
}
