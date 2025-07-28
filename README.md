#  PDF Outline Extractor

A lightweight tool to automatically extract hierarchical outlines (headings, subheadings) from PDF documents using layout-based heuristics and natural language filtering.


##  Approach

The extractor works in the following stages:

1. **Layout Parsing with PyMuPDF**
   - Extracts spans (text elements) from every page with bounding boxes, font size, and content.

2. **Heading Detection via Font Clustering**
   - Uses `KMeans` from `scikit-learn` to cluster font sizes.
   - Assigns heading levels (`H1`, `H2`, `H3`, etc.) based on cluster rank (larger = higher level).

3. **Noise & Table Filtering**
   - Removes spans that match patterns like tables, page numbers, or numerical sequences using regex.
   - Skips noisy tokens like punctuation, single characters, and non-informative headers.

4. **Text Validation with NLP**
   - Uses `nltk` for part-of-speech tagging.
   - Rejects spans that contain no meaningful nouns, verbs, or adjectives.

5. **Outline Generation**
   - Builds a structured outline with text, heading level, and page number.
   - Extracts document title either from metadata or the largest font on the first page.

---

## Libraries Used

| Library           | Purpose                            |
|------------------|------------------------------------|
| **PyMuPDF (fitz)**| PDF text & layout extraction       |
| **nltk**          | Tokenization, POS tagging, stopwords |
| **scikit-learn**  | Clustering font sizes (KMeans)     |
| **numpy**         | Numerical operations               |
| **re** (Regex)    | Text and table pattern detection   |

 ##
We will build the docker image using the following command: ```docker build --platform linux/amd64 -t mysolutionname:somerandomidentifier```
After building the image, we will run the solution using the run command specified in the submitted instructions. ```docker run --rm -v $(pwd)/input:/app/input -v $(pwd)/output:/app/output -- network none mysolutionname:somerandomidentifie  
