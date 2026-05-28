import enum


class UnitMeasure(str, enum.Enum):
    UNIDADE = "UNIDADE"
    METRO = "METRO"
    LITRO = "LITRO"
    QUILOGRAMA = "QUILOGRAMA"
    CAIXA = "CAIXA"
    PACOTE = "PACOTE"
    ROLO = "ROLO"
    PAR = "PAR"


class MovementType(str, enum.Enum):
    ENTRADA_COMPRA = "ENTRADA_COMPRA"       # Compra de fornecedor
    SAIDA_VENDA = "SAIDA_VENDA"             # Venda ao cliente
    SAIDA_BAIXA = "SAIDA_BAIXA"             # Baixa / descarte / perda
    ENTRADA_AJUSTE = "ENTRADA_AJUSTE"       # Ajuste manual de entrada
    SAIDA_AJUSTE = "SAIDA_AJUSTE"           # Ajuste manual de saída
    ENTRADA_DEVOLUCAO = "ENTRADA_DEVOLUCAO" # Devolução de cliente


class MovementDirection(str, enum.Enum):
    ENTRADA = "ENTRADA"
    SAIDA = "SAIDA"
