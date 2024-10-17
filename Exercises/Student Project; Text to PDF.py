from fpdf import FPDF
import glob

filepaths = glob.glob("Files/*.txt")

pdf = FPDF(orientation="p", unit="mm", format="a4")
pdf.set_auto_page_break(False)



for path in filepaths:
    pdf.add_page()

    pdf.set_font(family="Helvetica", style="B", size=20)
    pdf.cell(w=0, h=15, txt=path.split("\\")[1].split(".")[0].title(), ln=1)

    with open(path) as  file:
        content = file.read()

    pdf.set_font(family="Courier", size=12)
    pdf.multi_cell(w=0, h=6, txt=content)

pdf.output("Files/output.pdf")