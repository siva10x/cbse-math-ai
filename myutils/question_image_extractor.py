import os
import re
import cv2
import pytesseract
from pytesseract import Output
from pdf2image import convert_from_path
from collections import defaultdict

from myutils.logger import setup_logger

logger = setup_logger(__name__)

def extract_images_for_questions(pdf_path, output_dir="question_images"):
    os.makedirs(output_dir, exist_ok=True)

    pages = convert_from_path(pdf_path, dpi=300)
    logger.info(f"Total pages: {len(pages)}")

    global_question_boxes = []  # Track all question boxes across pages
    image_counts = defaultdict(int)

    image_records = defaultdict(list)  # Final list to return: (question_id, img_path)

    for page_num, page in enumerate(pages, start=1):
        logger.info(f"Processing Page {page_num}")

        image_path = f"temp_page_{page_num}.png"
        page.save(image_path, "PNG")

        img = cv2.imread(image_path)
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        # OCR: Extract question boxes
        data = pytesseract.image_to_data(gray, output_type=Output.DICT)
        current_page_qboxes = []

        for i, text in enumerate(data['text']):
            text = text.strip()
            if re.match(r"^\d+\.\s*$", text):
                x, y, w, h = data['left'][i], data['top'][i], data['width'][i], data['height'][i]
                question_id = text.split('.')[0]
                # Save with absolute position reference
                current_page_qboxes.append({
                    "qid": question_id,
                    "page": page_num,
                    "y": y
                })

        global_question_boxes.extend(current_page_qboxes)

        # Detect red boxes
        hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
        lower_red1 = (0, 70, 50)
        upper_red1 = (10, 255, 255)
        lower_red2 = (170, 70, 50)
        upper_red2 = (180, 255, 255)

        mask1 = cv2.inRange(hsv, lower_red1, upper_red1)
        mask2 = cv2.inRange(hsv, lower_red2, upper_red2)
        mask = cv2.bitwise_or(mask1, mask2)

        contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        for cnt in contours:
            x, y, w, h = cv2.boundingRect(cnt)
            image_top = y

            # 🔍 Find the last question before this image across all pages
            matching_qid = None
            matching_qpage = None

            for qbox in global_question_boxes:
                if qbox["page"] < page_num:
                    matching_qid = qbox["qid"]
                    matching_qpage = qbox["page"]
                elif qbox["page"] == page_num and qbox["y"] < image_top:
                    matching_qid = qbox["qid"]
                    matching_qpage = qbox["page"]
                else:
                    break  # All future qboxes will be lower

            if matching_qid:
                key = (page_num, matching_qid)
                image_counts[key] += 1
                index = image_counts[key]

                crop = img[y:y+h, x:x+w]
                filename = f"{output_dir}/p{page_num}_q{matching_qid}_{index}.png"
                cv2.imwrite(filename, crop)
                logger.info(f"Saved: {filename} (linked to Q{matching_qid} from Page {matching_qpage})")

                image_records[f"Q{matching_qid}"].append(filename)

        os.remove(image_path)

    logger.info("✅ Done processing all pages!")
    return image_records

# 🧪 Test it independently
if __name__ == "__main__":
    output = extract_images_for_questions("data/raw_pdfs/sample_boxes.pdf", "question_images")
    print("\nExtracted Images:")
    for qid, path in output:
        print(f"{qid} → {path}")