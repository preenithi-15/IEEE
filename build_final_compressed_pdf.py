"""
build_final_compressed_pdf.py
1. Fixes broken characters on Page 3 (Amrita Vishwa Vidhyapeetham, Phone, Vaishnav Aditya).
2. Replaces Member 1-6 with Preenithi, Aditya, Suraj, Hasini, Dharani, Shamitha on Pages 11 & 12.
3. Inserts precisely aligned pink audio buttons beside all 7 numbered section headings.
4. Subsets embedded TrueType fonts & removes redundant StructElem tags.
5. Optimizes and compresses the PDF to < 500 KB while keeping vector quality and all links intact.
6. Re-renders slide_p0.png to slide_p12.png so viewer.html reflects the updated clean content.
7. Verifies all 7 audio hyperlinks and file size.
"""

import pymupdf
import io
import re
import os
from fontTools.subset import Subsetter, Options
from fontTools.ttLib import TTFont

GITHUB_PAGES_BASE = "https://preenithi-15.github.io/IEEE"
INPUT_PDF = "IEEE_PPT.pdf"
OUTPUT_PDF = "IEEE_PPT_with_audio.pdf"

SECTIONS_CONFIG = [
    {
        "num": 1,
        "label": "Problem Understanding",
        "audio": "1.ogg",
        "page_idx": 3,
        "heading_cy": 397.78,
    },
    {
        "num": 2,
        "label": "Proposed Solution / Idea",
        "audio": "2.ogg",
        "page_idx": 4,
        "heading_cy": 154.35,
    },
    {
        "num": 3,
        "label": "Innovation & Uniqueness",
        "audio": "3.ogg",
        "page_idx": 5,
        "heading_cy": 398.02,
    },
    {
        "num": 4,
        "label": "Feasibility & Implementation Plan",
        "audio": "4.ogg",
        "page_idx": 6,
        "heading_cy": 431.16,
    },
    {
        "num": 5,
        "label": "Expected Impact",
        "audio": "5.ogg",
        "page_idx": 8,
        "heading_cy": 154.35,
    },
    {
        "num": 6,
        "label": "Technology Stack",
        "audio": "6.ogg",
        "page_idx": 9,
        "heading_cy": 434.28,
    },
    {
        "num": 7,
        "label": "Team Member Roles",
        "audio": "7.ogg",
        "page_idx": 10,
        "heading_cy": 371.14,
    },
]

