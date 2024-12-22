from spellchecker import SpellChecker

def spell_check_and_correct(paragraph):
    # Initialize the spell checker
    spell = SpellChecker()
    
    # Split the paragraph into words
    words = paragraph.split()
    
    # Identify misspelled words
    misspelled = spell.unknown(words)
    
    # Prepare the list of corrected words
    corrected_words = {}
    
    # Correct each misspelled word, but only up to 5 corrections
    correction_count = 0
    for word in misspelled:
        if correction_count < 5:
            corrected_words[word] = spell.correction(word)
            correction_count += 1
    
    # Apply corrections to the original paragraph
    corrected_paragraph = " ".join([corrected_words.get(word, word) for word in words])
    
    return corrected_paragraph, corrected_words

# Example usage:
input_paragraph = "This is a sampel paragrap with a few spellng mistakes for check."
corrected_paragraph, corrections = spell_check_and_correct(input_paragraph)

print("Original Paragraph: ", input_paragraph)
print("Corrected Paragraph: ", corrected_paragraph)
print("Corrections made: ", corrections)
