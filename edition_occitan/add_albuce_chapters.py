from bs4 import BeautifulSoup

with open('AlbucE_converted.xml') as f:
    soup = BeautifulSoup(f, 'xml')


def insert_new_div(new_div, start_p, end_p):
    start_p.insert_before(new_div)
    new_div.append(start_p.extract())
    if start_p == end_p:
        return
    for p in new_div.find_next_siblings():
        new_div.append(p.extract())
        if p == end_p:
            break


new_div = soup.new_tag('div', type='preface')
start_p = soup.find('p', id='p001')
end_p = soup.find('p', id='p016')
insert_new_div(new_div, start_p, end_p)

chapters = [
    ['p017', 'p173', '1'],
    ['p174', 'p743', '2'],
    ['p744', 'p887', '3'],
]

for start_id, end_id, chapter_number in chapters:
    new_div = soup.new_tag('div', type='chapter', n=chapter_number)
    start_p = soup.find('p', id=start_id)
    end_p = soup.find('p', id=end_id)
    insert_new_div(new_div, start_p, end_p)

# within each div of type "chapter", iterate over all <p> elements
# find the ids of all <p> elements the text of which starts with "Capitol"

for chapter in soup.find_all('div', type='chapter'):
    first_ps = []
    for p in chapter.find_all('p'):
        if (p.get_text().strip().startswith('Capitol')
            or (p.get_text().strip().startswith('De ')
                and not p.get_text().strip().startswith('De cauteri am foc')
                and not p.get_text().strip().startswith('De aquels so las')
                and not p.get_text().strip().startswith('De eyssiment del embrio')
                and not p.get_text().strip().startswith('De curacio de fistulas')
                and not p.get_text().strip().startswith('De las plaguas del col')
                )):
            first_ps.append(int(p['id'].removeprefix('p')))

    subch_num = 1
    # find the last <p> element in the chapter
    last_p = chapter.find_all('p')[-1]

    for p, next_p in list(zip(first_ps, first_ps[1:])):
        # note: the last item in first_ps is not included in the iteration
        # because the shifted list is one item shorter
        start_p = chapter.find('p', id=f'p{p:03}')
        end_p = chapter.find('p', id=f'p{next_p - 1:03}')
        new_div = soup.new_tag('div', type='subchapter', n=str(subch_num))
        subch_num += 1
        insert_new_div(new_div, start_p, end_p)

    # enclose the <p> element from the last item in first_ps up to last_p
    # in a new <div> element of type "subchapter"
    new_div = soup.new_tag('div', type='subchapter', n=str(subch_num))
    start_p = chapter.find('p', id=f'p{first_ps[-1]:03}')
    insert_new_div(new_div, start_p, last_p)


# save the modified XML to a new file
with open('AlbucE_chapters.xml', 'w') as f:
    f.write(soup.prettify())
