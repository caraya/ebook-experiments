#!/usr/bin/env python
import mimetypes
import glob
import os

mimetypes.init()
package = open('package.opf', 'w')

# The filenames of the HTML are listed in html_files
# This is really clunky and will require edits later but it's 
# the best I can do right now. 
package_content = glob.glob('OEBPS/*')
package_content += glob.glob('OEBPS/*/*')
package_content += glob.glob('OEBPS/*/*/*')



template_top = '''<package xmlns="http://www.idpf.org/2007/opf"
  unique-identifier="book-id"
  version="3.0" xml:lang="en">
  <metadata >
    <!-- TITLE -->
    <dc:title></dc:title>
    <!-- AUTHOR, PUBLISHER AND PUBLICATION DATES-->
    <dc:creator></dc:creator>
    <dc:publisher></dc:publisher>
     <dc:date></dc:date>
     <meta property="dcterms:modified"></meta>
     <!-- MISC INFORMATION -->
      <dc:language>en</dc:language>
      <dc:identifier id="book-id"></dc:identifier>
      <meta name="cover" content="img-cov" />
  <manifest>
  '''
template_transition = '''</manifest>
  <spine toc="ncx">'''

template_bottom = '''</spine>
</package>'''

manifest = ""
spine = ""

# Write each HTML file to the ebook, collect information for the index
for i, item in enumerate(package_content):
    basename = os.path.basename(item)
    mime = mimetypes.guess_type(item, strict=True)
    manifest += '\t<item id="file_%s" href="%s" media-type="%s"/>\n' % (i+1, basename, mime)
    spine += '\t<itemref idref="file_%s" />\n' % (i+1)

# I don't remember my python all that well to remember how to print the interpolated
# content. This should do for now.
package.write(template_top)
package.write(manifest)
package.write(template_transition)
package.write(spine)
package.write(template_bottom)
