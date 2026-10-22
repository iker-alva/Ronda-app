@echo off
setlocal
cd /d "%~dp0"
set "ROOT=%~dp0"

where python >nul 2>nul
if errorlevel 1 (
  echo.
  echo  No se ha encontrado Python en el PATH.
  echo  Instala Python 3.9 o superior desde https://www.python.org/downloads/windows/
  echo  y vuelve a ejecutar este archivo.
  echo.
  pause
  exit /b 1
)

python -c "import PyInstaller" >nul 2>nul
if errorlevel 1 (
  echo Instalando PyInstaller...
  python -m pip install --disable-pip-version-check pyinstaller
  if errorlevel 1 (
    echo No se pudo instalar PyInstaller.
    pause
    exit /b 1
  )
)

if not exist "static\icons\ronda.ico" (
  echo Generando iconos...
  python gen_icons.py
)

echo.
echo Creando Ronda.exe (esto puede tardar un minuto)...
echo.
python -m PyInstaller --noconfirm --clean --onefile --console --noupx ^
  --name Ronda ^
  --icon "%ROOT%static\icons\ronda.ico" ^
  --version-file "%ROOT%version_info.txt" ^
  --add-data "%ROOT%static;static" ^
  --distpath "%ROOT%dist" ^
  --workpath "%ROOT%build\work" ^
  --specpath "%ROOT%build" ^
  "%ROOT%server.py"
if errorlevel 1 (
  echo.
  echo La compilacion ha fallado.
  pause
  exit /b 1
)

copy /Y "LEEME.txt" "dist\LEEME.txt" >nul
if exist "dist\Ronda-Windows.zip" del /Q "dist\Ronda-Windows.zip"
powershell -NoProfile -Command "Compress-Archive -Path 'dist\Ronda.exe','dist\LEEME.txt' -DestinationPath 'dist\Ronda-Windows.zip' -Force"
if errorlevel 1 (
  echo.
  echo El .exe se ha creado, pero no se pudo preparar el ZIP.
  echo Lo tienes en: %CD%\dist\Ronda.exe
  pause
  exit /b 1
)

echo.
echo  Listo.
echo  - Ejecutable: %CD%\dist\Ronda.exe
echo  - Para compartir: %CD%\dist\Ronda-Windows.zip
echo.
echo  Abre Ronda.exe y comparte la direccion que aparece en la ventana.
echo.
pause
