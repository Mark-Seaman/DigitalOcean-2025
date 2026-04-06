Initialize a new publication or navigate to an existing one.

Arguments: $ARGUMENTS
Format: `<pub-name>` or `pub-dir <pub-name>`

## Steps

1. Parse `$ARGUMENTS`.
   - If the first word is `pub-dir`, extract `pub_name` from the remaining argument and skip to step 3.
   - Otherwise, treat the full argument as `pub_name` for a new publication.
   - If `pub_name` is missing, ask the user for the pub name and stop.

2. Run the bash command `pub <pub_name>` to initialize the publication files.
   - If the command fails, report the error and stop.

3. Find the pub directory by searching these two patterns using the Glob tool:
   - `/Users/seaman/Hammer/Obsidian/forge/*/<pub_name>`
   - `/Users/seaman/Hammer/Obsidian/Private/forge/*/<pub_name>`
   - Use the first match found. If no match is found, report that the directory was not found and stop.

4. Change the working directory to the pub directory using the Bash tool (`cd <path>`).

5. Write the pub directory path to `/Users/seaman/Hammer/claude/.claude/active_pub` using the Write tool (just the path, no newline).

6. Confirm to the user: the pub name and the directory path. If a new publication was created, also list any files created.
