"""
OCR Utility for reading PDF files
"""
import fitz  # PyMuPDF
import pytesseract
from PIL import Image
import io
import cv2
import numpy as np

class OCRReader:
    """Read text from PDF files using OCR"""
    
    def __init__(self):
        """Initialize OCR reader"""
        # You may need to specify the path to tesseract executable on Windows
        # pytesseract.pytesseract.tesseract_cmd = r'C:\\Program Files\\Tesseract-OCR\\tesseract.exe'
        pass
    
    def preprocess_image(self, image):
        """Preprocess image for better OCR results"""
        # Convert PIL image to OpenCV format
        img_cv = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)
        
        # Convert to grayscale
        gray = cv2.cvtColor(img_cv, cv2.COLOR_BGR2GRAY)
        
        # Apply threshold to get image with only black and white
        _, thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
        
        # Convert back to PIL Image
        return Image.fromarray(thresh)
    
    def read_pdf_with_ocr(self, pdf_path):
        """Extract text from PDF using OCR"""
        try:
            # Open the PDF
            doc = fitz.open(pdf_path)
            full_text = ""
            
            # Process each page
            for page_num in range(len(doc)):
                page = doc.load_page(page_num)
                
                # Get page as image
                mat = fitz.Matrix(2.0, 2.0)  # Zoom factor
                pix = page.get_pixmap(matrix=mat)
                
                # Convert to PIL Image
                img_data = pix.tobytes("ppm")
                image = Image.open(io.BytesIO(img_data))
                
                # Preprocess image
                processed_image = self.preprocess_image(image)
                
                # Perform OCR
                text = pytesseract.image_to_string(processed_image)
                full_text += f"--- Page {page_num + 1} ---\n{text}\n\n"
            
            doc.close()
            return full_text
        except Exception as e:
            print(f"Error reading PDF with OCR: {e}")
            return None
    
    def read_image_with_ocr(self, image_path):
        """Extract text from image using OCR"""
        try:
            # Open image
            image = Image.open(image_path)
            
            # Preprocess image
            processed_image = self.preprocess_image(image)
            
            # Perform OCR
            text = pytesseract.image_to_string(processed_image)
            return text
        except Exception as e:
            print(f"Error reading image with OCR: {e}")
            return None

# Example usage
if __name__ == "__main__":
    ocr_reader = OCRReader()
    
    # Example: Read a PDF file with OCR
    # text = ocr_reader.read_pdf_with_ocr("sample.pdf")
    # print(text)
    pass