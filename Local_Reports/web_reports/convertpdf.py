from weasyprint import HTML

# Path to your external HTML file
html_file_path = 'D:/WORK/FLOODNET/Local_Reports/web_reports/report.html'

# Path to your external CSS file
css_file_path = 'D:/WORK/FLOODNET/Local_Reports/web_reports/styles.css'

# Path to save the output PDF file
pdf_path = 'D:/WORK/FLOODNET/Local_Reports/web_reports/output.pdf'

# Create a WeasyPrint HTML object with external CSS
html = HTML( 
    filename=html_file_path, 
    # base_url='base_url'
    )

# Convert HTML to PDF
html.write_pdf(pdf_path)