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

    # Rule 1: Starts with "මම" must end with "මි"
    if text.startswith("මම"):
        if not text.endswith("මි"):
            errors.append("The sentence starts with 'මම' but does not end with 'මි'.")
            corrected_text = text.rstrip(".") + "මි."
            suggestions.append(corrected_text)

    # Rule 2: Starts with "අපි" must end with "මු"
    if text.startswith("අපි"):
        if not text.endswith("මු"):
            errors.append("The sentence starts with 'අපි' but does not end with 'මු'.")
            corrected_text = text.rstrip(".") + "මු."
            suggestions.append(corrected_text)

    return errors, suggestions

# Main function to run the checker
def main():
    text = input("Enter Sinhala text: ")
    
    # Step 1: Get grammar feedback from Gemini API
    gemini_response = check_grammar_with_gemini(text)
    print("Gemini API Response:")
    print(gemini_response)  # Display the response from Gemini
    
    # Step 2: Validate custom grammar rules
    errors, suggestions = validate_custom_rules(text)
    if errors:
        print("\nCustom Rule Errors:")
        for error in errors:
            print(f"- {error}")

        print("\nSuggestions:")
        for suggestion in suggestions:
            print(f"- {suggestion}")

    else:
        print("\nNo custom rule errors detected!")

if __name__ == "__main__":
    main()
