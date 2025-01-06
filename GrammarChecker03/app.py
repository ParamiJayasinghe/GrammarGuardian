import streamlit as st

# Rule-based Grammar Checker
# Incorrect and correct sentences lists
incorrect_sentences = [
    "මම යන්නෙමු", "මම යන්නෙමුවා", "මම යන්නෙහි", "මම යන්නෙහිවා", "මම යන්නේය"
]

correct_sentences = [
    "මම යන්නෙමි", "මම යන්නෙමි", "මම යන්නෙමි", "මම යන්නෙමි", "මම යන්නෙමි"
]

# Create a dictionary for fast lookup
correction_map = dict(zip(incorrect_sentences, correct_sentences))

# Streamlit UI
def main():
    st.title("Sinhala Rule-Based Grammar Checker")
    user_input = st.text_area("Enter your Sinhala sentence:")

    if st.button("Check Grammar"):
        if user_input.strip() in correction_map:
            st.write("ඔබ ඇතුලත්කල වාක්‍යයේ ව්‍යාකරණ දෝෂයක් පවතී. එය පහත සඳහන් ලෙස නිවැරදි විය යුතුය:")
            st.write(correction_map[user_input.strip()])
        elif user_input.strip() in correct_sentences:
            st.write("ඔබ ඇතුලත් කල වාක්‍යය නිවැරදියි.")
        else:
            st.write("මෙම වාක්‍යය සඳහා ව්‍යාකරණ දත්ත වල නොමැත. කරුණාකර නැවත පරීක්ෂා කරන්න.")

if __name__ == "__main__":
    main()
