Expand one or more source articles or outlines into four child pages each, one per key idea.

Arguments: $ARGUMENTS
Format: `<source_file_or_glob>`

## Steps

1. Parse `$ARGUMENTS` as `source_pattern`.
   - If missing, ask the user for the path and stop.
   - Resolve the path: if not absolute, check relative to the Obsidian vault root `/Users/seaman/Hammer/Obsidian/` first, then the current working directory.
   - If the argument contains a glob pattern (e.g. `0.*.md`), use the Glob tool to expand it into a list of matching files. Process each file independently.

2. For each matched file, read it. It may be an article, outline, or set of notes.

3. Identify the 4 key ideas in the source — the most distinct, expandable concepts present. Do not invent ideas not supported by the text.

4. Derive the output filenames from the source filename by appending `.1`, `.2`, `.3`, `.4` before the extension.
   - Example: `4.3.md` → `4.3.1.md`, `4.3.2.md`, `4.3.3.md`, `4.3.4.md`

5. For each of the 4 key ideas, write a page following these format rules:
   - 250–300 words total
   - `##` section title derived from the idea
   - 4–6 paragraphs, each 40–50 words
   - Deepen the idea — do not restate the source

6. Show all four pages to the user with their filenames.

7. Write each page to its output path using the Write tool.
