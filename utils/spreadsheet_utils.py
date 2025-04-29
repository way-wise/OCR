import pandas as pd
from pathlib import Path
from config import OUTPUT_DIR
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle
from reportlab.lib import colors

def handle_xlsx(file):
    try:
        # Read all sheets from Excel file
        excel_file = pd.ExcelFile(file)
        sheets_data = []
        
        for sheet_name in excel_file.sheet_names:
            df = pd.read_excel(file, sheet_name=sheet_name)
            sheets_data.append((sheet_name, df))
        
        # Create PDF
        pdf_path = OUTPUT_DIR / file.with_suffix(".pdf").name
        doc = SimpleDocTemplate(str(pdf_path), pagesize=letter)
        elements = []
        
        # Convert each sheet to text and add to PDF
        text_content = []
        for sheet_name, df in sheets_data:
            text_content.append(f"\nSheet: {sheet_name}\n")
            
            # Convert DataFrame to list for table
            data = [df.columns.tolist()] + df.values.tolist()
            
            # Create table
            table = Table(data)
            table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, 0), 12),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                ('TEXTCOLOR', (0, 1), (-1, -1), colors.black),
                ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
                ('FONTSIZE', (0, 1), (-1, -1), 10),
                ('GRID', (0, 0), (-1, -1), 1, colors.black)
            ]))
            elements.append(table)
            
            # Add sheet data to text content
            text_content.append(df.to_string())
        
        # Build PDF
        doc.build(elements)
        
        return pdf_path, "\n".join(text_content)
        
    except Exception as e:
        print(f"Error processing Excel file {file}: {str(e)}")
        return None, f"Error: {str(e)}" 