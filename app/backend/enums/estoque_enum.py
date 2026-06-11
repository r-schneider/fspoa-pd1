import enum


class UnidadeMedida(str, enum.Enum):
    UNIDADE = "UNIDADE"
    METRO = "METRO"
    LITRO = "LITRO"
    QUILOGRAMA = "QUILOGRAMA"
    CAIXA = "CAIXA"
    PACOTE = "PACOTE"
    ROLO = "ROLO"
    PAR = "PAR"


class TipoMovimentacao(str, enum.Enum):
    ENTRADA_COMPRA = "ENTRADA_COMPRA"
    SAIDA_VENDA = "SAIDA_VENDA"
    SAIDA_BAIXA = "SAIDA_BAIXA"
    ENTRADA_AJUSTE = "ENTRADA_AJUSTE"
    SAIDA_AJUSTE = "SAIDA_AJUSTE"
    ENTRADA_DEVOLUCAO = "ENTRADA_DEVOLUCAO"


class DirecaoMovimentacao(str, enum.Enum):
    ENTRADA = "ENTRADA"
    SAIDA = "SAIDA"
