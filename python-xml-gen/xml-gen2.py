from lxml import etree

try:
  from lxml import etree
  print("running with lxml.etree")
except ImportError:
  try:
    # Python 2.5
    import xml.etree.cElementTree as etree
    print("running with cElementTree on Python 2.5+")
  except ImportError:
    try:
      # Python 2.5
      import xml.etree.ElementTree as etree
      print("running with ElementTree on Python 2.5+")
    except ImportError:
      try:
        # normal cElementTree install
        import cElementTree as etree
        print("running with cElementTree")
      except ImportError:
        try:
          # normal ElementTree install
          import elementtree.ElementTree as etree
          print("running with ElementTree")
        except ImportError:
          print("Failed to import ElementTree from any known place")


# The root element of our opf file is package
package = etree.Element("package")
# Set attributes for the packge root
package.set('xmlns', 'http://www.idpf.org/2007/opf')
package.set('unique-identifier','book-id')
package.set('version', '3.0')
# YES!
package.set('{http://www.w3.org/XML/1998/namespace}lang', 'en-us')

metadata = etree.SubElement(package, "metadata")
# if we don't set the DC namespace in package we'll have to set it for
# every element in the DC namespace... this may be good enough for now
metadata.append('{http://purl.org/dc/elements/1.1/}author')

manifest = etree.SubElement(package, "manifest")

spine = etree.SubElement(package, "spine")

guide = etree.SubElement(package, "guide")

print(etree.tostring(package, pretty_print=True))