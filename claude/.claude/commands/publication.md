Initialize a new publication and go to its directory.

Arguments: $ARGUMENTS
Format: `<pub-name>`

## Steps

1. Parse `$ARGUMENTS` to get `pub_name`.
   - If missing, ask the user for the pub name and stop.

2. Run the bash command `pub <pub_name>` to initialize the publication files.
   - If the command fails, report the error and stop.

3. Find the pub directory by searching these two patterns using the Glob tool:
   - `/Users/seaman/Hammer/Obsidian/forge/*/<pub_name>`
   - `/Users/seaman/Hammer/Obsidian/Private/forge/*/<pub_name>`
   - Use the first match found. If no match is found, report that the directory was not created and stop.

4. Change the working directory to the pub directory using the Bash tool (`cd <path>`).

5. Confirm to the user: the pub name, the directory path, and any files created.
