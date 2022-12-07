import os
from datetime import date
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch, mm
from reportlab.lib.pagesizes import letter
from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_RIGHT
from reportlab.lib.colors import black, white, green
from reportlab.pdfgen import canvas

LOGO = __file__.replace('CreateReport.py', 'logo.png')

class reportePDF(object):
    """Exportar una lista de diccionarios a una tabla en un
       archivo PDF."""
    
    def __init__(self, titulo, cabecera, datos, nombrePDF, cliente = None, id = '', total = None):
        super(reportePDF, self).__init__()

        self.titulo = titulo
        self.cabecera = cabecera
        self.datos = datos
        self.nombrePDF = nombrePDF
        self.cliente = cliente
        self.id = id
        
        self.total = total

        self.estilos = getSampleStyleSheet()

    def convertirDatos(self):
        """Convertir la lista de diccionarios a una lista de listas para crear
           la tabla PDF."""

        estiloEncabezado = ParagraphStyle(name="estiloEncabezado", alignment=TA_LEFT,
                                          fontSize=10, textColor=white,
                                          fontName="Helvetica-Bold",
                                          parent=self.estilos["Normal"])

        estiloNormal = self.estilos["Normal"]
        estiloNormal.alignment = TA_LEFT

        claves, nombres = zip(*[[k, n] for k, n in self.cabecera])

        encabezado = [Paragraph(nombre, estiloEncabezado) for nombre in nombres]
        nuevosDatos = [tuple(encabezado)]

        for dato in self.datos:
            nuevosDatos.append([Paragraph(str(dato[clave]), estiloNormal) for clave in claves])
            
        return nuevosDatos
        
    def Exportar(self):
        """Exportar los datos a un archivo PDF."""
        self.ancho, self.alto = letter

        convertirDatos = self.convertirDatos()
    
        tabla = Table(convertirDatos, colWidths=(self.ancho-112)/len(self.cabecera), hAlign="CENTER")
        tabla.setStyle(TableStyle([
            ("BACKGROUND", (0, 0),(-1, 0), green),
            ("ALIGN", (0, 0),(0, -1), "LEFT"),
            ("VALIGN", (0, 0), (-1, -1), "MIDDLE"), # Texto centrado y alineado a la izquierda
            ("INNERGRID", (0, 0), (-1, -1), 0.50, black), # Lineas internas
            ("BOX", (0, 0), (-1, -1), 0.25, black), # Linea (Marco) externa
            ]))

        historia = []
        historia.append(Paragraph('FRUITEXCO S.A.S', ParagraphStyle(name="centrar", alignment=TA_LEFT, fontSize=10,
                                          leading=12, textColor=black,
                                          fontName="Helvetica-Bold",
                                          parent=self.estilos["Normal"])))
        historia.append(Paragraph('Frutas exóticas colombianas', ParagraphStyle(name="centrar", alignment=TA_LEFT, fontSize=8,
                                          leading=10, textColor=black,
                                          fontName="Helvetica-BoldOblique",
                                          parent=self.estilos["Normal"])))
        historia.append(Paragraph('Dirección: Calle 72 A # 48 56', ParagraphStyle(name="centrar", alignment=TA_LEFT, fontSize=8,
                                          leading=10, textColor=black,
                                          fontName="Helvetica-Oblique",
                                          parent=self.estilos["Normal"])))
        historia.append(Paragraph('Ciudad: Itagüí, Antioquia', ParagraphStyle(name="centrar", alignment=TA_LEFT, fontSize=8,
                                          leading=10, textColor=black,
                                          fontName="Helvetica-Oblique",
                                          parent=self.estilos["Normal"])))
        historia.append(Paragraph('Teléfono: 3113034794', ParagraphStyle(name="centrar", alignment=TA_LEFT, fontSize=8,
                                          leading=10, textColor=black,
                                          fontName="Helvetica-Oblique",
                                          parent=self.estilos["Normal"])))
        historia.append(Spacer(1, 0.16 * inch))
        
        today = date.today()
        
        historia.append(Paragraph('FECHA: ' + today.strftime('%d/%m/%Y') , ParagraphStyle(name="centrar", alignment=TA_LEFT, fontSize=10,
                                          leading=10, textColor=black,
                                          fontName="Helvetica",
                                          parent=self.estilos["Normal"])))
        
        historia.append(Spacer(1, 0.16 * inch))
        
        if(self.titulo == 'FACTURA'):
            historia.append(Paragraph('FACTURA: 000000001' , ParagraphStyle(name="centrar", alignment=TA_LEFT, fontSize=10,
                                            leading=10, textColor=black,
                                            fontName="Helvetica",
                                            parent=self.estilos["Normal"])))
            historia.append(Spacer(1, 0.32 * inch))
        if(self.cliente != None):
            historia.append(Paragraph('INFORMACION CLIENTE' , ParagraphStyle(name="centrar", alignment=TA_CENTER, fontSize=10,
                                            leading=10, textColor=white,
                                            fontName="Helvetica",
                                            parent=self.estilos["Normal"], backColor=green, borderPadding=(5,0,5,0))))
            
            historia.append(Spacer(1, 0.16 * inch))
            
            for dato in self.cliente:
                historia.append(Paragraph(f'{dato}: {self.cliente[dato]}' , ParagraphStyle(name="centrar", alignment=TA_LEFT, fontSize=11,
                                                leading=10, textColor=black,
                                                fontName="Helvetica",
                                                parent=self.estilos["Normal"])))
                historia.append(Spacer(1, 0.16 * inch))
                
        historia.append(Spacer(1, 0.32 * inch))
        
        historia.append(tabla)
        
        if self.total != None:
            tabla2 = Table([["TOTAL", self.total]], colWidths=(self.ancho-112)/2, hAlign="CENTER")
            tabla2.setStyle(TableStyle([
                ("BACKGROUND", (0, 0),(-1, 0), white),
                ("ALIGN", (0, 0),(0, -1), "LEFT"),
                ("VALIGN", (0, 0), (-1, -1), "MIDDLE"), # Texto centrado y alineado a la izquierda
                ("INNERGRID", (0, 0), (-1, -1), 0.50, black), # Lineas internas
                ("BOX", (0, 0), (-1, -1), 0.25, black), # Linea (Marco) externa
                ]))

            historia.append(tabla2)
        
        archivoPDF = SimpleDocTemplate(self.nombrePDF, leftMargin=50, rightMargin=50, pagesize=letter,
                                       title=self.titulo, author="FRUITEXCO SAS")
        
        try:
            archivoPDF.build(historia, canvasmaker=numeracionPaginas)
            
         # +------------------------------------+
            return "Reporte generado con éxito."
         # +------------------------------------+
        except PermissionError:
         # +--------------------------------------------+  
            return "Error inesperado: Permiso denegado."
         # +--------------------------------------------+


# ================== CLASE numeracionPaginas =======================

class numeracionPaginas(canvas.Canvas):
    def __init__(self, *args, **kwargs):
        canvas.Canvas.__init__(self, *args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        """Agregar información de la página a cada página (página x de y)"""
        numeroPaginas = len(self._saved_page_states)
        w, h = letter
        for index, state in enumerate(self._saved_page_states):
            self.__dict__.update(state)
            if index == 0:
                self.drawImage(LOGO, w - 150, h-170, width=100, height=100)
            canvas.Canvas.showPage(self)
        canvas.Canvas.save(self)
 
    def draw_page_number(self, conteoPaginas):
        self.drawRightString(204 * mm, 15 * mm + (0.2 * inch),
                             "Página {} de {}".format(self._pageNumber, conteoPaginas))