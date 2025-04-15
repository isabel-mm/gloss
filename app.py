import streamlit as st
import pandas as pd
import string

# ------------------------
# 🔢 Datos simulados
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
    "tema": ["corpus", "estadística", "nlp", "nlp", "corpus"]  # Categorías temáticas
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
# 🔍 Filtro 1: búsqueda por texto
# ------------------------
busqueda = st.text_input("Buscar término:")

# ------------------------
# 🔠 Filtro 2: letra inicial
# ------------------------
letras = list(string.ascii_uppercase)
letra_sel = st.selectbox("Filtrar por letra inicial del término:", ["Todas"] + letras)

# ------------------------
# 📂 Filtro 3: categoría temática
# ------------------------
categorías_disponibles = sorted(df["tema"].unique())
cat_sel = st.multiselect("Filtrar por categoría temática:", categorías_disponibles)

# ------------------------
# 🧠 Función de filtrado
# ------------------------
def filtrar(df, idioma, busqueda, letra, categorias):
    if idioma == "Español":
        campo_term = "término_es"
        campo_def = "definición_es"
    else:
        campo_term = "término_en"
        campo_def = "definición_en"

    df_filtrado = df.copy()

    if letra != "Todas":
        df_filtrado = df_filtrado[df_filtrado[campo_term].str.upper().str.startswith(letra)]

    if busqueda:
        df_filtrado = df_filtrado[df_filtrado[campo_term].str.contains(busqueda, case=False)]

    if categorias:
        df_filtrado = df_filtrado[df_filtrado["tema"].isin(categorias)]

    return df_filtrado[[campo_term, campo_def, "categoría", "tema"]].rename(
        columns={campo_term: "Término", campo_def: "Definición", "categoría": "Categoría", "tema": "Tema"}
    )

# ------------------------
# 📋 Mostrar resultados
# ------------------------
resultado = filtrar(df, idioma, busqueda, letra_sel, cat_sel)

if not resultado.empty:
    st.success(f"{len(resultado)} término(s) encontrado(s).")
    st.table(resultado)
else:
    st.warning("No se encontraron resultados con los filtros aplicados.")

# ------------------------
# 📌 Pie
# ------------------------
st.markdown("---")
st.markdown("🧠 Desarrollado por Isa · Lingüística computacional · Proyecto *Glosario Corpus*")
