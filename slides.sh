pandoc slides.md -t revealjs -s -o slides.html \
  --slide-level=2 \
  -V revealjs-url=https://unpkg.com/reveal.js \
  -V theme=white \
  -V transition=fade