import re

class SinhalaSpellChecker:
    def __init__(self, lexicon_file):
        """Initialize the spell checker with a lexicon file."""
        self.lexicon = self.load_lexicon(lexicon_file)
        # Define common Sinhala character variations
        self.variations = {
            # Vowel variations
            'ො': 'ා',    # යනවො -> යනවා
            'ූ': 'ු',    # කලූ -> කලු
            'ී': 'ි',    # නගී -> නගි
            'ෙ': 'ේ',
            'ொ': 'ො',
            
            # Consonant variations
            'ද': 'ඩ',    # උද -> උඩ
            'හ': 'හා',   # වහනය -> වාහනය
            'ග': 'ගණ',   # පරිගනකය -> පරිගණකය
            'න': 'නං',   # නගී -> නංගී
            'ය': 'යෙ',   # තියනවා -> තියෙනවා
        }
        
        # Common word patterns that need correction
        self.word_patterns = {
            'වහනය': 'වාහනය',
            'තියනවා': 'තියෙනවා',
            'පරිගනකය': 'පරිගණකය',
            'පවිච්චි': 'පාවිච්චි',
        }
        
    def load_lexicon(self, lexicon_file):
        """Load Sinhala words from the lexicon file."""
        try:
            with open(lexicon_file, 'r', encoding='utf-8') as file:
                return set(word.strip() for word in file.readlines())
        except FileNotFoundError:
            print(f"Error: Lexicon file '{lexicon_file}' not found.")
            return set()
            
    def get_word_variations(self, word):
        """Generate possible variations of a word for error correction."""
        variations = set()
        
        # 1. Check for direct word patterns
        if word in self.word_patterns:
            variations.add(self.word_patterns[word])
        
        # 2. Character variations
        for i in range(len(word)):
            # Check each character for possible variations
            if word[i] in self.variations:
                variations.add(word[:i] + self.variations[word[i]] + word[i+1:])
            
            # Handle special cases for compound characters
            if i < len(word) - 1:
                two_chars = word[i:i+2]
                if two_chars in self.variations:
                    variations.add(word[:i] + self.variations[two_chars] + word[i+2:])
        
        # 3. Special case for නග -> නංග
        if 'නග' in word:
            variations.add(word.replace('නග', 'නංග'))
            
        # 4. Handle missing vowel marks
        if 'පවි' in word:
            variations.add(word.replace('පවි', 'පාවි'))
            
        return variations

    def find_corrections(self, word):
        """Find possible corrections for a misspelled word."""
        if word in self.lexicon:
            return []
            
        variations = self.get_word_variations(word)
        corrections = [var for var in variations if var in self.lexicon]
        return corrections[:5]  # Return maximum 5 corrections
        
    def check_text(self, text):
        """Check spelling in the given text and return corrections."""
        words = re.findall(r'\S+', text)
        errors = {}
        error_count = 0
        
        for word in words:
            if word not in self.lexicon:
                corrections = self.find_corrections(word)
                if corrections and error_count < 5:  # Limit to 5 errors
                    errors[word] = corrections
                    error_count += 1
                    
        return errors

    def correct_text(self, text):
        """Automatically correct spelling errors in the text."""
        errors = self.check_text(text)
        corrected_text = text
        
        for error, corrections in errors.items():
            if corrections:
                corrected_text = corrected_text.replace(error, corrections[0])
                
        return corrected_text, errors

def main():
    # Initialize spell checker
    checker = SinhalaSpellChecker('sinhala_lexicon.txt')
    
    # Get input from user
    print("Enter Sinhala text to check:")
    text = input()
    
    # Check spelling and get corrections
    errors = checker.check_text(text)
    
    # Display results
    if errors:
        print("\nSpelling errors found:")
        for word, corrections in errors.items():
            if corrections:
                print(f"'{word}' might be misspelled. Suggestions: {', '.join(corrections)}")
            else:
                print(f"'{word}' might be misspelled. No suggestions available.")
    else:
        print("No spelling errors found.")
    
    # Show auto-corrected text
    corrected_text, _ = checker.correct_text(text)
    print("\nAuto-corrected text:")
    print(corrected_text)

if __name__ == "__main__":
    main()