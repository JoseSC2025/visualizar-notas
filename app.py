import streamlit as st
import pandas as pd
from datetime import datetime

EXCEL_FILE = 'estudiantes.xlsx'

def cargar_datos():
    return pd.read_excel(EXCEL_FILE, dtype={'Código de matrícula': str, 'DNI': str})

def guardar_datos(df):
    df.to_excel(EXCEL_FILE, index=False)

def verificar_credenciales(df, codigo, dni):
    fila_df = df[df['Código de matrícula'].str.strip() == codigo.strip()]
    if fila_df.empty:
        return False, None
    fila = fila_df.iloc[0]
    
    dni_guardado = str(fila['DNI']).strip()
    if dni_guardado == dni.strip():
        return True, fila
    return False, None

def actualizar_ingresos(df, codigo):
    df.loc[df['Código de matrícula'] == codigo, 'Ingresos'] += 1
    guardar_datos(df)

def mostrar_tabla_notas(fila):
    actividades = [
        "Examen parcial", "Examen Final", "Exposición Grupal",
        "Cuestionarios", "Participación (2%),\nAsistencia (3%)",
        "Laboratorio"
    ]
    ponderaciones = ["30 %", "30 %", "10 %", "5 %", "5 %", "20 %"]
    notas = [
        fila['Nota 1'], fila['Nota 2'], fila['Nota 3'],
        fila['Nota 4'], fila['Nota 5'], fila['Nota 6']
    ]
    df_notas = pd.DataFrame({
        "Actividades": actividades,
        "Ponderación": ponderaciones,
        "Nota": notas
    })
    st.dataframe(df_notas, use_container_width=True)

def app():
    st.set_page_config(page_title="Visualizar Notas de Física General", page_icon="📘")
    st.title("📘 Visualizar Notas de Física General")

    # Ejecuta rerun si fue marcado previamente
    if st.session_state.get("rerun_pendiente", False):
        st.session_state.rerun_pendiente = False
        st.experimental_rerun()

    if 'autenticado' not in st.session_state:
        st.session_state.autenticado = False

    df = cargar_datos()

    if not st.session_state.autenticado:
        codigo = st.text_input("Ingrese su Código de Matrícula", key='codigo')
        dni = st.text_input("Ingrese su DNI", type="password", key='dni')

        if st.button("Ingresar"):
            if len(codigo.strip()) != 8:
                st.error("El código debe tener 8 caracteres.")
                return

            acceso, fila = verificar_credenciales(df, codigo, dni)
            if acceso:
                actualizar_ingresos(df, codigo)
                st.session_state.autenticado = True
                st.session_state.fila = fila
                st.success("Bienvenido/a. Acceso exitoso.")
                st.session_state.rerun_pendiente = True  # Marca que se debe hacer rerun en el próximo ciclo
            else:
                st.error("Código o DNI incorrecto.")
    else:
        fila = st.session_state.fila
        st.subheader(f"{fila['Apellidos y Nombre']}")
#        st.write(f"**Código de Matrícula:** {fila['Código de matrícula']}")
        mostrar_tabla_notas(fila)

        st.markdown("### 💬 Sigamos estudiando 💪")
        st.markdown(f"🕒 Fecha y hora de acceso: `{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}`")

        if st.button("Salir"):
            st.session_state.clear()
            st.session_state.rerun_pendiente = True  # Forzar reinicio visual

if __name__ == "__main__":
    app()
