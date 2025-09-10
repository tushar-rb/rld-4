"""
Test script for data generator
"""
from app.utils.data_generator import DataGenerator

def test_data_generator():
    """Test the data generator functionality"""
    generator = DataGenerator()
    
    print("Testing data generator...")
    
    # Generate sample files
    print("Generating PDF billing file...")
    pdf_path, pdf_data = generator.generate_pdf_billing_file()
    print(f"Generated PDF: {pdf_path}")
    print(f"PDF records: {len(pdf_data)}")
    
    print("\nGenerating CSV provisioning file...")
    csv_path, csv_data = generator.generate_csv_provisioning_file()
    print(f"Generated CSV: {csv_path}")
    print(f"CSV records: {len(csv_data)}")
    
    print("\nGenerating JSON contract file...")
    json_path, json_data = generator.generate_json_contract_file()
    print(f"Generated JSON: {json_path}")
    print(f"JSON records: {len(json_data)}")
    
    # Test reading files
    print("\nTesting file reading...")
    
    # Read PDF (using PyMuPDF text extraction)
    pdf_content = generator.read_pdf_with_ocr(pdf_path)
    print(f"PDF content extracted: {len(pdf_content) if pdf_content else 0} characters")
    
    # Read CSV
    csv_content = generator.read_csv_file(csv_path)
    print(f"CSV records read: {len(csv_content) if csv_content else 0}")
    
    # Read JSON
    json_content = generator.read_json_file(json_path)
    print(f"JSON records read: {len(json_content) if json_content else 0}")

if __name__ == "__main__":
    test_data_generator()