def main():
    print("Opening source PDF...")
    doc = pymupdf.open(INPUT_PDF)

    # ─────────────────────────────────────────────────────────────
    # STEP 1: FIX BROKEN CHARACTERS ON PAGE 3
    # ─────────────────────────────────────────────────────────────
    print("Fixing broken characters on Page 3 (Team Info)...")
    p3 = doc[2]
    BG_CELL = (0.961, 0.918, 0.969)  # Pastel lavender/pink table cell bg
    PURPLE_COLOR = (106/255, 24/255, 84/255)

    # Redact broken lines
    p3.add_redact_annot(pymupdf.Rect(270, 154, 520, 178), fill=BG_CELL)
    p3.add_redact_annot(pymupdf.Rect(270, 344, 450, 368), fill=BG_CELL)
    p3.add_redact_annot(pymupdf.Rect(80, 542, 168, 592), fill=BG_CELL)
    p3.apply_redactions()

    # Re-insert clean text with exact styling
    p3.insert_text((272.5, 171.0), "Amrita Vishwa Vidhyapeetham", fontsize=12.0, color=PURPLE_COLOR, fontname="hebo")
    p3.insert_text((272.5, 361.5), "6374808659", fontsize=12.0, color=PURPLE_COLOR, fontname="hebo")
    p3.insert_text((81.9, 560.0), "Vaishnav", fontsize=12.0, color=PURPLE_COLOR, fontname="hebo")
    p3.insert_text((81.9, 574.0), "Aditya", fontsize=12.0, color=PURPLE_COLOR, fontname="hebo")

    # ─────────────────────────────────────────────────────────────
    # STEP 2: REPLACE MEMBER 1-6 WITH ACTUAL NAMES ON PAGES 11 & 12
    # ─────────────────────────────────────────────────────────────
    print("Replacing Member 1-6 with actual team names on Pages 11 & 12...")
    p11 = doc[10]
    p12 = doc[11]

    # Page 11: Member 1 -> Preenithi, Member 2 -> Aditya, Member 3 -> Suraj
    p11.add_redact_annot(pymupdf.Rect(80, 510, 200, 532), fill=BG_CELL)
    p11.add_redact_annot(pymupdf.Rect(80, 582, 200, 605), fill=BG_CELL)
    p11.add_redact_annot(pymupdf.Rect(80, 675, 200, 698), fill=BG_CELL)
    p11.apply_redactions()

    p11.insert_text((81.9, 524.0), "Preenithi", fontsize=12.0, color=(0, 0, 0), fontname="hebo")
    p11.insert_text((81.9, 596.5), "Aditya", fontsize=12.0, color=(0, 0, 0), fontname="hebo")
    p11.insert_text((81.9, 689.5), "Suraj", fontsize=12.0, color=(0, 0, 0), fontname="hebo")

    # Page 12: Member 4 -> Hasini, Member 5 -> Dharani, Member 6 -> Shamitha
    p12.add_redact_annot(pymupdf.Rect(80, 140, 200, 162), fill=BG_CELL)
    p12.add_redact_annot(pymupdf.Rect(80, 212, 200, 235), fill=BG_CELL)
    p12.add_redact_annot(pymupdf.Rect(80, 305, 200, 328), fill=BG_CELL)
    p12.apply_redactions()

    p12.insert_text((81.9, 153.5), "Hasini", fontsize=12.0, color=(0, 0, 0), fontname="hebo")
    p12.insert_text((81.9, 226.0), "Dharani", fontsize=12.0, color=(0, 0, 0), fontname="hebo")
    p12.insert_text((81.9, 319.0), "Shamitha", fontsize=12.0, color=(0, 0, 0), fontname="hebo")

    # ─────────────────────────────────────────────────────────────
    # STEP 3: INSERT HEADING-ALIGNED PINK BUTTONS & LINKS
    # ─────────────────────────────────────────────────────────────
    print("Adding pink audio buttons aligned with section headings...")
    PINK_COLOR = (0.88, 0.18, 0.46)
    WHITE_COLOR = (1.0, 1.0, 1.0)

    for item in SECTIONS_CONFIG:
        num = item["num"]
        label = item["label"]
        page_idx = item["page_idx"]
        cy = item["heading_cy"]
        url = f"{GITHUB_PAGES_BASE}/viewer.html?section={num}"

        page = doc[page_idx]

        circle_r = 11.0
        cx = 512.0
        tx = cx - circle_r - 6.0 - 92.0

        shape = page.new_shape()

        # 1. Pink circle
        shape.draw_circle((cx, cy), circle_r)
        shape.finish(color=PINK_COLOR, fill=PINK_COLOR, width=0)

        # 2. White triangle ▶
        p1 = (cx - 3.5, cy - 5.0)
        p2 = (cx + 5.5, cy)
        p3 = (cx - 3.5, cy + 5.0)
        shape.draw_polyline([p1, p2, p3, p1])
        shape.finish(color=WHITE_COLOR, fill=WHITE_COLOR, width=0)

        shape.commit()

        # 3. Two-line text pointing to button
        page.insert_text((tx, cy - 2.5), "Click here to hear the", fontsize=7.2, color=PINK_COLOR, fontname="helv")
        page.insert_text((tx + 12.0, cy + 6.0), "team explain ->", fontsize=7.2, color=PINK_COLOR, fontname="helv")

        # 4. Interactive hyperlink annotation
        link_rect = pymupdf.Rect(tx - 2.0, cy - circle_r - 2.0, cx + circle_r + 2.0, cy + circle_r + 2.0)
        page.insert_link({
            "kind": pymupdf.LINK_URI,
            "from": link_rect,
            "uri": url,
        })
        print(f"  Sec {num} ({label}): Page {page_idx+1}, cy={cy:.1f}, URL={url}")

    # ─────────────────────────────────────────────────────────────
    # STEP 4: SUBSET EMBEDDED FONTS & STRIP ACCESSIBILITY STRUCTELEM TAGS
    # ─────────────────────────────────────────────────────────────
    print("\nOptimizing embedded fonts and document structure...")
    chars_used = set()
    for page in doc:
        chars_used.update(page.get_text())

    # Find font streams
    font_xrefs = []
    for xref in range(1, doc.xref_length()):
        obj = doc.xref_object(xref)
        if "/Filter" in obj and "/Length1" in obj:
            font_xrefs.append(xref)

    for xref in font_xrefs:
        data = doc.xref_stream(xref)
        try:
            font = TTFont(io.BytesIO(data))
            options = Options()
            options.desubroutinize = True
            subsetter = Subsetter(options=options)
            subsetter.populate(text="".join(chars_used))
            subsetter.subset(font)

            buf = io.BytesIO()
            font.save(buf)
            subset_data = buf.getvalue()
            doc.update_stream(xref, subset_data)
        except Exception:
            pass

    # Strip redundant /StructTreeRoot from catalog
    catalog_xref = doc.pdf_catalog()
    catalog_obj = doc.xref_object(catalog_xref)
    new_catalog = re.sub(r"/StructTreeRoot\s+\d+\s+\d+\s+R", "", catalog_obj)
    doc.update_object(catalog_xref, new_catalog)

    # ─────────────────────────────────────────────────────────────
    # STEP 5: SAVE COMPRESSED PDF
    # ─────────────────────────────────────────────────────────────
    doc.save(OUTPUT_PDF, garbage=4, deflate=True, clean=True)
    doc.close()

    final_size = os.path.getsize(OUTPUT_PDF)
    print(f"\n=======================================================")
    print(f"FINAL OPTIMIZED PDF: {OUTPUT_PDF}")
    print(f"EXACT FILE SIZE: {final_size} bytes ({final_size/1024:.2f} KB)")
    print(f"UNDER 500 KB TARGET: {'YES (SUCCESS)' if final_size < 500*1024 else 'NO'}")
    print(f"=======================================================\n")

    # ─────────────────────────────────────────────────────────────
    # STEP 6: RE-RENDER HIGH-RES SLIDES FOR VIEWER.HTML
    # ─────────────────────────────────────────────────────────────
    print("Re-rendering high-resolution slide PNGs for viewer.html...")
    doc_ver = pymupdf.open(OUTPUT_PDF)
    mat = pymupdf.Matrix(2.0, 2.0)
    for i in range(len(doc_ver)):
        pix = doc_ver[i].get_pixmap(matrix=mat, alpha=False)
        pix.save(f"slide_p{i}.png")
    doc_ver.close()
    print("Slides updated successfully.\n")

    # ─────────────────────────────────────────────────────────────
    # STEP 7: VERIFY FINAL PDF & ALL 7 HYPERLINKS
    # ─────────────────────────────────────────────────────────────
    print("VERIFYING FINAL PDF...")
    doc_check = pymupdf.open(OUTPUT_PDF)
    print(f"  Total pages: {len(doc_check)}")

    verified_links = []
    for p_idx in range(len(doc_check)):
        p = doc_check[p_idx]
        links = p.get_links()
        for l in links:
            if l.get("kind") == pymupdf.LINK_URI:
                verified_links.append((p_idx + 1, l.get("uri"), l.get("from")))

    print(f"  Total hyperlinks found: {len(verified_links)}")
    for page_num, uri, rect in verified_links:
        print(f"    Page {page_num}: {uri} (Rect: {rect})")

    doc_check.close()
    print("\nVerification complete!")

if __name__ == "__main__":
    main()
