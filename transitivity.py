import streamlit as st
from transitivity_detector import analyze_transitivity

st.title("Transitivity Clause Detector")

text = st.text_area("Enter text (one or multiple sentences):")

if st.button("Analyze") and text.strip():
    sentences = [s.strip() for s in text.split(".") if s.strip()]
    
    for sentence in sentences:
        result = analyze_transitivity(sentence)
        st.write(f"### Sentence: {sentence}")

        for clause in result['clauses']:
            st.write(
                f"- **Verb:** {clause['verb']} | "
                f"**Object:** {clause['direct_object']} | "
                f"**Type:** {clause['clause_type']}"
            )
        st.write("---")
