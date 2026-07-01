@echo off
REM Crear entorno virtual
python -m venv env

REM Activar entorno virtual
call env\Scripts\activate.bat

REM IMPORTANTE: Instalar las dependencias
pip install mysql-connector-python

REM instalar pyside6
pip install PySide6

REM Ejecutar el programa
python main.py

pause