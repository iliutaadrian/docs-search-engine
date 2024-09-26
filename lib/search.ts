import fuzzysort from 'fuzzysort';
import { DocContent, getAllDocs } from './md-utils';

let docs: DocContent[] | null = null;

export function indexDocs() {
  if (!docs) {
    docs = getAllDocs();
  }
}

export interface SearchResult {
  slug: string;
  title: string;
  highlight: string;
}

export function search(query: string): SearchResult[] {
  if (!docs) {
    indexDocs();
  }

  const results = fuzzysort.go(query, docs!, {
    keys: ['title', 'content'],
    threshold: -10000,
  });

  return results.map((result) => ({
    slug: result.obj.slug,
    title: result.obj.title,
    highlight: fuzzysort.highlight(result[1]) || result.obj.content.substring(0, 100) + '...',
  }));
}