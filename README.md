# Rongocraft Launcher

Rongocraft Launcher es un lanzador personalizado para Minecraft con soporte para Forge, perfiles de usuario y configuración de memoria RAM. Permite instalar y ejecutar Minecraft fácilmente, así como empaquetar la aplicación como ejecutable.

## Requisitos
- Python 3.8 o superior
- Java 17 (el lanzador puede descargarlo automáticamente)
- Dependencias Python (ver más abajo)

## Instalación de dependencias
Instala las dependencias necesarias ejecutando:

```sh
pip install -r src/requirements.txt
```

En sistemas basados en Arch Linux, instala también el paquete de Tkinter:

```sh
sudo pacman -S tk
```

En Ubuntu/Debian:

```sh
sudo apt-get install python3-tk
```

## Dependencias para extracción de archivos RAR
Para que la función de extracción de archivos RAR funcione correctamente, asegúrate de tener instalada la librería Python `rarfile` (ya incluida en requirements.txt) y el programa `unrar` en tu sistema:

- **En Arch Linux:**
  ```sh
  sudo pacman -S unrar
  ```
- **En Ubuntu/Debian:**
  ```sh
  sudo apt-get install unrar
  ```
- **En Windows:**
  Descarga e instala [UnRAR para Windows](https://www.rarlab.com/rar_add.htm) y asegúrate de que el ejecutable `unrar.exe` esté en tu PATH.

La librería `rarfile` utiliza `unrar` para descomprimir archivos RAR.

## Uso
Ejecuta el lanzador con:

```sh
python main.py
```

- Puedes iniciar sesión y crear perfiles.
- Configura la cantidad de RAM desde el botón "Configuración RAM".
- Haz clic en "Play" para iniciar Minecraft con Forge.

## Cambiar la versión de Minecraft o Forge
Para cambiar la versión de Minecraft o Forge, edita las siguientes líneas en `config/__init__.py`:

```
# Minecraft and Forge configuration
MINECRAFT_VERSION = "1.18.2"
FORGE_VERSION = "40.3.0"
```

Reemplaza los valores por la versión de Minecraft y Forge que desees usar. Guarda el archivo y ejecuta el lanzador normalmente.

## Empaquetar la aplicación (crear ejecutable)
Puedes crear un ejecutable usando PyInstaller. Ejecuta:

```sh
pyinstaller --onefile --noconsole --icon=Launcher.ico --add-data "src/assets:assets" --hidden-import=PIL._tkinter_finder --hidden-import=PIL.ImageTk src/main.py
```

Esto generará un archivo ejecutable en la carpeta `dist/`.

## Créditos
- Usa [minecraft-launcher-lib](https://github.com/Hexeption/minecraft-launcher-lib)
- Usa [customtkinter](https://github.com/TomSchimansky/CustomTkinter)
