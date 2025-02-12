from django.core.mail import EmailMessage
from django.conf import settings
from io import BytesIO
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph
from reportlab.lib.styles import getSampleStyleSheet
from datetime import datetime
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors

def generar_pdf_factura(datos_factura):
    """Genera un PDF en memoria con mejor diseño para la factura."""
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter)
    
    elementos = []
    
    # Estilos para el texto
    styles = getSampleStyleSheet()
    style_title = styles['Title']
    style_normal = styles['Normal']
    
    # Encabezado
    encabezado = Paragraph('<strong>Factura de Compra</strong>', style_title)
    elementos.append(encabezado)

    # Datos de la empresa
    datos_empresa = [
        ["Empresa Western Union", "Teléfono: +593 96 704 2244"],
        ["Dirección: Calle Mariscal Sucre", "Email: soportealex68@gmail.com"],
        ["Cuenca, Ecuador", "010101"]
    ]
    
    table_empresa = Table(datos_empresa, colWidths=[250, 250])
    table_empresa.setStyle(TableStyle([ 
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 10),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
    ]))
    elementos.append(table_empresa)
    
    # Fecha de la factura
    fecha_factura = datetime.now().strftime('%d-%m-%Y')
    fecha_paragraph = Paragraph(f"<strong>Fecha:</strong> {fecha_factura}", style_normal)
    elementos.append(fecha_paragraph)

    # Datos del cliente
    datos_cliente = [
        ["Cliente:", datos_factura["cliente"]],
        ["Email:", datos_factura["email"]],
        ["Dirección de Envío:", datos_factura["direccion"]],  # Ahora tomamos el valor de "direccion" del diccionario
    ]
    
    table_cliente = Table(datos_cliente, colWidths=[200, 300])
    table_cliente.setStyle(TableStyle([ 
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 10),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
    ]))
    elementos.append(table_cliente)

    # Detalles de la factura (productos o servicios)
    data_factura = [
        ["Descripción", "Cantidad", "Precio Unitario", "Total"],
    ]
    
    for item in datos_factura["items"]:
        data_factura.append([item["descripcion"], item["cantidad"], f"${item['precio_unitario']}", f"${item['total']}"])

    table_factura = Table(data_factura, colWidths=[200, 100, 100, 100])
    table_factura.setStyle(TableStyle([ 
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
    ]))
    elementos.append(table_factura)

    # Total
    total_paragraph = Paragraph(f"<strong>Total: </strong>${datos_factura['total']}", style_normal)
    elementos.append(total_paragraph)
    
    # Pie de página
    pie_pagina = Paragraph(
        "<strong>Gracias por tu compra!</strong><br/>"
        "Para cualquier consulta, contáctanos en soportealex68@gmail.com",
        style_normal
    )
    elementos.append(pie_pagina)
    
    doc.build(elementos)
    buffer.seek(0)
    return buffer

def enviar_correo_factura(destinatario, datos_factura):
    """Envía un correo con un PDF adjunto de la factura."""
    pdf_buffer = generar_pdf_factura(datos_factura)
    
    email = EmailMessage(
        subject="Wetern Union le envia la factura de su pedido",
        body="Adjunto encontrarás la factura de su respectiva compra.",
        from_email=settings.EMAIL_HOST_USER,
        to=[destinatario],
    )
    
    email.attach('factura.pdf', pdf_buffer.read(), 'application/pdf')
    email.send()
