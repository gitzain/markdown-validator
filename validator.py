import markdown, sys, xmlschema, logging, frontmatter, urllib, pathlib, argparse

def validate(filename_md, filename_xsd=None, raise_exception=False):
    """
    Provide a schema (XSD file) and a markdown file and
    this function will let you know if the markdown file conforms or not.
    Note: This function needs to convert the markdown to xhtml and then the xhtml is validated against the schema file.
    :param filename_xsd: the path to the schema
    :param filename_md: the markdown to be validated
    :param raise_exception: 'False' will ensure this function returns True if successful or False for any other reason. If this is set to 'True' the function will return True if it's successful else it will raise an exception detailing what went wrong.
    :return boolean: True or False depending if the file validates or not.
    """

    # Open the markdown file and grab the content without the frontmatter
    markdown_to_check = frontmatter.load(filename_md).content

    # Convert markdown to xhtml. It's the xhtml we'll validating.
    xhtml = "<root>\n" + markdown.markdown(markdown_to_check) + "\n</root>"

    # Get the schema. If there's a schema passed in then that will be used, else we'll try and find a schema in the frontmatter
    try:
        if not filename_xsd:
            filename_xsd = frontmatter.load(filename_md).metadata['context']['asset']['schema']

        if ("http://" in filename_xsd) or ("https://" in filename_xsd):
            resource = urllib.request.urlopen(filename_xsd)
            schema_to_check = resource.read().decode(resource.headers.get_content_charset())
        else:
            schema_to_check = pathlib.Path(filename_xsd).read_text()
    except Exception as error:
        print("Markdown Validator: Validation FAILED. Couldn't find and open your schema. Make sure you've supplied a schema file and the location is correct.")
        if raise_exception: raise
        return False

     # Validate against schema
    try:
        xmlschema.validate(xhtml, schema_to_check)
        print("Markdown Validator: Validation successful. " + filename_md + " conforms to the schema " + filename_xsd)
        return True
    except Exception as error:
        print("Markdown Validator: Validation FAILED. " + filename_md + " DOES NOT conform to the schema " + filename_xsd + ". Details of the error: " + str(error))
        if raise_exception: raise
        return False

if __name__ == "__main__":
    # Entry point to this app if the commandline is used. Don't forget if a python program runs successfully via the commandline then the program exit(0) by default.
    parser = argparse.ArgumentParser()
    parser.add_argument('markdown', help='location of the markdown file')
    parser.add_argument('-s', '--schema', default=None, help='locaiton of the xsd schema file. This can be on disk or on the web')
    args = parser.parse_args()

    if not validate(args.markdown, args.schema):
        exit(1)
# was 65
