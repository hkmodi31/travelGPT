import bz2
import lxml.etree as etree
import os
from urllib.parse import quote

def extract_article_texts(dump_file, output_folder):
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    with bz2.BZ2File(dump_file, 'r') as file:
        context = etree.iterparse(file, events=('start', 'end'))
        _, root = next(context)  # Get the root element

        for event, elem in context:
            if event == 'end' and elem.tag == '{http://www.mediawiki.org/xml/export-0.10/}page':
                title = elem.findtext('{http://www.mediawiki.org/xml/export-0.10/}title')
                text = elem.findtext('{http://www.mediawiki.org/xml/export-0.10/}revision/{http://www.mediawiki.org/xml/export-0.10/}text')
                if text:
                    # Create a file for the article
                    file_name = quote(title.replace('/', '_')) + '.txt'
                    file_path = os.path.join(output_folder, file_name)
                    with open(file_path, 'w', encoding='utf-8') as out_file:
                        out_file.write(text)

                root.clear()  # Free up memory

if __name__ == '__main__':
    dump_file = 'enwikivoyage-latest-pages-articles-multistream.xml.bz2'
    output_folder = 'articles'
    extract_article_texts(dump_file, output_folder)