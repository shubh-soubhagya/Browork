import fitz  # PyMuPDF

def extract_text_from_pdf(pdf_path):
    text = ""
    with fitz.open(pdf_path) as doc:
        for page_num, page in enumerate(doc, start=1):
            page_text = page.get_text()
            text += f"\n--- Page {page_num} ---\n{page_text}"

    return text  # return the variable directly

# if __name__ == "__main__":
#     text = extract_text_from_pdf("Question.pdf")
#     print("✅ PDF text extracted and stored in variable 'pdf_text'.")
#     print("\n📝 Preview:\n")
#     print(text[:1000])  # print first 1000 characters for preview

pdf_text = extract_text_from_pdf("Question.pdf")
