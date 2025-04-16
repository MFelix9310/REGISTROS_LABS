import sys
from PySide6.QtWidgets import QApplication

from database.database import engine
from database.models import Base
from ui.main_window import MainWindow

def main():
    # Crear tablas en la base de datos
    Base.metadata.create_all(bind=engine)
    
    # Iniciar la aplicación
    app = QApplication(sys.argv)
    app.setApplicationName("REGISTROS_LABORATORIOS")
    window = MainWindow()
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main() 