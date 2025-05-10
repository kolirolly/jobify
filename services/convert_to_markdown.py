import markdown
from weasyprint import HTML


def markdown_to_pdf(markdown_text: str, output_pdf_path: str):
    """Converts Markdown text to a PDF file."""
    # Convert Markdown to HTML
    html_content = markdown.markdown(markdown_text)

    # Create a full HTML document (optional but good for styling)
    full_html = f"""
    <html>
        <head>
            <meta charset="utf-8">
            <style>
                body {{
                    font-family: Arial, sans-serif;
                    margin: 40px;
                }}
                h1, h2, h3, h4, h5, h6 {{
                    color: #333;
                }}
                p {{
                    margin: 10px 0;
                }}
                ul, ol {{
                    margin: 10px 20px;
                }}
            </style>
        </head>
        <body>
            {html_content}
        </body>
    </html>
    """

    # Convert the HTML to a PDF
    HTML(string=full_html).write_pdf(output_pdf_path)
    return True
    # print(f"PDF created successfully at: {output_pdf_path}")
