# Source enrichment

Before reading deeply, check whether the source is *substantive* or just a thin landing page. `raw/` should hold the real content, not metadata about the content. If you encounter a landing page, fix it at the start of ingest rather than lossily summarizing the thin version.

## Auto-enrich (no need to ask)

- **arxiv abs page** — detect via URL pattern `arxiv.org/abs/<id>`, title pattern `[<id>] <paper title>`, or structural signals (Abstract section + bibliographic metadata + no body sections). Auto-refetch from `arxiv.org/html/<id>` (the HTML version of most papers). If 404, fall back to `ar5iv.labs.arxiv.org/html/<id>` (third-party LaTeX→HTML mirror), then to `arxiv.org/pdf/<id>` as last resort. **Replace the raw file in place** — same filename, full content. Append to log: `## [YYYY-MM-DD] enrich | replaced arxiv abs page with HTML version for <id>`.

- **Blog post linking to a companion podcast with a transcript** — when a post is essentially a discussion of, response to, or interview-companion to a specific podcast episode, and the episode's page has a transcript, auto-fetch the transcript and capture it alongside the post as a sibling raw file (`YYYY-MM-DD-<post-slug>-podcast-transcript.md`). The post + transcript become a multi-file source set; apply the multi-page sources rule when ingesting. Append to log: `## [YYYY-MM-DD] enrich | added podcast transcript to <post-slug> source set`.
  - Detection: the post links out to a podcast URL (apple.com/podcasts/, open.spotify.com/episode/, podlink.to/, transistor.fm, podbean.com, simplecast.com, anchor.fm, an individual podcast site's `/episodes/<slug>` page) AND the post's substance is *about* that episode (interview write-up, discussion, summary, response) — not a passing reference among many. When in doubt, ask.
  - Transcript extraction: fetch the podcast episode page; if it contains a transcript section, capture it. If only an audio file is available with no transcript, skip — do not transcribe audio yourself.

These cases auto because the answer is unambiguous (HTML arxiv twins always have ≥ the abs content; podcast transcripts paired to discussion-posts are the substantive material the post references).

## Ask first

- **YouTube video URL only** — ask the user whether to fetch the transcript before processing.
- **Twitter/X thread URL, GitHub repo URL** — ask before fetching the surrounding context.

## Personal-workflow extensions

The user's `personal-workflow` skill (if loaded) may add more enrichment patterns — e.g., extracting an email body from a `message:` URL when their task-capture flow stores them. Those patterns live there because the *source* is system-specific (Apple Mail, the user's task shortcut), even though the resulting raw file is generic.
