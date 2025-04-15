import streamlit as st
import pandas as pd
import string

# Simulamos un glosario bilingüe de lingüística de corpus
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

# Configuración general
st.set_page_config(page_title="Glosario Lingüística de Corpus", layout="wide")
st.title("📘 Glosario Bilingüe de Lingüística de Corpus")

# Selección de idioma
idioma = st.radio("Selecciona el idioma de visualización:", ["Español", "Inglés"], horizontal=True)

# Campo de búsqueda libre
busqueda = st.text_input("🔍 Buscar término:")

# Navegación alfabética
letras = list(string.ascii_uppercase)
letra_sel = st.selectbox("📚 Filtrar por letra inicial del término:", letras)

# Función auxiliar para aplicar filtros
def filtrar_glosario(df, idioma, busqueda, letra):
    if idioma == "Español":
        campo_termino = "término_es"
        campo_def = "definición_es"
    else:
        campo_termino = "término_en"
        campo_def = "definición_en"

    df_filtrado = df[df[campo_termino].str.upper().str.startswith(letra.upper())]

    if busqueda:
        df_filtrado = df_filtrado[df_filtrado[campo_termino].str.contains(busqueda, case=False)]

    df_mostrar = df_filtrado[[campo_termino, campo_def, "categoría"]]
    df_mostrar.columns = ["Término", "Definición", "Categoría"]
    return df_mostrar

# Mostrar resultados
resultado = filtrar_glosario(df, idioma, busqueda, letra_sel)

if not resultado.empty:
    st.table(resultado)
else:
    st.warning("No se encontraron términos que coincidan con los filtros.")

# Pie de página
st.markdown("---")
st.markdown("📚 Proyecto en desarrollo por Isa · Lingüística computacional · Semaínein 🧠")
