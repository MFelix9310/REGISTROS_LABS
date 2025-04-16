from PySide6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QFormLayout,
                              QLabel, QLineEdit, QComboBox, QPushButton,
                              QDateEdit, QTimeEdit, QMessageBox, QFrame,
                              QScrollArea, QGridLayout, QSizePolicy, QTabWidget,
                              QFileDialog, QTableWidget, QTableWidgetItem, QHeaderView)
from PySide6.QtCore import Qt, QDate, QTime
from PySide6.QtGui import QFont

import csv
import datetime

from database.database import get_db
from database.models import Docente, Carrera, Laboratorio, Periodo, RegistroUso

class RegistrosTab(QWidget):
    def __init__(self):
        super().__init__()
        
        # Inicializar atributos de la pestaña de importación CSV
        self.csv_periodo_combo = None
        self.csv_carrera_combo = None
        self.csv_lab_combo = None
        self.csv_docente_combo = None
        self.csv_file_path = None
        self.preview_table = None
        self.selected_file_label = None
        
        self.setup_ui()
        self.load_data()
        
    def setup_ui(self):
        # Layout principal
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.setSpacing(25)
        
        # Header frame con título
        header_frame = QFrame()
        header_frame.setStyleSheet("background-color: #C00; border-radius: 10px;")
        header_frame.setMinimumHeight(120)
        header_layout = QVBoxLayout(header_frame)
        header_layout.setAlignment(Qt.AlignCenter)
        
        # Título del módulo
        title_label = QLabel("Registro de Uso de Laboratorios")
        title_label.setStyleSheet("font-size: 28pt; font-weight: bold; color: white;")
        title_label.setAlignment(Qt.AlignCenter)
        header_layout.addWidget(title_label)
        
        # Subtítulo
        subtitle_label = QLabel("Control de acceso y actividades realizadas")
        subtitle_label.setStyleSheet("font-size: 14pt; color: #eee;")
        subtitle_label.setAlignment(Qt.AlignCenter)
        header_layout.addWidget(subtitle_label)
        
        main_layout.addWidget(header_frame)
        
        # Crear un TabWidget para las subpestañas
        self.tab_widget = QTabWidget()
        main_layout.addWidget(self.tab_widget)
        
        # Crear las subpestañas
        self.registro_manual_tab = QWidget()
        self.importar_csv_tab = QWidget()
        
        # Inicializar los layouts para las subpestañas
        registro_layout = QVBoxLayout(self.registro_manual_tab)
        importar_layout = QVBoxLayout(self.importar_csv_tab)
        
        # Añadir las subpestañas al TabWidget
        self.tab_widget.addTab(self.registro_manual_tab, "Registro Manual")
        self.tab_widget.addTab(self.importar_csv_tab, "Importar desde CSV")
        
        # Configurar las subpestañas después de añadirlas al TabWidget
        self.setup_registro_manual_tab(registro_layout)
        self.setup_importar_csv_tab(importar_layout)
        
    def setup_registro_manual_tab(self, layout):
        # Área de scroll
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setFrameShape(QFrame.NoFrame)
        scroll_area.setStyleSheet("background-color: transparent;")
        
        scroll_content = QWidget()
        scroll_layout = QVBoxLayout(scroll_content)
        scroll_layout.setSpacing(30)
        scroll_layout.setContentsMargins(10, 20, 10, 20)
        
        # Panel de información básica
        info_frame = QFrame()
        info_frame.setStyleSheet("""
            background-color: #292929; 
            border-radius: 15px; 
            padding: 15px;
            border: 1px solid #444;
        """)
        info_layout = QVBoxLayout(info_frame)
        info_layout.setSpacing(20)
        
        # Título de sección
        section_title = QLabel("Información General del Registro")
        section_title.setStyleSheet("color: #C00; font-size: 16pt; font-weight: bold;")
        section_title.setAlignment(Qt.AlignCenter)
        info_layout.addWidget(section_title)
        
        # Descripción
        desc_label = QLabel("Complete la información para registrar el uso del laboratorio")
        desc_label.setStyleSheet("font-size: 12pt; color: #AAA;")
        desc_label.setAlignment(Qt.AlignCenter)
        info_layout.addWidget(desc_label)
        
        # Grid para los campos básicos
        basic_grid = QGridLayout()
        basic_grid.setVerticalSpacing(25)
        basic_grid.setHorizontalSpacing(30)
        basic_grid.setContentsMargins(20, 10, 20, 10)
        
        # Campo de fecha
        fecha_label = QLabel("Fecha:")
        fecha_label.setStyleSheet("font-size: 13pt; color: #DDD; font-weight: bold;")
        basic_grid.addWidget(fecha_label, 0, 0)
        
        self.fecha_edit = QDateEdit()
        self.fecha_edit.setDisplayFormat("dd/MM/yyyy")
        self.fecha_edit.setDate(QDate.currentDate())
        self.fecha_edit.setCalendarPopup(True)
        self.fecha_edit.setStyleSheet("""
            font-size: 13pt;
            padding: 10px;
            border-radius: 8px;
            background-color: #333;
            border: 1px solid #555;
        """)
        self.fecha_edit.setMinimumHeight(45)
        basic_grid.addWidget(self.fecha_edit, 0, 1)
        
        # Selector de período académico
        periodo_label = QLabel("Período Académico:")
        periodo_label.setStyleSheet("font-size: 13pt; color: #DDD; font-weight: bold;")
        basic_grid.addWidget(periodo_label, 1, 0)
        
        self.periodo_combo = QComboBox()
        self.periodo_combo.setStyleSheet("""
            font-size: 13pt;
            padding: 10px;
            border-radius: 8px;
            background-color: #333;
            border: 1px solid #555;
        """)
        self.periodo_combo.setMinimumHeight(45)
        basic_grid.addWidget(self.periodo_combo, 1, 1)
        
        info_layout.addLayout(basic_grid)
        scroll_layout.addWidget(info_frame)
        
        # Panel de selección de laboratorio
        lab_frame = QFrame()
        lab_frame.setStyleSheet("""
            background-color: #292929; 
            border-radius: 15px; 
            padding: 15px;
            border: 1px solid #444;
        """)
        lab_layout = QVBoxLayout(lab_frame)
        lab_layout.setSpacing(20)
        
        # Título de sección
        lab_section_title = QLabel("Ubicación y Docente")
        lab_section_title.setStyleSheet("color: #C00; font-size: 16pt; font-weight: bold;")
        lab_section_title.setAlignment(Qt.AlignCenter)
        lab_layout.addWidget(lab_section_title)
        
        # Grid para carrera, laboratorio y docente
        select_grid = QGridLayout()
        select_grid.setVerticalSpacing(25)
        select_grid.setHorizontalSpacing(30)
        select_grid.setContentsMargins(20, 10, 20, 10)
        
        # Selector de carrera
        carrera_label = QLabel("Carrera:")
        carrera_label.setStyleSheet("font-size: 13pt; color: #DDD; font-weight: bold;")
        select_grid.addWidget(carrera_label, 0, 0)
        
        self.carrera_combo = QComboBox()
        self.carrera_combo.setStyleSheet("""
            font-size: 13pt;
            padding: 10px;
            border-radius: 8px;
            background-color: #333;
            border: 1px solid #555;
        """)
        self.carrera_combo.setMinimumHeight(45)
        select_grid.addWidget(self.carrera_combo, 0, 1)
        
        # Selector de laboratorio
        lab_label = QLabel("Laboratorio:")
        lab_label.setStyleSheet("font-size: 13pt; color: #DDD; font-weight: bold;")
        select_grid.addWidget(lab_label, 1, 0)
        
        self.lab_combo = QComboBox()
        self.lab_combo.setStyleSheet("""
            font-size: 13pt;
            padding: 10px;
            border-radius: 8px;
            background-color: #333;
            border: 1px solid #555;
        """)
        self.lab_combo.setMinimumHeight(45)
        select_grid.addWidget(self.lab_combo, 1, 1)
        
        # Selector de docente
        docente_label = QLabel("Docente:")
        docente_label.setStyleSheet("font-size: 13pt; color: #DDD; font-weight: bold;")
        select_grid.addWidget(docente_label, 2, 0)
        
        self.docente_combo = QComboBox()
        self.docente_combo.setStyleSheet("""
            font-size: 13pt;
            padding: 10px;
            border-radius: 8px;
            background-color: #333;
            border: 1px solid #555;
        """)
        self.docente_combo.setMinimumHeight(45)
        select_grid.addWidget(self.docente_combo, 2, 1)
        
        lab_layout.addLayout(select_grid)
        scroll_layout.addWidget(lab_frame)
        
        # Panel de detalles de actividad
        activity_frame = QFrame()
        activity_frame.setStyleSheet("""
            background-color: #292929; 
            border-radius: 15px; 
            padding: 15px;
            border: 1px solid #444;
        """)
        activity_layout = QVBoxLayout(activity_frame)
        activity_layout.setSpacing(20)
        
        # Título de sección
        activity_title = QLabel("Detalles de la Actividad")
        activity_title.setStyleSheet("color: #C00; font-size: 16pt; font-weight: bold;")
        activity_title.setAlignment(Qt.AlignCenter)
        activity_layout.addWidget(activity_title)
        
        # Campo para actividad
        activity_label = QLabel("Actividad realizada:")
        activity_label.setStyleSheet("font-size: 13pt; color: #DDD; font-weight: bold;")
        activity_layout.addWidget(activity_label)
        
        self.actividad_input = QLineEdit()
        self.actividad_input.setPlaceholderText("Describa la actividad realizada en el laboratorio")
        self.actividad_input.setStyleSheet("""
            font-size: 13pt;
            padding: 10px;
            border-radius: 8px;
            background-color: #333;
            border: 1px solid #555;
        """)
        self.actividad_input.setMinimumHeight(45)
        activity_layout.addWidget(self.actividad_input)
        
        # Horario
        time_layout = QHBoxLayout()
        time_layout.setSpacing(30)
        
        entrada_layout = QVBoxLayout()
        entrada_label = QLabel("Hora de entrada:")
        entrada_label.setStyleSheet("font-size: 13pt; color: #DDD; font-weight: bold;")
        entrada_layout.addWidget(entrada_label)
        
        self.hora_entrada = QTimeEdit()
        self.hora_entrada.setDisplayFormat("HH:mm")
        self.hora_entrada.setTime(QTime(8, 0))
        self.hora_entrada.setStyleSheet("""
            font-size: 13pt;
            padding: 10px;
            border-radius: 8px;
            background-color: #333;
            border: 1px solid #555;
        """)
        self.hora_entrada.setMinimumHeight(45)
        entrada_layout.addWidget(self.hora_entrada)
        
        salida_layout = QVBoxLayout()
        salida_label = QLabel("Hora de salida:")
        salida_label.setStyleSheet("font-size: 13pt; color: #DDD; font-weight: bold;")
        salida_layout.addWidget(salida_label)
        
        self.hora_salida = QTimeEdit()
        self.hora_salida.setDisplayFormat("HH:mm")
        self.hora_salida.setTime(QTime(10, 0))
        self.hora_salida.setStyleSheet("""
            font-size: 13pt;
            padding: 10px;
            border-radius: 8px;
            background-color: #333;
            border: 1px solid #555;
        """)
        self.hora_salida.setMinimumHeight(45)
        salida_layout.addWidget(self.hora_salida)
        
        time_layout.addLayout(entrada_layout)
        time_layout.addLayout(salida_layout)
        
        activity_layout.addLayout(time_layout)
        scroll_layout.addWidget(activity_frame)
        
        # Botones
        buttons_layout = QHBoxLayout()
        buttons_layout.setSpacing(20)
        buttons_layout.setContentsMargins(20, 10, 20, 20)
        
        self.clear_btn = QPushButton("Limpiar Formulario")
        self.clear_btn.setStyleSheet("""
            background-color: #333;
            color: white;
            font-size: 13pt;
            padding: 12px 25px;
            border-radius: 8px;
            border: 1px solid #555;
        """)
        self.clear_btn.setMinimumHeight(50)
        self.clear_btn.clicked.connect(self.clear_form)
        buttons_layout.addWidget(self.clear_btn)
        
        buttons_layout.addStretch()
        
        self.save_btn = QPushButton("  Guardar Registro  ")
        self.save_btn.setStyleSheet("""
            background-color: #C00;
            color: white;
            font-size: 14pt;
            font-weight: bold;
            padding: 15px 30px;
            border-radius: 8px;
        """)
        self.save_btn.setMinimumHeight(50)
        self.save_btn.clicked.connect(self.save_registro)
        buttons_layout.addWidget(self.save_btn)
        
        scroll_layout.addLayout(buttons_layout)
        scroll_layout.addStretch()
        
        scroll_area.setWidget(scroll_content)
        self.registro_manual_tab.layout().addWidget(scroll_area)
        
        # Conectar señales
        self.carrera_combo.currentIndexChanged.connect(self.update_laboratorios)
        self.lab_combo.currentIndexChanged.connect(self.update_docentes)
        self.carrera_combo.currentIndexChanged.connect(self.update_docentes)  # También al cambiar carrera
        
        # Después de crear todos los combos:
        # Evitar que los combos cambien con el scroll del mouse
        self.carrera_combo.wheelEvent = self.ignore_wheel_event
        self.lab_combo.wheelEvent = self.ignore_wheel_event
        self.docente_combo.wheelEvent = self.ignore_wheel_event
        self.periodo_combo.wheelEvent = self.ignore_wheel_event
        # Añadir protección a los campos de hora:
        self.hora_entrada.wheelEvent = self.ignore_wheel_event
        self.hora_salida.wheelEvent = self.ignore_wheel_event
        # Añadir protección al campo de fecha:
        self.fecha_edit.wheelEvent = self.ignore_wheel_event
        
    def load_data(self):
        """Carga los datos iniciales en los selectores"""
        db = get_db()
        
        # Cargar carreras en ambas pestañas
        carreras = db.query(Carrera).all()
        for carrera in carreras:
            self.carrera_combo.addItem(carrera.nombre, carrera.id)
            if self.csv_carrera_combo:
                self.csv_carrera_combo.addItem(carrera.nombre, carrera.id)
        
        # Cargar períodos como función separada
        self.load_periodos()
        
        # Inicializar otros selectores
        self.update_laboratorios()
        self.update_docentes()
        
        # Actualizar los selectores de la pestaña de importación CSV si ya existen
        if all([self.csv_carrera_combo, self.csv_lab_combo, self.csv_docente_combo]):
            self.csv_update_laboratorios()
            self.csv_update_docentes()
        
    def load_periodos(self):
        """Carga los períodos académicos en el combo"""
        # Guardar el período seleccionado actualmente (si hay)
        selected_id = self.periodo_combo.currentData()
        
        # Limpiar y recargar
        self.periodo_combo.clear()
        if self.csv_periodo_combo:
            self.csv_periodo_combo.clear()
        
        db = get_db()
        periodos = db.query(Periodo).all()
        for periodo in periodos:
            self.periodo_combo.addItem(periodo.nombre, periodo.id)
            if self.csv_periodo_combo:
                self.csv_periodo_combo.addItem(periodo.nombre, periodo.id)
        
        # Intentar restaurar la selección anterior
        if selected_id:
            for i in range(self.periodo_combo.count()):
                if self.periodo_combo.itemData(i) == selected_id:
                    self.periodo_combo.setCurrentIndex(i)
                    break
        
    def update_laboratorios(self):
        """Actualiza la lista de laboratorios según la carrera seleccionada"""
        self.lab_combo.clear()
        
        carrera_id = self.carrera_combo.currentData()
        if not carrera_id:
            return
            
        db = get_db()
        labs = db.query(Laboratorio).filter(Laboratorio.carrera_id == carrera_id).all()
        
        for lab in labs:
            self.lab_combo.addItem(lab.nombre, lab.id)
    
    def update_docentes(self):
        """Actualiza la lista de docentes según la carrera y laboratorio seleccionados"""
        self.docente_combo.clear()
        
        carrera_id = self.carrera_combo.currentData()
        lab_id = self.lab_combo.currentData()
        
        if not carrera_id or not lab_id:
            return
            
        db = get_db()
        
        try:
            # Consulta mejorada para obtener docentes que pertenecen a la carrera 
            # y tienen asignado el laboratorio seleccionado
            docentes = db.query(Docente)\
                .filter(Docente.carrera_id == carrera_id)\
                .join(Docente.laboratorios)\
                .filter(Laboratorio.id == lab_id)\
                .all()
            
            # Mostrar mensaje si no hay docentes asignados
            if not docentes:
                self.docente_combo.addItem("No hay docentes asignados a este laboratorio", None)
                print(f"No se encontraron docentes para carrera_id={carrera_id} y lab_id={lab_id}")
            else:
                # Añadir los docentes encontrados al combo
                for docente in docentes:
                    display_name = f"{docente.nombre} {docente.apellido}"
                    self.docente_combo.addItem(display_name, docente.id)
                    print(f"Añadido docente: {display_name}")
        
        except Exception as e:
            print(f"Error al buscar docentes: {str(e)}")
            self.docente_combo.addItem("Error al cargar docentes", None)
    
    def save_registro(self):
        """Guarda el registro de uso en la base de datos"""
        try:
            fecha = self.fecha_edit.date().toPython()
            hora_entrada = self.hora_entrada.time().toPython()
            hora_salida = self.hora_salida.time().toPython()
            actividad = self.actividad_input.text().strip()
            periodo_id = self.periodo_combo.currentData()
            carrera_id = self.carrera_combo.currentData()
            lab_id = self.lab_combo.currentData()
            docente_id = self.docente_combo.currentData()
            
            # Validaciones
            if not periodo_id:
                QMessageBox.warning(self, "Datos incompletos", "Por favor seleccione un período académico.")
                return
                
            # NUEVA VALIDACIÓN: Verificar que la fecha está dentro del período académico
            db = get_db()
            periodo = db.query(Periodo).get(periodo_id)
            if periodo and (fecha < periodo.fecha_inicio or fecha > periodo.fecha_fin):
                QMessageBox.warning(self, "Fecha inválida", 
                                   f"La fecha seleccionada ({fecha.strftime('%d/%m/%Y')}) no está dentro del período académico "
                                   f"'{periodo.nombre}' ({periodo.fecha_inicio.strftime('%d/%m/%Y')} - {periodo.fecha_fin.strftime('%d/%m/%Y')}).")
                return
                
            if not carrera_id:
                QMessageBox.warning(self, "Datos incompletos", "Por favor seleccione una carrera.")
                return
                
            if not lab_id:
                QMessageBox.warning(self, "Datos incompletos", "Por favor seleccione un laboratorio.")
                return
                
            if not docente_id:
                QMessageBox.warning(self, "Datos incompletos", "Por favor seleccione un docente.")
                return
                
            if not actividad:
                QMessageBox.warning(self, "Datos incompletos", "Por favor ingrese la actividad realizada.")
                return
                
            if hora_entrada >= hora_salida:
                QMessageBox.warning(self, "Horario inválido", "La hora de entrada debe ser anterior a la hora de salida.")
                return
            
            # Guardar en la base de datos
            db = get_db()
            nuevo_registro = RegistroUso(
                fecha=fecha,
                hora_entrada=hora_entrada,
                hora_salida=hora_salida,
                actividad=actividad,
                docente_id=docente_id,
                laboratorio_id=lab_id,
                periodo_id=periodo_id
            )
            db.add(nuevo_registro)
            db.commit()
            
            QMessageBox.information(self, "Éxito", "Registro guardado correctamente.")
            self.clear_form()
            
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Ocurrió un error al guardar el registro: {str(e)}")
        
    def clear_form(self):
        """Limpia parcialmente el formulario"""
        self.fecha_edit.setDate(QDate.currentDate())
        self.actividad_input.clear()
        self.hora_entrada.setTime(QTime(8, 0))
        self.hora_salida.setTime(QTime(10, 0))
    
    def ignore_wheel_event(self, event):
        """Ignora eventos de rueda de mouse para evitar cambios accidentales"""
        event.ignore()

    def setup_importar_csv_tab(self, layout):
        # Header frame con título (similar a otras pestañas)
        header_frame = QFrame()
        header_frame.setStyleSheet("background-color: #C00; border-radius: 10px;")
        header_frame.setMinimumHeight(120)
        header_layout = QVBoxLayout(header_frame)
        header_layout.setAlignment(Qt.AlignCenter)
        
        # Título del módulo
        title_label = QLabel("Importación CSV")
        title_label.setStyleSheet("font-size: 28pt; font-weight: bold; color: white;")
        title_label.setAlignment(Qt.AlignCenter)
        header_layout.addWidget(title_label)
        
        # Subtítulo
        subtitle_label = QLabel("Importar registros desde archivo CSV")
        subtitle_label.setStyleSheet("font-size: 14pt; color: #eee;")
        subtitle_label.setAlignment(Qt.AlignCenter)
        header_layout.addWidget(subtitle_label)
        
        layout.addWidget(header_frame)
        
        # Área de scroll para contenido
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setFrameShape(QFrame.NoFrame)
        scroll_area.setStyleSheet("background-color: transparent;")
        
        scroll_content = QWidget()
        scroll_layout = QVBoxLayout(scroll_content)
        scroll_layout.setSpacing(30)
        scroll_layout.setContentsMargins(10, 20, 10, 20)
        
        # Panel de información
        info_frame = QFrame()
        info_frame.setStyleSheet("""
            background-color: #292929; 
            border-radius: 15px; 
            padding: 20px;
        """)
        info_layout = QVBoxLayout(info_frame)
        info_layout.setSpacing(20)
        
        # Instrucciones
        instrucciones_frame = QFrame()
        instrucciones_frame.setStyleSheet("""
            background-color: #333; 
            border-radius: 10px; 
            padding: 15px;
            border: 1px solid #444;
        """)
        instrucciones_layout = QVBoxLayout(instrucciones_frame)
        
        instrucciones_title = QLabel("Formato del Archivo CSV")
        instrucciones_title.setStyleSheet("font-size: 16pt; font-weight: bold; color: white; margin-bottom: 10px;")
        instrucciones_layout.addWidget(instrucciones_title)
        
        instrucciones_text = QLabel(
            "El archivo CSV debe contener las siguientes columnas en este orden:\n"
            "• <b>actividad</b>: Descripción de la actividad realizada\n"
            "• <b>fecha</b>: En formato DD/MM/YYYY (ej. 15/05/2023)\n"
            "• <b>hora_entrada</b>: En formato HH:MM (ej. 08:30)\n"
            "• <b>hora_salida</b>: En formato HH:MM (ej. 10:30)"
        )
        instrucciones_text.setStyleSheet("font-size: 13pt; color: #ddd; line-height: 1.5;")
        instrucciones_text.setWordWrap(True)
        instrucciones_layout.addWidget(instrucciones_text)
        
        info_layout.addWidget(instrucciones_frame)
        
        # Panel de selección de datos
        datos_frame = QFrame()
        datos_frame.setStyleSheet("""
            background-color: #333; 
            border-radius: 10px; 
            padding: 15px;
            border: 1px solid #444;
        """)
        datos_layout = QVBoxLayout(datos_frame)
        
        datos_title = QLabel("Asignación de Datos")
        datos_title.setStyleSheet("font-size: 16pt; font-weight: bold; color: white; margin-bottom: 10px;")
        datos_layout.addWidget(datos_title)
        
        datos_subtitle = QLabel("Seleccione el período, carrera, laboratorio y docente al que se asignarán los registros importados:")
        datos_subtitle.setStyleSheet("font-size: 13pt; color: #ddd; margin-bottom: 15px;")
        datos_subtitle.setWordWrap(True)
        datos_layout.addWidget(datos_subtitle)
        
        # Formulario para seleccionar datos
        form_layout = QFormLayout()
        form_layout.setSpacing(15)
        form_layout.setFieldGrowthPolicy(QFormLayout.AllNonFixedFieldsGrow)
        form_layout.setLabelAlignment(Qt.AlignRight)
        
        form_label_style = "font-size: 13pt; color: #fff; font-weight: bold; padding-right: 15px;"
        combo_style = """
            padding: 10px;
            font-size: 13pt;
            background-color: #3a3a3a;
            color: white;
            border-radius: 8px;
            border: 1px solid #555;
            min-height: 45px;
        """
        
        # Combo para Período
        periodo_label = QLabel("Período:")
        periodo_label.setStyleSheet(form_label_style)
        self.csv_periodo_combo = QComboBox()
        self.csv_periodo_combo.setStyleSheet(combo_style)
        self.csv_periodo_combo.setMinimumWidth(350)
        form_layout.addRow(periodo_label, self.csv_periodo_combo)
        
        # Combo para Carrera
        carrera_label = QLabel("Carrera:")
        carrera_label.setStyleSheet(form_label_style)
        self.csv_carrera_combo = QComboBox()
        self.csv_carrera_combo.setStyleSheet(combo_style)
        self.csv_carrera_combo.currentIndexChanged.connect(self.csv_update_laboratorios)
        self.csv_carrera_combo.currentIndexChanged.connect(self.csv_update_docentes)
        form_layout.addRow(carrera_label, self.csv_carrera_combo)
        
        # Combo para Laboratorio
        lab_label = QLabel("Laboratorio:")
        lab_label.setStyleSheet(form_label_style)
        self.csv_lab_combo = QComboBox()
        self.csv_lab_combo.setStyleSheet(combo_style)
        form_layout.addRow(lab_label, self.csv_lab_combo)
        
        # Combo para Docente
        docente_label = QLabel("Docente:")
        docente_label.setStyleSheet(form_label_style)
        self.csv_docente_combo = QComboBox()
        self.csv_docente_combo.setStyleSheet(combo_style)
        form_layout.addRow(docente_label, self.csv_docente_combo)
        
        datos_layout.addLayout(form_layout)
        info_layout.addWidget(datos_frame)
        
        # Panel para selección e importación
        import_frame = QFrame()
        import_frame.setStyleSheet("""
            background-color: #333; 
            border-radius: 10px; 
            padding: 15px;
            border: 1px solid #444;
        """)
        import_layout = QVBoxLayout(import_frame)
        
        import_title = QLabel("Selección e Importación")
        import_title.setStyleSheet("font-size: 16pt; font-weight: bold; color: white; margin-bottom: 10px;")
        import_layout.addWidget(import_title)
        
        # Botones para seleccionar archivo y para importar
        buttons_layout = QHBoxLayout()
        buttons_layout.setSpacing(20)
        
        self.select_file_btn = QPushButton("Seleccionar archivo CSV")
        self.select_file_btn.setStyleSheet("""
            QPushButton {
                background-color: #444;
                color: white;
                border-radius: 8px;
                padding: 12px 25px;
                font-size: 13pt;
                border: 1px solid #555;
            }
            QPushButton:hover {
                background-color: #555;
            }
        """)
        self.select_file_btn.setMinimumHeight(50)
        self.select_file_btn.clicked.connect(self.select_csv_file)
        buttons_layout.addWidget(self.select_file_btn)
        
        buttons_layout.addStretch()
        
        self.import_btn = QPushButton("  Importar Registros  ")
        self.import_btn.setStyleSheet("""
            QPushButton {
                background-color: #C00;
                color: white;
                border-radius: 8px;
                padding: 15px 30px;
                font-size: 14pt;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #D00;
            }
            QPushButton:disabled {
                background-color: #888;
                color: #ccc;
            }
        """)
        self.import_btn.setMinimumHeight(50)
        self.import_btn.clicked.connect(self.import_csv_data)
        self.import_btn.setEnabled(False)
        buttons_layout.addWidget(self.import_btn)
        
        import_layout.addLayout(buttons_layout)
        
        # Etiqueta de archivo seleccionado
        self.selected_file_label = QLabel("Ningún archivo seleccionado")
        self.selected_file_label.setStyleSheet("font-size: 12pt; color: #aaa; margin-top: 10px;")
        self.selected_file_label.setAlignment(Qt.AlignCenter)
        import_layout.addWidget(self.selected_file_label)
        
        info_layout.addWidget(import_frame)
        
        # Vista previa de datos
        preview_frame = QFrame()
        preview_frame.setStyleSheet("""
            background-color: #333; 
            border-radius: 10px; 
            padding: 15px;
            border: 1px solid #444;
        """)
        preview_layout = QVBoxLayout(preview_frame)
        
        preview_title = QLabel("Vista Previa del Archivo")
        preview_title.setStyleSheet("font-size: 16pt; font-weight: bold; color: white; margin-bottom: 10px;")
        preview_layout.addWidget(preview_title)
        
        self.preview_table = QTableWidget()
        self.preview_table.setStyleSheet("""
            QTableWidget {
                background-color: #3a3a3a;
                color: white;
                gridline-color: #555;
                border: none;
                border-radius: 8px;
                padding: 5px;
            }
            QHeaderView::section {
                background-color: #C00;
                color: white;
                padding: 8px;
                border: none;
                font-weight: bold;
                font-size: 12pt;
            }
            QTableWidget::item {
                padding: 8px;
                border-bottom: 1px solid #555;
            }
        """)
        self.preview_table.setMinimumHeight(250)
        self.preview_table.horizontalHeader().setStretchLastSection(True)
        self.preview_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.preview_table.verticalHeader().setVisible(False)
        preview_layout.addWidget(self.preview_table)
        
        info_layout.addWidget(preview_frame)
        
        # Añadir todo al layout principal
        scroll_layout.addWidget(info_frame)
        scroll_layout.addStretch()
        
        scroll_area.setWidget(scroll_content)
        layout.addWidget(scroll_area)
        
        # Evitar que los combos cambien con el scroll del mouse
        self.csv_periodo_combo.wheelEvent = self.ignore_wheel_event
        self.csv_carrera_combo.wheelEvent = self.ignore_wheel_event
        self.csv_lab_combo.wheelEvent = self.ignore_wheel_event
        self.csv_docente_combo.wheelEvent = self.ignore_wheel_event

    def csv_update_laboratorios(self):
        if not self.csv_lab_combo or not self.csv_carrera_combo:
            return
            
        self.csv_lab_combo.clear()
        
        session = get_db()
        try:
            carrera_id = self.csv_carrera_combo.currentData()
            if carrera_id:
                laboratorios = session.query(Laboratorio).filter_by(carrera_id=carrera_id).all()
                for lab in laboratorios:
                    self.csv_lab_combo.addItem(lab.nombre, lab.id)
        finally:
            session.close()
            
    def csv_update_docentes(self):
        if not self.csv_docente_combo or not self.csv_carrera_combo:
            return
            
        self.csv_docente_combo.clear()
        
        session = get_db()
        try:
            carrera_id = self.csv_carrera_combo.currentData()
            if carrera_id:
                docentes = session.query(Docente).filter_by(carrera_id=carrera_id).all()
                for docente in docentes:
                    self.csv_docente_combo.addItem(f"{docente.nombre} {docente.apellido}", docente.id)
        finally:
            session.close()

    def select_csv_file(self):
        file_dialog = QFileDialog()
        file_path, _ = file_dialog.getOpenFileName(
            self, 
            "Seleccionar archivo CSV", 
            "", 
            "CSV Files (*.csv)"
        )
        
        if file_path:
            self.csv_file_path = file_path
            self.import_btn.setEnabled(True)
            self.load_csv_preview(file_path)
            
            # Actualizar etiqueta con el nombre del archivo seleccionado
            file_name = file_path.split("/")[-1]
            self.selected_file_label.setText(f"Archivo seleccionado: {file_name}")
            self.selected_file_label.setStyleSheet("font-size: 12pt; color: #4CAF50; margin-top: 10px; font-weight: bold;")
    
    def load_csv_preview(self, file_path):
        try:
            with open(file_path, 'r', encoding='utf-8') as csv_file:
                csv_reader = csv.reader(csv_file)
                header = next(csv_reader)  # Leer el encabezado
                
                # Configurar la tabla de vista previa
                self.preview_table.setRowCount(0)
                self.preview_table.setColumnCount(len(header))
                self.preview_table.setHorizontalHeaderLabels(header)
                
                # Mostrar hasta 10 filas para la vista previa
                for i, row in enumerate(csv_reader):
                    if i >= 10:  # Limitar a 10 filas para la vista previa
                        break
                    
                    # Añadir fila a la tabla
                    self.preview_table.insertRow(i)
                    for j, cell in enumerate(row):
                        self.preview_table.setItem(i, j, QTableWidgetItem(cell))
                
                # Ajustar tamaños de columnas
                self.preview_table.resizeColumnsToContents()
                
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error al leer archivo CSV: {str(e)}")
    
    def import_csv_data(self):
        if not self.csv_file_path:
            QMessageBox.warning(self, "Advertencia", "Por favor seleccione un archivo CSV primero.")
            return
        
        # Obtener los valores seleccionados
        periodo_id = self.csv_periodo_combo.currentData()
        laboratorio_id = self.csv_lab_combo.currentData()
        docente_id = self.csv_docente_combo.currentData()
        
        if not periodo_id or not laboratorio_id or not docente_id:
            QMessageBox.warning(self, "Datos incompletos", "Por favor seleccione período, laboratorio y docente.")
            return
        
        try:
            total_importados = 0
            with open(self.csv_file_path, 'r', encoding='utf-8') as csv_file:
                csv_reader = csv.reader(csv_file)
                next(csv_reader)  # Saltar encabezado
                
                session = get_db()
                try:
                    for row in csv_reader:
                        if len(row) < 4:  # Verificar que haya suficientes columnas
                            continue
                        
                        actividad, fecha_str, hora_entrada_str, hora_salida_str = row
                        
                        # Convertir fecha (formato esperado: DD/MM/YYYY)
                        try:
                            fecha_obj = datetime.datetime.strptime(fecha_str.strip(), "%d/%m/%Y").date()
                        except ValueError:
                            continue  # Saltar si la fecha no es válida
                        
                        # Convertir horas (formato esperado: HH:MM)
                        try:
                            hora_entrada_obj = datetime.datetime.strptime(hora_entrada_str.strip(), "%H:%M").time()
                            hora_salida_obj = datetime.datetime.strptime(hora_salida_str.strip(), "%H:%M").time()
                        except ValueError:
                            continue  # Saltar si las horas no son válidas
                        
                        # Crear nuevo registro
                        nuevo_registro = RegistroUso(
                            actividad=actividad.strip(),
                            fecha=fecha_obj,
                            hora_entrada=hora_entrada_obj,
                            hora_salida=hora_salida_obj,
                            docente_id=docente_id,
                            laboratorio_id=laboratorio_id,
                            periodo_id=periodo_id
                        )
                        
                        session.add(nuevo_registro)
                        total_importados += 1
                    
                    session.commit()
                    QMessageBox.information(self, "Importación exitosa", 
                                          f"Se importaron {total_importados} registros correctamente.")
                except Exception as e:
                    session.rollback()
                    QMessageBox.critical(self, "Error", f"Error al importar datos: {str(e)}")
                finally:
                    session.close()
                    
                # Limpiar después de importar
                self.csv_file_path = None
                self.import_btn.setEnabled(False)
                self.preview_table.setRowCount(0)
                self.preview_table.setColumnCount(0)
                
                # Restablecer etiqueta de archivo seleccionado
                self.selected_file_label.setText("Ningún archivo seleccionado")
                self.selected_file_label.setStyleSheet("font-size: 12pt; color: #aaa; margin-top: 10px;")
                
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error al procesar archivo CSV: {str(e)}") 