import fs from 'fs';
import path from 'path';
import matter from 'gray-matter';

export interface DocContent {
  slug: string;
  title: string;
  content: string;
}

export function getAllDocs(): DocContent[] {
  const docsDirectory = path.join(process.cwd(), 'docs');
  const filenames = fs.readdirSync(docsDirectory);
  
  return filenames.map((filename) => {
    const slug = filename.replace(/\.md$/, '');
    const fullPath = path.join(docsDirectory, filename);
    const fileContents = fs.readFileSync(fullPath, 'utf8');
    const { data, content } = matter(fileContents);

    return {
      slug,
      title: data.title || slug,
      content: content,
    };
  });
}