import pathlib
import argparse
import urllib
import xmlschema
import markdown
import frontmatter


def get_markdown_content(markdown_file):
    try:
        return frontmatter.load(markdown_file).content
    except:
        raise Exception('Error loading markdown file. Make sure the location is correct and you have a valid markdown file.')


def markdown_to_xhtml(markdown_content):
    return "<root>\n" + markdown.markdown(markdown_content) + "\n</root>"


def has_schema(filename_md, filename_xsd=None):
    try:
        if filename_xsd is None:
            filename_xsd = frontmatter.load(filename_md).metadata['context']['asset']['schema']
    except:
        return None

    return filename_xsd


def get_schema(filename_xsd):
    try:
        if ("http://" in filename_xsd) or ("https://" in filename_xsd):
            resource = urllib.request.urlopen(filename_xsd)
            return filename_xsd, resource.read().decode(resource.headers.get_content_charset())
        else:
            return filename_xsd, pathlib.Path(filename_xsd).read_text()
    except:
        raise Exception('Error loading schema. Make sure the location is correct and you have a valid schema file.')


def validate(filename_md, filename_xsd=None, raise_exception=False, ignore_no_schema=True):
    """
    Provide a schema (XSD file) and a markdown file and
    this function will let you know if the markdown file conforms or not.
    Note: This function needs to convert the markdown to xhtml and then the xhtml is validated against the schema file.
    :param filename_xsd: the path to the schema
    :param filename_md: the markdown to be validated
    :param raise_exception: 'False' will ensure this function returns True if successful or False for any other reason. If this is set to 'True' the function will return True if it's successful else it will raise an exception detailing what went wrong.
    :return boolean: True or False depending if the file validates or not.
    """
    try:
        markdown_content = get_markdown_content(filename_md)
        xhtml_to_check = markdown_to_xhtml(markdown_content)

        filename_xsd = has_schema(filename_md, filename_xsd)
        if filename_xsd is None and ignore_no_schema is True:
            print("Markdown Validator: Validation successful. " + filename_md + " didn't have a schema to check against")
            return True

        filename_xsd, schema_to_check = get_schema(filename_xsd)

        xmlschema.validate(xhtml_to_check, schema_to_check)
        print("Markdown Validator: Validation successful. " + filename_md + " conforms to the schema " + filename_xsd)
        return True
    except Exception as error:
        if raise_exception: 
            raise
        print("Markdown Validator: Validation FAILED. Details of the error: " + str(error))
        return False


if __name__ == "__main__":
    # Entry point to this app if the commandline is used. Don't forget if a python program runs successfully via the commandline then the program exit(0) by default.
    parser = argparse.ArgumentParser()
    parser.add_argument('markdown', help='location of the markdown file')
    parser.add_argument('-s', '--schema', default=None, help='locaiton of the xsd schema file. This can be on disk or on the web')
    parser.add_argument('-i', '--ignore', action="store_true", default=False, help='if this is set to false and no schema can be found the validator will say the markdown is valid')
    args = parser.parse_args()

    if not validate(args.markdown, filename_xsd=args.schema, raise_exception=False, ignore_no_schema=args.ignore):
        exit(1)