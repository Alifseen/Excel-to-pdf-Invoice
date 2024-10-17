"""Convert Excel Sheets tracking Sales into PDF Invoices
"""
## 1. Imported Libraries
from fpdf import FPDF  ## To create PDF
import glob  ## To save all file paths in a python list
import pandas as pd  ## to open and process excel file
import pathlib  ## to get the date and invoice number from filename

## 2. Save all files in Files folder ending with .xlsx in a variable
filepaths = glob.glob("Files/*.xlsx")

## 3. For loop to go over the filepath list to operate on each file.
for path in filepaths:

    ## 4. Initiate a PDF with portrait A4 with mm units and no auto page breaks. Do not initiate outside the loop.
    pdf = FPDF(orientation="P", unit="mm", format="A4")
    pdf.set_auto_page_break(False)

    ## 12. Add a variable to store total from each row in the
    total_amount = 0

    ## 5. Load the excel file and sheet
    df = pd.read_excel(path, sheet_name="Sheet 1")

    ## 6. Get invoice number and date from file name
    filename = pathlib.Path(path).stem  ## get file name from the file path using stem method
    invoice_number = filename.split("-")[0]  ## get invoice number by splitting filename with "-" and get first half
    invoice_date = filename.split("-")[1]  ## get date by splitting filename with "-" and get second half
    year, month, day = invoice_date.split(".")  ## Split date into day, month and year (optional)

    ## 7. Add a page
    pdf.add_page()

    ## 8. Add invoice number and date as invoice heading
    pdf.set_font(family="Helvetica", style="B", size=15)
    pdf.cell(w=0, h=10, txt=f"Invoice No: {invoice_number}", ln=1, border=0)
    pdf.cell(w=0, h=10, txt=f"Date: {day}-{month}-{year}", ln=1, border=0)

    ## 9. Add line breaks for the table
    pdf.ln(7)

    ## 10. Add table headers
    pdf.set_font(family="Helvetica", style="B", size=10)
    pdf.cell(w=30, h=7, txt="Product ID", ln=0, border=1)  ## no line break from first till last cell in row
    pdf.cell(w=70, h=7, txt="Product Name", ln=0, border=1)
    pdf.cell(w=30, h=7, txt="Quantity", ln=0, border=1)
    pdf.cell(w=30, h=7, txt="Price per Unit", ln=0, border=1)
    pdf.cell(w=30, h=7, txt="Total", ln=1, border=1) ## line break for next row

    ## 11. Add content of the xlsx file into the table under the relevant table header
    for index, row in df.iterrows():
        pdf.set_font(family="Times", style="", size=8)
        pdf.set_text_color(80,80,80)
        pdf.cell(w=30, h=7, txt=f"{row["product_id"]}", ln=0, border=1)  ## no line break from first till last cell in row
        pdf.cell(w=70, h=7, txt=f"{row["product_name"]}", ln=0, border=1)
        pdf.cell(w=30, h=7, txt=f"{row["amount_purchased"]}", ln=0, border=1)
        pdf.cell(w=30, h=7, txt=f"{row["price_per_unit"]}", ln=0, border=1)
        pdf.cell(w=30, h=7, txt=f"{row["total_price"]}", ln=1, border=1) ## line break for next row
        total_amount = total_amount + row["total_price"]  ## Add the total of each product to a variable for reusability

    ## 13. Add the last row with total amount
    pdf.set_font(family="Times", style="", size=8)
    pdf.cell(w=30, h=7, txt="", ln=0, border=1)
    pdf.cell(w=70, h=7, txt="", ln=0, border=1)
    pdf.cell(w=30, h=7, txt="", ln=0, border=1)
    pdf.cell(w=30, h=7, txt="", ln=0, border=1)
    pdf.cell(w=30, h=7, txt=f"{total_amount}", ln=1, border=1)

    ## 14. Add line breaks for the text
    pdf.ln(15)
    pdf.set_font(family="Times", style="B", size=10)
    pdf.cell(w=0, h=7, txt=f"The total due amount is {total_amount} Euros", ln=1, border=0)
    pdf.cell(w=0, h=7, txt=f"LVLUP", ln=1, border=0)

    ## 15. Output each file in the files folder.
    pdf.output(f"Files/{filename}.pdf")
