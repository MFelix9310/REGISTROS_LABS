"""
Este archivo contiene recursos embebidos para la aplicación como imágenes pequeñas
"""

from PySide6.QtCore import QByteArray, QBuffer, QIODevice
from PySide6.QtGui import QPixmap, QImage

def get_down_arrow():
    """Retorna una flecha hacia abajo como un arreglo de bytes"""
    # Crear una imagen de flecha simple
    img = QImage(14, 14, QImage.Format_ARGB32)
    img.fill(0)
    
    for y in range(0, 7):
        for x in range(7 - y, 7 + y + 1):
            img.setPixelColor(x, y + 3, QColor(255, 255, 255))
    
    # Convertir a bytes
    ba = QByteArray()
    buffer = QBuffer(ba)
    buffer.open(QIODevice.WriteOnly)
    img.save(buffer, "PNG")
    
    return ba 