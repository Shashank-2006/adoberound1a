import fitz
import nltk
import re
import numpy as np
from sklearn.cluster import KMeans
from nltk import pos_tag, word_tokenize
from nltk.corpus import stopwords

class PDFOutlineExtractor:
    def __init__(self):
        self.font_threshold = 0.2
        self.min_heading_length = 4
        self.ignored_words = set(stopwords.words("english"))

    def extract_outline(self, pdf_path):
        doc = fitz.open(pdf_path)
        title = self.extract_title(doc)
        spans = self.extract_spans(doc)
        font_clusters = self.cluster_fonts(spans)
        outline = self.build_outline(spans, font_clusters)
        return {"title": title, "outline": outline}

    def extract_title(self, doc):
        meta_title = doc.metadata.get("title", "")
        if meta_title:
            return meta_title.strip()
        first_page = doc[0]
        blocks = first_page.get_text("dict")["blocks"]
        candidates = []
        for block in blocks:
            if "lines" in block:
                for line in block["lines"]:
                    for span in line["spans"]:
                        if len(span["text"].strip()) > 5:
                            candidates.append((span["size"], span["text"].strip()))
        if not candidates:
            return "Untitled"
        candidates.sort(reverse=True)
        return candidates[0][1]

    def extract_spans(self, doc):
        spans = []
        for page_num, page in enumerate(doc, start=1):
            blocks = page.get_text("dict")["blocks"]
            for block in blocks:
                if "lines" not in block:
                    continue
                for line in block["lines"]:
                    for span in line["spans"]:
                        text = span["text"].strip()
                        if not text or self.is_table_like(text) or self.is_noise(text):
                            continue
                        spans.append({
                            "text": text,
                            "font_size": span["size"],
                            "page": page_num,
                            "x": span["bbox"][0],
                            "y": span["bbox"][1]
                        })
        return spans

    def cluster_fonts(self, spans):
        font_sizes = np.array([[s["font_size"]] for s in spans])
        unique_sizes = np.unique(font_sizes)
        n_clusters = min(len(unique_sizes), 3)
        if n_clusters == 0:
            return {}
        kmeans = KMeans(n_clusters=n_clusters, n_init="auto").fit(font_sizes)
        size_to_level = {}
        for i, center in enumerate(sorted(kmeans.cluster_centers_.flatten(), reverse=True)):
            size_to_level[round(center, 1)] = f"H{i + 1}"
        cluster_map = {}
        for span in spans:
            size = round(span["font_size"], 1)
            level = size_to_level.get(size)
            if level:
                cluster_map[(span["text"], span["page"])] = level
        return cluster_map

    def build_outline(self, spans, cluster_map):
        seen = set()
        outline = []
        for span in spans:
            key = (span["text"], span["page"])
            if key in seen:
                continue
            seen.add(key)
            level = cluster_map.get(key)
            if not level:
                continue
            if self.is_false_heading(span["text"]):
                continue
            outline.append({
                "text": span["text"],
                "level": level,
                "page": span["page"]
            })
        return outline

    def is_table_like(self, text):
        if len(text) < 3:
            return False
        if re.match(r"^\d+[\d\s\.\,\%\$\-\/]*$", text):
            return True
        if re.search(r"\s{2,}", text):
            return True
        if re.match(r"^\(?[A-Za-z]{1,2}\)?\s+\d", text):
            return True
        return False

    def is_noise(self, text):
        if re.match(r"^[\s\.,;:\-–—_]+$", text):
            return True
        if re.match(r"^[0-9\.,\-]+$", text):
            return True
        return False

    def is_false_heading(self, text):
        if len(text) < self.min_heading_length:
            return True
        if text.lower() in self.ignored_words:
            return True
        tokens = word_tokenize(text)
        if len(tokens) > 0:
            tags = pos_tag(tokens)
            if all(tag[1] not in {"NN", "NNP", "VB", "JJ"} for tag in tags):
                return True
        if text.endswith(":"):
            return True
        return False
