import streamlit as st
import pandas as pd
from datetime import datetime

EXCEL_FILE = 'estudiantes.xlsx'

def cargar_datos():
    return pd.read_excel(EXCEL_FILE, dtype={'Código de matrícula': str, 'DNI': str})

def guardar_datos(df):
    df.to_excel(EXCEL_FILE, index=False)

def verificar_credenciales(df, codigo, contrasena):
    fila_df = df[df['Código de matrícula'].str.strip() == codigo.strip()]
    if fila_df.empty:
        return False, None
    fila = fila_df.iloc[0]

    dni_guardado = str(fila['DNI']).strip()
    nueva_contra = str(fila['contraseña nueva']).strip() if pd.notna(fila['contraseña nueva']) else ""

    if nueva_contra == "" or nueva_contra.lower() == 'nan':  # Primer ingreso
        if dni_guardado == contrasena.strip():
            return True, fila
    elif nueva_contra == contrasena.strip():
        return True, fila

    return False, None

def actualizar_ingresos(df, codigo):
    df.loc[df['Código de matrícula'] == codigo, 'Ingresos'] += 1
    guardar_datos(df)

def actualizar_contrasena(df, codigo, nueva):
    df.loc[df['Código de matrícula'] == codigo, 'contraseña nueva'] = nueva
    guardar_datos(df)

def mostrar_tabla_notas(fila):
    actividades = [
        "Examen parcial", "Examen Final", "Exposición Grupal",
        "Cuestionarios", "Participación en clase (2%)\nResponsabilidad y puntualidad (3%)",
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

    df = cargar_datos()

    codigo = st.text_input("Ingrese su Código de Matrícula (8 caracteres)")
    contrasena = st.text_input("Ingrese su contraseña o DNI", type="password")

    if st.button("Ingresar"):
        if len(codigo) != 8:
            st.error("El código debe tener 8 caracteres.")
            return

        acceso, fila = verificar_credenciales(df, codigo, contrasena)
        if acceso:
            if str(fila['contraseña nueva']).strip().lower() in ["", "nan"]:
                st.info("Primer ingreso detectado. Por favor, defina una nueva contraseña.")
                nueva_contra = st.text_input("Nueva contraseña", type="password")
                confirmar = st.text_input("Confirmar nueva contraseña", type="password")
                if nueva_contra and nueva_contra == confirmar:
                    actualizar_contrasena(df, codigo, nueva_contra)
                    st.success("Contraseña actualizada correctamente. Por favor, vuelva a iniciar sesión.")
                elif nueva_contra and nueva_contra != confirmar:
                    st.warning("Las contraseñas no coinciden.")
                return
            else:
                actualizar_ingresos(df, codigo)
                st.success("Bienvenido/a. Acceso exitoso.")
                st.subheader(f"{fila['Apellidos y Nombre']}")
                st.write(f"**Código de Matrícula:** {codigo}")
                mostrar_tabla_notas(fila)

                st.markdown("### 💬 Sigamos estudiando 💪")
                st.markdown(f"🕒 Fecha y hora de acceso: `{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}`")

                if st.button("Salir"):
                    st.experimental_rerun()
        else:
            st.error("Código o contraseña incorrectos.")

if __name__ == "__main__":
    app()
