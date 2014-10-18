# Python package.opf generator

This is the first pass at a script to generate a basic <code>package.opf</code> file for epub3 ebooks using Python 2.X.

## What it does

When you run it from the root of your ebook, the script will create a <code>package.opf</code> file, populate it with basic metadata as required by the epub3 specification, it will also create metadata and spine sections based on the content of the OEBPS duirectory.

## How it does it

The script only uses modules from the default lirbary. I want the script to be portable and I don't want to worry whether a module is compatible with 2.X and 3.X or just one of them

At the top of the script we use the environment 'shebang' to identify the location of the Python executable without hardcoding it. 

We import the following modules for a specific function:

* ***mimetypes*** to identify the mimetype of our files automatically
* ***glob*** to create the list of files under OEBPS
* ***os*** and ***os.path*** to create the items we populate our package file with

After loading the modules the first thing we do is initialize our mime-type database. This will ensure, as much as possible, that we match the file with the correct mime-type.

We then open our package.opf file in write mode. 

The last step in this stage is to create the glob expression that will tell the rest of the scripts what files to work with. 

We are now ready to create the content we'll write to the file. 

```python
#!/usr/bin/env python 

import mimetypes
import glob
import os
import os.path

# Initialize the mimetypes database
mimetypes.init()
# Create the package.opf file
package = open('package.opf', 'w')

# WARNING: This glob will add all files and directories 
# to the variable. You will have to edit the file and remove
# empty directories and the package.opf file reference from
# both the manifest and the spine
package_content = glob.glob('OEBPS/**/*')
```
The second stage is to create the templates for the XML portions of the package. There are two things to notice with this portion. 

* The XML elements are not filled in. Only attributes are filled as necessary
* I create static templates rather than using a generator module because all the modules I found had issues when working with namespaces. 

The three templates will be used when building the file.

```python
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
</package>

```
The enumeration builds the dynamic portion of the file. We first create two variables to hold the content and spine of the manifest.

For each element of our <code>package_content</code> (the content of the OEBPS directory) we do the following:

* Set the basename variable to the part of the current item
* Get the mime type for the item
* Add the item xml tag to the manifest assigning it an ID, the base path and the mime type
* Add the item to the spine by creating the idref element with an ID matching the one we used for the item tag above

When this is done we have a lit of all the files under OEBPS and are now ready to, finally, build the package file.

```python
manifest = ""
spine = ""

for i, item in enumerate(package_content):
  basename = os.path.basename(item)
  mime = mimetypes.guess_type(item, strict=True)
  manifest += '\t<item id="file_%s" href="%s" media-type="%s"/>\n' % (i+1, basename, mime[0])
  spine += '\n\t<itemref idref="file_%s" />' % (i+1)
```
After all the work, actually creating the file is almost anticlimatic. We print each section in the following order:

* template_top
* manifest
* template_transition
* spine
* template_bottom


```python
# I don't remember my python all that well to remember 
# how to print the interpolated content. 
# This should do for now.
package.write(template_top)
package.write(manifest)
package.write(template_transition)
package.write(spine)
package.write(template_bottom)
```
An example of the complete file looks like this:

```xml
<package xmlns="http://www.idpf.org/2007/opf"
  unique-identifier="book-id"¬
  version="3.0" 
  xml:lang="en">
  <metadata >¬
    <!-- TITLE -->¬
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
  </metadata
  <manifest>
    <item id="file_1" href="styles.css" media-type="text/css"/>
    <item id="file_2" href="type" media-type="None"/>
    <item id="file_3" href="book_cover.jpg" media-type="image/jpeg"/>
  </manifest>

  <spine toc="ncx">
    <itemref idref="file_1" />
    <itemref idref="file_2" />
    <itemref idref="file_3" />
  </spine>
</package>
```

### Gotchas

One thing I need to figure out is how to skip or remove empty folders. In the example above the media folder needs to be removed manually before the packagefile will pass epubcheck validation.

Another thing we'll have to research is whether the glob expression takes all the files we need. For geeks, how many levels deep does **/* go?

## Future Proofing


