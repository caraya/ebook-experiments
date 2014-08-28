#!/bin/sh

rm -rf mybook.epub
echo "book file deleted"

find . -type f -name '*.DS_Store' -ls -delete
echo "deleted mac specific files"

zip -r -X mybook.epub mimetype META-INF OEBPS

java -jar /usr/local/java/epubcheck/epubcheck-3.0/epubcheck-3.0.jar mybook.epub
echo "All Done"

#open mybook.epub