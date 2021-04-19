import PyPDF2

def get_tree_pages(root, info, depth=0):
    """
        Recursively iterate the outline tree
        Find the pages pointed by the outline item
        and get the assigned physical order id

        Decrement with padding if necessary
    """
    if isinstance(root, dict):
        # print(root)
        page = root['/Page'].getObject()
        # print(id(page))
        t = root['/Title']
        title = t
        if isinstance(t, PyPDF2.generic.ByteStringObject):
            title = t.original_bytes.decode('utf8')
        title = title.strip()
        title = title.replace('\n', '')
        title = title.replace('\r', '')

        page_num = info['all_pages'].get(id(page), 0)
        if page_num == 0:
            print('Not found page number for /Page!', page)
        elif page_num < info['padding']:
            page_num = 0
        else:
            page_num -= info['padding']


        str_val = '%-5d' % page_num
        str_val += '\t' * depth
        str_val += title + '\t' + '%3d' % page_num
        print(str_val)
        return 
    for elem in root:
        get_tree_pages(elem, info, depth+1)

def recursive_numbering(obj, info):
    """
        Recursively iterate through all the pages in order and assign them a physical
        order number
    """
    # print(id(obj), obj)
    if obj['/Type'] == '/Page':
        obj_id = id(obj)
        if obj_id not in info['all_pages']:
            info['all_pages'][obj_id] = info['current_page_id']
        info['current_page_id'] += 1
        return
    elif obj['/Type'] == '/Pages':
        for page in obj['/Kids']:
            recursive_numbering(page.getObject(), info)
        
    
def create_text_outline(pdf_path, page_number_padding):
    # print('Running the script for [%s] with padding [%d]' % (pdf_path, page_number_padding))
    # creating an object 
    with open(pdf_path, 'rb') as file:
        fileReader = PyPDF2.PdfFileReader(file)

        info = {
            'all_pages': {},
            'current_page_id': 1, 
            'padding': page_number_padding
        }

        pages = fileReader.trailer['/Root']['/Pages'].getObject()
        recursive_numbering(pages, info)
        #for page_num, page in enumerate(pages['/Kids']):
        #    page_obj = page.getObject()
        #    all_pages[id(page_obj)] = page_num + 1 # who starts counting from 0 anyways?
        get_tree_pages(fileReader.getOutlines(), info)

if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser(description="""
        Create a text version of a pdf\'s outlines with page numbers.
        The pdf has to have some kind of outline for the script to work
    """)
    parser.add_argument('pdf_path', type=str,
                        help='Path to the input pdf')
    parser.add_argument('--padding', type=int, default=0, help="""In case the pdf page numbering doesn\'t start from the first physical page. 
        It tells how many physical pages are there until you see the 1 numbering somewhere
    """)
    args = parser.parse_args()
    create_text_outline(args.pdf_path, args.padding)