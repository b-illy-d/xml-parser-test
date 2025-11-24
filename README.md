# Data Engineering Test

## Install and run

From the repo root:

1. Install dependecies:

```
uv sync
source .venv/bin/activate
```

2. Run the program with the `parser` script:

```
usage: parser [-h] [-f PATH | -u URL | -s]

options:
  -h, --help            show this help message and exit
  -f PATH, --file PATH  Read XML from a local file path.
  -u URL, --url URL     Read XML from a public Google Cloud Storage URL.
  -s, --stdin           Explicitly read XML from stdin (default when no other source is provided).

Examples:
    parser -f ~/example.xml
    parser -u https://storage.googleapis.com/billys_xml_example_test/example.xml # <-- this is a public bucket url
    cat ~/example.xml | parser
```

Of course, you could save yourself some keystrokes and just run `uv run parser <OPTIONS>` and then
`uv` will install all the dependecies before running the script.

## Objective

The program should read an input XML from one of three sources:
- stdin
- local file
- public GS url

The program should parse the XML doc and extract the value of any `</doc-number>` tags found.

The program should return these doc-number values as a list of integers.

The returned list should have any doc numbers found in an "EPO" entry listed first, followed by doc numbers from "patent-office" entries.

If there are no doc-numbers found in the document, the program should return an empty list.

The returned value is printed to stdout.

## Assumptions about the structure of the input document

I'm writing my code under the following assumptions:

  - the `root` element MAY have one or more `application-reference` element(s) as children
  - an `application-reference` element MAY have one or more `document-id` element(s) as children
  - a `document-id` MUST appear as a child of an `application-reference` element
    - therefore I can just ignore any child of the `root` that isn't `application-reference`
  - a `document-id` element MAY have one or more `doc-number` element(s) as children
    - all such elements should be collected
  - a `document-id` element MAY have EITHER a `format="epo"` attribute OR a `load-source="patent-office"` attribute
    - a `document-id` element without either of these will be ignored

## Decisions

  - Dependencies: the only one is `lxml`, a widely used and trusted xml library for python. Would be idiotic to write a parser here.
  - Stream instead of string: Don't load the whole xml doc into memory at once, be sure to clear elements from memory once we're done with them.

  - The meat of the parser code is a little hard to understand, since it's a lot of nested if/then logic. I tried to make it readable and extensible:
    - I find that `match` blocks are easy to read and reason about. It makes for nice, idiomatic Python.
    - I extracted the logic for finding the source of a doc-number, with the idea that other sources could be added more easily this way.
      - Rather than having to understand that heavy if/else logic, future devs can add/re-arrange sources by:
        - Creating a test function `_is_some_source` that receives the doc-number element and returns a bool
        - Adding it to the `SOURCES_TESTS` list in the place that those doc-numbers should appear with respect to other sources.

So I've optimised the writing of the code for adding new sources and/or changing the sort order of sources.
If it's the case that, for example, we know these sources are the only two we will ever care about, but that the structure of the document will tend to change, then the code should have been written to make it more flexible with regard to document structure.
Obviously in a real life situation it would be easier to know the context that such trade-offs are being made in, but here I've just picked one.



