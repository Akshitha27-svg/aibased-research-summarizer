import fitz


def extract_text_from_pdf(path):

    doc = fitz.open(path)

    text = ""

    for page in doc:
        text += page.get_text()

    return text


def chunk_text(text, size=350, overlap=120):

    words = text.split()

    chunks = []

    for i in range(0, len(words), size - overlap):

        chunk = " ".join(words[i:i+size])

        chunks.append(chunk)

    return chunks