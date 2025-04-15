import streamlit as st
import pandas as pd
import string

# ------------------------
# 📚 Datos simulados
# ------------------------
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
    "categoría": ["búsqueda", "estadística", "frecuencia", "análisis morfosintáctico", "combinatoria"],
    "tema": ["corpus", "estadística", "nlp", "nlp", "corpus"]
}
df = pd.DataFrame(data)

# ------------------------
# ⚙️ Configuración
# ------------------------
st.set_page_config(page_title="Glosario Lingüística de Corpus", layout="wide")
st.title("📘 Glosario Bilingüe de Lingüística de Corpus")

# ------------------------
# 🌍 Idioma
# ------------------------
idioma = st.radio("Selecciona el idioma de visualización:", ["Español", "Inglés"], horizontal=True)

# ------------------------
# 🔍 Filtros combinados
# ------------------------
busqueda = st.text_input("Buscar término (por texto):")

letras = list(string.ascii_uppercase)
letra_sel = st.selectbox("Filtrar por letra inicial:", ["Todas"] + letras)

categorías_disponibles = sorted(df["tema"].unique())
cat_sel = st.multiselect("Filtrar por categoría temática:", categorías_disponibles)

# ------------------------
# 🔍 Aplicar filtros
# ------------------------
if idioma == "Español":
    campo_term = "término_es"
    campo_def = "definición_es"
else:
    campo_term = "término_en"
    campo_def = "definición_en"

df_filtrado = df.copy()

if letra_sel != "Todas":
    df_filtrado = df_filtrado[df_filtrado[campo_term].str.upper().str.startswith(letra_sel)]

if busqueda:
    df_filtrado = df_filtrado[df_filtrado[campo_term].str.contains(busqueda, case=False)]

if cat_sel:
    df_filtrado = df_filtrado[df_filtrado["tema"].isin(cat_sel)]

terminos_disponibles = df_filtrado[campo_term].tolist()

# ------------------------
# 📘 Mostrar listado de términos y entrada terminológica
# ------------------------
if terminos_disponibles:
    st.success(f"{len(terminos_disponibles)} término(s) encontrado(s).")

    termino_seleccionado = st.selectbox("Selecciona un término para ver su entrada:", terminos_disponibles)

    entrada = df[df[campo_term] == termino_seleccionado].iloc[0]

    st.markdown("### 📝 Entrada terminológica")

    st.markdown(f"**Término:** {entrada[campo_term]}")
    st.markdown(f"**Definición:** {entrada[campo_def]}")
    st.markdown(f"**Categoría gramatical:** {entrada['categoría']}")
    st.markdown(f"**Tema:** {entrada['tema']}")
else:
    st.warning("No se encontraron términos con los filtros aplicados.")

# ------------------------
# 📌 Pie
# ------------------------
st.markdown("---")
st.markdown("🧠 Desarrollado por Isa · Lingüística computacional · Proyecto *Glosario Corpus*")
