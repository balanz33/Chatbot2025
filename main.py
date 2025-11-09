
import streamlit as st
import groq

# =========================
# VARIABLES Y CONSTANTES
# =========================
altura_contenedor_chat = 400
MODELOS = [
    "llama-3.1-8b-instant",
    "llama-3.3-70b-versatile",
    "meta-llama/llama-guard-4-12b"
]

# =========================
# FUNCIONES
# =========================

def configurar_pagina():
    """Configura la interfaz principal de la app."""
    st.set_page_config(page_title="Balanz😎", page_icon="🥳")
    st.title("💬 Balanz - Chat con IA")

    st.sidebar.title("⚙️ Selección de modelo")
    elegir_modelo = st.sidebar.selectbox("Elegí un modelo", options=MODELOS, index=0)
    
    # Botón para borrar historial
    if st.sidebar.button("🧹 Borrar historial"):
        st.session_state.mensajes = []

    return elegir_modelo


def crear_usuario():
    """Crea el cliente de Groq usando la clave API."""
    clave_secreta = st.secrets["CLAVE_API"]
    return groq.Groq(api_key=clave_secreta)


def configurar_modelo(cliente, modelo_elegido, prompt_usuario):
    """Genera la respuesta del modelo."""
    return cliente.chat.completions.create(
        model=modelo_elegido,
        messages=[{"role": "user", "content": prompt_usuario}],
        stream=False
    )


def inicializar_estado():
    """Crea la lista de mensajes si no existe todavía."""
    if "mensajes" not in st.session_state:
        st.session_state.mensajes = []


def actualizar_historial(rol, contenido, avatar):
    """Guarda un mensaje nuevo en el historial."""
    st.session_state.mensajes.append({
        "role": rol,
        "content": contenido,
        "avatar": avatar
    })


def mostrar_historial():
    """Muestra todos los mensajes guardados en orden."""
    for mensaje in st.session_state.mensajes:
        with st.chat_message(mensaje["role"], avatar=mensaje["avatar"]):
            st.write(mensaje["content"])


def area_chat():
    """Contenedor visible del chat."""
    contenedor = st.container(height=altura_contenedor_chat, border=True)
    with contenedor:
        mostrar_historial()


# =========================
# CÓDIGO PRINCIPAL
# =========================

modelo_elegido = configurar_pagina()
cliente = crear_usuario()
inicializar_estado()

prompt_usuario = st.chat_input("✏️ Escribí tu mensaje:")

if prompt_usuario:
    # Guardar mensaje del usuario
    actualizar_historial("user", prompt_usuario, "🎃")
    print(f"Usuario: {prompt_usuario}")

    # Obtener respuesta del modelo y guardarla
    try:
        respuesta = configurar_modelo(cliente, modelo_elegido, prompt_usuario)
        respuesta_texto = respuesta.choices[0].message.content

        actualizar_historial("assistant", respuesta_texto, "👻")
        print(f"Bot: {respuesta_texto}")

    except Exception as e:
        st.error(f"❌ Error al pedir respuesta al modelo: {e}")
        # opcional: guardar mensaje de error en historial
        actualizar_historial("assistant", "Lo siento, hubo un error al obtener la respuesta.", "👻")

# Mostrar historial actualizado

area_chat()
