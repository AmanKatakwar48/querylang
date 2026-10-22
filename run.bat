@echo off
setlocal
if exist "C:\msys64\ucrt64\bin\python.exe" (
    set "PYTHON_EXE=C:\msys64\ucrt64\bin\python.exe"
) else (
    set "PYTHON_EXE=python"
)

"%PYTHON_EXE%" "%~dp0main.py" %*
endlocal
