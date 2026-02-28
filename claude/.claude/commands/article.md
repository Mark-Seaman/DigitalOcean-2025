Write an article from a context file and save it to the requested output file.

Arguments: $ARGUMENTS
Format: `<output_file> <context_file>`

## Steps

1. Parse `$ARGUMENTS` into `output_file` (first token) and `context_file` (second token).
   - If either is missing, ask the user for the missing argument and stop.
   - Resolve each path: if not absolute, check relative to the Obsidian vault root `/Users/seaman/Hammer/Obsidian/` first, then the current working directory.

2. Read the context file at `context_file`. It contains an AI prompt describing what to write.

3. Write an article following these format rules (from `/Users/seaman/Hammer/Obsidian/forge/ai/Article.md`):
   - 1000–1200 words total
   - Clear title at the top
   - Strong opening paragraph that carries the conclusion
   - 4 sections, each with a `##` heading and title (do not number headings)
   - Paragraph breaks every 40–50 words
   - Deepen meaning — do not pad content

4. Show the generated article to the user.

5. Ask the user: **"Save to `<output_file>`? [y/N]"**

6. If confirmed, write the content to `output_file` using the Write tool.
