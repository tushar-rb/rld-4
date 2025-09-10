"""
Data Generator for Revenue Leakage Detection System
Generates sample PDF, CSV, and JSON files with realistic billing, provisioning, and contract data
"""
import os
import json
import csv
import random
from datetime import datetime, timedelta
from fpdf import FPDF
import fitz  # PyMuPDF
import pandas as pd

class DataGenerator:
    """Generate sample data files for testing the Revenue Leakage Detection System"""
    
    def __init__(self, output_dir="sample_data"):
        """Initialize the data generator"""
        self.output_dir = output_dir
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
    
    def generate_sample_billing_data(self, num_records=50):
        """Generate sample billing data"""
        billing_data = []
        customer_ids = [f"CUST-{i:03d}" for i in range(1, 21)]
        service_ids = [f"SERVICE-{i:03d}" for i in range(1, 11)]
        
        for i in range(num_records):
            billing_record = {
                "id": f"BILL-{1000+i}",
                "customer_id": random.choice(customer_ids),
                "invoice_id": f"INV-{random.randint(10000, 99999)}",
                "service_id": random.choice(service_ids),
                "amount": round(random.uniform(50.0, 500.0), 2),
                "currency": "USD",
                "billing_date": (datetime.now() - timedelta(days=random.randint(0, 365))).strftime("%Y-%m-%d"),
                "due_date": (datetime.now() + timedelta(days=random.randint(7, 30))).strftime("%Y-%m-%d"),
                "status": random.choice(["paid", "unpaid", "overdue"]),
                "billing_period_start": (datetime.now() - timedelta(days=random.randint(30, 90))).strftime("%Y-%m-%d"),
                "billing_period_end": (datetime.now() - timedelta(days=random.randint(0, 30))).strftime("%Y-%m-%d")
            }
            billing_data.append(billing_record)
        
        return billing_data
    
    def generate_sample_provisioning_data(self, num_records=50):
        """Generate sample provisioning data"""
        provisioning_data = []
        customer_ids = [f"CUST-{i:03d}" for i in range(1, 21)]
        service_ids = [f"SERVICE-{i:03d}" for i in range(1, 11)]
        plans = ["BASIC", "PREMIUM", "ENTERPRISE", "STANDARD"]
        
        for i in range(num_records):
            provisioning_record = {
                "id": f"PROV-{1000+i}",
                "customer_id": random.choice(customer_ids),
                "service_id": random.choice(service_ids),
                "provision_date": (datetime.now() - timedelta(days=random.randint(0, 365))).strftime("%Y-%m-%d"),
                "status": random.choice(["active", "inactive", "suspended"]),
                "plan_id": random.choice(plans),
                "start_date": (datetime.now() - timedelta(days=random.randint(0, 365))).strftime("%Y-%m-%d"),
                "end_date": (datetime.now() + timedelta(days=random.randint(30, 365))).strftime("%Y-%m-%d") if random.choice([True, False]) else None
            }
            provisioning_data.append(provisioning_record)
        
        return provisioning_data
    
    def generate_sample_usage_data(self, num_records=100):
        """Generate sample usage data"""
        usage_data = []
        customer_ids = [f"CUST-{i:03d}" for i in range(1, 21)]
        service_ids = [f"SERVICE-{i:03d}" for i in range(1, 11)]
        usage_types = ["bandwidth", "storage", "api_calls", "transactions"]
        units = ["GB", "MB", "calls", "transactions"]
        
        for i in range(num_records):
            usage_record = {
                "id": f"USAGE-{1000+i}",
                "customer_id": random.choice(customer_ids),
                "service_id": random.choice(service_ids),
                "usage_date": (datetime.now() - timedelta(days=random.randint(0, 365))).strftime("%Y-%m-%d"),
                "usage_type": random.choice(usage_types),
                "quantity": round(random.uniform(10.0, 1000.0), 2),
                "unit": random.choice(units),
                "cost": round(random.uniform(5.0, 200.0), 2)
            }
            usage_data.append(usage_record)
        
        return usage_data
    
    def generate_sample_contract_data(self, num_records=20):
        """Generate sample contract data"""
        contract_data = []
        customer_ids = [f"CUST-{i:03d}" for i in range(1, 21)]
        
        for i in range(num_records):
            contract_record = {
                "id": f"CONTRACT-{1000+i}",
                "customer_id": random.choice(customer_ids),
                "contract_date": (datetime.now() - timedelta(days=random.randint(30, 730))).strftime("%Y-%m-%d"),
                "effective_date": (datetime.now() - timedelta(days=random.randint(0, 365))).strftime("%Y-%m-%d"),
                "expiry_date": (datetime.now() + timedelta(days=random.randint(30, 730))).strftime("%Y-%m-%d") if random.choice([True, False]) else None,
                "status": random.choice(["active", "expired", "terminated"]),
                "clauses": [
                    {
                        "id": f"CLAUSE-{1000+i}-01",
                        "contract_id": f"CONTRACT-{1000+i}",
                        "clause_type": "rate",
                        "content": f"Service rate is ${round(random.uniform(100.0, 1000.0), 2)} per month",
                        "effective_date": (datetime.now() - timedelta(days=random.randint(0, 365))).strftime("%Y-%m-%d"),
                        "expiry_date": (datetime.now() + timedelta(days=random.randint(30, 730))).strftime("%Y-%m-%d") if random.choice([True, False]) else None
                    }
                ]
            }
            contract_data.append(contract_record)
        
        return contract_data
    
    def generate_pdf_billing_file(self, filename="sample_billing.pdf", num_records=20):
        """Generate a sample PDF billing file"""
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", "B", 16)
        
        # Title
        pdf.cell(0, 10, "Monthly Billing Statement", ln=True, align="C")
        pdf.ln(10)
        
        # Generate sample billing data
        billing_data = self.generate_sample_billing_data(num_records)
        
        # Table header
        pdf.set_font("Arial", "B", 12)
        pdf.cell(30, 10, "Invoice ID", 1)
        pdf.cell(30, 10, "Customer ID", 1)
        pdf.cell(30, 10, "Service ID", 1)
        pdf.cell(30, 10, "Amount (USD)", 1)
        pdf.cell(30, 10, "Billing Date", 1)
        pdf.cell(30, 10, "Status", 1)
        pdf.ln()
        
        # Table rows
        pdf.set_font("Arial", size=10)
        for record in billing_data:
            pdf.cell(30, 10, record["invoice_id"][:10], 1)
            pdf.cell(30, 10, record["customer_id"][:10], 1)
            pdf.cell(30, 10, record["service_id"][:10], 1)
            pdf.cell(30, 10, f"${record['amount']:.2f}", 1)
            pdf.cell(30, 10, record["billing_date"], 1)
            pdf.cell(30, 10, record["status"][:10], 1)
            pdf.ln()
        
        # Save the PDF
        filepath = os.path.join(self.output_dir, filename)
        pdf.output(filepath)
        return filepath, billing_data
    
    def generate_csv_provisioning_file(self, filename="sample_provisioning.csv", num_records=20):
        """Generate a sample CSV provisioning file"""
        provisioning_data = self.generate_sample_provisioning_data(num_records)
        
        filepath = os.path.join(self.output_dir, filename)
        with open(filepath, 'w', newline='') as csvfile:
            fieldnames = ["id", "customer_id", "service_id", "provision_date", "status", "plan_id", "start_date", "end_date"]
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            
            writer.writeheader()
            for record in provisioning_data:
                writer.writerow(record)
        
        return filepath, provisioning_data
    
    def generate_json_contract_file(self, filename="sample_contracts.json", num_records=10):
        """Generate a sample JSON contract file"""
        contract_data = self.generate_sample_contract_data(num_records)
        
        filepath = os.path.join(self.output_dir, filename)
        with open(filepath, 'w') as jsonfile:
            json.dump(contract_data, jsonfile, indent=2)
        
        return filepath, contract_data
    
    def read_pdf_with_ocr(self, pdf_path):
        """Read PDF file content using OCR (placeholder implementation)"""
        try:
            # Open the PDF
            doc = fitz.open(pdf_path)
            text = ""
            
            # Extract text from each page
            for page_num in range(len(doc)):
                page = doc.load_page(page_num)
                text += page.get_text()
            
            doc.close()
            return text
        except Exception as e:
            print(f"Error reading PDF: {e}")
            return None
    
    def read_csv_file(self, csv_path):
        """Read CSV file content"""
        try:
            df = pd.read_csv(csv_path)
            return df.to_dict('records')
        except Exception as e:
            print(f"Error reading CSV: {e}")
            return None
    
    def read_json_file(self, json_path):
        """Read JSON file content"""
        try:
            with open(json_path, 'r') as file:
                data = json.load(file)
            return data
        except Exception as e:
            print(f"Error reading JSON: {e}")
            return None

# Example usage
if __name__ == "__main__":
    generator = DataGenerator()
    
    # Generate sample files
    pdf_path, pdf_data = generator.generate_pdf_billing_file()
    print(f"Generated PDF: {pdf_path}")
    
    csv_path, csv_data = generator.generate_csv_provisioning_file()
    print(f"Generated CSV: {csv_path}")
    
    json_path, json_data = generator.generate_json_contract_file()
    print(f"Generated JSON: {json_path}")
    
    # Read the files back
    pdf_content = generator.read_pdf_with_ocr(pdf_path)
    print(f"PDF content length: {len(pdf_content) if pdf_content else 0} characters")
    
    csv_content = generator.read_csv_file(csv_path)
    print(f"CSV records: {len(csv_content) if csv_content else 0}")
    
    json_content = generator.read_json_file(json_path)
    print(f"JSON records: {len(json_content) if json_content else 0}")