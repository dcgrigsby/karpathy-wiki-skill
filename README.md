# karpathy-wiki

Operate a [Karpathy-style LLM-maintained wiki](https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f) — a personal knowledge base where source material in `raw/` is processed by an AI agent into a cross-linked synthesis in `wiki/`.

## What it does

This skill teaches an agent to:

- **Ingest** sources from `raw/` into structured wiki pages (with source enrichment for arxiv pages, podcast-companion posts, and crawl handling for multi-file source sets)
- **Query** the wiki against a question, citing `[[wiki-link]]` references
- **Lint** for orphan pages, contradictions, under-linked concepts, missing back-references
- **Unwind** a source: remove its wiki pages and scrub references to it from elsewhere

The skill owns the conventions: page format (frontmatter spec, page types — source/entity/concept/synthesis/question/overview), wiki-link style, the security boundary around untrusted `raw/` content, the qmd search index integration, the wiki/log.md operation log.

## Operate from inside the wiki repo

The skill assumes `pwd` is the karpathy-wiki repo root, with `raw/` and `wiki/` as direct subdirs. Run from elsewhere and scripts will fail loudly. Multi-wiki support is intentionally out of scope.

## Install

```bash
npx skills add <repo-url> -g -a claude-code -a gemini-cli -a codex -a pi -y
```

(Replace `<repo-url>` with this skill's git URL.)

## Set up a wiki repo

A karpathy-wiki repo has this shape:

```
my-wiki/
├── AGENTS.md          # repo-local schema + lore (and CLAUDE.md symlink for Claude Code)
├── raw/               # immutable source material
└── wiki/              # AI-maintained synthesis (created on first ingest)
```

`AGENTS.md` is short — it identifies the repo as a karpathy-wiki and carries any repo-specific lore (scope, no-touch paths, git remote). The skill itself owns the operations.

## Safety

See [NOTICE](./NOTICE). The skill writes, deletes, and pushes — read it before granting an agent access.

## License

Apache 2.0 — see [LICENSE](./LICENSE).
