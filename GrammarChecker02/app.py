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

# Function to validate the custom rules
def validate_custom_rules(text):
    errors = []
    suggestions = []
    corrected_text = text  # Keep track of the corrected text

    # Rule 1: Starts with "මම" must end with "මි"
    if text.startswith("මම"):
        if not (text.endswith("මි") or text.endswith("මී") or text.endswith("යයි") or text.endswith("වී")):
            errors.append("The sentence starts with 'මම' but does not end with 'මි', 'මී', 'යයි', or 'වී'.")
            corrected_text = text.rstrip(".") + "මි."

    # Rule 2: Starts with "අපි" must end with "මු"
    if text.startswith("අපි"):
        if not (text.endswith("මු") or text.endswith("ෙමු") or text.endswith("යමු") or text.endswith("වෙමු")):
            errors.append("The sentence starts with 'අපි' but does not end with 'මු', 'ෙමු', 'යමු', or 'වෙමු'.")
            corrected_text = text.rstrip(".") + "මු."

    # Return the errors and corrected text
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
