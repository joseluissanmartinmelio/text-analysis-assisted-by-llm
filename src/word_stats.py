import re
from collections import Counter

def count_words(text):
    words = re.findall(r'\b\w+\b|[^\w\s]', text)
    word_count = len(words)
    unique_words = len(set(words))
    words_frequencies = Counter(words)
    most_common = words_frequencies.most_common(10)

    return {
        "total": word_count,
        "unique": unique_words,
        "most_common": most_common
    }