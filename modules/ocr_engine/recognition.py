import pytesseract
import cv2

def ocr_read(img, mask, langs):
    # Наложить маску
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    text = pytesseract.image_to_string(gray, lang='+'.join(langs), config='--psm 7')
    text = ''.join(filter(str.isalnum, text)).upper()
    # Доверие как средняя вероятность символов (заглушка)
    confidence = 0.9
    return text, confidence