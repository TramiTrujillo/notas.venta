import streamlit as st
from fpdf import FPDF
from datetime import datetime
import io

# --- Configuración de la Página ---
st.set_page_config(page_title="TramiTRUJILLO - Notas de Venta", page_icon="📄")

if 'productos' not in st.session_state:
    st.session_state.productos = []

# --- Función para crear el PDF ---
def crear_pdf(numero_nota, cliente, vendedor, metodo, total, productos):
    pdf = FPDF('P', 'mm', (120, 250))
    pdf.add_page()
    pdf.set_font("Helvetica", "B", 12)
    pdf.cell(100, 10, "TramiTRUJILLO", ln=True, align="C")
    
    pdf.set_font("Helvetica", "", 9)
    pdf.cell(100, 5, f"Nota: {numero_nota}", ln=True)
    pdf.cell(100, 5, f"Cliente: {cliente}", ln=True)
    pdf.ln(5)
    
    # Tabla
    pdf.set_font("Helvetica", "B", 9)
    pdf.cell(50, 6, "Descripción", border="B")
    pdf.cell(20, 6, "Cant.", border="B", align="R")
    pdf.cell(30, 6, "Total", border="B", align="R", ln=True)
    
    pdf.set_font("Helvetica", "", 9)
    for p in productos:
        pdf.cell(50, 6, p['desc'])
        pdf.cell(20, 6, str(p['cant']), align="R")
        pdf.cell(30, 6, f"{p['subtotal']:.2f}", align="R", ln=True)
    
    pdf.ln(5)
    pdf.set_font("Helvetica", "B", 10)
    pdf.cell(100, 10, f"TOTAL: S/ {total:.2f}", align="R")
    
    return bytes(pdf.output())

# --- Interfaz Principal ---
st.title("📄 Generador de Notas de Venta")

# Formulario similar a tu imagen del SATT
with st.form("mi_formulario"):
    col1, col2 = st.columns(2)
    with col1:
        n_nota = st.text_input("Número de Nota", value="NV-000001")
        cliente = st.text_input("Apellidos y Nombres", placeholder="Cliente Varios")
    with col2:
        vendedor = st.text_input("Vendedor", value="Antonny Carlos")
        metodo = st.selectbox("Método de Pago", ["Efectivo", "Yape", "Plin"])
    
    # Este es el botón que querías (igual al de la imagen)
    submit_button = st.form_submit_button("Generar PDF con Texto Completo")

# Sección de productos (debe estar fuera del form para actualizar la lista)
st.subheader("🛒 Lista de Productos")
c1, c2, c3 = st.columns([3, 1, 1])
p_desc = c1.text_input("Producto/Servicio")
p_cant = c2.number_input("Cantidad", min_value=1.0, value=1.0)
p_prec = c3.number_input("Precio Unit.", min_value=0.0, value=0.0)

if st.button("Añadir a la lista ➕"):
    if p_desc:
        st.session_state.productos.append({
            "desc": p_desc, "cant": p_cant, "subtotal": p_cant * p_prec
        })
        st.rerun()

if st.session_state.productos:
    st.table(st.session_state.productos)

# --- Lógica de Generación ---
if submit_button:
    if not st.session_state.productos:
        st.error("No hay productos en la lista.")
    else:
        # Aquí se genera el PDF solo cuando presionas el botón del formulario
        total_final = sum(p['subtotal'] for p in st.session_state.productos)
        pdf_bytes = crear_pdf(n_nota, cliente, vendedor, metodo, total_final, st.session_state.productos)
        
        st.success("✅ PDF generado con éxito.")
        
        # Ahora aparece el botón de descarga solo como resultado final
        st.download_button(
            label="⬇️ Click aquí para descargar archivo",
            data=pdf_bytes,
            file_name=f"{n_nota}.pdf",
            mime="application/pdf"
        )
