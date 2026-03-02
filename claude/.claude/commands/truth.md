Extract truth from the markdown files in the current directory and save the result to Truth.md.

Arguments: $ARGUMENTS
Format: (none required — operates on current directory)

## Steps

1. List all `.md` files in the current working directory. Exclude `Truth.md` if it exists.

2. Read each file and concatenate the content into a single body of source text.

3. Read the Extract Truth schema from `/Users/seaman/Hammer/Obsidian/forge/ai/Truth.md`.

4. Apply the EXTRACT_TRUTH operation to the source text following the schema exactly:
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

5. Save the output to `Truth.md` in the current working directory using the Write tool. Confirm the path to the user after saving.
