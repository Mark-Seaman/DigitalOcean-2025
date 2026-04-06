Extract truth from markdown files in the active pub directory and build a 4x4 outline and Deep Outline. Produces Truth.md, 4x4.md, and Deep Outline.md.

Arguments: $ARGUMENTS
Format: (none required — operates on active pub directory)

## Steps

1. Read the pub directory from `/Users/seaman/Hammer/claude/.claude/active_pub`.
   - If it does not exist or is empty, tell the user to run `/pub` first and stop.
   - Trim any whitespace. This is `pub_dir`.

2. List all `.md` files in `pub_dir`. Exclude `Truth.md`, `4x4.md`, and `Deep Outline.md` if they exist.

3. Read each file and concatenate the content into a single body of source text.

4. Read the Extract Truth schema from `/Users/seaman/Hammer/Obsidian/forge/ai/Truth.md`.

5. Apply the EXTRACT_TRUTH operation to the source text following the schema exactly:
   - Act as an Idea Synthesizer in pure structural extraction mode
   - Extract the underlying truth structure already present in the text
   - Eliminate duplication, reconcile competing hierarchies, assign each idea a single structural home
   - Produce a canonical deep outline: 80–100 nodes, 3–4 levels deep
   - Node labels: phrases only — no sentences, no prose, no new concepts
   - Level 1: 6–10 Domains (mutually exclusive, collectively exhaustive)
   - Level 2: 3–6 Subdomains per domain
   - Level 3: Elements — most densely populated, directly traceable to source
   - Level 4: Qualifiers — optional, used sparingly for conditions, tensions, tradeoffs
   - Output format: hyphenated Markdown outline only — no commentary, no headings outside the outline

6. Save the output to `<pub_dir>/Truth.md` using the Write tool.

7. Read the outline formats from `/Users/seaman/Hammer/Obsidian/forge/ai/outline.md`.

8. Synthesize a 4x4 outline from Truth.md following these rules exactly:
   - 1 Main Topic — single phrase, no label, captures the whole subject
   - 4 Key Topics — one level below, no bold, each a distinct major dimension
   - 4 Subtopics under each Key Topic — the most essential ideas
   - Every bullet: 5 words maximum
   - Total nodes: 21 (1 + 4 + 16)
   - Indentation: 4 spaces per level
   - Format: hyphenated bullet list, no prose, no commentary

9. Save the 4x4 outline to `<pub_dir>/4x4.md` using the Write tool.

10. Expand the 4x4 outline into a Deep Outline following these rules exactly:
    - Preserve the 3 levels from the 4x4 (Main Topic, 4 Key Topics, 16 Subtopics)
    - Add a 4th level: 4 detail nodes under each of the 16 Subtopics
    - Every bullet: 5 words maximum
    - Total nodes: 85 (1 + 4 + 16 + 64)
    - Indentation: 4 spaces per level
    - Format: hyphenated bullet list, no prose, no commentary
    - Draw detail nodes from Truth.md — no invented concepts

11. Save the Deep Outline to `<pub_dir>/Deep Outline.md` using the Write tool.

12. Confirm all three output paths to the user.
