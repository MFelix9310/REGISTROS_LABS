# Sistema de Gestión de Registros de Laboratorios UAGRO

![Logo UAGRO](https://via.placeholder.com/150x50)

Un sistema completo de gestión para el registro, seguimiento y análisis del uso de laboratorios universitarios. Desarrollado con Python, PySide6 y SQLAlchemy, esta aplicación proporciona una solución integral para administrar la ocupación de laboratorios, docentes y estudiantes en entornos universitarios.

## 📋 Características

### Gestión de Periodos Académicos
- Creación y administración de periodos académicos
- Configuración de fechas de inicio y fin
- Estado activo/inactivo de periodos

### Catálogo de Docentes
- Registro completo de información de docentes
- Asignación de docentes a carreras específicas
- Búsqueda y filtrado por nombre, apellido o carrera

### Administración de Laboratorios
- Registro de laboratorios por carrera
- Configuración de capacidad y características
- Categorización por tipo y uso

### Registro de Ocupación
- **Registro Manual**: Ingreso detallado de uso de laboratorios
  - Fecha y hora de entrada/salida
  - Cantidad de estudiantes
  - Asignatura
  - Propósito del uso
  - Observaciones
  
- **Importación desde CSV**: Carga masiva de registros
  - Mapeo flexible de columnas
  - Validación de datos
  - Resolución de conflictos

### Visualización y Análisis
- Consulta de registros históricos
- Filtrado por múltiples criterios (periodo, docente, laboratorio, fechas)
- Estadísticas de uso y ocupación
- Exportación de datos para análisis externos
- Eliminación de registros con confirmación

## 🔧 Requisitos del Sistema

- Windows 7/8/10/11 (64-bit)
- Python 3.8 o superior
- 4GB RAM mínimo recomendado
- 100MB de espacio en disco para la aplicación
- Espacio adicional para la base de datos (dependiendo del volumen de registros)

## 📥 Instalación

### Desde el Código Fuente

1. **Clona el repositorio**
   ```bash
   git clone https://github.com/tuusuario/registros-laboratorios.git
   cd registros-laboratorios
   ```

2. **Crea un entorno virtual**
   ```bash
   python -m venv venv
   ```

3. **Activa el entorno virtual**
   - Windows:
     ```bash
     venv\Scripts\activate
     ```
   - Linux/Mac:
     ```bash
     source venv/bin/activate
     ```

4. **Instala las dependencias**
   ```bash
   pip install -r requirements.txt
   ```

5. **Ejecuta la aplicación**
   ```bash
   python main.py
   ```

### Usando el Instalador (Para Usuarios Finales)

1. Descarga el último instalador desde la sección de releases
2. Ejecuta el archivo `RegistrosLaboratorios_Setup.exe`
3. Sigue las instrucciones del asistente de instalación
4. La aplicación estará disponible en el menú de inicio y opcionalmente en el escritorio

## 📝 Guía de Uso

### Primeros Pasos

1. **Configuración Inicial**
   - Al iniciar por primera vez, establece al menos un periodo académico
   - Registra las carreras relevantes para tu institución
   - Configura los laboratorios disponibles

2. **Registro de Docentes**
   - Ingresa la información de los docentes que utilizarán los laboratorios
   - Asigna los docentes a sus respectivas carreras

3. **Registro de Uso**
   - Selecciona el método de registro (manual o importación CSV)
   - Completa todos los campos requeridos
   - Guarda los registros

### Visualización y Reportes

1. Navega a la pestaña "Visualización"
2. Utiliza los filtros para definir el conjunto de datos que deseas analizar
3. Consulta la tabla de resultados
4. Para eliminar registros, selecciona las filas y utiliza el botón "Eliminar"

### Consejos Útiles

- Actualiza regularmente los catálogos de docentes y laboratorios
- Realiza copias de seguridad periódicas de la base de datos
- Para grandes volúmenes de datos, utiliza la importación por CSV

## 🗂️ Estructura del Proyecto

```
registros-laboratorios/
├── main.py                 # Punto de entrada de la aplicación
├── database/               # Configuración de la base de datos
│   ├── __init__.py
│   ├── database.py         # Configuración de conexión
│   └── models.py           # Modelos SQLAlchemy
├── ui/                     # Interfaz de usuario
│   ├── __init__.py
│   ├── main_window.py      # Ventana principal
│   ├── periodos_tab.py     # Gestión de periodos
│   ├── docentes_tab.py     # Gestión de docentes
│   ├── registros_tab.py    # Registro de uso
│   └── visualizacion_tab.py # Visualización y reportes
└── utils/                  # Utilidades generales
    └── __init__.py
```

## 🔄 Modelo de Datos

El sistema utiliza SQLite para almacenar los datos en un archivo local. Los principales modelos son:

- **Periodo**: Almacena información sobre periodos académicos
- **Carrera**: Catálogo de carreras universitarias
- **Docente**: Información de docentes asociados a carreras
- **Laboratorio**: Catálogo de laboratorios asociados a carreras
- **Registro**: Registros de uso de laboratorios

## 🔨 Desarrollo

### Crear un Ejecutable

Para generar un archivo ejecutable (.exe):

1. Instala PyInstaller:
   ```bash
   pip install pyinstaller
   ```

2. Crea el ejecutable:
   ```bash
   pyinstaller --clean --windowed --add-data "database;database" --add-data "ui;ui" main.py
   ```

3. El ejecutable estará disponible en la carpeta `dist/`

### Crear un Instalador

1. Instala Inno Setup
2. Utiliza el script `install_script.iss` incluido
3. Compila para generar el instalador

## ❓ Solución de Problemas

### La aplicación no inicia
- Verifica que todas las dependencias estén instaladas correctamente
- Asegúrate de que Python 3.8 o superior esté instalado
- Comprueba los permisos de escritura en la carpeta de la aplicación

### Error al guardar registros
- Verifica los permisos de escritura en la carpeta de la base de datos
- Asegúrate de completar todos los campos obligatorios

### Problemas con la importación CSV
- Verifica el formato del archivo CSV
- Asegúrate de que las columnas coincidan con los datos esperados
- Utiliza el visor de CSV integrado para previsualizar los datos

## 📄 Licencia

Desarrollado exclusivamente para la Universidad Autónoma de Guerrero (UAGRO) - 2025

## ✉️ Contacto

Para soporte técnico, contacta al desarrollador en: [ejemplo@email.com](mailto:ejemplo@email.com) 