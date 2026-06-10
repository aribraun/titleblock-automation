import fitz
from pathlib import Path

TITLEBLOCK = Path("titleblock.pdf")
PLANS_DIR = Path("plans")
OUTPUT_DIR = Path("output")


FRAME = fitz.Rect(35, 35, 1000, 755)


def place_plan_in_titleblock(plan_path: Path):
    OUTPUT_DIR.mkdir(exist_ok=True)

    title_doc = fitz.open(TITLEBLOCK)
    plan_doc = fitz.open(plan_path)

    if len(title_doc) == 0:
        raise ValueError("Titleblock PDF has no pages.")

    if len(plan_doc) == 0:
        raise ValueError(f"{plan_path.name} has no pages.")

    output_doc = fitz.open()

    for page_number in range(len(plan_doc)):
        title_page_doc = fitz.open(TITLEBLOCK)
        title_page = title_page_doc[0]

        plan_page = plan_doc[page_number]

        # Places the plan page into the frame.
        title_page.show_pdf_page(
            FRAME,
            plan_doc,
            page_number,
            keep_proportion=True,
            overlay=True,
        )

        output_doc.insert_pdf(title_page_doc)

    output_path = OUTPUT_DIR / f"{plan_path.stem}_titleblocked.pdf"
    output_doc.save(output_path)
    output_doc.close()
    plan_doc.close()
    title_doc.close()

    print(f"Created: {output_path}")


def main():
    if not TITLEBLOCK.exists():
        raise FileNotFoundError("Missing titleblock.pdf")

    pdfs = list(PLANS_DIR.glob("*.pdf"))

    if not pdfs:
        raise FileNotFoundError("No PDF files found in plans/")

    for plan_path in pdfs:
        place_plan_in_titleblock(plan_path)


if __name__ == "__main__":
    main()
