import os
import re
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfdocument import PDFDocument
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.pdfpage import PDFPage
from pdfminer.pdfparser import PDFParser
from io import StringIO

pdf_dir = "pdf_files"  # No need for 'r' prefix, and remove the trailing slash

pdf_files = [f for f in os.listdir(pdf_dir) if f.endswith(".pdf")]

selected_pages = [8, 20]
paragraph_patterns = [re.compile(r'\n(.*?)\n', re.DOTALL)]

output_string = StringIO()

for pdf_file in pdf_files:
  pdf_path = os.path.join(pdf_dir, pdf_file)  # Build the full path to the PDF
  with open(pdf_path, 'rb') as pdf_file:
    parser = PDFParser(pdf_file)
    pdf_reader = PDFPage.get_pages(pdf_file, set())
    resource_manager = PDFResourceManager()
    doc = PDFDocument(parser)
    codec = 'utf-8'
    laparams = LAParams()
    device = TextConverter(resource_manager, output_string, laparams=LAParams())
    interpreter = PDFPageInterpreter(resource_manager, device)

    current_page = 8
    for page in PDFPage.create_pages(doc):
      current_page += 1
      if current_page not in selected_pages:
        continue

      interpreter.process_page(page)

      page_text = output_string.getvalue()
      for pattern in paragraph_patterns:
        if pattern.search(page_text):
          print(page_text)
          break  # Once a pattern is found, stop searching for more matches
      output_string.truncate(0)
      output_string.seek(0)

# print(output_string.getvalue())
# if re.search(r"to be held (at|on)", output_string.lower()):
#       print(output_string)
#       output_string += output_string + "\n"

# You can use 'extracted_text' for further processing or save it to a file
