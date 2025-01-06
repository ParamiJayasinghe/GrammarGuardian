import streamlit as st
import google.generativeai as genai

# Step 1: Configure your API Key
genai.configure(api_key="YOUR_API_KEY")  # Replace with your actual API key

# Function to call Gemini and check grammar
def check_grammar_with_gemini(text):
    try:
        # Step 2: Call Gemini to generate content based on the input text
        model = genai.GenerativeModel("gemini-1.5-flash")  # Model you want to use (you can specify the model name)
        
        # Generate content from the input sentence
        response = model.generate_content(f"Check the grammar of the following sentence in Sinhala: {text}")
        
        # Step 3: Return the response text from Gemini API
        return response.text
    except Exception as e:
        return f"Error: {e}"

# Modified validate_custom_rules function
def validate_custom_rules(text):
    errors = []
    suggestions = []
    corrected_text = text  # Initialize with the original text

    # Define correction patterns for "මම" and "අපි"
    correction_patterns_mama = {
        "ටා": "ටෙමි", "නා": "නෙමි", "තා": "තෙමි", "දා": "දෙමි", "බා": "බෙමි",
        "මා": "මෙමි", "යා": "යෙමි", "නවා":"මි", "වා": "වෙමි", "සා": "සෙමි",
        "ටාය": "ටෙමි", "නාය": "නෙමි", "තාය": "තෙමි", "දාය": "දෙමි", "බාය": "බෙමි",
        "මාය": "මෙමි", "යාය": "යෙමි", "වාය": "වෙමි", "සාය": "සෙමි",
        "ටේය": "ටෙමි", "ටී": "ටිමි", "ටෙහි": "ටෙමි", "තේය": "තෙමි", "නේය": "නෙමි", "ටෙමු":"ටෙමි"
    }

    correction_patterns_api = {
        "ටා": "ටෙමු", "නා": "නෙමු", "තා": "තෙමු", "දා": "දෙමු", "බා": "බෙමු",
        "මා": "මෙමු", "යා": "යෙමු", "නවා":"මු", "වා": "වෙමු", "සා": "සෙමු",
        "ටාය": "ටෙමු", "නාය": "නෙමු", "තාය": "තෙමු", "දාය": "දෙමු", "බාය": "බෙමු",
        "මාය": "මෙමු", "යාය": "යෙමු", "වාය": "වෙමු", "සාය": "සෙමු",
        "ටේය": "ටෙමු", "ටී": "ටිමු", "ටෙහි": "ටෙමු", "තේය": "තෙමු", "නේය": "නෙමු", "ටෙමි":"ටෙමු"
    }

    is_correct = False  # Flag to determine if the sentence matches the rules

    # Check for sentences starting with "මම"
    if text.startswith("මම"):
        for pattern, replacement in correction_patterns_mama.items():
            if text.endswith(replacement):  # Check if it ends with a correct pattern
                is_correct = True
                break

        # If no match, check if it ends with "මි"
        if not is_correct and text.endswith("මි"):
            is_correct = True

        # If still no match, it's incorrect
        if not is_correct:
            for pattern, replacement in correction_patterns_mama.items():
                if text.endswith(pattern):  # Check for incorrect patterns
                    errors.append(f"")
                    corrected_text = text[: -len(pattern)] + replacement
                    suggestions.append(corrected_text)
                    break

    # Check for sentences starting with "අපි"
    if text.startswith("අපි"):
        for pattern, replacement in correction_patterns_api.items():
            if text.endswith(replacement):  # Check if it ends with a correct pattern
                is_correct = True
                break

        # If no match, check if it ends with "මු"
        if not is_correct and text.endswith("මු"):
            is_correct = True

        # If still no match, it's incorrect
        if not is_correct:
            for pattern, replacement in correction_patterns_api.items():
                if text.endswith(pattern):  # Check for incorrect patterns
                    errors.append(f"")
                    corrected_text = text[: -len(pattern)] + replacement
                    suggestions.append(corrected_text)
                    break

    return errors, corrected_text, is_correct

# Streamlit UI
def main():
    # Set the title of the page
    st.title("සිංහල ව්‍යාකරණ පර්‍ර්ක්ශාව")
    st.title("Sinhala Grammar Checker")

    # Input text from user
    user_input = st.text_area("වාක්‍යය ඇතුලත් කරන්න/Enter Sinhala Text:", "", height=200)

    # Button to trigger grammar check
    if st.button("පරීක්ශා කරන්න/Check Grammar"):
        if user_input.strip():
            # Validate custom grammar rules
            errors, corrected_text, is_correct = validate_custom_rules(user_input)

            if is_correct:
                # If the sentence is grammatically correct
                st.subheader("")
                st.write("ඔබ ඇතුලත් කල වාක්‍යය නිවැරදියි")
            elif errors:
                # If there are errors
                st.subheader("")
                st.write("ඔබ ඇතුලත්කල වාක්‍යයේ ව්‍යාකරණ දෝශයක් පවතී. එය පහත සඳහන් ලෙස නිවැරදි විය යුතුය.")
                st.write(corrected_text)  # Display the corrected sentence
        else:
            st.error("කරුණාකර පුරාකළ වාක්‍යක් ඇතුලත් කරන්න.")

if __name__ == "__main__":
    main()


