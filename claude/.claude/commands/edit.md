Apply a named transform to a file.

Arguments: $ARGUMENTS
Format: `<file_path> <transform_name>`

Transforms are defined as markdown files in `/Users/seaman/Hammer/claude/transforms/`.

## Steps

1. Parse `$ARGUMENTS` into `file_path` (first token) and `transform_name` (second token).
   - If either is missing, list available transforms from `/Users/seaman/Hammer/claude/transforms/` and stop.
   - Resolve the file path: if not absolute, check relative to the Obsidian vault root `/Users/seaman/Hammer/Obsidian/` first, then the current working directory.

2. Read the file at `file_path`.

3. Read the transform definition from `/Users/seaman/Hammer/claude/transforms/<transform_name>.md`.
   - If the transform file does not exist, list available transforms and stop.

4. Apply the transform instructions to the file content directly — do not shell out or use any subprocess. Return only the transformed text — no preamble or commentary.

5. Show a unified diff between the original and transformed content.
   - If there are no changes, say so and stop.

6. Write the revised content back to the file using the Edit or Write tool. Confirm to the user that changes were applied.
