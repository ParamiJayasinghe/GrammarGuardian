import streamlit as st
import google.generativeai as genai

# Step 1: Configure your API Key
genai.configure(api_key="AIzaSyCPHqFRMpblUyiENpsQAq4KnOgQcdzQbIU")  # Replace with your actual API key

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

def validate_custom_rules(text):
    errors = []
    suggestions = []
    corrected_text = text  # Initialize with the original text

    # Define correction patterns for "මම" and "අපි"
    correction_patterns_mama = {
        "ටා": "ටෙමි", "නා": "නෙමි", "තා": "තෙමි", "දා": "දෙමි", "බා": "බෙමි",
        "මා": "මෙමි", "යා": "යෙමි", "වා": "වෙමි", "සා": "සෙමි",
        "ටාය": "ටෙමි", "නාය": "නෙමි", "තාය": "තෙමි", "දාය": "දෙමි", "බාය": "බෙමි",
        "මාය": "මෙමි", "යාය": "යෙමි", "වාය": "වෙමි", "සාය": "සෙමි",
        "ටේය": "ටෙමි", "ටී": "ටිමි", "ටෙහි": "ටෙමි"
    }

    correction_patterns_api = {
        "ටා": "ටෙමු", "නා": "නෙමු", "තා": "තෙමු", "දා": "දෙමු", "බා": "බෙමු",
        "මා": "මෙමු", "යා": "යෙමු", "වා": "වෙමු", "සා": "සෙමු",
        "ටාය": "ටෙමු", "නාය": "නෙමු", "තාය": "තෙමු", "දාය": "දෙමු", "බාය": "බෙමු",
        "මාය": "මෙමු", "යාය": "යෙමු", "වාය": "වෙමු", "සාය": "සෙමු",
        "ටේය": "ටෙමු", "ටී": "ටිමු", "ටෙහි": "ටෙමු"
    }

    # Check for sentences starting with "මම"
    if text.startswith("මම"):
        # Loop through the correction patterns for "මම"
        for pattern, replacement in correction_patterns_mama.items():
            if text.endswith(pattern):
                errors.append(f"The sentence starts with 'මම' but ends with '{pattern}', which is incorrect.")
                corrected_text = text[: -len(pattern)] + replacement
                suggestions.append(corrected_text)
                break  # Only apply the first matching correction

        # If no pattern matched, check the default ending with "මි"
        if not any(text.endswith(pat) for pat in correction_patterns_mama.keys()):
            if not text.endswith("මි"):
                errors.append("The sentence starts with 'මම' but does not end with 'මි'.")
                corrected_text = text.rstrip(".") + "මි."
                suggestions.append(corrected_text)

    # Check for sentences starting with "අපි"
    if text.startswith("අපි"):
        # Loop through the correction patterns for "අපි"
        for pattern, replacement in correction_patterns_api.items():
            if text.endswith(pattern):
                errors.append(f"The sentence starts with 'අපි' but ends with '{pattern}', which is incorrect.")
                corrected_text = text[: -len(pattern)] + replacement
                suggestions.append(corrected_text)
                break  # Only apply the first matching correction

        # If no pattern matched, check the default ending with "මු"
        if not any(text.endswith(pat) for pat in correction_patterns_api.keys()):
            if not text.endswith("මු"):
                errors.append("The sentence starts with 'අපි' but does not end with 'මු'.")
                corrected_text = text.rstrip(".") + "මු."
                suggestions.append(corrected_text)

    return errors, corrected_text

# Streamlit UI
def main():
    # Set the title of the page
    st.title("Sinhala Grammar Checker")

    # Input text from user
    user_input = st.text_area("Enter Sinhala Text:", "", height=200)

    # Button to trigger grammar check
    if st.button("Check Grammar"):
        if user_input.strip():
            # Get grammar feedback from Gemini API
            gemini_response = check_grammar_with_gemini(user_input)
            st.subheader("Gemini API Response:")
            st.write(gemini_response)  # Display the response from Gemini

            # Validate custom grammar rules
            errors, corrected_text = validate_custom_rules(user_input)

            if errors:
                st.subheader("Custom Rule Errors:")
                for error in errors:
                    st.write(f"- {error}")

                st.subheader("Corrected Sentence:")
                st.write(f"{corrected_text}")  # Display the corrected sentence
            else:
                st.write("\nNo custom rule errors detected!")
        else:
            st.error("Please enter Sinhala text to check.")

if __name__ == "__main__":
    main()
