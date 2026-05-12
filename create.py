import json
from pathlib import Path
SAMPLE_VIDEOS = [
    {
        "title": "Python Tutorial for Beginners",
        "channel": "Code Academy",
        "views": "1.2M views",
        "time": "2 days ago",
        "description": "Learn Python from scratch with easy examples and hands-on practice.",
        "thumbnail": "https://via.placeholder.com/320x180.png?text=Python+Tutorial",
    },
    {
        "title": "Build a Web App with Flask",
        "channel": "Dev Simplified",
        "views": "890K views",
        "time": "1 week ago",
        "description": "A complete walkthrough for building a Flask web application.",
        "thumbnail": "https://via.placeholder.com/320x180.png?text=Flask+App",
    },
    {
        "title": "JavaScript Project Ideas",
        "channel": "Frontend Fun",
        "views": "640K views",
        "time": "3 weeks ago",
        "description": "Project ideas for intermediate JavaScript developers.",
        "thumbnail": "https://via.placeholder.com/320x180.png?text=JS+Ideas",
    },
]


def build_youtube_html(videos):
    cards = []
    for video in videos:
        cards.append(
            f"""
            <article class="video-card">
                <img src="{video['thumbnail']}" alt="{video['title']} thumbnail" class="thumbnail" />
                <h3>{video['title']}</h3>
                <p class="meta">{video['channel']} • {video['views']} • {video['time']}</p>
                <p class="description">{video['description']}</p>
            </article>
            """
        )

    return f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>Mini YouTube Clone</title>
    <style>
        body {{
            margin: 0;
            font-family: Arial, sans-serif;
            background: #f9f9f9;
            color: #111;
        }}

        .header {{
            display: flex;
            align-items: center;
            padding: 16px 24px;
            background: #ffffff;
            border-bottom: 1px solid #ddd;
        }}

        .logo {{
            font-weight: 700;
            font-size: 24px;
            color: #cc0000;
            margin-right: auto;
        }}

        .search-bar {{
            display: flex;
            width: 400px;
            border: 1px solid #ccc;
            border-radius: 24px;
            overflow: hidden;
            background: #f1f1f1;
        }}

        .search-bar input {{
            flex: 1;
            border: none;
            padding: 10px 14px;
            font-size: 14px;
            background: transparent;
        }}

        .search-bar button {{
            background: #e2e2e2;
            border: none;
            padding: 0 16px;
            cursor: pointer;
        }}

        .content {{
            padding: 24px;
            max-width: 1200px;
            margin: 0 auto;
        }}

        .video-grid {{
            display: grid;
            gap: 24px;
            grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
        }}

        .video-card {{
            background: #ffffff;
            border-radius: 12px;
            box-shadow: 0 2px 10px rgba(0, 0, 0, 0.06);
            overflow: hidden;
        }}

        .thumbnail {{
            width: 100%;
            display: block;
        }}

        .video-card h3 {{
            margin: 16px;
            font-size: 18px;
        }}

        .meta {{
            margin: 0 16px;
            color: #555;
            font-size: 13px;
        }}

        .description {{
            margin: 12px 16px 16px;
            color: #333;
            line-height: 1.5;
            font-size: 14px;
        }}
    </style>
</head>
<body>
    <header class="header">
        <div class="logo">YouTube Clone</div>
        <form class="search-bar" onsubmit="event.preventDefault();">
            <input type="text" placeholder="Search" />
            <button>Search</button>
        </form>
    </header>
    <main class="content">
        <div class="video-grid">
            {''.join(cards)}
        </div>
    </main>
</body>
</html>
"""


def save_html(content, filename='youtube_clone.html'):
    path = Path(filename)
    path.write_text(content, encoding='utf-8')
    return path


if __name__ == '__main__':
    html = build_youtube_html(SAMPLE_VIDEOS)
    output_path = save_html(html)
    print(f'Generated: {output_path.resolve()}')

