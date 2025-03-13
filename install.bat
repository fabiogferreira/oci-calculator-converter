@echo off
echo Instalando OCI Calculator Converter...
echo.

REM Verificar se o Python está instalado
python --version > nul 2>&1
if %errorlevel% neq 0 (
    echo Python não encontrado. Por favor, instale o Python 3.6 ou superior.
    echo Você pode baixá-lo em: https://www.python.org/downloads/
    pause
    exit /b 1
)

echo Python encontrado. Verificando versão...
for /f "tokens=2" %%i in ('python --version 2^>^&1') do set pyver=%%i
echo Versão do Python: %pyver%
echo.

REM Verificar se o pip está instalado
python -m pip --version > nul 2>&1
if %errorlevel% neq 0 (
    echo Pip não encontrado. Instalando pip...
    echo Isso pode levar alguns minutos...
    python -m ensurepip --upgrade
    if %errorlevel% neq 0 (
        echo Erro ao instalar pip. Por favor, instale o pip manualmente.
        pause
        exit /b 1
    )
)
echo Pip encontrado ou instalado com sucesso.
echo.

echo Configuração concluída! O OCI Calculator Converter está pronto para uso.
echo.
echo Para usar o programa, execute:
echo python oci-calculator-converter.py exemplo-csv.csv --label "Minha Estimativa"
echo.
echo Consulte o README.md para mais informações.

pause 