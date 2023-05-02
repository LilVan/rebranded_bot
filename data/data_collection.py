from bs4 import BeautifulSoup
import re
import csv
import cp1252


with open("yale.html", "r",  encoding='utf-8') as f:
    html_doc = f.read()
s = BeautifulSoup(html_doc, "html.parser")


def doubledecode(text, as_unicode=True):
    text = text.decode('utf-8')
    # remove the windows gremlins O^1
    for src, dest in cp1252.cp1252.items():
        text = text.replace(src, dest)
    text = text.encode('raw_unicode_escape')
    if as_unicode:
        # return as unicode string
        text = text.decode('utf-8', 'ignore')
    return text


with open('brands.csv', mode='w', encoding="utf-8") as brands:
    brand_info = csv.writer(brands, delimiter=';', quotechar='"', quoting=csv.QUOTE_MINIMAL, lineterminator='\n')
    brand_info.writerow(['Name', 'Action', 'Industry', 'Company', "Текущее имя"])

    pars = s.find_all('tr', class_="table__row")
    for par in pars:
        block = 0
        row = []
        for attr in re.finditer(re.compile("<td class=\"table__cell\">(.* ?)</td>"), str(par)):
            block += 1
            row += [attr.group(1).replace(';', ',')]
            if block % 4 == 0:
                brand_info.writerow(row+['None'])
                row = []
