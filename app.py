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
# 🌍 Idioma
# ------------------------
idioma = st.radio("Idioma de visualización:", ["Español", "Inglés"], horizontal=True)

# ------------------------
# 🔍 Filtros
# ------------------------
busqueda = st.text_input("Buscar término:")
letras = list(string.ascii_uppercase)
letra_sel = st.selectbox("Filtrar por letra inicial:", ["Todas"] + letras)
categorías_disponibles = sorted(df["tema"].unique())
cat_sel = st.multiselect("Filtrar por categoría temática:", categorías_disponibles)

# ------------------------
# 📦 Aplicar filtros
# ------------------------
campo_term = "término_es" if idioma == "Español" else "término_en"
campo_def = "definición_es" if idioma == "Español" else "definición_en"

df_filtrado = df.copy()

if letra_sel != "Todas":
    df_filtrado = df_filtrado[df_filtrado[campo_term].str.upper().str.startswith(letra_sel)]

if busqueda:
    df_filtrado = df_filtrado[df_filtrado[campo_term].str.contains(busqueda, case=False)]

if cat_sel:
    df_filtrado = df_filtrado[df_filtrado["tema"].isin(cat_sel)]

# ------------------------
# 🧭 Navegación con query params
# ------------------------
query_params = st.query_params
termino_actual = query_params.get("termino", None)

# ------------------------
# 📘 Mostrar entradas o listado de términos
# ------------------------
if termino_actual:
    # Mostrar entrada terminológica
    entrada = df[df[campo_term] == termino_actual]
    if not entrada.empty:
        row = entrada.iloc[0]
        st.markdown(f"### 📝 Entrada terminológica: {row[campo_term]}")
        st.markdown(f"**Definición:** {row[campo_def]}")
        st.markdown(f"**Categoría gramatical:** {row['categoría']}")
        st.markdown(f"**Tema:** {row['tema']}")
        st.markdown("[🔙 Volver al glosario](?)")
    else:
        st.error("No se encontró el término.")
else:
    st.success(f"{len(df_filtrado)} término(s) encontrado(s). Haz clic en uno para ver su entrada completa.")
    for termino in sorted(df_filtrado[campo_term]):
        st.markdown(f"- [{termino}](?termino={termino})")

# ------------------------
# 📌 Pie
# ------------------------
st.markdown("---")
st.markdown("🧠 Desarrollado por Isabel Moyano |  Proyecto *en construcción*")
