import os
from datetime import datetime
from urllib.parse import urljoin

# === CONFIGURATION ===
BASE_URL = "https://projectbuddyofficial.netlify.app/"
VALID_EXTENSIONS = {'.html', '.htm', '.php'}

def generate_sitemap():
    url_entries = []
    page_count = 0

    for root, dirs, files in os.walk("."):
        for file in files:
            ext = os.path.splitext(file)[1].lower()
            if ext in VALID_EXTENSIONS:
                page_count += 1

                file_path = os.path.join(root, file)

                # Create relative URL path
                relative_path = os.path.relpath(file_path, ".").replace("\\", "/")

                # SEO-friendly URL handling
                if file == "index.html":
                    full_url = urljoin(BASE_URL + "/", relative_path.replace("index.html", ""))
                else:
                    full_url = urljoin(BASE_URL + "/", relative_path)

                lastmod = datetime.fromtimestamp(os.path.getmtime(file_path)).date().isoformat()

                url_entries.append(f"""  <url>
    <loc>{full_url}</loc>
    <lastmod>{lastmod}</lastmod>
    <changefreq>monthly</changefreq>
    <priority>0.8</priority>
  </url>""")

                # 🔢 Live count output
                print(f"Visited [{page_count}] → {full_url}")

    sitemap_content = (
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
        + "\n".join(url_entries) +
        '\n</urlset>'
    )

    with open("sitemap.xml", "w", encoding="utf-8") as f:
        f.write(sitemap_content)

    print("\n✅ sitemap.xml created successfully.")
    print(f"📄 Total pages indexed: {page_count}")

if __name__ == "__main__":
    generate_sitemap()
