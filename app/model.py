import re
from collections import Counter
import math
from typing import List

def process_file_tfidf(file_path: str, existing_documents: List[set] = None) -> dict:
    """Обрабатывает файл и возвращает TF-IDF статистику"""
    with open(file_path, 'r', encoding='utf-8') as file:
        text = file.read()
    
    # Предобработка текста
    def preprocess_text(text):
        text = text.lower()
        text = re.sub(r'[^a-zа-яё\s]', '', text)
        return text.split()
    
    words = preprocess_text(text)
    
    if existing_documents is None:
        existing_documents = []
    
    # Расчет TF
    word_counts = Counter(words)
    total_words = len(words)
    tf = {word: count/total_words for word, count in word_counts.items()}
    
    # Добавляем слова текущего документа
    current_doc_words = set(words)
    all_docs = existing_documents + [current_doc_words]
    
    # Расчет IDF
    idf = {}
    for word in current_doc_words:
        doc_count = sum(1 for doc in all_docs if word in doc)
        idf[word] = math.log(len(all_docs) / (doc_count + 1e-10))
    
    # Формирование результата
    result = {
        "word_stats": {
            word: {
                "tf": tf.get(word, 0),
                "idf": idf.get(word, 0),
                "tfidf": tf.get(word, 0) * idf.get(word, 0)
            }
            for word in current_doc_words
        },
        "document_words": current_doc_words
    }
    
    return result