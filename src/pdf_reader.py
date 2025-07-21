import fitz

def extract_text_without_footer_header(pdf_path):
    doc = fitz.open(pdf_path)
    full_text = []

    for page in doc:
        blocks = page.get_text("blocks")
        page_height = page.rect.height

        page_text = []

        for block in blocks:
            x0, y0, x1, y1, text, *_ = block

            if y0 < page_height * 0.07:
                continue

            page_text.append(text.strip())

        full_text.append("\n".join(page_text))

    return "\n\n".join(full_text)
