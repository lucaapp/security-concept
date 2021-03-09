# Luca Security Concept

This is the document source of luca's security concept.
Please go here for the HTML version: https://luca-app.de/securityconcept

## Getting in Touch

We're interested in your feedback! Please start discussions or participate in the ["Discussions" section](https://github.com/lucaapp/security-concept/discussions) of this repository.

Despite the document's language being English, please feel free to open discussions in either German or English. Whatever you're more comfortable with.

## Building the Document

This document is written as a `jupyter-book`. Install the python requirements via `pip`:

```sh
pip install -r requirements.txt
```

To render the diagrams you need `plantuml`. Install it via your package manager or download the `.jar` file directly:

```sh
wget -O - "http://sourceforge.net/projects/plantuml/files/plantuml-nodot.1.2021.1.jar/download" > plantuml.jar
```

Finally, run the `buildhtml.sh` from this directoy:

```sh
./buildhtml.sh
```

### Rendering a PDF

You can render a PDF document using LaTeX. First, install LaTeX on your system. Currently you will need to run `./buildhtml.sh` once, to set up jupyter-book's `_config.yml` and then run:

```sh
PLANTUMLPATH='<your path to plantuml.jar>' PLANTUMLFORMAT='png' jupyter-book build content --builder pdflatex
```

## Style Guidelines

Please adhere to the following rules when editing this document:

 * in text blocks, write one sentence per line in the markdown file for Git-friendliness
 * section headlines should have a [Target Header marker](https://jupyterbook.org/reference/cheatsheet.html#target-headers) following the form `(chapter:section)=` (e.g. `(process:location_registration)=`)
 * prefer [List Tables](https://jupyterbook.org/reference/cheatsheet.html#tables) over markdown tables
 * use underscores `_` instead of spaces in file names
 * don't skip header levels (i.e. no `###` outside `#` and `##`)
 * use exactly one first level header (`#`) per page
 * Python code must be [black](https://github.com/psf/black) formatted
