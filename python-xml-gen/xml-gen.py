#!/usr/bin/env python 
import mimetypes
import glob
import os
import os.path

# Initialize the mimetypes database
mimetypes.init()
# Create the package.opf file
package = open('package.opf', 'w')

# The glob below should encompass everything under 
# OEBPS. Right now I'm trying to remove empty directories
# and the package_content variable. 
# WARNING: This glob will add all files and directories 
# to the variable. You will have to edit the file and remove
# empty directories and the package.opf file reference from
# both the manifest and the spine
package_content = glob.glob('OEBPS/**/*')

# FIRST PASS AT WRITING FUNCTION TO ADDRESS ISSUE ABOVE
#for file in os.listdir( location ):
#  if os.path.isfile(os.path.join('OEBPS', file)):
#    package_content = ''
#    package_contet += file
  

# Rather than use a templating system we build the XML portion
# by hand
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
  </metadata>
  <manifest>
  '''
template_transition = '''</manifest>
  <spine toc="ncx">'''

template_bottom = '''</spine>
</package>'''

manifest = ""
spine = ""

# Write the content of OEBPS into the manifest and spines
for i, item in enumerate(package_content):
    basename = os.path.basename(item)
    mime = mimetypes.guess_type(item, strict=True)
    manifest += '\t<item id="file_%s" href="%s" media-type="%s"/>\n' % (i+1, basename, mime[0])
    spine += '\n\t<itemref idref="file_%s" />' % (i+1)

# I don't remember my python all that well to remember 
# how to print the interpolated content. 
# This should do for now.
package.write(template_top)
package.write(manifest)
package.write(template_transition)
package.write(spine)
package.write(template_bottom)
