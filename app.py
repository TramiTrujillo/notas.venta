import streamlit as st
from fpdf import FPDF
from datetime import datetime
import pytz  # Librería para manejar zonas horarias

# --- Configuración ---
st.set_page_config(page_title="Generador TramiTRUJILLO", page_icon="📄")

if 'productos' not in st.session_state:
    st.session_state.productos = []

# --- Función para convertir números a letras (Básico) ---
def total_a_letras(total):
    enteros = int(total)
    centimos = int(round((total - enteros) * 100))
    return f"SON: {enteros} CON {centimos:02d}/100 SOLES"

# --- Función Maestra del PDF ---
def crear_pdf(n_nota, caja, vendedor, cliente, metodo, productos):
    # Obtener hora de Perú (UTC-5)
    tz_peru = pytz.timezone('America/Lima')
    fecha_peru = datetime.now(tz_peru).strftime('%d-%m-%Y %H:%M')

    # Formato tipo ticket
    pdf = FPDF('P', 'mm', (105, 220)) 
    pdf.add_page()
    pdf.set_margins(7, 7, 7)
    
    # ENCABEZADO
    pdf.set_font("Helvetica", "B", 14)
    pdf.cell(0, 7, "TramiTRUJILLO", ln=True, align="C")
    pdf.set_font("Helvetica", "", 8)
    pdf.cell(0, 4, "SIMPLIFICANDO TUS GESTIONES TRIBUTARIAS", ln=True, align="C")
    pdf.cell(0, 4, "Psj. Pasaje San Agustín N° 110 - Trujillo", ln=True, align="C")
    pdf.cell(0, 4, "acarlosa@unitru.edu.pe", ln=True, align="C")
    pdf.cell(0, 4, "Cel: 935534706", ln=True, align="C")
    pdf.ln(4)
    
    # INFO NOTA
    pdf.set_font("Helvetica", "B", 9)
    pdf.cell(0, 5, f"NOTA DE VENTA N°: {n_nota}", ln=True)
    pdf.set_font("Helvetica", "", 9)
    pdf.cell(0, 5, f"Caja: {caja}", ln=True)
    pdf.cell(0, 5, f"Fecha: {fecha_peru}", ln=True) 
    pdf.cell(0, 5, f"Vendedor: {vendedor}", ln=True)
    pdf.cell(0, 5, f"Cliente: {cliente if cliente else 'Clientes Varios'}", ln=True)
    pdf.ln(2)
    
    # CABECERA TABLA
    pdf.set_font("Helvetica", "B", 8)
    pdf.cell(45, 6, "Descripción", border="TB")
    pdf.cell(12, 6, "Cant.", border="TB", align="C")
    pdf.cell(15, 6, "P.Unit", border="TB", align="R")
    pdf.cell(18, 6, "Total", border="TB", align="R")
    pdf.ln(7)
    
    # CUERPO TABLA
    pdf.set_font("Helvetica", "", 8)
    total_acumulado = 0
    for p in productos:
        pdf.cell(45, 5, p['desc'])
        pdf.cell(12, 5, str(p['cant']), align="C")
        pdf.cell(15, 5, f"{p['precio']:.2f}", align="R")
        pdf.cell(18, 5, f"{p['subtotal']:.2f}", align="R")
        pdf.ln()
        total_acumulado += p['subtotal']
    
    pdf.ln(2)
    pdf.set_draw_color(200, 200, 200)
    pdf.line(7, pdf.get_y(), 98, pdf.get_y())
    pdf.ln(2)
    
    # TOTALES
    pdf.set_font("Helvetica", "", 9)
    pdf.cell(72, 6, "Subtotal:", align="R")
    pdf.cell(18, 6, f"{total_acumulado:.2f}", align="R", ln=True)
    
    pdf.set_font("Helvetica", "B", 10)
    pdf.cell(72, 6, "Total:", align="R")
    pdf.cell(18, 6, f"{total_acumulado:.2f}", align="R", ln=True)
    pdf.ln(2)
    
    # MONTO EN LETRAS Y PAGO
    pdf.set_font("Helvetica", "B", 8)
    pdf.cell(0, 5, total_a_letras(total_acumulado), ln=True)
    pdf.set_font("Helvetica", "", 9)
    pdf.cell(0, 5, f"Método de pago: {metodo}", ln=True)
    pdf.ln(4)
    
    # PIE DE PÁGINA
    pdf.set_font("Helvetica", "B", 9)
    pdf.cell(0, 5, "¡Gracias por su preferencia!", ln=True, align="C")
    pdf.set_font("Helvetica", "", 8)
    pdf.cell(0, 4, "Consulte nuestros servicios al 935534706", ln=True, align="C")
    
    pdf.set_text_color(0, 0, 255)
    pdf.set_font("Helvetica", "U", 8)
    wa_url = "https://wa.me/51935534706"
    pdf.cell(0, 4, "Presiona aquí para WhatsApp", ln=True, align="C", link=wa_url)
    
    pdf.set_text_color(0, 0, 0)
    pdf.ln(3)
    pdf.set_font("Helvetica", "I", 7)
    pdf.multi_cell(0, 3, "Documento no válido como comprobante de pago ante SUNAT. Uso Informativo", align="C")
    
    # --- EL CAMBIO ESTÁ AQUÍ ---
    # Usamos dest='S' para retornar los bytes correctamente en FPDF
    return pdf.output(dest='S').encode('latin-1')

# --- Interfaz de Streamlit ---
st.title("📄 Generador TramiTRUJILLO")

with st.form("datos_nota"):
    col1, col2 = st.columns(2)
    with col1:
        n_nota = st.text_input("Nota de Venta N°", value="NV-000052")
        caja = st.text_input("Caja", value="1")
        vendedor = st.text_input("Vendedor", value="Carlos Daniel")
    with col2:
        cliente = st.text_input("Cliente", value="Clientes Varios")
        metodo = st.selectbox("Método de Pago", ["Yape", "Efectivo", "Plin", "Transferencia"])
    
    submit_button = st.form_submit_button("Generar PDF")

st.subheader("Añadir Productos")
c1, c2, c3 = st.columns([3, 1, 1])
p_desc = c1.text_input("Descripción")
p_cant = c2.number_input("Cant", min_value=1, value=1)
p_prec = c3.number_input("P.Unit", min_value=0.0, value=0.0, step=0.1)

if st.button("Añadir a la lista ➕"):
    if p_desc:
        st.session_state.productos.append({
            "desc": p_desc, "cant": p_cant, "precio": p_prec, "subtotal": p_cant * p_prec
        })
        st.rerun()

if st.session_state.productos:
    st.table(st.session_state.productos)
    if st.button("Vaciar Lista 🗑️"):
        st.session_state.productos = []
        st.rerun()

if submit_button:
    if not st.session_state.productos:
        st.warning("Agrega productos antes de generar el PDF.")
    else:
        pdf_bytes = crear_pdf(n_nota, caja, vendedor, cliente, metodo, st.session_state.productos)
        st.success("PDF generado según el formato oficial.")
        st.download_button(
            label="⬇️ Descargar Nota de Venta",
            data=pdf_bytes,
            file_name=f"{n_nota}.pdf",
            mime="application/pdf",
            use_container_width=True
        )
