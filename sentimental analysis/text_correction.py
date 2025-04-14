from spellchecker import SpellChecker
import re

def correct_text(text):
    spell = SpellChecker()

    word_pattern = re.compile(r'\b\w+\b')

    words = word_pattern.findall(text)
    
    corrections = {word: spell.correction(word) for word in words}
    
    def replace_match(match):
        word = match.group()
        corrected = corrections.get(word.lower(), word)
        # Preserve original case
        if word.istitle():
            return corrected.title()
        elif word.isupper():
            return corrected.upper()
        return corrected
    
    # Apply corrections while preserving non-word characters
    return word_pattern.sub(replace_match, text)

if __name__ == "__main__":
    # Example usage
    input_text = ""
    corrected_text = correct_text(input_text)
    print(f"Original: {input_text}")
    print(f"Corrected: {corrected_text}")