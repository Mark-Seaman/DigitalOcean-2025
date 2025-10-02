from pathlib import Path
from django.template.loader import render_to_string
from publish.files import read_json


def book_cover_html(pub='becoming', output_path=None):
    """
    Generate book cover HTML file from PubCoverView template and save to root directory.

    Args:
        pub: Publication name to get data from
        output_path: Optional custom output path, defaults to 'book_cover.html' in root

    Returns:
        str: Path to the generated HTML file
    """
    if output_path is None:
        output_path = Path('book_cover.html')
    else:
        output_path = Path(output_path)

    # Get publication data similar to PubCoverView
    try:
        # Try to find publication path
        pub_dir = None
        for base_dir in ["growth", "playbooks", "spirituality", "guides"]:
            path = Path("Obsidian/forge") / base_dir / pub
            if path.exists():
                pub_dir = path
                break

        if pub_dir:
            # Read JSON data
            json_file = pub_dir / 'dev' / f'{pub}.json'
            if json_file.exists():
                data = read_json(json_file)
            else:
                data = {}
        else:
            data = {}

        # Set default values if not found in JSON
        context = {
            'title': data.get('title', 'Being Transformed'),
            'subtitle': data.get('subtitle', 'The Journey that Changes Everything'),
            'author': data.get('author', 'Mark Seaman'),
            'image': '/static/images/CoverArtwork.png'
        }

    except Exception as e:
        print(f"Error reading publication data: {e}")
        # Use default values
        context = {
            'title': 'Being Transformed',
            'subtitle': 'The Journey that Changes Everything',
            'author': 'Mark Seaman',
            'image': '/static/images/CoverArtwork.png'
        }

    # Render the template
    try:
        html_content = render_to_string('pub/cover.html', context)
    except Exception as e:
        print(f"Error rendering template: {e}")
        # Fallback to static HTML
        html_content = generate_static_cover_html(context)

    # Write to file
    output_path.write_text(html_content, encoding='utf-8')
    print(f"Book cover HTML generated: {output_path.absolute()}")

    return str(output_path)


def generate_static_cover_html(context):
    """
    Generate static HTML when Django template rendering is not available.
    """
    return f"""<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <title>{context['title']}</title>
    <style>
      @import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@700&family=Lato:wght@300;400;700&display=swap');
      
      html,
      body {{
        margin: 0;
        padding: 0;
        width: 100%;
        height: 100%;
        background: #000;
      }}
      
      .cover {{
        position: relative;
        width: 900px;
        height: 1600px;
        background: url({context['image']}) no-repeat center center;
        background-size: cover;
        overflow: hidden;
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;
        text-align: center;
        font-family: 'Lato', sans-serif;
        color: white;
      }}
      
      .overlay {{
        position: absolute;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background: rgba(0, 0, 0, 0.2);
        z-index: 1;
      }}
      
      .content {{
        position: relative;
        z-index: 2;
        padding: 20px;
        width: 85%;
        display: flex;
        flex-direction: column;
        align-items: center;
      }}
      
      .pre-title {{
        font-size: 40px;
        font-weight: 700;
        letter-spacing: 2px;
        text-transform: uppercase;
        margin-top: 15%;
        margin-bottom: 30px;
        text-shadow: 1px 1px 5px rgba(0, 0, 0, 0.7);
      }}
      
      .title {{
        font-family: 'Playfair Display', serif;
        font-size: 80px;
        font-weight: 700;
        margin-bottom: 20px;
        text-shadow: 2px 2px 5px rgba(0, 0, 0, 0.7);
        line-height: 1.1;
      }}
      
      .subtitle {{
        font-weight: 700;
        font-size: 40px;
        font-style: italic;
        margin-top: 5%;
        margin-bottom: 85%;
        text-shadow: 2px 2px 5px rgba(0, 0, 0, 0.6);
      }}
      
      .author {{
        font-size: 50px;
        font-weight: 700;
        margin-top: auto;
        text-transform: uppercase;
        text-shadow: 1px 1px 5px rgba(0, 0, 0, 0.6);
      }}
    </style>
  </head>

  <body>
    <div class="cover">
      <div class="content">
        <div class="pre-title">A Seaman's Guide</div>
        <div class="title">{context['title']}</div>
        <div class="subtitle">{context['subtitle']}</div>
        <div class="author">{context['author']}</div>
      </div>
    </div>
  </body>
</html>"""
