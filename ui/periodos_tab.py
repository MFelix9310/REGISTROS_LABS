from PySide6.QtWidgets import (QWidget, QVBoxLayout, QFormLayout, QHBoxLayout,
                              QLabel, QLineEdit, QPushButton,
                              QMessageBox, QDateEdit, QFrame)
from PySide6.QtCore import Qt, QDate

from database.database import get_db
from database.models import Periodo

class PeriodosTab(QWidget):
    def __init__(self, main_window=None):
        super().__init__()
        self.main_window = main_window
        self.setup_ui()
        
    def setup_ui(self):
        # Layout principal
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.setSpacing(20)
        
        # Header frame con título
        header_frame = QFrame()
        header_frame.setStyleSheet("background-color: #C00; border-radius: 10px;")
        header_layout = QVBoxLayout(header_frame)
        
        # Título del módulo
        title_label = QLabel("Gestión de Períodos Académicos")
        title_label.setStyleSheet("font-size: 24pt; font-weight: bold; color: white; padding: 15px;")
        title_label.setAlignment(Qt.AlignCenter)
        header_layout.addWidget(title_label)
        
        main_layout.addWidget(header_frame)
        
        # Frame para el formulario
        form_frame = QFrame()
        form_frame.setStyleSheet("background-color: #292929; border-radius: 10px; padding: 20px;")
        form_layout = QVBoxLayout(form_frame)
        
        # Descripción
        desc_label = QLabel("Configure los períodos académicos para el registro de actividades")
        desc_label.setStyleSheet("font-size: 14pt; color: #CCC; margin-bottom: 15px;")
        form_layout.addWidget(desc_label)
        
        # Formulario con mejor diseño
        input_layout = QFormLayout()
        input_layout.setSpacing(15)
        input_layout.setLabelAlignment(Qt.AlignRight)
        
        # Nombre del período con estilo mejorado
        self.nombre_input = QLineEdit()
        self.nombre_input.setPlaceholderText("Ej: Primer Semestre 2023")
        self.nombre_input.setStyleSheet("font-size: 12pt;")
        input_layout.addRow("Nombre del período:", self.nombre_input)
        
        # Fechas de inicio y fin
        date_layout = QHBoxLayout()
        date_layout.setSpacing(20)
        
        fecha_inicio_layout = QVBoxLayout()
        fecha_inicio_label = QLabel("Fecha de inicio:")
        fecha_inicio_layout.addWidget(fecha_inicio_label)
        
        self.fecha_inicio = QDateEdit()
        self.fecha_inicio.setDisplayFormat("dd/MM/yyyy")
        self.fecha_inicio.setDate(QDate.currentDate())
        self.fecha_inicio.setCalendarPopup(True)
        self.fecha_inicio.setStyleSheet("font-size: 12pt;")
        fecha_inicio_layout.addWidget(self.fecha_inicio)
        
        fecha_fin_layout = QVBoxLayout()
        fecha_fin_label = QLabel("Fecha de finalización:")
        fecha_fin_layout.addWidget(fecha_fin_label)
        
        self.fecha_fin = QDateEdit()
        self.fecha_fin.setDisplayFormat("dd/MM/yyyy")
        self.fecha_fin.setDate(QDate.currentDate().addMonths(6))
        self.fecha_fin.setCalendarPopup(True)
        self.fecha_fin.setStyleSheet("font-size: 12pt;")
        fecha_fin_layout.addWidget(self.fecha_fin)
        
        date_layout.addLayout(fecha_inicio_layout)
        date_layout.addLayout(fecha_fin_layout)
        
        form_layout.addLayout(input_layout)
        form_layout.addSpacing(20)
        form_layout.addLayout(date_layout)
        
        main_layout.addWidget(form_frame)
        
        # Botones
        button_layout = QHBoxLayout()
        
        self.clear_btn = QPushButton("Limpiar Formulario")
        self.clear_btn.setStyleSheet("""
            background-color: #333;
            color: white;
            font-size: 12pt;
            padding: 10px 20px;
        """)
        self.clear_btn.clicked.connect(self.clear_form)
        button_layout.addWidget(self.clear_btn)
        
        button_layout.addStretch()
        
        self.save_btn = QPushButton("Guardar Período")
        self.save_btn.setStyleSheet("""
            background-color: #C00;
            color: white;
            font-size: 14pt;
            font-weight: bold;
            padding: 12px 25px;
            border-radius: 8px;
        """)
        self.save_btn.clicked.connect(self.save_periodo)
        button_layout.addWidget(self.save_btn)
        
        main_layout.addLayout(button_layout)
        main_layout.addStretch()
        
        # Evitar que los DateEdit cambien con el scroll del mouse
        self.fecha_inicio.wheelEvent = self.ignore_wheel_event
        self.fecha_fin.wheelEvent = self.ignore_wheel_event
        
    def save_periodo(self):
        """Guarda el período académico en la base de datos"""
        nombre = self.nombre_input.text().strip()
        fecha_inicio = self.fecha_inicio.date().toPython()
        fecha_fin = self.fecha_fin.date().toPython()
        
        if not nombre:
            QMessageBox.warning(self, "Datos incompletos", "Por favor ingrese el nombre del período.")
            return
            
        if fecha_inicio > fecha_fin:
            QMessageBox.warning(self, "Fechas inválidas", "La fecha de inicio debe ser anterior a la fecha de finalización.")
            return
        
        # Guardar en la base de datos
        db = get_db()
        nuevo_periodo = Periodo(
            nombre=nombre,
            fecha_inicio=fecha_inicio,
            fecha_fin=fecha_fin
        )
        db.add(nuevo_periodo)
        db.commit()
        
        # Emitir señal para actualizar otros componentes
        if self.main_window and hasattr(self.main_window, "refresh_periodos_signal"):
            self.main_window.refresh_periodos_signal.emit()
            print("Señal de actualización emitida")
        else:
            print("No se pudo emitir la señal de actualización")
        
        QMessageBox.information(self, "Éxito", "Período académico guardado correctamente.")
        self.clear_form()
        
    def clear_form(self):
        """Limpia el formulario"""
        self.nombre_input.clear()
        self.fecha_inicio.setDate(QDate.currentDate())
        self.fecha_fin.setDate(QDate.currentDate().addMonths(6))
        
    def ignore_wheel_event(self, event):
        """Ignora eventos de rueda de mouse para evitar cambios accidentales"""
        event.ignore() 