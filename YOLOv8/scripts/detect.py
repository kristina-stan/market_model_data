from pdf2image import convert_from_path
pages = convert_from_path('example.pdf', dpi=200)
for page in pages:
    page.save('out.png', 'PNG')
