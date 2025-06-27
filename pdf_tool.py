import tkinter as tk
from tkinter import filedialog, messagebox, simpledialog
from PyPDF2 import PdfReader, PdfWriter
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib.colors import Color

root = tk.Tk()
root.title("PDF Automation Tool")
root.geometry("400x300")
tk.Label(root, text="PDF Automation Tool", font=("Arial", 16)).pack(pady=10)


# -------------------------------
# MERGE PDFs
# -------------------------------
def merge_pdfs():
    files = filedialog.askopenfilenames(title="Select PDFs to Merge", filetypes=[("PDF files", "*.pdf")])
    if not files:
        return
    output_path = filedialog.asksaveasfilename(defaultextension=".pdf", filetypes=[("PDF files", "*.pdf")])
    if not output_path:
        return
    
    from PyPDF2 import PdfMerger
    merger = PdfMerger()
    for f in files:
        merger.append(f)
    merger.write(output_path)
    merger.close()
    messagebox.showinfo("Success", f"Merged PDF saved to:\n{output_path}")


# -------------------------------
# SPLIT PDF
# -------------------------------
def split_pdf():
    file = filedialog.askopenfilename(title="Select PDF to Split", filetypes=[("PDF files", "*.pdf")])
    if not file:
        return
    reader = PdfReader(file)
    for i, page in enumerate(reader.pages):
        writer = PdfWriter()
        writer.add_page(page)
        output_filename = f"{file[:-4]}_page_{i+1}.pdf"
        with open(output_filename, "wb") as f_out:
            writer.write(f_out)
    messagebox.showinfo("Success", "PDF split into individual pages!")


# -------------------------------
# CREATE TRANSPARENT WATERMARK
# -------------------------------
def create_watermark_pdf(text, output_path):
    c = canvas.Canvas(output_path, pagesize=letter)
    transparent_black = Color(0, 0, 0, alpha=0.2)
    c.setFont("Helvetica-Bold", 60)
    c.setFillColor(transparent_black)
    c.saveState()
    c.translate(300, 400)
    c.rotate(45)
    c.drawCentredString(0, 0, text)
    c.restoreState()
    c.save()


# -------------------------------
# ADD WATERMARK
# -------------------------------
def add_watermark():
    # Ask for input PDF
    pdf_file = filedialog.askopenfilename(title="Select PDF to Add Watermark", filetypes=[("PDF files", "*.pdf")])
    if not pdf_file:
        return

    # Ask for watermark text
    watermark_text = simpledialog.askstring("Watermark Text", "Enter watermark text:")
    if not watermark_text:
        return

    # Create temporary watermark PDF
    watermark_pdf = "temp_watermark.pdf"
    create_watermark_pdf(watermark_text, watermark_pdf)

    # Ask for output file
    output_path = filedialog.asksaveasfilename(defaultextension=".pdf", filetypes=[("PDF files", "*.pdf")])
    if not output_path:
        return

    # Merge watermark
    reader = PdfReader(pdf_file)
    watermark = PdfReader(watermark_pdf).pages[0]
    writer = PdfWriter()

    for page in reader.pages:
        page.merge_page(watermark)  # transparency makes watermark look in background
        writer.add_page(page)

    with open(output_path, "wb") as f_out:
        writer.write(f_out)

    messagebox.showinfo("Success", f"Watermarked PDF saved to:\n{output_path}")


# -------------------------------
# BUTTONS
# -------------------------------
merge_btn = tk.Button(root, text="Merge PDFs", command=merge_pdfs, width=30)
merge_btn.pack(pady=5)

split_btn = tk.Button(root, text="Split PDF into Pages", command=split_pdf, width=30)
split_btn.pack(pady=5)

watermark_btn = tk.Button(root, text="Add Transparent Watermark", command=add_watermark, width=30)
watermark_btn.pack(pady=5)

root.mainloop()
