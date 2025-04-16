from PySide6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QFormLayout,
                              QLabel, QComboBox, QPushButton, QTableWidget,
                              QTableWidgetItem, QHeaderView, QFileDialog, QMessageBox)
from PySide6.QtCore import Qt, QDir, QRectF, QUrl
from PySide6.QtGui import QPainter, QPageLayout, QPixmap, QFont, QPen, QPageSize, QDesktopServices
from PySide6.QtPrintSupport import QPrinter, QPrintDialog, QPrintPreviewDialog
from datetime import datetime

from database.database import get_db
from database.models import Docente, Carrera, Laboratorio, Periodo, RegistroUso

class VisualizacionTab(QWidget):
    def __init__(self):
        super().__init__()
        self.setup_ui()
        self.load_data()
        
    def setup_ui(self):
        # Layout principal
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(20, 20, 20, 20)
        
        # Título del módulo
        title_label = QLabel("Visualización y Reportes")
        title_label.setStyleSheet("font-size: 18pt; font-weight: bold;")
        main_layout.addWidget(title_label)
        
        # Filtros
        filter_layout = QHBoxLayout()
        
        # Selector de período
        periodo_form = QFormLayout()
        self.periodo_combo = QComboBox()
        self.periodo_combo.addItem("-- Todos --", None)
        periodo_form.addRow("Período:", self.periodo_combo)
        filter_layout.addLayout(periodo_form)
        
        # Selector de carrera
        carrera_form = QFormLayout()
        self.carrera_combo = QComboBox()
        self.carrera_combo.addItem("-- Todas --", None)
        carrera_form.addRow("Carrera:", self.carrera_combo)
        filter_layout.addLayout(carrera_form)
        
        # Selector de laboratorio
        lab_form = QFormLayout()
        self.lab_combo = QComboBox()
        self.lab_combo.addItem("-- Todos --", None)
        lab_form.addRow("Laboratorio:", self.lab_combo)
        filter_layout.addLayout(lab_form)
        
        # Selector de docente
        docente_form = QFormLayout()
        self.docente_combo = QComboBox()
        self.docente_combo.addItem("-- Todos --", None)
        docente_form.addRow("Docente:", self.docente_combo)
        filter_layout.addLayout(docente_form)
        
        # Botón de filtrado
        self.filter_btn = QPushButton("Filtrar")
        self.filter_btn.clicked.connect(self.filter_data)
        filter_layout.addWidget(self.filter_btn, alignment=Qt.AlignBottom)
        
        main_layout.addLayout(filter_layout)
        
        # Etiqueta para mostrar el número de registros
        self.status_label = QLabel("")
        self.status_label.setStyleSheet("font-style: italic;")
        main_layout.addWidget(self.status_label)
        
        # Tabla de resultados - Configurar para permitir selección de filas
        self.results_table = QTableWidget()
        self.results_table.setColumnCount(5)
        self.results_table.setHorizontalHeaderLabels(["Docente", "Actividad", "Hora Entrada", "Hora Salida", "Fecha"])
        self.results_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.results_table.setSelectionBehavior(QTableWidget.SelectRows)  # Seleccionar filas completas
        self.results_table.setSelectionMode(QTableWidget.ExtendedSelection)  # Permitir selección múltiple
        main_layout.addWidget(self.results_table)
        
        # Botón para imprimir
        self.print_btn = QPushButton("Imprimir PDF")
        self.print_btn.setStyleSheet("font-size: 12pt; padding: 8px;")
        
        # Botones de acción en un layout horizontal
        buttons_layout = QHBoxLayout()
        
        # Botón para eliminar registros seleccionados
        self.delete_btn = QPushButton("Eliminar Registros Seleccionados")
        self.delete_btn.setStyleSheet("""
            QPushButton {
                background-color: #d9534f;
                color: white;
                font-size: 12pt; 
                padding: 8px 12px;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #c9302c;
            }
        """)
        self.delete_btn.clicked.connect(self.delete_selected_records)
        buttons_layout.addWidget(self.delete_btn)
        
        # Espacio flexible
        buttons_layout.addStretch()
        
        # Añadir el botón de imprimir al layout de botones
        buttons_layout.addWidget(self.print_btn)
        
        # Añadir el layout de botones al layout principal
        main_layout.addLayout(buttons_layout)
        
        # Conectar señales
        self.carrera_combo.currentIndexChanged.connect(self.update_laboratorios)
        
        # Evitar que los combos cambien con el scroll del mouse
        if hasattr(self, 'periodo_combo'):
            self.periodo_combo.wheelEvent = self.ignore_wheel_event
        if hasattr(self, 'carrera_combo'):
            self.carrera_combo.wheelEvent = self.ignore_wheel_event
        if hasattr(self, 'lab_combo'):
            self.lab_combo.wheelEvent = self.ignore_wheel_event
        if hasattr(self, 'docente_combo'):
            self.docente_combo.wheelEvent = self.ignore_wheel_event
        
        # Conectar el botón de imprimir a la función
        self.print_btn.clicked.connect(self.print_report)
        
    def load_data(self):
        """Carga los datos iniciales en los combos"""
        try:
            db = get_db()
            
            # Cargar períodos
            self.periodo_combo.clear()
            self.periodo_combo.addItem("-- Todos --", None)
            periodos = db.query(Periodo).all()
            for periodo in periodos:
                self.periodo_combo.addItem(periodo.nombre, periodo.id)
            
            # Cargar carreras
            self.carrera_combo.clear()
            self.carrera_combo.addItem("-- Todas --", None)
            carreras = db.query(Carrera).all()
            for carrera in carreras:
                self.carrera_combo.addItem(carrera.nombre, carrera.id)
            
            # Cargar los laboratorios (evitando duplicados manualmente)
            self.lab_combo.clear()
            self.lab_combo.addItem("-- Todos --", None)
            lab_names = set()  # Conjunto para verificar duplicados
            labs = db.query(Laboratorio).all()
            for lab in labs:
                if lab.nombre not in lab_names:
                    self.lab_combo.addItem(lab.nombre, lab.id)
                    lab_names.add(lab.nombre)
            
            # Cargar todos los docentes
            self.docente_combo.clear()
            self.docente_combo.addItem("-- Todos --", None)
            docentes = db.query(Docente).all()
            for docente in docentes:
                nombre_completo = f"{docente.nombre} {docente.apellido}" if docente.apellido else docente.nombre
                self.docente_combo.addItem(nombre_completo, docente.id)
            
            # Mostrar todos los registros al inicio
            self.filter_data()
        except Exception as e:
            print(f"Error al cargar datos iniciales: {e}")
            import traceback
            traceback.print_exc()
    
    def update_laboratorios(self):
        """Actualiza la lista de laboratorios según la carrera seleccionada"""
        try:
            # Guardar el item seleccionado actual (si existe)
            current_lab_name = self.lab_combo.currentText() if self.lab_combo.currentIndex() >= 0 else None
            
            # Limpiar el combo
            self.lab_combo.clear()
            self.lab_combo.addItem("-- Todos --", None)
            
            carrera_id = self.carrera_combo.currentData()
            
            db = get_db()
            
            # Conjunto para controlar nombres únicos
            lab_names = set()
            
            # Obtener laboratorios según la carrera seleccionada
            if carrera_id:
                query = db.query(Laboratorio).filter(Laboratorio.carrera_id == carrera_id)
            else:
                query = db.query(Laboratorio)
            
            labs = query.all()
            
            # Añadir laboratorios sin duplicados
            for lab in labs:
                if lab.nombre not in lab_names:
                    self.lab_combo.addItem(lab.nombre, lab.id)
                    lab_names.add(lab.nombre)
            
            # Intentar restaurar la selección anterior
            if current_lab_name:
                index = self.lab_combo.findText(current_lab_name)
                if index >= 0:
                    self.lab_combo.setCurrentIndex(index)
        
        except Exception as e:
            print(f"Error al actualizar laboratorios: {e}")
            import traceback
            traceback.print_exc()
    
    def filter_data(self):
        """Filtra los datos según los criterios seleccionados"""
        try:
            # Obtener criterios de filtro
            docente_id = self.docente_combo.currentData()
            periodo_id = self.periodo_combo.currentData()
            laboratorio_id = self.lab_combo.currentData()
            carrera_id = self.carrera_combo.currentData()
            
            db = get_db()
            
            # Construir la consulta base
            query = db.query(RegistroUso)
            
            # Filtrar por docente si está seleccionado
            if docente_id:
                query = query.filter(RegistroUso.docente_id == docente_id)
            
            # Filtrar por laboratorio si está seleccionado
            if laboratorio_id:
                query = query.filter(RegistroUso.laboratorio_id == laboratorio_id)
            # Si no hay laboratorio específico pero hay carrera seleccionada, filtrar por laboratorios de esa carrera
            elif carrera_id:
                # Obtener todos los laboratorios de la carrera
                labs_carrera = db.query(Laboratorio.id).filter(Laboratorio.carrera_id == carrera_id).all()
                lab_ids = [lab[0] for lab in labs_carrera]
                
                if lab_ids:  # Solo aplicar el filtro si hay laboratorios en esta carrera
                    query = query.filter(RegistroUso.laboratorio_id.in_(lab_ids))
            
            # Filtrar por período si está seleccionado
            if periodo_id:
                # Obtener las fechas del período
                periodo = db.query(Periodo).filter(Periodo.id == periodo_id).first()
                if periodo and hasattr(periodo, 'fecha_inicio') and hasattr(periodo, 'fecha_fin'):
                    # Filtrar por el rango de fechas del período
                    query = query.filter(RegistroUso.fecha.between(periodo.fecha_inicio, periodo.fecha_fin))
            
            # Añadir joins para poder acceder a propiedades relacionadas
            query = query.join(Docente, RegistroUso.docente_id == Docente.id)
            query = query.join(Laboratorio, RegistroUso.laboratorio_id == Laboratorio.id)
            
            # Ordenar por fecha descendente (más reciente primero)
            query = query.order_by(RegistroUso.fecha.desc(), RegistroUso.hora_entrada.desc())
            
            # Obtener registros con límite para evitar sobrecarga
            registros = query.limit(1000).all()
            
            # Actualizar tabla
            self.results_table.setRowCount(0)  # Limpiar tabla
            
            # Guardar los IDs de los registros para poder eliminarlos más tarde
            self.registro_ids = []
            
            for i, registro in enumerate(registros):
                self.results_table.insertRow(i)
                
                # Guardar el ID del registro para usar en la eliminación
                self.registro_ids.append(registro.id)
                
                # Docente
                docente_nombre = f"{registro.docente.nombre} {registro.docente.apellido}" if registro.docente else ""
                self.results_table.setItem(i, 0, QTableWidgetItem(docente_nombre))
                
                # Actividad
                self.results_table.setItem(i, 1, QTableWidgetItem(registro.actividad or ""))
                
                # Hora entrada
                hora_entrada = registro.hora_entrada.strftime("%H:%M") if registro.hora_entrada else ""
                self.results_table.setItem(i, 2, QTableWidgetItem(hora_entrada))
                
                # Hora salida
                hora_salida = registro.hora_salida.strftime("%H:%M") if registro.hora_salida else ""
                self.results_table.setItem(i, 3, QTableWidgetItem(hora_salida))
                
                # Fecha
                fecha = registro.fecha.strftime("%d/%m/%Y") if registro.fecha else ""
                self.results_table.setItem(i, 4, QTableWidgetItem(fecha))
            
            # Actualizar el label de estado con el número de registros
            if len(registros) == 1000:
                self.status_label.setText(f"Se encontraron más de 1000 registros. Mostrando los 1000 más recientes.")
            else:
                self.status_label.setText(f"Se encontraron {len(registros)} registros.")
            
        except Exception as e:
            print(f"Error al filtrar datos: {str(e)}")
            # Intentar obtener una traza de la excepción para diagnóstico
            import traceback
            traceback.print_exc()
    
    def ignore_wheel_event(self, event):
        """Ignora eventos de rueda de mouse para evitar cambios accidentales"""
        event.ignore()

    def load_periodos(self):
        """Carga los períodos académicos en el combo"""
        # Guardar el período seleccionado actualmente (si hay)
        selected_id = self.periodo_combo.currentData()
        
        # Limpiar y recargar
        self.periodo_combo.clear()
        self.periodo_combo.addItem("-- Todos --", None)
        
        db = get_db()
        periodos = db.query(Periodo).all()
        for periodo in periodos:
            self.periodo_combo.addItem(periodo.nombre, periodo.id)
        
        # Intentar restaurar la selección anterior
        if selected_id:
            for i in range(self.periodo_combo.count()):
                if self.periodo_combo.itemData(i) == selected_id:
                    self.periodo_combo.setCurrentIndex(i)
                    break 

    def print_report(self):
        """Imprime el reporte en PDF con formato de tabla mejorado"""
        try:
            printer = QPrinter(QPrinter.HighResolution)
            printer.setPageSize(QPageSize(QPageSize.A4))
            printer.setPageOrientation(QPageLayout.Landscape)
            printer.setOutputFormat(QPrinter.PdfFormat)
            
            file_dialog = QFileDialog()
            file_path, _ = file_dialog.getSaveFileName(
                self, 
                "Guardar Reporte PDF", 
                QDir.homePath() + "/reporte_laboratorio.pdf", 
                "PDF (*.pdf)"
            )
            
            if not file_path:
                return
            
            printer.setOutputFileName(file_path)
            
            # Obtener registros de la tabla filtrada
            registros_filtrados = []
            for row in range(self.results_table.rowCount()):
                docente = self.results_table.item(row, 0).text() if self.results_table.item(row, 0) else ""
                actividad = self.results_table.item(row, 1).text() if self.results_table.item(row, 1) else ""
                hora_entrada = self.results_table.item(row, 2).text() if self.results_table.item(row, 2) else ""
                hora_salida = self.results_table.item(row, 3).text() if self.results_table.item(row, 3) else ""
                fecha = self.results_table.item(row, 4).text() if self.results_table.item(row, 4) else ""
                
                registros_filtrados.append({
                    'docente': docente,
                    'actividad': actividad,
                    'hora_entrada': hora_entrada,
                    'hora_salida': hora_salida,
                    'fecha': fecha
                })
            
            # Ordenar registros por fecha (de más antigua a más reciente)
            registros_filtrados.sort(key=lambda x: datetime.strptime(x['fecha'], "%d/%m/%Y"))
            
            # Calcular número de páginas necesarias
            registros_por_pagina = 9  # Aumentado de 7 a 9 celdas por página
            total_paginas = max(1, (len(registros_filtrados) + registros_por_pagina - 1) // registros_por_pagina)
            
            # Iniciar el painter
            painter = QPainter()
            if not painter.begin(printer):
                QMessageBox.critical(self, "Error", "No se pudo iniciar la impresión.")
                return
            
            try:
                for pagina_actual in range(total_paginas):
                    # Si no es la primera página, comenzar una nueva
                    if pagina_actual > 0:
                        printer.newPage()
                    
                    # Obtener medidas de página - CORRECCIÓN DEL ERROR
                    page_rect = printer.pageRect(QPrinter.DevicePixel)
                    page_width = page_rect.width()
                    
                    # ===== TÍTULOS CENTRADOS =====
                    # Título principal
                    painter.setFont(QFont("Cambria", 16, QFont.Bold))
                    
                    title = "ESCUELA SUPERIOR POLITÉCNICA DE CHIMBORAZO"
                    title_metrics = painter.fontMetrics()
                    title_width = title_metrics.horizontalAdvance(title)
                    title_x = (page_width - title_width) / 2
                    title_y = 250
                    
                    painter.drawText(int(title_x), title_y, title)
                    
                    # Definir espaciado vertical constante para todo el documento
                    vertical_spacing = 300  # Usar el mismo espaciado en todo el documento
                    
                    # Subtítulo - Facultad
                    painter.setFont(QFont("Cambria", 14, QFont.Bold))
                    
                    subtitle = "FACULTAD DE MECÁNICA"
                    subtitle_metrics = painter.fontMetrics()
                    subtitle_width = subtitle_metrics.horizontalAdvance(subtitle)
                    subtitle_x = (page_width - subtitle_width) / 2
                    subtitle_y = title_y + vertical_spacing
                    
                    painter.drawText(int(subtitle_x), subtitle_y, subtitle)
                    
                    # Tercer título - Laboratorio
                    painter.setFont(QFont("Cambria", 12, QFont.Bold))
                    
                    lab_name = "N/A"  # Valor por defecto cambiado de "METROLOGÍA" a "N/A"
                    if self.lab_combo.currentText() != "-- Todos --":
                        lab_name = self.lab_combo.currentText().upper()
                        
                    lab_title = f"LABORATORIO DE {lab_name}"
                    lab_metrics = painter.fontMetrics()
                    lab_width = lab_metrics.horizontalAdvance(lab_title)
                    lab_x = (page_width - lab_width) / 2
                    lab_y = subtitle_y + vertical_spacing
                    
                    painter.drawText(int(lab_x), lab_y, lab_title)
                    
                    # ===== MARGEN IZQUIERDO FIJO EN 12CM =====
                    left_margin = 460  # 12cm desde el borde izquierdo
                    
                    # ===== PERÍODO =====
                    periodo_y = lab_y + vertical_spacing + 152 + 228  # Posición del período
                    
                    # "PERÍODO:" en negrita y cursiva
                    font_periodo_label = QFont("Cambria", 11)
                    font_periodo_label.setBold(True)
                    font_periodo_label.setItalic(True)
                    painter.setFont(font_periodo_label)
                    
                    # Dibujar "PERÍODO:" con margen izquierdo ajustado
                    painter.drawText(left_margin, periodo_y, "PERÍODO:")
                    
                    # Medir el ancho de "PERÍODO:" para posicionar el valor
                    label_width = painter.fontMetrics().horizontalAdvance("PERÍODO:")
                    
                    # Configurar fuente para el valor del período (solo cursiva)
                    font_periodo_valor = QFont("Cambria", 11)
                    font_periodo_valor.setItalic(True)
                    font_periodo_valor.setBold(False)
                    painter.setFont(font_periodo_valor)
                    
                    # Obtener el período seleccionado
                    periodo_texto = "N/A"
                    if self.periodo_combo.currentText() != "-- Todos --":
                        periodo_texto = self.periodo_combo.currentText()
                    
                    # Dibujar el valor del período con DOS ESPACIOS adicionales
                    espacio_width = painter.fontMetrics().horizontalAdvance("  ")
                    
                    # Dibujar el valor con los dos espacios adicionales
                    painter.drawText(left_margin + label_width + espacio_width, periodo_y, periodo_texto)
                    
                    # ===== DOCENTE (después de período con el mismo espaciado) =====
                    docente_y = periodo_y + vertical_spacing  # Mismo espaciado que entre títulos
                    
                    # Resetear completamente el painter para eliminar cualquier efecto residual
                    painter.resetTransform()
                    painter.save()
                    painter.restore()
                    painter.setPen(QPen(Qt.black))
                    painter.setBrush(Qt.NoBrush)
                    
                    # "DOCENTE:" en negrita y cursiva (mismo formato que PERÍODO)
                    font_docente_label = QFont("Cambria", 11)
                    font_docente_label.setBold(True)
                    font_docente_label.setItalic(True)
                    painter.setFont(font_docente_label)
                    
                    # Limpiar cualquier efecto de renderizado previo
                    painter.setOpacity(1.0)
                    painter.setCompositionMode(QPainter.CompositionMode_SourceOver)
                    
                    # Dibujar "DOCENTE:" con el mismo margen izquierdo
                    painter.drawText(left_margin, docente_y, "DOCENTE:")
                    
                    # Medir el ancho de "DOCENTE:" para posicionar el valor
                    docente_label_width = painter.fontMetrics().horizontalAdvance("DOCENTE:")
                    
                    # Configurar fuente para el valor del docente (solo cursiva)
                    font_docente_valor = QFont("Cambria", 11)
                    font_docente_valor.setItalic(True)
                    font_docente_valor.setBold(False)
                    painter.setFont(font_docente_valor)
                    
                    # Obtener el docente seleccionado
                    docente_texto = "N/A"
                    if self.docente_combo.currentText() != "-- Todos --":
                        docente_texto = f"Ing. {self.docente_combo.currentText()}"
                    
                    # Dibujar el valor del docente con DOS ESPACIOS adicionales
                    painter.drawText(left_margin + docente_label_width + espacio_width, docente_y, docente_texto)
                    
                    # ===== CARRERA (después de docente con el mismo espaciado) =====
                    carrera_y = docente_y + vertical_spacing  # Mismo espaciado que entre los campos anteriores
                    
                    # "CARRERA:" en negrita y cursiva (mismo formato que PERÍODO y DOCENTE)
                    font_carrera_label = QFont("Cambria", 11)
                    font_carrera_label.setBold(True)
                    font_carrera_label.setItalic(True)
                    painter.setFont(font_carrera_label)
                    
                    # Dibujar "CARRERA:" con el mismo margen izquierdo
                    painter.drawText(left_margin, carrera_y, "CARRERA:")
                    
                    # Medir el ancho de "CARRERA:" para posicionar el valor
                    carrera_label_width = painter.fontMetrics().horizontalAdvance("CARRERA:")
                    
                    # Configurar fuente para el valor de la carrera (solo cursiva)
                    font_carrera_valor = QFont("Cambria", 11)
                    font_carrera_valor.setItalic(True)
                    font_carrera_valor.setBold(False)
                    painter.setFont(font_carrera_valor)
                    
                    # Obtener la carrera seleccionada
                    carrera_texto = "N/A"
                    if self.carrera_combo.currentText() != "-- Todas --":
                        carrera_texto = self.carrera_combo.currentText()
                    
                    # Dibujar el valor de la carrera con DOS ESPACIOS adicionales
                    painter.drawText(left_margin + carrera_label_width + espacio_width, carrera_y, carrera_texto)
                    
                    # ===== TABLA DE REGISTROS =====
                    # Posición inicial de la tabla (después de la información de carrera)
                    table_y = carrera_y + 200  # 200px después de carrera
                    
                    # Asegurar que cualquier configuración anterior no afecte nuestro dibujo
                    painter.resetTransform()
                    painter.setPen(QPen(Qt.black, 1, Qt.SolidLine))
                    
                    # Calcular anchos de columna (proporcional al contenido típico)
                    table_left = 80  # 2cm desde el borde izquierdo
                    table_width = page_width - table_left - 80  # Ancho hasta el margen derecho
                    
                    col_widths = [
                        int(table_width * 0.35),  # Actividades (35%)
                        int(table_width * 0.15),  # Fecha (15%)
                        int(table_width * 0.15),  # Hora Entrada (15%)
                        int(table_width * 0.15),  # Hora Salida (15%)
                        int(table_width * 0.20)   # Firma (20%)
                    ]
                    
                    # Altura de la fila de encabezados
                    header_height = 456  # 12cm (para encabezados)
                    
                    # Altura de las filas de datos
                    data_row_height = 532  # 14cm (para filas de datos)
                    
                    # Obtener registros para esta página
                    inicio_rango = pagina_actual * registros_por_pagina
                    fin_rango = min(inicio_rango + registros_por_pagina, len(registros_filtrados))
                    registros_pagina = registros_filtrados[inicio_rango:fin_rango]
                    
                    # Número de filas de datos en esta página (máximo 9)
                    num_filas_datos = len(registros_pagina)
                    # Si no hay registros, mostramos una fila vacía
                    if num_filas_datos == 0:
                        num_filas_datos = 1
                    
                    # Altura total de la tabla (encabezado + filas de datos)
                    table_height = header_height + (data_row_height * num_filas_datos)
                    
                    # Dibujar el borde exterior de toda la tabla
                    painter.setPen(QPen(Qt.black, 2))  # Borde exterior más grueso
                    painter.drawRect(table_left, table_y, table_width, table_height)
                    
                    # Volver al trazo normal para las líneas interiores
                    painter.setPen(QPen(Qt.black, 1))
                    
                    # ===== 1. DIBUJAR FILA DE ENCABEZADOS =====
                    header_texts = ["Actividades", "Fecha", "Hora Entrada", "Hora Salida", "Firma"]
                    
                    # Fuente para encabezados
                    header_font = QFont("Cambria", 12)
                    header_font.setBold(True)
                    painter.setFont(header_font)
                    
                    # Dibujar fila de encabezados
                    x_pos = table_left
                    for i, col_width in enumerate(col_widths):
                        # Dibujar fondo gris para encabezados
                        painter.setBrush(Qt.lightGray)
                        painter.drawRect(x_pos, table_y, col_width, header_height)
                        painter.setBrush(Qt.NoBrush)
                        
                        # Centrar texto en la celda
                        header = header_texts[i]
                        fm = painter.fontMetrics()
                        text_width = fm.horizontalAdvance(header)
                        text_height = fm.height()
                        
                        # Centrado normal para todas las columnas
                        text_x = x_pos + (col_width - text_width) / 2
                        text_y = table_y + (header_height / 2) + (text_height / 2) - fm.descent()
                        painter.drawText(int(text_x), int(text_y), header)
                        
                        x_pos += col_width
                    
                    # Dibujar línea horizontal separando encabezados de datos
                    painter.drawLine(table_left, table_y + header_height, 
                                    table_left + table_width, table_y + header_height)
                    
                    # ===== 2. DIBUJAR FILAS DE DATOS (14cm cada una) =====
                    # Fuente para datos
                    data_font = QFont("Cambria", 11)
                    painter.setFont(data_font)
                    
                    # Dibujar cada fila de datos o celdas vacías
                    for fila in range(num_filas_datos):
                        # Posición Y de esta fila de datos
                        fila_y = table_y + header_height + (fila * data_row_height)
                        
                        # Dibujar celdas de esta fila
                        x_pos = table_left
                        for col, col_width in enumerate(col_widths):
                            # Dibujar borde de celda
                            painter.drawRect(x_pos, fila_y, col_width, data_row_height)
                            
                            # Si hay datos para esta celda, mostrarlos
                            if fila < len(registros_pagina):
                                registro = registros_pagina[fila]
                                
                                if col == 0:  # Actividad
                                    texto = registro['actividad']
                                    # Alineado a la izquierda con ajuste de texto automático
                                    if texto:
                                        # Crear un rectángulo donde dibujar el texto con margen
                                        text_rect = QRectF(x_pos + 10, fila_y + 10, col_width - 20, data_row_height - 20)
                                        # Dibujar texto con ajuste automático
                                        painter.drawText(text_rect, Qt.AlignLeft | Qt.AlignVCenter | Qt.TextWordWrap, texto)
                                
                                elif col == 1:  # Fecha
                                    texto = registro['fecha'] if 'fecha' in registro else ""
                                    # Centrada
                                    if texto:
                                        fm = painter.fontMetrics()
                                        text_width = fm.horizontalAdvance(texto)
                                        text_height = fm.height()
                                        text_x = x_pos + (col_width - text_width) / 2
                                        text_y = fila_y + (data_row_height / 2) + (text_height / 2) - fm.descent()
                                        painter.drawText(int(text_x), int(text_y), texto)
                                
                                elif col == 2:  # Hora Entrada
                                    texto = registro['hora_entrada']
                                    # Centrada
                                    if texto:
                                        fm = painter.fontMetrics()
                                        text_width = fm.horizontalAdvance(texto)
                                        text_height = fm.height()
                                        text_x = x_pos + (col_width - text_width) / 2
                                        text_y = fila_y + (data_row_height / 2) + (text_height / 2) - fm.descent()
                                        painter.drawText(int(text_x), int(text_y), texto)
                                
                                elif col == 3:  # Hora Salida
                                    texto = registro['hora_salida']
                                    # Centrada
                                    if texto:
                                        fm = painter.fontMetrics()
                                        text_width = fm.horizontalAdvance(texto)
                                        text_height = fm.height()
                                        text_x = x_pos + (col_width - text_width) / 2
                                        text_y = fila_y + (data_row_height / 2) + (text_height / 2) - fm.descent()
                                        painter.drawText(int(text_x), int(text_y), texto)
                            
                            # Avanzar a la siguiente columna
                            x_pos += col_width
                        
                        # Dibujar líneas verticales para todas las columnas
                        x_acumulado = table_left
                        for i in range(len(col_widths) - 1):
                            x_acumulado += col_widths[i]
                            painter.drawLine(x_acumulado, table_y, 
                                            x_acumulado, table_y + table_height)
                        
                    # ===== FIRMA DEL TÉCNICO EN LA PARTE INFERIOR =====
                    # Posición base desde la parte inferior (para el cargo)
                    bottom_margin = page_rect.height() - 608  # 16cm desde abajo

                    # Posición del nombre del técnico (6cm más arriba que el cargo)
                    nombre_y = bottom_margin - 228  # 6cm = 228px

                    # Fuente para el nombre del técnico
                    firma_font = QFont("Cambria", 11)
                    firma_font.setBold(True)
                    painter.setFont(firma_font)

                    # Dibujar el nombre del técnico centrado más arriba
                    nombre_tecnico = "Ing. Félix Ruiz M."
                    nombre_width = painter.fontMetrics().horizontalAdvance(nombre_tecnico)
                    nombre_x = (page_width - nombre_width) / 2
                    painter.drawText(int(nombre_x), nombre_y, nombre_tecnico)

                    # Fuente para el cargo (sin negrita)
                    cargo_font = QFont("Cambria", 11)
                    painter.setFont(cargo_font)

                    # Dibujar el cargo centrado en su posición original
                    cargo_tecnico = "Técnico de Laboratorio"
                    cargo_width = painter.fontMetrics().horizontalAdvance(cargo_tecnico)
                    cargo_x = (page_width - cargo_width) / 2
                    cargo_y = bottom_margin + 40  # Mantener posición original
                    painter.drawText(int(cargo_x), cargo_y, cargo_tecnico)
            
            finally:
                painter.end()
                
            QMessageBox.information(
                self, 
                "PDF Generado", 
                f"El reporte ha sido generado correctamente en {total_paginas} página(s)."
            )
            
            # Abrir automáticamente el PDF generado
            QDesktopServices.openUrl(QUrl.fromLocalFile(file_path))
            
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error al generar el PDF: {str(e)}") 

    def delete_selected_records(self):
        """Elimina los registros seleccionados de la base de datos"""
        try:
            # Obtener las filas seleccionadas
            selected_rows = sorted([index.row() for index in self.results_table.selectedIndexes() if index.column() == 0], reverse=True)
            
            if not selected_rows:
                QMessageBox.information(self, "Información", "No hay registros seleccionados para eliminar.")
                return
            
            # Confirmar la eliminación
            confirmation = QMessageBox.question(
                self,
                "Confirmar eliminación",
                f"¿Está seguro de que desea eliminar {len(set(selected_rows))} registro(s)?",
                QMessageBox.Yes | QMessageBox.No,
                QMessageBox.No
            )
            
            if confirmation == QMessageBox.No:
                return
            
            # Eliminar registros de la base de datos
            db = get_db()
            try:
                deleted_count = 0
                for row in set(selected_rows):
                    # Obtener el ID del registro correspondiente a esta fila
                    if row < len(self.registro_ids):
                        registro_id = self.registro_ids[row]
                        
                        # Eliminar de la base de datos
                        registro = db.query(RegistroUso).filter(RegistroUso.id == registro_id).first()
                        if registro:
                            db.delete(registro)
                            deleted_count += 1
                
                # Confirmar la transacción
                db.commit()
                
                # Mostrar mensaje de éxito
                QMessageBox.information(
                    self,
                    "Eliminación exitosa",
                    f"Se eliminaron {deleted_count} registro(s) correctamente."
                )
                
                # Actualizar la vista
                self.filter_data()
                
            except Exception as e:
                db.rollback()
                QMessageBox.critical(self, "Error", f"Error al eliminar registros: {str(e)}")
            finally:
                db.close()
                
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error durante la eliminación: {str(e)}") 