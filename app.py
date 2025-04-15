import streamlit as st
import pandas as pd

# Simulamos un glosario bilingüe de términos de lingüística de corpus
data = {
    "término_es": ["concordancia", "frecuencia de tokens", "n-grama", "etiquetado POS", "collocación"],
    "término_en": ["concordance", "token frequency", "n-gram", "POS tagging", "collocation"],
    "definición_es": [
        "Lista de ocurrencias de una palabra clave en su contexto inmediato.",
        "Número de veces que un token aparece en un corpus.",
        "Secuencia contigua de n elementos lingüísticos.",
        "Asignación automática de categorías gramaticales a palabras.",
        "Combinación frecuente de palabras que aparecen juntas más de lo esperado."
    ],
    "definición_en": [
        "A list of occurrences of a keyword in its immediate context.",
        "The number of times a token appears in a corpus.",
        "A contiguous sequence of n linguistic elements.",
        "Automatic assignment of grammatical categories to words.",
        "A frequent combination of words appearing together more than expected."
    ],
    "categoría": ["búsqueda", "estadística", "frecuencia", "análisis morfosintáctico", "combinatoria"]
}

df = pd.DataFrame(data)

# Título de la app
st.title("📘 Glosario Bilingüe de Lingüística de Corpus")

# Filtro por idioma
idioma = st.radio("Selecciona el idioma de visualización:", ["Español", "Inglés"])

# Búsqueda de términos
busqueda = st.text_input("Buscar término:")

# Filtrar según búsqueda
if idioma == "Español":
    filtro = df["término_es"].str.contains(busqueda, case=False)
    resultado = df[filtro][["término_es", "definición_es", "categoría"]].rename(
        columns={
            "término_es": "Término",
            "definición_es": "Definición",
            "categoría": "Categoría"
        })
else:
    filtro = df["término_en"].str.contains(busqueda, case=False)
    resultado = df[filtro][["término_en", "definición_en", "categoría"]].rename(
        columns={
            "término_en": "Term",
            "definición_en": "Definition",
            "categoría": "Category"
        })

# Mostrar resultados
if not resultado.empty:
    st.table(resultado)
else:
    st.info("No se encontraron términos que coincidan con la búsqueda.")

# Pie de página
st.markdown("---")
st.markdown("Desarrollado por Isa · Lingüística computacional · 🧠📊")

