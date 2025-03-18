import json
import fitz  # PyMuPDF
import os

def extract_text_from_pdf(pdf_path):
    """Extract text from PDF and save as JSON."""
    try:
        doc = fitz.open(pdf_path)
        text = "\n".join([page.get_text("text") for page in doc])
        doc.close()

        # Clean up movie title
        movie_name = os.path.basename(pdf_path).replace(".pdf", "").replace("_", " ").replace("\xa0", " ")

        # Normalize whitespace
        text = " ".join(text.split())

        # Save JSON
        output_folder = "extracted"
        os.makedirs(output_folder, exist_ok=True)
        json_filename = os.path.join(output_folder, f"{movie_name}.json")

        with open(json_filename, "w", encoding="utf-8") as json_file:
            json.dump({"title": movie_name, "text": text}, json_file, indent=4, ensure_ascii=False)

        print(f"Extracted text saved as: {json_filename}")

    except Exception as e:
        print(f"Error extracting text from {pdf_path}: {e}")
