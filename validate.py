import markdown, sys
from lxml import etree
from io import StringIO

# File names as command line arguments
filename_xsd = sys.argv[1]
filename_md = sys.argv[2]


# Open and read both files
with open(filename_md, "r", encoding="utf-8") as input_file:
    markdown_text = input_file.read()

with open(filename_xsd, 'r') as schema_file:
    schema_to_check = schema_file.read()


# Convert markdown to xhtml
xhtml = markdown.markdown(markdown_text)
xhtml = "<root>\n" + xhtml + "\n</root>"


""" # Write out html. Useful for debugging
with open("output.html", "w", encoding="utf-8", errors="xmlcharrefreplace") as output_file:
    output_file.write(xhtml) """


# Make sure we have valid xhtml
try:
    doc = etree.parse(StringIO(xhtml))
    print('XML well formed, syntax ok.')

except IOError:
    print('Invalid File')

except etree.XMLSyntaxError as err:
    print('XML Syntax Error, see error_syntax.log')
    with open('error_syntax.log', 'w') as error_log_file:
        error_log_file.write(str(err.error_log))
    quit()

except:
    print('Unknown error, exiting.')
    quit()


# Validate against schema
try:
    xmlschema_doc = etree.parse(StringIO(schema_to_check))
    xmlschema = etree.XMLSchema(xmlschema_doc)
    xmlschema.assertValid(doc)
    print('XML valid, schema validation ok.')

except etree.DocumentInvalid as err:
    print('Schema validation error, see error_schema.log')
    with open('error_schema.log', 'w') as error_log_file:
        error_log_file.write(str(err.error_log))
    quit()

except:
    print('Unknown error, exiting.')
    quit()