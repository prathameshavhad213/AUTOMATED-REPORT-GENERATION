import csv
import os
from fpdf import FPDF

# Function to read data from CSV file
def read_csv_file(file_path):
    """Reads data from a CSV file and returns it as a list of dictionaries."""
    data = []
    try:
        with open(file_path, newline='', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                data.append(row)
    except FileNotFoundError:
        print("Error: File not found!")
    except Exception as e:
        print(f"Error reading file: {e}")
    return data

# Function to analyze the data
def analyze_data(data):
    """Calculates total sales and number of records."""
    try:
        total_sales = sum(float(row['Quantity']) * float(row['Price']) for row in data)
        total_records = len(data)
        return total_sales, total_records
    except KeyError:
        print("Error: Invalid CSV format. Ensure 'Quantity' and 'Price' columns exist.")
        return 0, 0
    except Exception as e:
        print(f"Error analyzing data: {e}")
        return 0, 0

# Function to generate PDF report
def generate_pdf_report(data, total_sales, total_records, output_file):
    """Generates a PDF report from the analyzed data."""
    try:
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", size=12)

        # Report Title
        pdf.set_font("Arial", style="B", size=16)
        pdf.cell(200, 10, txt="Automated Sales Report", ln=True, align='C')
        pdf.ln(10)

        # Table Headers
        pdf.set_font("Arial", style="B", size=12)
        pdf.cell(60, 10, txt="Product", border=1, align='C')
        pdf.cell(40, 10, txt="Quantity", border=1, align='C')
        pdf.cell(40, 10, txt="Price (INR)", border=1, align='C')
        pdf.cell(50, 10, txt="Total (INR)", border=1, align='C')
        pdf.ln()

        # Table Data
        pdf.set_font("Arial", size=12)
        for row in data:
            product = row['Product']
            quantity = int(row['Quantity'])
            price = float(row['Price'])
            total = quantity * price

            pdf.cell(60, 10, txt=product, border=1)
            pdf.cell(40, 10, txt=str(quantity), border=1)
            pdf.cell(40, 10, txt=f"INR {price:.2f}", border=1)
            pdf.cell(50, 10, txt=f"INR {total:.2f}", border=1)
            pdf.ln()

        # Summary Section
        pdf.ln(10)
        pdf.cell(60, 10, txt=f"Total Records: {total_records}")
        pdf.ln(10)
        pdf.cell(60, 10, txt=f"Total Sales: INR {total_sales:.2f}")

        # Save PDF
        pdf.output(output_file)
        print(f"PDF report successfully generated: {output_file}")

    except Exception as e:
        print(f"Error generating PDF: {e}")

# Main Execution
if __name__ == "__main__":
    csv_file_path = input("Enter the path to your CSV file: ").strip()
    if not os.path.exists(csv_file_path):
        print("Error: File does not exist. Please provide a valid file path.")
    else:
        data = read_csv_file(csv_file_path)
        if data:
            total_sales, total_records = analyze_data(data)
            if total_records > 0:
                generate_pdf_report(data, total_sales, total_records, "professional_sales_report.pdf")
            else:
                print("Error: No valid records found in the CSV file.")
        else:
            print("Error: Unable to process the CSV file.")
