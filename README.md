# OCI Calculator Converter

Uma ferramenta para converter arquivos CSV em formato JSON compatível com o Oracle Cloud Infrastructure (OCI) Calculator.

## Descrição

O OCI Calculator Converter é uma ferramenta de linha de comando que permite converter dados de máquinas virtuais e armazenamento de um arquivo CSV para o formato JSON utilizado pelo OCI Calculator. Isso facilita a criação de estimativas de custo para infraestrutura na Oracle Cloud.

## Requisitos

- Python 3.6 ou superior
- pip (gerenciador de pacotes do Python)

Observação: O programa utiliza apenas bibliotecas padrão do Python (csv, json, uuid, datetime, argparse, re), então não é necessário instalar pacotes adicionais. O arquivo requirements.txt está incluído para facilitar futuras extensões.

## Instalação

### Método Automático (Recomendado)

1. Clone ou baixe este repositório
2. Execute o script de instalação apropriado para seu sistema operacional:
   - Windows: `install.bat`
   - Linux/macOS: `./install.sh`

O script de instalação verificará se o Python está instalado, instalará o pip se necessário e configurará o ambiente para execução do programa.

### Instalação Manual

1. Clone ou baixe este repositório
2. Verifique se o Python 3.6 ou superior está instalado:
   ```
   python --version
   ```
3. Se estiver usando Linux/macOS, torne o script executável:
   ```
   chmod +x oci-calculator-converter.py
   ```

## Formato do Arquivo CSV

O arquivo CSV deve ter as seguintes colunas, separadas por ponto e vírgula (`;`):

| Coluna | Descrição | Obrigatório |
|--------|-----------|-------------|
| Label | Nome da configuração | Sim |
| Qtd | Quantidade de instâncias | Não (padrão: 1) |
| OS | Sistema operacional (centos, windows, oracle, ubuntu, etc.) | Sim |
| Shape | Tipo de instância (ex: VM.Standard.E4.Flex) | Não (padrão: VM.Standard.E4.Flex) |
| OCPU | Número de OCPUs | Não (padrão: 8) |
| RAM_GB | Quantidade de RAM em GB | Não (calculado como OCPU * 16 se não fornecido) |
| Storage_GB | Tamanho do armazenamento em GB | Não (padrão: 100) |
| Performance_Units | Unidades de performance do armazenamento | Não (padrão: 1000) |

### Exemplo de Arquivo CSV

```
Label;Qtd;OS;Shape;OCPU;RAM_GB;Storage_GB;Performance_Units
CentOS;1;centos;VM.Standard.E4.Flex;7;14;100;1000
Windows;1;windows;VM.Standard.E4.Flex;1;8;100;1000
```

## Uso

```
python oci-calculator-converter.py arquivo.csv --label "Minha Estimativa"
```

### Parâmetros

- `csv_file`: Caminho para o arquivo CSV de entrada (obrigatório)
- `--label`, `-l`: Rótulo da estimativa (opcional, padrão: "Generated Estimate")

### Saída

O programa gera um arquivo JSON com o nome baseado no rótulo da estimativa. Por exemplo, se o rótulo for "Minha Estimativa", o arquivo de saída será "Minha_Estimativa.json".

Este arquivo JSON pode ser importado no OCI Calculator para visualizar a estimativa de custos.

## Características

- Suporte para múltiplas configurações de VM em um único arquivo
- Cálculo automático de custos baseado em OCPUs, RAM, armazenamento e performance
- Suporte para licenças do Windows
- Geração de identificadores únicos para cada serviço
- Formatação de saída compatível com o OCI Calculator

## Limitações

- O programa assume valores padrão para alguns parâmetros se não forem fornecidos
- Os SKUs e preços são fixos no código e podem precisar ser atualizados conforme mudanças na OCI
- A moeda está fixada como BRL (Real Brasileiro)

## Atenção em relação aos valores padrão!
- O programa assume valores padrão mas não há com o que se preocupar uma vez que a calculadora da Oracle OCI atualiza para os valores corretos quanto da importação
- O objetivo deste programa não é unicamente facilitar a importação de um grande número de registros de máquinas virtuais de uma única vez, os ajustes preferencialmente devem ser feito na própria calculadora OCI após a importação

## Solução de Problemas

### Erro ao abrir o arquivo CSV

Verifique se o arquivo CSV existe no caminho especificado e se tem permissões de leitura.

### Erro no formato do arquivo CSV

Verifique se o arquivo CSV está no formato correto, com as colunas necessárias e separadas por ponto e vírgula (;).

### Erro ao executar o programa

Verifique se o Python está instalado corretamente e se o arquivo do programa tem permissões de execução.

## Contribuições

Contribuições são bem-vindas! Sinta-se à vontade para abrir issues ou enviar pull requests.

## Licença

Este projeto está licenciado sob a licença MIT - veja o arquivo LICENSE para detalhes. 
