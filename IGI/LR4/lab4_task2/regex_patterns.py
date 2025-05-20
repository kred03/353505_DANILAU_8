import re

# Предложения
sentence_pattern = re.compile(r'\s*([^.!?]*[.!?])')

# Типы предложений
declarative_pattern = re.compile(r'[^!?]*\.(?!\w)')  # Повествовательные
interrogative_pattern = re.compile(r'[^.!]*\?(?!\w)')  # Вопросительные
exclamatory_pattern = re.compile(r'[^.!]*\!(?!\w)')  # Восклицательные

# Смайлики
smiley_pattern = re.compile(r'(?:[:;])\-*\(?\)*|\-*\[+\]+')

# Слова с заглавными буквами и цифрами
upper_digit_words_pattern = re.compile(r'\b(?=\w*[A-Z])(?=\w*\d)\w+\b')

# Надёжный пароль
secure_password_pattern = re.compile(r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[!@#$%^&*])[A-Za-z\d!@#$%^&*]{8,}$')

# Все слова
word_pattern = re.compile(r'\b[a-zA-Z]+\b')

# Прописные слова
uppercase_word_pattern = re.compile(r'\b[A-Z]+\b')

# Слова на "l"
starts_with_l_pattern = re.compile(r'\bl\w*\b', re.IGNORECASE)