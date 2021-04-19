# pdftoc

Extract the PDF outline (table of contents) as a tree and try to assign a page number to each of the elements.

## Use cases
You have a book that you want to print, but its outline doesn't have page numberings so you'll end up with a useless block of pages

## How
Run `pdftoc <path_to_pdf> > outline.txt`, it will generate a text file outline, which you can then pass though some txt-to-pdf service and insert in into your book, then print it

If, for example, the pdf page numbering (the actual page 1) starts from the physical page 27, run the program with the optional argument `--padding X` like that: `pdftoc <path_to_pdf> --padding 26 > outline.txt`


## Does it work?
Maybe, I don't know. I don't know the PDF format and I don't care to know. I tested it on the book I needed to print and some other book I had in my collection. If it doesn't work for you, issues or pull requests are welcome