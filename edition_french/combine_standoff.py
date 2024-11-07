from bs4 import BeautifulSoup

def next_s(s_id):
    s_number = int(s_id[1:])
    return f"s{s_number + 1:04d}"

with open('chapters_standoff.xml') as f:
    standoff = BeautifulSoup(f, 'xml')

with open('ChirAlbT_text_bfm_mod.xml') as f:
    text = BeautifulSoup(f, 'xml')

new_soup = BeautifulSoup('<body></body>', 'xml')
body = new_soup.body
# add new <div type="preface"> element to body
preface = new_soup.new_tag('div')
preface['type'] = 'preface'
body.append(preface)
preface.append(new_soup.new_tag('p'))

# find element with id 'prologue' in standoff
prologue = standoff.find('chapter', id='prologue')
curr_s = prologue['start_s']
end_s = prologue['end_s']

while curr_s != end_s:
    preface.p.append(text.find('s', id=curr_s))
#    print(curr_s)
    curr_s = next_s(curr_s)

#print(curr_s)
preface.p.append(text.find('s', id=curr_s))

for chapter in standoff.find_all('chapter'):
    if chapter['id'] == 'prologue':
        continue
    new_chapter = new_soup.new_tag('div')
    new_chapter['type'] = 'chapter'
    new_chapter['n'] = chapter['n']
    new_chapter.append(new_soup.new_tag('p'))

    curr_s = chapter['start_s']
    end_s = chapter['end_s']

    while curr_s != end_s:
        new_chapter.p.append(text.find('s', id=curr_s))
#        print(curr_s)
        curr_s = next_s(curr_s)
#    print(curr_s)
    new_chapter.p.append(text.find('s', id=curr_s))

    for subchapter in chapter.find_all('subchapter'):
        new_subchapter = new_soup.new_tag('div')
        new_subchapter['type'] = 'subchapter'
        new_subchapter['n'] = subchapter['n']
        new_subchapter.append(new_soup.new_tag('p'))

        curr_s = subchapter['start_s']
        end_s = subchapter['end_s']

        while curr_s != end_s:
            new_subchapter.p.append(text.find('s', id=curr_s))
#            print(curr_s)
            curr_s = next_s(curr_s)

#        print(curr_s)
        new_subchapter.p.append(text.find('s', id=curr_s))

        new_chapter.append(new_subchapter)

    body.append(new_chapter)

with open('chapters_combined.xml', 'w') as f:
    f.write(str(new_soup))
