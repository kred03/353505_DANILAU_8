import re
import os
import zipfile
from collections import Counter
from regex_patterns import *

def read_text(filename: str) -> str:
    with open(filename, encoding='utf-8') as file:
        return file.read()

def save_results(filename: str, content: str):
    with open(filename, 'w', encoding='utf-8') as file:
        file.write(content)

def archive_file(input_file: str, archive_name: str):
    with zipfile.ZipFile(archive_name, 'w') as archive:
        archive.write(input_file, os.path.basename(input_file))

def archive_info(archive_name: str):
    with zipfile.ZipFile(archive_name, 'r') as archive:
        for info in archive.infolist():
            return f"Archive contains: {info.filename}, Size: {info.file_size} bytes"

def analyze_text(text: str) -> str:
    results = []

    # Статистика предложений
    sentences = sentence_pattern.findall(text)
    results.append(f"Total sentences: {len(sentences)}")
    results.append(f"Declarative: {len(declarative_pattern.findall(text))}")
    results.append(f"Interrogative: {len(interrogative_pattern.findall(text))}")
    results.append(f"Exclamatory: {len(exclamatory_pattern.findall(text))}")

    # Средняя длина
    words = word_pattern.findall(text)
    avg_word_len = sum(len(word) for word in words) / len(words) if words else 0
    avg_sent_len = sum(len(s) for s in sentences) / len(sentences) if sentences else 0
    results.append(f"Average sentence length (chars): {avg_sent_len:.2f}")
    results.append(f"Average word length (chars): {avg_word_len:.2f}")

    # Распознавание смайликов
    smileys = re.findall(r'[:;]-*[\(\)\[\]]+', text)
    results.append(f"Number of smileys: {len(smileys)}")

    # Слова из заглавных букв и цифр
    mix_words = upper_digit_words_pattern.findall(text)
    results.append("Words with uppercase letters and digits:")
    results.extend(mix_words)

    # Тест безопасности пароля (демо)
    results.append("\nPassword test samples:")
    for pwd in ["C00l_Pass", "SupperPas1", "Cool_pass", "C00l"]:
        res = "✔️" if secure_password_pattern.fullmatch(pwd) else "❌"
        results.append(f"{pwd}: {res}")

    # Слова, написанные полностью заглавными буквами
    upper_words = uppercase_word_pattern.findall(text)
    results.append(f"\nAll-uppercase words count: {len(upper_words)}")

    # Самое длинное слово, начинающееся с «л»
    l_words = starts_with_l_pattern.findall(text)
    longest_l = max(l_words, key=len) if l_words else 'None'
    results.append(f"Longest word starting with 'l': {longest_l}")

    # Повторяющиеся слова
    word_counts = Counter(w.lower() for w in words)
    repeated = [word for word, count in word_counts.items() if count > 1]
    results.append("Repeated words:")
    results.extend(repeated)

    return "\n".join(results)
