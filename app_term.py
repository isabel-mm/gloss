# app.py

import streamlit as st
import spacy
import pandas as pd
import joblib
import numpy as np

# Cargar modelo y scaler
model = joblib.load("rf_model.joblib")
scaler = joblib.load("scaler.joblib")

# Cargar modelo spaCy
nlp = spacy.load("en_core_web_trf")

# Título de la app
st.title("🔍 Identificación automática de términos")
texto = st.text_area("Pega tu texto aquí:", height=250)

if st.button("Detectar términos"):
    with st.spinner("Procesando..."):
        doc = nlp(texto)
        rows = []
        for sent_id, sent in enumerate(doc.sents):
            for i, token in enumerate(sent):
                rows.append({
                    "token": token.text,
                    "lemma": token.lemma_,
                    "pos": token.pos_,
                    "shape": token.shape_,
                    "is_stop": token.is_stop,
                    "position_in_sentence": i,
                    "is_in_noun_phrase": token.dep_ in {"nsubj", "dobj", "pobj", "nmod"},
                    "has_adjective_modifier": any(child.dep_ == "amod" for child in token.children),
                    "has_pre_modifier": any(child.dep_ in {"poss", "compound"} for child in token.children),
                    "is_noun": token.pos_ == "NOUN",
                    "is_adj": token.pos_ == "ADJ",
                    "is_propn": token.pos_ == "PROPN",
                    "is_verb": token.pos_ == "VERB",
                    "is_acronym": token.text.isupper() and len(token.text) > 1,
                    "definition_pattern": False,  # simplificado
                    "token_norm": token.text.lower()
                })

        df = pd.DataFrame(rows)

        # Calcular pos_probability
        lemma_pos_counts = df.groupby(["lemma", "pos"]).size().unstack(fill_value=0)
        pos_prob = lemma_pos_counts.div(lemma_pos_counts.sum(axis=1), axis=0).max(axis=1).to_dict()
        df["pos_probability"] = df["lemma"].map(pos_prob)

        # Rellenar rasgos estadísticos con ceros
        for f in ["freq_in_text", "freq_global", "document_frequency", "tf_idf",
                  "lexical_variety", "avg_position_in_sentence", "dispersion"]:
            df[f] = 0.0

        # Rellenar definición patrón
        df["definition_pattern"] = (
            df["token_norm"].shift(1) + " " + df["token_norm"]
        ).isin(["is a", "is defined"]).fillna(False)

        df["is_multiword_term"] = False

        features = [
            "is_stop", "position_in_sentence", "is_in_noun_phrase",
            "has_adjective_modifier", "has_pre_modifier",
            "freq_in_text", "freq_global", "document_frequency",
            "tf_idf", "lexical_variety", "avg_position_in_sentence", "dispersion",
            "is_noun", "is_adj", "is_propn", "is_verb",
            "is_multiword_term", "definition_pattern", "is_acronym", "pos_probability"
        ]

        # Escalar
        X = df[features]
        X_scaled = scaler.transform(X)
        df["prediction"] = model.predict(X_scaled)

        # Mostrar resultado con resaltado
        st.markdown("### Resultado:")
        out = []
        for token, pred in zip(df["token"], df["prediction"]):
            if pred == 1:
                out.append(f"**:blue[{token}]**")
            else:
                out.append(token)
        st.markdown(" ".join(out))
