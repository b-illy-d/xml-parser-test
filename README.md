# Cypris Data Engineering Test

## Install and run

From the repo root:

```python
uv sync
uv run parse
```

## Problem statement

### Objective

The program should read an input XML from one of three sources:
- stdin
- local file
- public GS url

The program should parse the XML doc and extract the value of any `</doc-number>` tags found.

The program should return these doc-number values as a list of integers.

The returned list should have any doc numbers found in an "EPO" entry listed first, followed by doc numbers from "patent-office" entries.

If there are no doc-numbers found in the document, the program should return an empty list.

The returned value is printed to stdout.

### Assumptions about the structure of the input document

I'm writing my code under the following assumptions:

  - the `root` element MAY have one or more `application-reference` element(s) as children
  - an `application-reference` element MAY have one or more `document-id` element(s) as children
  - a `document-id` element MAY have one or more `doc-number` element(s) as children
  - a `document-id` element MAY have EITHER a `format="epo"` attribute OR a `load-source="patent-office"` attribute

