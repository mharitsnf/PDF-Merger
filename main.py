import sys
import os
from PyPDF2 import PdfFileReader, PdfFileWriter
from PIL import Image
import img2pdf

dirpath = os.getcwd()


def clean(pdfs):
    for pdf in pdfs:
        os.remove(pdf+'.pdf')


def convertimg(image):
    openimg = Image.open(image)
    pdf_bytes = img2pdf.convert(openimg.filename)

    with open(image+'.pdf', 'wb') as out:
        out.write(pdf_bytes)
    openimg.close()

    return image+'.pdf'


def merge(pdfs, is_image, output):
    pdf_writer = PdfFileWriter()

    for pdf in pdfs:
        path = pdf

        if is_image:
            path = convertimg(pdf)

        pdf_reader = PdfFileReader(path)
        for page_no in range(pdf_reader.getNumPages()):
            pdf_writer.addPage(pdf_reader.getPage(page_no))

    with open(output, 'wb') as out:
        pdf_writer.write(out)

    if is_image:
        clean(pdfs)

    print("Successful")


def error_exit():
    print('Arguments unknown')
    print('Use --pdf to list the pdf files')
    print(' example: --pdf=1.pdf,2.pdf,3.pdf')
    print('Use --is-image=yes if your files are image (jpg, jpeg, png)')
    print('Use --output for your desired filename')
    print(' example: --output=result.pdf')
    exit()


if __name__ == '__main__':
    command = sys.argv[1]
    arguments = sys.argv[2:]

    if len(arguments) == 0:
        error_exit()

    is_image = False
    pdfs = []
    output = ''

    for arg in arguments:
        if '--pdf=' in arg:
            file_arg = arg.split('=')[1]
            pdfs = file_arg.split(',')
            pdfs = [dirpath + '/' + x for x in pdfs]

        elif '--is-image=' in arg:
            status = arg.split('=')[1]
            if status == 'yes':
                is_image = True
            else:
                is_image = False

        elif '--output=' in arg:
            output = dirpath + '/' + arg.split('=')[1]

        else:
            error_exit()

    if command == 'merge':
        merge(pdfs, is_image, output)
