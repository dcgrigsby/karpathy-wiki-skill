# Multi-page sources (crawls): one wiki page per named breakout

When the source is a *crawl* — multiple raw files representing one site, one paper, or one multi-part doc — handle it explicitly:

**At the start of ingest:**

- Enumerate the file set (e.g., `ls raw/2026-05-07-strongdm-factory-*`) and treat the count as the *minimum* read budget. Do not start writing the source page after reading just the lead file.
- Build a map: which raw file corresponds to which named section / technique / product / chapter on the original. The mapping is usually obvious from filenames (Web Clipper preserves the URL slug) but verify by skimming the first lines of each.
- Confirm with the user in step 3 (key takeaways / angle): "I see N raw files for this source — the lead essay plus K named breakouts (list them). I plan to promote J of them as their own wiki pages and fold L. Sound right?" This is the cheapest place to catch under-promotion.

**When deciding promotion (per breakout):**

When a crawl includes **dedicated breakout pages for distinct named techniques, products, concepts, or entities** — and each has substantive content (more than a couple sentences) — **default to creating one wiki page per breakout**, not folding them into prose mentions on the source page.

The failure mode this prevents: cross-link starvation. If a downstream page wants to reference "Gene Transfusion" as a discrete idea, but the only mention of it is buried in a paragraph on the source page, there is no slug to `[[link]]` to. The wiki under-connects, and queries against it return the source page for everything instead of the actual concept page.

The decision rule, in order:

1. **Did the original author give it a name?** If the source has it with its own heading, URL, or named-section, that's a strong signal it deserves its own slug.
2. **Is there enough content to write a real page?** If the breakout has unique examples, a defined flow, or a distinct claim that wouldn't survive being collapsed into a sentence, promote it.
3. **Is folding genuinely cleaner?** Two valid reasons to fold:
   - The breakout is a *literal restatement* of an existing wiki concept (e.g., the author's term for [[scenario-and-satisfaction]]). Cross-link to the existing page from the source page; no new page needed.
   - The breakout is *inseparable* from another concept you're already promoting (e.g., the StrongDM "Shift Work" technique and the broader "non-interactive development" regime — same idea at two granularities, one page covers both).
4. **"Less novel than the others" is not a sufficient reason to fold.** Wiki pages don't have to be groundbreaking to earn their slugs — they have to be *referenceable*.

When you decline to promote a named breakout, log the reason briefly in the ingest log entry so a future audit can tell intent from oversight.

**At the end of ingest, before committing**: cross-check the breakout map against the wiki pages produced. Every breakout should have either (a) its own wiki page, or (b) a logged justification for folding. If neither, it's an oversight — fix before commit.
