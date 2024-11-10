# albuc_translate

Repository for examining the capability of several open and closed LLMs to translate Albucasis from various historical languages (Occitan, Arabic, Latin, Old French) into modern English.

# Aligning a language
After a high-quality English translation has been generated for a language with an LLM (ChatGPT, Claude or Gemini), run `python divide_chatgpt_chapters.py` on that language like this:
```
python divide_chatgpt_chapters.py lat chatgpt_lat/combined.txt
```
Obviously replace "lat" by the language name (the directory holding the `all_text.txt` file for that language) and `chatgpt_lat/combined.txt` by the file holding the high-quality English translation of the lines in `all_text.txt`. Accordingly, that file will contain the same number of lines as `all_text.txt`, and each line will exactly correspond to (i.e. will be the translation of) the line with the corresponding line number in `all_text.txt`. This will populate a "lat" (or whatever name is specified as `argv[1]`) directory in `sentalign_input`.

Align the `lat` directory chapter by chapter to the existing `eng` directory according to the user guide of SentAlign on GitHub. Set the command line options to `python sentAlign.py -sl eng -tl lat`, obviously replace "lat", and obviously you have to populate the "lat" (whatever) subdirectory of this repository with the same number of chapter files as the "eng" directory with the corresponding content.

Rename `sentalign_input/output` to `sentalign_input/output_lat` or whatever your language is.

Run `python combine_aligned.py lat` (replace language). This creates the `combined_aligned_*.txt` and the `combined_path_*.txt` file for your language.

Run `print_unaligned.py lat` (replace language). This creates an `unaligned_*.txt` file that lists the unaligned segments. Create a copy of `combined_path_*.txt`, call it `combined_path_*_manual.txt`, manually review the unaligned segments, and if they really belong together (which is mostly true), then adjust the alignment in `manual.txt`.

## Where do I get an `all_text.txt` file for my language?
It's extracted automatically along with all the chapter files using `extract_text_by_subchapter_v2.py` from an XML that has the necessary structure. That structure needs to mirror the final XML file in the existing `edition_*` directories precisely. Either create that structure manually, or script it, it's your choice. The chapters for your language need to correspond to the "eng" chapters with the same number and being part of the same book, otherwise an alignment is not possible. It is therefore crucial for the XML to have the correct structure.
