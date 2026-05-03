import streamlit as st
from fpdf import FPDF
from datetime import datetime
import io

# --- Configuración de la Página ---
st.set_page_config(page_title="TramiTRUJILLO - Notas de Venta", page_icon="📄")

# --- Datos fijos ---
EMPRESA = "TramiTRUJILLO"
LEMA = "SIMPLIFICANDO TUS GESTIONES TRIBUTARIAS"
CELULAR = "935534706"
DIRECCION = "Psj. Pasaje San Agustín N° 110 - Trujillo"

# --- Inicialización del Estado ---
if 'productos' not in st.session_state:
    st.session_state.productos = []

# --- Función para generar PDF ---
def generar_nota_pdf(n_nota, cliente, vendedor, metodo, total, lista_prod):
    pdf = FPDF('P', 'mm', (120, 250))
    pdf.add_page()
    pdf.set_font("Helvetica", "B", 10)
    
    # Encabezado
    pdf.cell(100, 5, EMPRESA, ln=True, align="C")
    pdf.set_font("Helvetica", "", 8)
    pdf.cell(100, 5, LEMA, ln=True, align="C")
    pdf.cell(100, 5, DIRECCION, ln=True, align="C")
    pdf.ln(5)
    
    pdf.set_font("Helvetica", "B", 10)
    pdf.cell(100, 5, f"NOTA DE VENTA: {n_nota}", ln=True, align="C")
    pdf.set_font("Helvetica", "", 9)
    pdf.cell(100, 5, f"Fecha: {datetime.now().strftime('%d/%m/%Y %H:%M')}", ln=True)
    pdf.cell(100, 5, f"Cliente: {cliente if cliente else 'Cliente Varios'}", ln=True)
    pdf.cell(100, 5, f"Método: {metodo}", ln=True)
    pdf.ln(2)
    
    # Tabla
    pdf.set_font("Helvetica", "B", 9)
    pdf.cell(50, 6, "Desc.", border="B")
    pdf.cell(15, 6, "Cant.", border="B", align="R")
    pdf.cell(15, 6, "P.U.", border="B", align="R")
    pdf.cell(20, 6, "Total", border="B", align="R")
    pdf.ln()
    
    pdf.set_font("Helvetica", "", 9)
    for p in lista_prod:
        pdf.cell(50, 6, p['desc'])
        pdf.cell(15, 6, str(p['cant']), align="R")
        pdf.cell(15, 6, f"{p['precio']:.2f}", align="R")
        pdf.cell(20, 6, f"{p['subtotal']:.2f}", align="R")
        pdf.ln()
        
    pdf.ln(5)
    pdf.set_font("Helvetica", "B", 10)
    pdf.cell(100, 5, f"TOTAL: S/ {total:.2f}", ln=True, align="R")
    pdf.ln(10)
    pdf.set_font("Helvetica", "I", 7)
    pdf.multi_cell(100, 4, "Documento no válido como comprobante de pago ante SUNAT. Uso Informativo.", align="C")
    
    return pdf.output()

# --- Interfaz de Usuario ---
st.title("📄 Notas de Venta - TramiTRUJILLO")

with st.sidebar:
    st.header("Configuración")
    numero_nv = st.number_input("N° Nota", min_value=1, value=1)
    numero_nota_str = f"NV-{numero_nv:06d}"
    vendedor = st.text_input("Vendedor", value="Antonny Carlos")
    metodo_pago = st.selectbox("Pago", ["Efectivo", "Yape", "Plin", "Transferencia"])

cliente = st.text_input("Nombre del Cliente", placeholder="Cliente Varios")

st.subheader("Añadir Productos")
c1, c2, c3 = st.columns([3, 1, 1])
desc = c1.text_input("Descripción")
cant = c2.number_input("Cant.", min_value=1.0, value=1.0)
precio = c3.number_input("P. Unit", min_value=0.0, value=0.0)

if st.button("Agregar ➕"):
    if desc:
        st.session_state.productos.append({
            "desc": desc, "cant": cant, "precio": precio, "subtotal": cant * precio
        })
        st.rerun()

# --- Mostrar Tabla y Botones Finales ---
if st.session_state.productos:
    st.divider()
    st.table(st.session_state.productos)
    total_final = sum(p['subtotal'] for p in st.session_state.productos)
    st.metric("Total", f"S/ {total_final:.2f}")

    col_btn1, col_btn2 = st.columns(2)
    with col_btn1:
        if st.button("Limpiar 🗑️"):
            st.session_state.productos = []
            st.rerun()
    
    with col_btn2:
        # AQUÍ ESTÁ EL TRUCO: Generamos los bytes primero
        try:
            pdf_bytes = generar_nota_pdf(numero_nota_str, cliente, vendedor, metodo_pago, total_final, st.session_state.productos)
            st.download_button(
                label="Descargar PDF 📥",
                data=pdf_bytes,
                file_name=f"Nota_{numero_nota_str}.pdf",
                mime="application/pdf"
            )
        except Exception as e:
            st.error("Error al preparar el PDF. Intenta de nuevo.")
