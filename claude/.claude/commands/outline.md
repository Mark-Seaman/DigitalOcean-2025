Create a 4x4 outline and a Deep Outline from Truth.md in the current directory. Save as 4x4.md and Deep Outline.md.

Arguments: $ARGUMENTS
Format: (none required — operates on current directory)

## Steps

1. Read `Truth.md` in the current working directory.
   - If it does not exist, tell the user to run /truth first and stop.

2. Read the outline formats from `/Users/seaman/Hammer/Obsidian/forge/ai/outline.md`.

3. Synthesize a 4x4 outline from the Truth.md content following these rules exactly:
   - 1 Main Topic — single phrase, no label, captures the whole subject
   - 4 Key Topics — one level below, no bold, each a distinct major dimension
   - 4 Subtopics under each Key Topic — the most essential ideas
   - Every bullet: 5 words maximum
   - Total nodes: 21 (1 + 4 + 16)
   - Indentation: 4 spaces per level
   - Format: hyphenated bullet list, no prose, no commentary

4. Save the 4x4 outline to `4x4.md` in the current working directory using the Write tool.

5. Expand the 4x4 outline into a Deep Outline following these rules exactly:
   - Preserve the 3 levels from the 4x4 (Main Topic, 4 Key Topics, 16 Subtopics)
   - Add a 4th level: 4 detail nodes under each of the 16 Subtopics
   - Every bullet: 5 words maximum
   - Total nodes: 85 (1 + 4 + 16 + 64)
   - Indentation: 4 spaces per level
   - Format: hyphenated bullet list, no prose, no commentary
   - Draw detail nodes from Truth.md — no invented concepts

6. Save the Deep Outline to `Deep Outline.md` in the current working directory using the Write tool. Confirm both paths to the user after saving.
