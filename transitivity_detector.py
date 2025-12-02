import streamlit as st
import spacy

# -----------------------------
# Load spaCy model (cached so it loads once)
# -----------------------------
@st.cache_resource
def load_model():
    try:
        return spacy.load("en_core_web_sm")
    except OSError:
        import subprocess, sys
        subprocess.run(
            [sys.executable, "-m", "spacy", "download", "en_core_web_sm"]
        )
        return spacy.load("en_core_web_sm")

nlp = load_model()


# -----------------------------
# Transitivity analysis function
# -----------------------------
def analyze_transitivity(sentence: str):
    """
    Analyzes a sentence for transitivity:
    - finds verbs
    - checks if they have a direct object
    - labels as Transitive / Intransitive
    """
    doc = nlp(sentence)
    clauses = []

    for token in doc:
        if token.pos_ == "VERB":
            verb = token
            dobj = None

            # Look for direct object dependents
            for child in verb.children:
                if child.dep_ in ("dobj", "obj"):
                    dobj = child
                    break

            clause_type = "Transitive" if dobj else "Intransitive"

            clauses.append({
                "verb": verb.text,
                "direct_object": dobj.text if dobj else None,
                "clause_type": clause_type,
            })

    return {
        "sentence": sentence,
        "clauses": clauses
    }


# -----------------------------
# Streamlit UI
# -----------------------------
st.title("Transitivity Clause Detector")

text = st.text_area("Enter text (one or more sentences):")

if st.button("Analyze") and text.strip():
    # very simple sentence split on periods
    sentences = [s.strip() for s in text.split(".") if s.strip()]

    for sentence in sentences:
        result = analyze_transitivity(sentence)
        st.markdown(f"### Sentence: {sentence}")

        if not result["clauses"]:
            st.write("- No verbs detected.")
        else:
            for clause in result["clauses"]:
                st.write(
                    f"- **Verb:** `{clause['verb']}` | "
                    f"**Object:** `{clause['direct_object']}` | "
                    f"**Type:** **{clause['clause_type']}**"
                )
        st.write("---")
