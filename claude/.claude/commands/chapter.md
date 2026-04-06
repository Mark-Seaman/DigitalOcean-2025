Build a chapter article for a publication.

Arguments: $ARGUMENTS
Format: `<chapter_number>` (e.g., `2`)

## Steps

1. Parse `$ARGUMENTS` to get `chapter_number` (e.g., `2`).
   - If missing, ask the user for the chapter number and stop.

2. Read the pub directory from `/Users/seaman/Hammer/claude/.claude/active_pub`.
   - If it does not exist or is empty, tell the user to run `/pub` first and stop.
   - Trim any whitespace. This is `pub_dir`.

3. Read the context file at `<pub_dir>/dev/outlines/<chapter_number>.md`.
   - If it does not exist, tell the user and stop.

3. The context file contains a deep outline followed by a prompt. Use both the outline structure and the prompt instruction to write the article.

4. Write an article following these format rules (from `/Users/seaman/Hammer/Obsidian/forge/ai/Article.md`):
   - 1000–1200 words total
   - Clear title at the top
   - Strong opening paragraph that carries the conclusion
   - 4 sections, each with a `##` heading (use the outline's top-level nodes as section titles)
   - Paragraph breaks every 40–50 words
   - Write in first person
   - Deepen meaning — do not pad content

5. Write the content to `<pub_dir>/<chapter_number>.md` using the Write tool.

6. Show the generated article to the user and confirm the path it was saved to.
