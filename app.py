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

# --- Función Maestra de PDF ---
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
    
    # Tabla de productos
    pdf.set_font("Helvetica", "B", 9)
    pdf.cell(50, 6, "Desc.", border="B")
    pdf.cell(15, 6, "Cant.", border="B", align="R")
    pdf.cell(15, 6, "P.U.", border="B", align="R")
    pdf.cell(20, 6, "Total", border="B", align="R")
    pdf.ln()
    
    pdf.set_font("Helvetica", "", 9)
    if not lista_prod:
        pdf.cell(100, 10, "Sin productos registrados", ln=True, align="C")
    else:
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

# --- Interfaz Principal ---
st.title("📄 Notas de Venta - TramiTRUJILLO")

# Sidebar siempre visible
with st.sidebar:
    st.header("Datos de Nota")
    numero_nv = st.number_input("N° Correlativo", min_value=1, value=1)
    numero_nota_str = f"NV-{numero_nv:06d}"
    vendedor = st.text_input("Vendedor", value="Antonny Carlos")
    metodo_pago = st.selectbox("Pago", ["Efectivo", "Yape", "Plin", "Transferencia"])

# Formulario de entrada
cliente = st.text_input("Nombre del Cliente", value="Cliente Varios")

st.subheader("🛒 Carrito de Compras")
c1, c2, c3 = st.columns([3, 1, 1])
desc = c1.text_input("Servicio/Producto")
cant = c2.number_input("Cant.", min_value=1.0, value=1.0)
precio = c3.number_input("P. Unit", min_value=0.0, value=0.0)

if st.button("Agregar a la Nota ➕"):
    if desc:
        st.session_state.productos.append({
            "desc": desc, "cant": cant, "precio": precio, "subtotal": cant * precio
        })
        st.rerun()

# --- Zona de Descarga (Siempre visible) ---
st.divider()
total_actual = sum(p['subtotal'] for p in st.session_state.productos)

# Mostramos la tabla si hay productos, si no, un aviso
if st.session_state.productos:
    st.table(st.session_state.productos)
else:
    st.info("La lista está vacía. El PDF se generará con S/ 0.00 hasta que agregues productos.")

st.write(f"### Total acumulado: S/ {total_actual:.2f}")

# El botón de descarga está fuera de cualquier 'if', igual que en tu código de SATT
pdf_preparado = generar_nota_pdf(numero_nota_str, cliente, vendedor, metodo_pago, total_actual, st.session_state.productos)

st.download_button(
    label="⬇️ Descargar Nota ahora",
    data=pdf_preparado,
    file_name=f"Nota_{numero_nota_str}.pdf",
    mime="application/pdf",
    use_container_width=True # Lo hace ver más como un botón de app profesional
)

if st.button("Vaciar Lista 🗑️"):
    st.session_state.productos = []
    st.rerun()
