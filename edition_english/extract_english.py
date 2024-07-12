'''
This extracts the English translation of Albucasis
from the Spink and Lewis edition.
The main issue is separating the main text from
various sorts of footnotes. This is done by extracting
the first block of text from each page, remembering the
left and right coordinates of the block, and then
breaking when the next block is not exactly below the
previous block, i.e. if either the left or the right
edge of the block differ from the previous (and by
transitivity from the first) block.
This is not perfect, but it works for most pages.
There are some exceptions that contain title lines
or where a paragraph is split into blocks line by line,
and thus at least the first and last blocks are not
directly in line with the others.
In these cases, the dict BLOCK_EXCEPTIONS is used to
specify manually the number of blocks to extract from
the page (starting from block 0).
'''

import fitz  # PyMuPDF
import re
import yaml


# Open the pdf file
file_path = '/storage/sata2tbssd/albuc_translate/spink_lewis.pdf'
doc = fitz.open(file_path)

# Save the extracted text to a file
output_file = '/storage/sata2tbssd/albuc_translate/spink_lewis.txt'
out_handle = open(output_file, 'w')

BLOCK_EXCEPTIONS = {
    23: 3,
    39: 0,
    43: 7,
    65: 0,
    165: 7,
    181: 2,
    207: 1,
    211: 15,
    213: 10,
    267: 1,
    289: 1,
    349: 0,
    361: 5,
    363: 14,
    365: 2,
    367: 2,
    369: 6,
    371: 8,
    477: 2,
    509: 1,
    545: 2,
    547: 2,
    567: 2,
    579: 1,
    605: 2,
    639: 4,
    649: 16,
    653: 1,
    657: 0,
    683: 1,
    691: 2,}

# Page 309 can't be fixed with this method
# because the footnote is in the same block as the text.
# This needs to be removed manually.

# Pages where the text is split by line
# These are the printed page numbers, not the pdf page numbers
SPLIT_BY_LINE = [
    28, 150, 196, 198, 348, 354, 356, 634
]

# Extract text from even pages in the range of 18 to 852
extracted_pages = []
for page_num in range(17, 852, 2):
    page = doc[page_num]
    # Extract the first block of text from each page
    page_text = page.get_text('blocks', flags=fitz.TEXT_INHIBIT_SPACES|fitz.TEXT_DEHYPHENATE)
    extracted_text = ''
    prev_block_left = 0
    prev_block_right = 0
    for block_nr, text_block in enumerate(page_text):
        text_block_text = text_block[4]
        if prev_block_left == 0:
            prev_block_left = text_block[0]
            prev_block_right = text_block[2]
        if page_num in BLOCK_EXCEPTIONS:
            if block_nr > BLOCK_EXCEPTIONS[page_num]:
                break
        elif (not page_text[block_nr - 1][4].lower().startswith('chapter')
              and (abs(text_block[0] - prev_block_left) > 2
              or abs(text_block[2] - prev_block_right) > 2)):
            # print("Next", text_block[4], file=out_handle)
            break
        elif text_block_text.startswith('1 '):
            break
        elif text_block_text.strip().isnumeric():
            break
        # elif :
        #     break
        text_block_text = text_block_text.replace('\n', ' ')
        text_block_text = re.sub(r'\s+', ' ', text_block_text)
        if block_nr > 0:
            extracted_text += '\n'
        extracted_text += text_block_text
        prev_block_left = text_block[0]
        prev_block_right = text_block[2]
    # save the extracted text to a list with the printed page number
    extracted_pages.append([page_num - 15, extracted_text])

    # print(page_num, extracted_text, file=out_handle)
    # for block in page_text:
    #     print(block, file=out_handle)
    # print(file=out_handle)

yaml.dump(extracted_pages, out_handle)
out_handle.close()

for id, (page_num, extracted_text) in enumerate(extracted_pages):
    if page_num not in SPLIT_BY_LINE:
        continue
    new_text = ''
    for line in extracted_text.split('\n'):
        if line.strip().endswith('-'):
            new_text += line.rstrip()[:-1]
        else:
            new_text += line
    extracted_pages[id][1] = new_text

combined_text = ''
for (_, first_page), (_, next_page) in zip(extracted_pages, extracted_pages[1:]):
    if first_page.rstrip().endswith('-'):
        combined_text += first_page.rstrip()[:-1]
    elif next_page[0].islower():
        combined_text += first_page
    else:
        combined_text += first_page.rstrip() + '\n'
combined_text += extracted_pages[-1][1]

# Fix some OCR errors and reinsert deleted hyphens
# in the combined text only!
ocr_errors = {'^butter': 'butter',
              'jriay': 'may',
              'letterg\\': 'letter g;',
              'inflamed tumour\xBB': 'inflamed tumour,',
              'betweèn': 'between',
              'reached.and': 'reached and',
              'mlddje': 'middle',
              'sawingoff': 'sawing-off',
              'foursided': 'four-sided',
              'finerpointed': 'finer-pointed',
              'cuppingvessel': 'cupping-vessel',
              'mughathand sukk\\': 'mughath,1 and sukk;',
              'bccause': 'because',
              'thirtytwo': 'thirty-two',
              'crosslegged': 'cross-legged',
              'bayrammeaning': 'bayram,1 meaning',
              'twohanded': 'two-handed',
}
for error, correction in ocr_errors.items():
    combined_text = combined_text.replace(error, correction)

with open('/storage/sata2tbssd/albuc_translate/spink_lewis_combined.txt', 'w') as out_handle:
    print(combined_text, file=out_handle)

doc.close()
print('Text extracted successfully and saved to', output_file)
