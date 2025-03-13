#!/bin/bash

echo "Instalando OCI Calculator Converter..."
echo

# Verificar se o Python está instalado
if command -v python3 &>/dev/null; then
    PYTHON_CMD="python3"
elif command -v python &>/dev/null; then
    PYTHON_CMD="python"
else
    echo "Python não encontrado. Por favor, instale o Python 3.6 ou superior."
    echo "Para Ubuntu/Debian: sudo apt install python3"
    echo "Para macOS: brew install python3"
    exit 1
fi

echo "Python encontrado. Verificando versão..."
$PYTHON_CMD --version
echo

# Verificar se o pip está instalado
PIP_CMD="${PYTHON_CMD} -m pip"
if ! $PIP_CMD --version &>/dev/null; then
    echo "pip não encontrado. Verificando se pode ser instalado..."
    if $PYTHON_CMD -m ensurepip --version &>/dev/null; then
        echo "Instalando pip via ensurepip..."
        $PYTHON_CMD -m ensurepip --upgrade
    else
        echo "ensurepip não disponível. Tentando método alternativo..."
        if [[ "$OSTYPE" == "linux-gnu"* ]]; then
            echo "Detectado Linux. Tentando instalar via apt..."
            sudo apt-get update
            sudo apt-get install -y python3-pip
        elif [[ "$OSTYPE" == "darwin"* ]]; then
            echo "Detectado macOS. Baixando get-pip.py..."
            curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py
            $PYTHON_CMD get-pip.py
            rm get-pip.py
        else
            echo "Sistema operacional não suportado para instalação automática do pip."
            echo "O programa funcionará sem pip, mas recomendamos instalar o pip manualmente."
        fi
    fi
    
    # Verificar novamente se o pip foi instalado
    if ! $PIP_CMD --version &>/dev/null; then
        echo "Aviso: pip não pôde ser instalado, mas o programa funcionará sem ele."
        echo "Recomendamos instalar o pip manualmente para futuras extensões."
    else
        echo "pip instalado com sucesso."
    fi
else
    echo "pip encontrado."
fi
echo

echo "Configuração concluída! O OCI Calculator Converter está pronto para uso."
echo
echo "Para usar o programa, execute:"
echo "$PYTHON_CMD oci-calculator-converter.py exemplo-csv.csv --label \"Minha Estimativa\""
echo
echo "Consulte o README.md para mais informações."

# Tornar o script executável
chmod +x oci-calculator-converter.py

echo
echo "O script oci-calculator-converter.py agora é executável." 