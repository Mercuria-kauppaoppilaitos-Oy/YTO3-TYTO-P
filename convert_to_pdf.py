#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Muuntaa YTO3-TYTO-P Uuden kurssin suunnitelma.md -> PDF"""

import markdown
import os
import subprocess
import tempfile

MD_FILE = os.path.join(os.path.dirname(__file__), "YTO3-TYTO-P Uuden kurssin suunnitelma.md")
PDF_FILE = os.path.join(os.path.dirname(__file__), "YTO3-TYTO-P Uuden kurssin suunnitelma.pdf")

CSS = """
@import url('https://fonts.googleapis.com/css2?family=Noto+Sans:wght@400;600;700&display=swap');

* { box-sizing: border-box; }

body {
    font-family: 'Noto Sans', Arial, sans-serif;
    font-size: 11pt;
    line-height: 1.6;
    color: #1a1a1a;
    margin: 0;
    padding: 0;
}

h1 {
    font-size: 20pt;
    font-weight: 700;
    color: #003366;
    border-bottom: 3px solid #003366;
    padding-bottom: 8px;
    margin-top: 0;
    margin-bottom: 16px;
}

h2 {
    font-size: 15pt;
    font-weight: 700;
    color: #004080;
    border-bottom: 2px solid #cce0ff;
    padding-bottom: 5px;
    margin-top: 28px;
    margin-bottom: 12px;
}

h3 {
    font-size: 13pt;
    font-weight: 600;
    color: #005099;
    margin-top: 22px;
    margin-bottom: 8px;
}

h4 {
    font-size: 11.5pt;
    font-weight: 600;
    color: #333;
    margin-top: 16px;
    margin-bottom: 6px;
}

p {
    margin: 6px 0 10px 0;
}

ul, ol {
    margin: 6px 0 10px 20px;
    padding: 0;
}

li {
    margin: 3px 0;
}

table {
    width: 100%;
    border-collapse: collapse;
    margin: 12px 0 16px 0;
    font-size: 9.5pt;
    table-layout: fixed;
    word-wrap: break-word;
}

th {
    background-color: #003366;
    color: #ffffff;
    font-weight: 600;
    padding: 7px 8px;
    text-align: left;
    border: 1px solid #003366;
}

td {
    padding: 6px 8px;
    border: 1px solid #c8d8e8;
    vertical-align: top;
}

tr:nth-child(even) td {
    background-color: #f0f6ff;
}

tr:hover td {
    background-color: #e0eeff;
}

code {
    background-color: #f4f6f8;
    border: 1px solid #d0d8e0;
    border-radius: 3px;
    padding: 1px 4px;
    font-family: 'Consolas', 'Courier New', monospace;
    font-size: 9pt;
}

pre {
    background-color: #f4f6f8;
    border: 1px solid #c8d8e0;
    border-radius: 5px;
    padding: 12px 14px;
    overflow-x: auto;
    margin: 10px 0 14px 0;
    font-size: 8.5pt;
    line-height: 1.5;
}

pre code {
    background: none;
    border: none;
    padding: 0;
    font-size: 8.5pt;
    white-space: pre;
}

blockquote {
    border-left: 4px solid #4a90d9;
    background-color: #f0f6ff;
    margin: 10px 0;
    padding: 8px 14px;
    color: #333;
    font-style: italic;
}

strong {
    font-weight: 700;
    color: #1a1a1a;
}

em {
    font-style: italic;
    color: #333;
}

hr {
    border: none;
    border-top: 2px solid #cce0ff;
    margin: 20px 0;
}

a {
    color: #0066cc;
    text-decoration: none;
}

.page-break {
    page-break-after: always;
}

@page {
    size: A4;
    margin: 18mm 16mm 18mm 18mm;
    @bottom-right {
        content: counter(page) " / " counter(pages);
        font-size: 9pt;
        color: #888;
    }
}
"""

def build_html(md_text: str) -> str:
    md = markdown.Markdown(
        extensions=[
            "tables",
            "fenced_code",
            "codehilite",
            "nl2br",
            "sane_lists",
            "attr_list",
        ],
        extension_configs={
            "codehilite": {"css_class": "highlight", "guess_lang": False},
        }
    )
    body = md.convert(md_text)

    return f"""<!DOCTYPE html>
<html lang="fi">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>YTO3-TYTO-P – Uuden kurssin suunnitelma</title>
<style>
{CSS}
</style>
</head>
<body>
{body}
</body>
</html>
"""


def find_chrome() -> str:
    candidates = [
        r"C:\Program Files\Google\Chrome\Application\chrome.exe",
        r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe",
        r"C:\Program Files\Microsoft\Edge\Application\msedge.exe",
        r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",
    ]
    for path in candidates:
        if os.path.isfile(path):
            return path
    raise FileNotFoundError("Chrome tai Edge ei löydy oletuspoluista.")


def main():
    with open(MD_FILE, "r", encoding="utf-8") as f:
        md_text = f.read()

    html_content = build_html(md_text)

    with tempfile.NamedTemporaryFile(
        mode="w", suffix=".html", encoding="utf-8", delete=False
    ) as tmp:
        tmp.write(html_content)
        html_path = tmp.name

    try:
        chrome = find_chrome()
        print(f"Käytetään: {chrome}")
        print(f"HTML-väliaikatiedosto: {html_path}")

        cmd = [
            chrome,
            "--headless=new",
            "--disable-gpu",
            "--disable-software-rasterizer",
            "--no-sandbox",
            "--disable-dev-shm-usage",
            "--run-all-compositor-stages-before-draw",
            "--print-to-pdf-no-header",
            f"--print-to-pdf={PDF_FILE}",
            f"file:///{html_path.replace(chr(92), '/')}",
        ]
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=60)
        if result.returncode != 0:
            print("STDERR:", result.stderr)
            raise RuntimeError(f"Chromium poistui koodilla {result.returncode}")

        if os.path.isfile(PDF_FILE):
            size_kb = os.path.getsize(PDF_FILE) / 1024
            print(f"\n✓ PDF luotu onnistuneesti: {PDF_FILE}")
            print(f"  Tiedostokoko: {size_kb:.1f} KB")
        else:
            raise FileNotFoundError("PDF-tiedostoa ei löydy odotetussa sijainnissa.")
    finally:
        os.unlink(html_path)


if __name__ == "__main__":
    main()
