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

    ## 4. Initiate a PDF with portrait A4 with mm units and no auto page breaks inside the loop so a different pdf is created for each xlsx file
    pdf = FPDF(orientation="P", unit="mm", format="A4")
    pdf.set_auto_page_break(False)

    ## 12. No need for this
    # total_amount = 0

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

    ## 10. Add table headers using list comprehension and pandas columns method
    columns = df.columns  ## New
    columns = [item.replace("_", " ").title() for item in columns]
    pdf.set_font(family="Helvetica", style="B", size=10)
    pdf.cell(w=30, h=7, txt=columns[0], ln=0, border=1)  ## no line break from first till last cell in row
    pdf.cell(w=70, h=7, txt=columns[1], ln=0, border=1)
    pdf.cell(w=30, h=7, txt=columns[2].split(" ")[0], ln=0, border=1)  ## Reduced "Amount Purchased" to "Amount" since it was taking too much space.
    pdf.cell(w=30, h=7, txt=columns[3], ln=0, border=1)
    pdf.cell(w=30, h=7, txt=columns[4], ln=1, border=1) ## line break for next row

    ## 11. Add content of the xlsx file into the table under the relevant table header
    for index, row in df.iterrows():
        pdf.set_font(family="Times", style="", size=8)
        pdf.set_text_color(80,80,80)
        pdf.cell(w=30, h=7, txt=f"{row["product_id"]}", ln=0, border=1)  ## no line break from first till last cell in row
        pdf.cell(w=70, h=7, txt=f"{row["product_name"]}", ln=0, border=1)
        pdf.cell(w=30, h=7, txt=f"{row["amount_purchased"]}", ln=0, border=1)
        pdf.cell(w=30, h=7, txt=f"{row["price_per_unit"]}", ln=0, border=1)
        pdf.cell(w=30, h=7, txt=f"{row["total_price"]}", ln=1, border=1) ## line break for next row

    ## 13. Add the last row with total amount
    pdf.set_font(family="Times", style="", size=8)
    pdf.cell(w=30, h=7, txt="", ln=0, border=1)
    pdf.cell(w=70, h=7, txt="", ln=0, border=1)
    pdf.cell(w=30, h=7, txt="", ln=0, border=1)
    pdf.cell(w=30, h=7, txt="", ln=0, border=1)
    pdf.cell(w=30, h=7, txt=str(df["total_price"].sum()), ln=1, border=1)  ## Add the total of each product using pandas

    ## 14. Add line breaks for the text
    pdf.ln(15)
    pdf.set_font(family="Times", style="B", size=10)
    pdf.cell(w=0, h=7, txt=f"The total due amount is {df["total_price"].sum()} Euros", ln=1, border=0)
    pdf.cell(w=15, h=7, txt=f"LVLUP")
    pdf.image("Files/python_logo.jpg", w=7)  ## Added an image to the logo.
    ## The image above was not loading before because the extension was jpeg, but FPDF only reads JPG, PNG or GIF, so I renamed it.

    ## 15. Output each file in the files folder.
    pdf.output(f"Files/{filename}.pdf")
