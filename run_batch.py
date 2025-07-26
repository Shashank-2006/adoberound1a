import os
import json
from pdf_extractor import PDFOutlineExtractor

INPUT_DIR = "/app/input"
OUTPUT_DIR = "/app/output"

def main():
    extractor = PDFOutlineExtractor()
    pdf_files = [f for f in os.listdir(INPUT_DIR) if f.lower().endswith(".pdf")]

    for pdf_file in pdf_files:
        pdf_path = os.path.join(INPUT_DIR, pdf_file)
        result = extractor.extract_outline(pdf_path)
        output_filename = os.path.splitext(pdf_file)[0] + ".json"
        output_path = os.path.join(OUTPUT_DIR, output_filename)
        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(result, f, indent=2, ensure_ascii=False)
        print(f"Processed {pdf_file} -> {output_filename}")

if __name__ == "__main__":
    main()
