# Markdown Validator
Want your markdown files to have a certain structure? Create schema (XSD), create your markdown file and both to this tool to see if it validates.

## Table of content

- [Motivation](#motivation)
- [Installation & Usage](#installation--usage)
    - [Installation](#installation)
    - [Usage](#usage)
- [Contributing](#contributing)
- [History](#history)
- [Credits](#credits)
- [License](#license)

## Motivation
Markdown is a great way to write all sorts of technical documentation. When you have lots of teams producing technical documentation like policies, standards etc you need a way to ensure they're all sticking to the recommended structure. For example we might want to mandate a principal document must contain certain headers, paragraphs in a certain order.

Markdown Validator works by converting the markdown file to xhtml which can be validated against a schema (XSD file). XSD (XML Schema Definition) is a World Wide Web Consortium (W3C) recommendation that specifies how to formally describe the elements in an Extensible Markup Language (XML) document. 

Ultimately all you have to do is provide a schema (XSD file) and a markdown file and the tool will let you know if the markdown file conforms or not.

## Installation & Usage

### Installation
1. Download the files
2. Navigate to the directory that contains the files from this project
3. Run `pip3 install -r requirements.txt` to make sure you have all the requirements installed
4. Run the validator: `python3 validate.py "schema/principal.xsd" "markdown/principal.md"`. The first parameter is the path to the schema, the second is the markdown to be validated. Test files have been provided so this command will work out the box.

### Usage
TODO: Write usage instructions as below and delete this line

## Contributing
1. Fork it!
2. Create your feature branch: `git checkout -b my-new-feature`
3. Commit your changes: `git commit -am 'Added some feature'`
4. Push to the branch: `git push origin my-new-feature`
5. Submit a pull request :D

## History
v1 - Initial release

## Credits
- Template for this README is <a href="https://github.com/gitzain/template-README">Template-README</a> created by <a href="https://iamzain.com">Zain Khan</a>

## License
See the LICENSE file in this project's directory.