def camel_case_to_words(text: str) -> str:
    words = []
    for letter in text:
        if letter.isupper():
            words.append(letter.lower())
        else:
            words[-1] += letter
    return ' '.join(words).title()