Report on monthly time spent from daily log files.

Arguments: $ARGUMENTS
Format: `<month>` (e.g., `02` for February)

## Steps

1. Parse `$ARGUMENTS` to get `month` (e.g., `02`).
   - If missing, ask for it and stop.

2. Run the bash command `agent time /Users/seaman/Hammer/Obsidian/Private/history/2026/<month>` to concatenate daily logs into the monthly file.

3. Read the resulting file at `/Users/seaman/Hammer/Obsidian/Private/history/2026/<month>.md`.

4. Parse the file: for each line matching `^([A-Z][a-z]+)\s+(\d+)\s*$` at column 0 (no leading whitespace), accumulate hours per category. This distinguishes category headers from indented activity notes (e.g., "    Hawaii 50"). Categories include: Friends, Church, Family, Innovate, Write, Fun, Grow, Travel, Health, Business, Household, Teach, Organize.

5. Calculate total hours. For each category compute hours and percentage of total.

6. Group categories and display a formatted report:

```
## <Month Name> <Year> — Time Report

### Connect (<pct>% / <hrs> hrs)
  Friends    <hrs> hrs  (<pct>%)
  Church     <hrs> hrs  (<pct>%)
  Family     <hrs> hrs  (<pct>%)

### Create (<pct>% / <hrs> hrs)
  Innovate   <hrs> hrs  (<pct>%)
  Write      <hrs> hrs  (<pct>%)

### Enjoy (<pct>% / <hrs> hrs)
  Fun        <hrs> hrs  (<pct>%)
  Grow       <hrs> hrs  (<pct>%)
  Travel     <hrs> hrs  (<pct>%)

### Work (<pct>% / <hrs> hrs)
  Health     <hrs> hrs  (<pct>%)
  Business   <hrs> hrs  (<pct>%)
  Household  <hrs> hrs  (<pct>%)

**Total: <total> hrs**
```

   - Show only categories with hours > 0.
   - Show only groups that have at least one non-zero category.
   - Round percentages to nearest whole number.

7. Save the report to `/Users/seaman/Hammer/Obsidian/Private/history/2026/summary/<MonthName>-<Year>-summary.md` (e.g., `Feb-2026-summary.md`). Use the Write tool. Confirm the path to the user after saving.
