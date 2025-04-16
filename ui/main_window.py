from PySide6.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QTabWidget, QApplication
from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QPalette, QColor

from .docentes_tab import DocentesTab
from .periodos_tab import PeriodosTab
from .registros_tab import RegistrosTab
from .visualizacion_tab import VisualizacionTab

class MainWindow(QMainWindow):
    # Añadir esta señal para comunicar entre pestañas
    refresh_periodos_signal = Signal()
    
    def __init__(self):
        super().__init__()
        
        # Configurar la ventana principal
        self.setWindowTitle("Sistema de Gestión de Laboratorios")
        self.setMinimumSize(1024, 768)
        self.showMaximized()
        
        # Aplicar estilos
        self.apply_styles()
        
        # Widget central y layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)
        
        # Configurar el TabWidget para las pestañas a la izquierda
        self.tab_widget = QTabWidget()
        self.tab_widget.setTabPosition(QTabWidget.West)
        main_layout.addWidget(self.tab_widget)
        
        # Conectar la señal a la actualización de períodos
        self.refresh_periodos_signal.connect(self.update_periodos_in_tabs)
        
        # Añadir las pestañas para cada módulo - CAMBIO DE ORDEN
        self.periodos_tab = PeriodosTab(self)
        self.docentes_tab = DocentesTab()
        self.registros_tab = RegistrosTab()
        self.visualizacion_tab = VisualizacionTab()
        
        # Añadir pestañas en el nuevo orden
        self.tab_widget.addTab(self.periodos_tab, "Períodos Académicos")
        self.tab_widget.addTab(self.docentes_tab, "Gestión de Docentes")
        self.tab_widget.addTab(self.registros_tab, "Registro de Uso")
        self.tab_widget.addTab(self.visualizacion_tab, "Visualización")
        
        # Estilo específico para las pestañas
        self.tab_widget.setStyleSheet("""
            QTabBar::tab {
                background-color: #222;
                color: white;
                padding: 10px 20px;
                margin: 2px;
                border-radius: 5px;
            }
            QTabBar::tab:selected {
                background-color: #C00;
                font-weight: bold;
            }
            QTabBar::tab:hover {
                background-color: #600;
            }
        """)
    
    def apply_styles(self):
        """Aplica un tema de colores rojo y negro a toda la aplicación"""
        # Crear una paleta personalizada para la aplicación
        app = QApplication.instance()
        
        # Estilo general con CSS
        app.setStyleSheet("""
            QMainWindow, QWidget {
                background-color: #1a1a1a;
                color: white;
            }
            
            QLabel {
                color: white;
            }
            
            QLineEdit, QDateEdit, QTimeEdit, QComboBox {
                background-color: #2a2a2a;
                color: white;
                border: 1px solid #C00;
                border-radius: 4px;
                padding: 5px;
                min-height: 25px;
            }
            
            QComboBox::drop-down {
                border: 0px;
            }
            
            QComboBox::down-arrow {
                image: url(down_arrow.png);
                width: 14px;
                height: 14px;
            }
            
            QPushButton {
                background-color: #C00;
                color: white;
                font-weight: bold;
                border: none;
                border-radius: 4px;
                padding: 8px 16px;
            }
            
            QPushButton:hover {
                background-color: #F00;
            }
            
            QPushButton:pressed {
                background-color: #900;
            }
            
            QTableWidget {
                background-color: #2a2a2a;
                color: white;
                gridline-color: #444;
                selection-background-color: #C00;
            }
            
            QHeaderView::section {
                background-color: #333;
                color: white;
                padding: 5px;
                border: 1px solid #444;
                font-weight: bold;
            }
            
            QScrollBar:vertical {
                border: none;
                background: #2a2a2a;
                width: 14px;
                margin: 15px 0 15px 0;
            }
            
            QScrollBar::handle:vertical {
                background: #C00;
                min-height: 30px;
                border-radius: 7px;
            }
            
            QScrollBar::add-line:vertical {
                border: none;
                background: none;
                height: 15px;
                subcontrol-position: bottom;
                subcontrol-origin: margin;
            }
            
            QScrollBar::sub-line:vertical {
                border: none;
                background: none;
                height: 15px;
                subcontrol-position: top;
                subcontrol-origin: margin;
            }
            
            QListWidget {
                background-color: #2a2a2a;
                color: white;
                border: 1px solid #C00;
                border-radius: 4px;
            }
            
            QListWidget::item:selected {
                background-color: #C00;
            }
        """) 
    
    def update_periodos_in_tabs(self):
        """Actualiza los períodos académicos en todas las pestañas que los usan"""
        # Actualizar en la pestaña de Registro
        if hasattr(self, "registros_tab"):
            self.registros_tab.load_periodos()
        
        # Actualizar en la pestaña de Visualización si es necesario
        if hasattr(self, "visualizacion_tab"):
            if hasattr(self.visualizacion_tab, "load_periodos"):
                self.visualizacion_tab.load_periodos() 