from collections import defaultdict
import math
import os
import string


def process_file_tfidf(folder_path):
    """Обработка всех файлов в указанной папке"""
    documents = {}
    # Чтение и обработка всех текстовых файлов
    for filename in os.listdir(folder_path):
        if filename.endswith(".txt"):
            file_path = os.path.join(folder_path, filename)
            with open(file_path, 'r', encoding='utf-8') as f:
                text = f.read().lower()
                text = text.translate(str.maketrans('', '', string.punctuation))
                documents[filename] = text.split()

    if not documents:
        return {}

    # Расчет TF
    tfs = defaultdict(dict)
    for doc, words in documents.items():
        word_count = len(words)
        freq = defaultdict(int)
        for word in words:
            freq[word] += 1
        for word, count in freq.items():
            tfs[doc][word] = count / word_count

    # Расчет IDF
    doc_freq = defaultdict(int)
    total_docs = len(documents)
    for words in documents.values():
        for word in set(words):
            doc_freq[word] += 1

    idf = {word: math.log(total_docs / (1 + count)) for word, count in doc_freq.items()}

    # Расчет TF-IDF
    tfidf_result = defaultdict(dict)
    for doc in documents:
        for word in tfs[doc]:
            tf_val = tfs[doc][word]
            idf_val = idf[word]
            tfidf_result[doc][word] = {
                "tf": round(tf_val, 6),
                "idf": round(idf_val, 6),
                "tfidf": round(tf_val * idf_val, 6)
            }

    return tfidf_result