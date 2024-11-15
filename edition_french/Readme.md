# Preprocessing

## Round 1

The preprocessing of the Old French XML had be redone from scratch twice. On the first occasion:
- sentence segmentation was not implemented within the XML;
- ChatGPT did the sentence segmentation, resulting in an output where it could not be established in a straightforward way from which part of the XML each ChatGPT output line had come;
- sentence segments were in part much too long (a whole chapter being a single sentence), in part too short, and in the latter cases not real sentences but simply shorter parts of a long sentence.
Overall this was judged as an unsatisfactory solution. (I tried the same for Arabic, but with Gemini Pro instead of ChatGPT, and within the XML paragraph elements. The sentence segmentation was inconsistent and unsatisfactory in that case in the same way, see the `ara_gemini` directory).

## Round 2

On the second occasion, sentence segmentation was done using Spacy within the original XML structure, with a standoff annotation file specifying the correct chapter boundaries, `chapters_standoff.xml`, which was written by me by manually comparing the beginnings and ends as well as the numbering of the chapters marked in Spink & Lewis to the Trotter XML. It aligns the chapters as marked in the Trotter editions and as annotated in `ChirAlbT_text_bfm.xml` with the Spink & Lewis chapter structure which appears in `edition_arabic`, `edition_english` and `edition_occ`. The point of this was to leave the structure and content of the Trotter XML untouched apart from corrections that are necessarily independently of this conversion.

Specifically, lots of `<num>` element markings were missing around Roman numerals appearing in the Trotter XML. These tags were evidently inserted automatically around numerals that looked like `.iij.`, but when either of the periods were missing or not where they should have been, like `est. iij.`, then the markup was missing around them, causing problems for further processing. The punctuation was corrected and the missing `<num>` tags added manually to `ChirAlbT_text_bfm.xml` directly, so this is already a modified file compared with what we started out with. The punctuation mistakes were already there in the Trotter printed book, so they were not introduced during the conversion into XML format.

When it came to aligning the Old French translation to the Spink & Lewis reference, it turned out that the Spacy segmentation was also far from satisfactory. In general, the sentences marked by full stops in the Trotter edition are extremely long, often as long as 10 to 15 sentences in the Spink & Lewis translation. Many segments could not be properly aligned, except by very long m:n bisegments. Some French "sentences" were the length of entire pages.

## Round 3

For these reasons, the segmentation had to be redone yet again. The sentences marked by full stops were further subdivided along colons and semicolons. This increased the number of sentence segments from 1400 to 3600. At the same time, the standoff annotation for the chapter boundaries had to be adjusted as a consequence. The current final version of this file is `updated_standoff_renumbered.xml`.

# Further processing

To generate the `ofr` directory, the following steps are necessary.

1. `python ChirAlb_divide_sentences_v2.py`, which adds paragraph numbering and segments the paragraphs into sentences (using spacy, then along colons and semicolons), but adds a few minor adjustments as well. This creates `ChirAlbT_text_bfm_mod_subsents.xml`.
2. `python combine_standoff.py`: reads `ChirAlbT_text_bfm.xml` and `updated_standoff_renumbered.xml`, and generates, based on these, `chapters_combined_updated.xml`.
3. `python extract_text_by_subchapter_v2.py ofr edition_french/chapters_combined_updated.xml -s` then populates the `ofr` directory.
