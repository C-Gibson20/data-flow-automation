import PyPDF2
from pdfminer.high_level import extract_pages
from pdfminer.layout import LTTextContainer, LTChar
import pdfplumber


def text_extraction(element):

    line_text = element.get_text()
    line_formats = []

    for text_line in element:
        if isinstance(text_line, LTTextContainer):
            for character in text_line:
                if isinstance(character, LTChar):
                    line_formats.append(character.fontname)
    format_per_line = list(set(line_formats))
    
    return (line_text, format_per_line)


def candidate_filtering(txt_lst):

    filtered = []
    
    for i in range(len(txt_lst)):
        if len(txt_lst[i]) > 0 and txt_lst[i][0] != '-':
            if (txt_lst[i][-9:] != 'addendum '):
                if (txt_lst[i][-3:] == 'um '):
                    filtered.append(txt_lst[i+1])
                    #print(txt_lst[i+1])
                elif (txt_lst[i][-5:] == 'um # '):
                    filtered.append(txt_lst[i+1])

    filtered = [item for item in filtered if (len(item) != 0) and (' ' not in item[:-5])]
    #filtered = [item for item in filtered if (len(item) != 0)]
    return filtered


pdf_path = 'pl131.pdf'
pdf_file_obj = open(pdf_path, 'rb')

# Create a pdf reader object
pdf_reader = PyPDF2.PdfReader(pdf_file_obj)

text_per_page = {}
page_text = []


for pagenum, page in enumerate(extract_pages(pdf_path)):

    page_obj = pdf_reader.pages[pagenum]
    line_format = []
    page_content = []

    pdf = pdfplumber.open(pdf_path)

    # Find the examined page
    page_tables = pdf.pages[pagenum]

    # Find all the elements
    page_elements = [(element.y1, element) for element in page._objs]
    # Sort all the element as they appear in the page 
    page_elements.sort(key=lambda a: a[0], reverse=True)

    

    for i,component in enumerate(page_elements):
        
        element = component[1]

        if isinstance(element, LTTextContainer):

            (line_text, format_per_line) = text_extraction(element)
            page_content.append([line_text])
    
            
            text_split = line_text.split('\n')

            for frmt in format_per_line:
                if 'Bold' in str(frmt):
                    
                    page_text += candidate_filtering(text_split)
    
    #if pagenum == 2:
        #print(page_content)


pdf_file_obj.close()

for i in page_text:
    print(i)
