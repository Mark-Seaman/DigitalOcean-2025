for m in 01 02 03 04 05 06 07 08 09 10 11 12; do
  next=$((10#$m + 1))
  printf -v next "%02d" "$next"
  task 31 "2025-${next}-01" activity > "$t/monthly/$m.md"
done