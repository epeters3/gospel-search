## ER Description

**Collection**: Segments

**Description**: Each document is a scripture verse or paragraph of a conference talk.

**Fields**:

- \_id: The URL of the scripture minus the `lang` query string parameter and the base URL.
- text: The actual verse or talk paragraph.
- links: The text of links found among the footnotes of the segment.
- index: The verse number of the scripture or paragraph number of the conference talk corresponding to the segment.
- parent_doc: The chapter number or conference talk name the verse or paragraph is a part of.
- work: The book or conference year the segment is a part of.
- volume: The volume of scripture or conference session the segment is a part of.
- type: Whether its a scripture verse or conference talk paragraph.

## Notes on General Conference talks:

- The superscript style links are all of the form `<a class="note-ref" href="/#notei">i</a>`, where `i` is an integer. The corresponding scripture reference in the Related Content section has the same `href`. I think I could find them among the paragraphs, so I can know the id of the paragraph the reference occurs in, then look them all up in the Related Content section by that same href so I can grab the text of the scripture.
- The parenthetical style links are all of the form `<a class="scripture-ref" href="/study/path-to-scripture">scripture name</a>`.
- Each paragraph is of the form `<p data-aid="..." id="pi">...</p>`, where `i` is the id of the paragraph.
- When poetry or lyrics are cited, each line has it's own `<p>` tag, and the parents of all the lines is a `<div class="poetry" />` tag.

## Notes on the Scriptures:

- The Related Content includes the verse number in each note e.g. `<a href="/#noteij">scripture name</a>`, where `i` is the verse number and `j` is the letter identifying which footnote in the verse it is.
