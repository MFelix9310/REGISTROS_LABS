from PySide6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QFormLayout,
                              QLabel, QLineEdit, QComboBox, QPushButton,
                              QListWidget, QListWidgetItem, QMessageBox, QFrame,
                              QScrollArea, QGridLayout, QSizePolicy)
from PySide6.QtCore import Qt
from PySide6.QtGui import QFont, QIcon

from database.database import get_db
from database.models import Docente, Carrera, Laboratorio

class DocentesTab(QWidget):
    def __init__(self):
        super().__init__()
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
        title_label = QLabel("Gestión de Docentes")
        title_label.setStyleSheet("font-size: 28pt; font-weight: bold; color: white;")
        title_label.setAlignment(Qt.AlignCenter)
        header_layout.addWidget(title_label)
        
        # Subtítulo
        subtitle_label = QLabel("Registro y asignación de laboratorios")
        subtitle_label.setStyleSheet("font-size: 14pt; color: #eee;")
        subtitle_label.setAlignment(Qt.AlignCenter)
        header_layout.addWidget(subtitle_label)
        
        main_layout.addWidget(header_frame)
        
        # Contenedor principal con scroll
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setFrameShape(QFrame.NoFrame)
        scroll_area.setStyleSheet("background-color: transparent;")
        
        scroll_content = QWidget()
        scroll_layout = QVBoxLayout(scroll_content)
        scroll_layout.setSpacing(30)
        scroll_layout.setContentsMargins(10, 20, 10, 20)
        
        # Panel de información personal
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
        section_title = QLabel("Información Personal del Docente")
        section_title.setStyleSheet("color: #C00; font-size: 16pt; font-weight: bold;")
        section_title.setAlignment(Qt.AlignCenter)
        info_layout.addWidget(section_title)
        
        # Grid para los campos de entrada
        input_grid = QGridLayout()
        input_grid.setVerticalSpacing(25)
        input_grid.setHorizontalSpacing(30)
        input_grid.setContentsMargins(20, 10, 20, 10)
        
        # Campos de nombre y apellido con etiquetas mejoradas
        name_label = QLabel("Nombre:")
        name_label.setStyleSheet("font-size: 13pt; color: #DDD; font-weight: bold;")
        input_grid.addWidget(name_label, 0, 0)
        
        self.nombre_input = QLineEdit()
        self.nombre_input.setPlaceholderText("Ingrese el nombre del docente")
        self.nombre_input.setStyleSheet("""
            font-size: 13pt;
            padding: 10px;
            border-radius: 8px;
            background-color: #333;
            border: 1px solid #555;
        """)
        self.nombre_input.setMinimumHeight(45)
        input_grid.addWidget(self.nombre_input, 0, 1)
        
        lastname_label = QLabel("Apellido:")
        lastname_label.setStyleSheet("font-size: 13pt; color: #DDD; font-weight: bold;")
        input_grid.addWidget(lastname_label, 1, 0)
        
        self.apellido_input = QLineEdit()
        self.apellido_input.setPlaceholderText("Ingrese el apellido del docente")
        self.apellido_input.setStyleSheet("""
            font-size: 13pt;
            padding: 10px;
            border-radius: 8px;
            background-color: #333;
            border: 1px solid #555;
        """)
        self.apellido_input.setMinimumHeight(45)
        input_grid.addWidget(self.apellido_input, 1, 1)
        
        carrera_label = QLabel("Carrera:")
        carrera_label.setStyleSheet("font-size: 13pt; color: #DDD; font-weight: bold;")
        input_grid.addWidget(carrera_label, 2, 0)
        
        self.carrera_combo = QComboBox()
        self.carrera_combo.setStyleSheet("""
            font-size: 13pt;
            padding: 10px;
            border-radius: 8px;
            background-color: #333;
            border: 1px solid #555;
            min-width: 250px;
        """)
        self.carrera_combo.setMinimumHeight(45)
        self.carrera_combo.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        input_grid.addWidget(self.carrera_combo, 2, 1)
        
        # Configurar las columnas del grid
        input_grid.setColumnStretch(0, 1)  # Columna de etiquetas
        input_grid.setColumnStretch(1, 3)  # Columna de campos
        
        info_layout.addLayout(input_grid)
        scroll_layout.addWidget(info_frame)
        
        # Panel de asignación de laboratorios
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
        lab_title = QLabel("Asignación de Laboratorios")
        lab_title.setStyleSheet("color: #C00; font-size: 16pt; font-weight: bold;")
        lab_title.setAlignment(Qt.AlignCenter)
        lab_layout.addWidget(lab_title)
        
        # Descripción
        lab_desc = QLabel("Seleccione los laboratorios que el docente utilizará:")
        lab_desc.setStyleSheet("font-size: 12pt; color: #AAA;")
        lab_desc.setAlignment(Qt.AlignCenter)
        lab_layout.addWidget(lab_desc)
        
        # Selector de laboratorio con botón
        lab_select_layout = QHBoxLayout()
        lab_select_layout.setSpacing(15)
        lab_select_layout.setContentsMargins(20, 10, 20, 10)
        
        self.lab_combo = QComboBox()
        self.lab_combo.setStyleSheet("""
            font-size: 13pt;
            padding: 10px;
            border-radius: 8px;
            background-color: #333;
            border: 1px solid #555;
        """)
        self.lab_combo.setMinimumHeight(45)
        lab_select_layout.addWidget(self.lab_combo, 4)
        
        self.lab_add_btn = QPushButton("Añadir Laboratorio")
        self.lab_add_btn.setStyleSheet("""
            font-size: 13pt;
            padding: 10px 20px;
            border-radius: 8px;
            background-color: #900;
            color: white;
            font-weight: bold;
        """)
        self.lab_add_btn.setMinimumHeight(45)
        self.lab_add_btn.clicked.connect(self.add_laboratorio)
        lab_select_layout.addWidget(self.lab_add_btn, 2)
        
        lab_layout.addLayout(lab_select_layout)
        
        # Lista de laboratorios seleccionados
        lab_list_label = QLabel("Laboratorios asignados al docente:")
        lab_list_label.setStyleSheet("font-size: 13pt; color: #DDD; margin-top: 10px;")
        lab_layout.addWidget(lab_list_label)
        
        self.lab_list = QListWidget()
        self.lab_list.setStyleSheet("""
            font-size: 13pt;
            background-color: #333;
            border-radius: 8px;
            padding: 10px;
            border: 1px solid #555;
        """)
        self.lab_list.setMinimumHeight(200)
        lab_layout.addWidget(self.lab_list)
        
        # Instrucciones
        tip_label = QLabel("Nota: Puede añadir múltiples laboratorios a un mismo docente")
        tip_label.setStyleSheet("font-size: 11pt; color: #888; font-style: italic;")
        lab_layout.addWidget(tip_label)
        
        scroll_layout.addWidget(lab_frame)
        
        # Botones de acción
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
        
        self.save_btn = QPushButton("  Guardar Docente  ")
        self.save_btn.setStyleSheet("""
            background-color: #C00;
            color: white;
            font-size: 14pt;
            font-weight: bold;
            padding: 15px 30px;
            border-radius: 8px;
        """)
        self.save_btn.setMinimumHeight(50)
        self.save_btn.clicked.connect(self.save_docente)
        buttons_layout.addWidget(self.save_btn)
        
        scroll_layout.addLayout(buttons_layout)
        
        # Agregar espaciado al final
        scroll_layout.addStretch()
        
        # Configurar el área de desplazamiento
        scroll_area.setWidget(scroll_content)
        main_layout.addWidget(scroll_area)
        
        # Conectar señales
        self.carrera_combo.currentIndexChanged.connect(self.update_laboratorios)
        
        # Evitar que los combos cambien con el scroll del mouse
        self.carrera_combo.wheelEvent = self.ignore_wheel_event
        self.lab_combo.wheelEvent = self.ignore_wheel_event
        
    def load_data(self):
        """Carga los datos iniciales en los combos"""
        db = get_db()
        
        # Cargar carreras
        carreras = db.query(Carrera).all()
        for carrera in carreras:
            self.carrera_combo.addItem(carrera.nombre, carrera.id)
            
        # Si no hay carreras, cargar datos iniciales
        if not carreras:
            self.load_initial_data()
        else:
            # Asegurar que todas las carreras tengan los 4 laboratorios
            self.verify_laboratories()
    
    def load_initial_data(self):
        """Carga los datos iniciales en la base de datos"""
        db = get_db()
        
        # Crear carreras
        carreras = [
            Carrera(nombre="Mecánica"),
            Carrera(nombre="Industrial"),
            Carrera(nombre="Automotriz"),
            Carrera(nombre="Mantenimiento Industrial")
        ]
        db.add_all(carreras)
        db.commit()
        
        # Obtener las carreras con sus IDs asignados
        carreras_db = db.query(Carrera).all()
        
        # Crear los cuatro laboratorios para cada carrera
        laboratorios = []
        for carrera in carreras_db:
            laboratorios.extend([
                Laboratorio(nombre="Resistencia de Materiales", carrera_id=carrera.id),
                Laboratorio(nombre="Turbomaquinaria e Hidráulica", carrera_id=carrera.id),
                Laboratorio(nombre="Metrología", carrera_id=carrera.id),
                Laboratorio(nombre="Instrumentación y Control", carrera_id=carrera.id)
            ])
        
        db.add_all(laboratorios)
        db.commit()
        
        # Recargar datos
        self.carrera_combo.clear()
        carreras = db.query(Carrera).all()
        for carrera in carreras:
            self.carrera_combo.addItem(carrera.nombre, carrera.id)
    
    def verify_laboratories(self):
        """Verifica que todas las carreras tengan los 4 laboratorios y los añade si faltan"""
        db = get_db()
        
        # Nombres de los laboratorios que deben existir para cada carrera
        lab_names = [
            "Resistencia de Materiales", 
            "Turbomaquinaria e Hidráulica", 
            "Metrología", 
            "Instrumentación y Control"
        ]
        
        # Verificar para cada carrera
        carreras = db.query(Carrera).all()
        for carrera in carreras:
            # Obtener laboratorios existentes para esta carrera
            existing_labs = db.query(Laboratorio).filter(
                Laboratorio.carrera_id == carrera.id
            ).all()
            
            # Verificar qué laboratorios faltan
            existing_names = [lab.nombre for lab in existing_labs]
            
            # Añadir los laboratorios que faltan
            labs_to_add = []
            for lab_name in lab_names:
                if lab_name not in existing_names:
                    labs_to_add.append(
                        Laboratorio(nombre=lab_name, carrera_id=carrera.id)
                    )
                    
            if labs_to_add:
                db.add_all(labs_to_add)
                db.commit()
                print(f"Se añadieron {len(labs_to_add)} laboratorios nuevos a la carrera {carrera.nombre}")
    
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
    
    def add_laboratorio(self):
        """Añade un laboratorio a la lista de seleccionados"""
        lab_id = self.lab_combo.currentData()
        lab_name = self.lab_combo.currentText()
        
        if not lab_id:
            return
            
        # Verificar si ya está en la lista
        for i in range(self.lab_list.count()):
            if self.lab_list.item(i).data(Qt.UserRole) == lab_id:
                QMessageBox.information(self, "Información", 
                                        f"El laboratorio '{lab_name}' ya está en la lista.")
                return
                
        # Añadir a la lista
        item = QListWidgetItem(lab_name)
        item.setData(Qt.UserRole, lab_id)
        self.lab_list.addItem(item)
    
    def save_docente(self):
        """Guarda el docente en la base de datos"""
        nombre = self.nombre_input.text().strip()
        apellido = self.apellido_input.text().strip()
        carrera_id = self.carrera_combo.currentData()
        
        if not nombre or not apellido:
            QMessageBox.warning(self, "Datos incompletos", "Por favor ingrese nombre y apellido del docente.")
            return
            
        if self.lab_list.count() == 0:
            QMessageBox.warning(self, "Datos incompletos", "Por favor seleccione al menos un laboratorio.")
            return
        
        # Crear docente
        db = get_db()
        nuevo_docente = Docente(
            nombre=nombre,
            apellido=apellido,
            carrera_id=carrera_id
        )
        db.add(nuevo_docente)
        db.commit()
        
        # Asignar laboratorios
        for i in range(self.lab_list.count()):
            lab_id = self.lab_list.item(i).data(Qt.UserRole)
            lab = db.query(Laboratorio).get(lab_id)
            nuevo_docente.laboratorios.append(lab)
        
        db.commit()
        
        QMessageBox.information(self, "Éxito", f"Docente {nombre} {apellido} guardado correctamente.")
        self.clear_form()
        
    def clear_form(self):
        """Limpia el formulario"""
        self.nombre_input.clear()
        self.apellido_input.clear()
        self.lab_list.clear()
    
    def ignore_wheel_event(self, event):
        """Ignora eventos de rueda de mouse para evitar cambios accidentales"""
        event.ignore() 