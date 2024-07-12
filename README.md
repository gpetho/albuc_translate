# albuc_translate

Repository for examining the capability of several open and closed LLMs to translate Albucasis from various historical languages (Occitan, Arabic, Latin, Old French) into modern English.

## Extracting the gold English translation from Spink & Lewis's edition of the Arabic original

Create and activate a conda environment to run PyMuPDF and the other required modules:

```
conda create -n pymupdf --file pymupdf.yaml
conda activate pymupdf
```

Then run `extract_english.py`. This generates the two text files `spink_lewis.txt` and `spink_lewis_combined.txt`.
The latter contains the English translation.
