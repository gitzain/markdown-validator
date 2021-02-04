import markdown, sys, xmlschema

def validate(filename_xsd, filename_md):
    # Open and read both files
    with open(filename_md, "r", encoding="utf-8") as input_file:
        markdown_text = input_file.read()

    with open(filename_xsd, 'r') as schema_file:
        schema_to_check = schema_file.read()

    # Convert markdown to xhtml
    xhtml = markdown.markdown(markdown_text)
    xhtml = "<root>\n" + xhtml + "\n</root>"

    # Write out html. Useful for debugging
    with open("output.html", "w", encoding="utf-8", errors="xmlcharrefreplace") as output_file:
        output_file.write(xhtml)

    # Validate against schema
    xmlschema.validate('output.html', filename_xsd)
    print('Schema validation ok.')


if __name__ == "__main__":
    # File names as command line arguments
    filename_xsd = sys.argv[1]
    filename_md = sys.argv[2]
    validate(filename_xsd, filename_md)