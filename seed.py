from app.core.database import SessionLocal, engine
from app.models.models import Base, Categoria, Produto
from app.enums.unit_measure_enum import UnitMeasure

print("rodando seed...")

Base.metadata.create_all(bind=engine)

db = SessionLocal()

db.query(Produto).delete()
db.query(Categoria).delete()
db.commit()

categorias_data = [
    {"nome": "Parafusos e Fixadores",  "lugar": "Prateleira A1"},
    {"nome": "Ferramentas Manuais",    "lugar": "Prateleira B1"},
    {"nome": "Ferramentas Elétricas",  "lugar": "Prateleira C1"},
    {"nome": "Tintas e Vernizes",      "lugar": "Prateleira D1"},
    {"nome": "Hidráulica",             "lugar": "Prateleira E1"},
    {"nome": "Elétrica",               "lugar": "Prateleira F1"},
    {"nome": "Segurança do Trabalho",  "lugar": "Prateleira G1"},
    {"nome": "Construção e Cimento",   "lugar": "Área Externa"},
    {"nome": "Jardim e Irrigação",     "lugar": "Prateleira H1"},
    {"nome": "Peças e Vedação",        "lugar": "Prateleira A2"},
    {"nome": "Limpeza e Manutenção",   "lugar": "Prateleira B2"},
    {"nome": "Madeiras e Compensados", "lugar": "Área Externa"},
]

cats = {}
for c in categorias_data:
    obj = Categoria(**c)
    db.add(obj)
    db.flush()
    cats[c["nome"]] = obj.id

produtos_data = [
    # (nome, codigo_barra, estoque_atual, estoque_minimo, preco_compra, preco_venda, categoria)
    ("Parafuso Sextavado M6x25",    "7891234560001", 600, 150, 0.10, 0.30,  "Parafusos e Fixadores"),
    ("Parafuso Sextavado M8x30",    "7891234560002", 500, 100, 0.15, 0.45,  "Parafusos e Fixadores"),
    ("Porca Sextavada M6",          "7891234560003", 700, 200, 0.06, 0.18,  "Parafusos e Fixadores"),
    ("Arruela Zincada M6",          "7891234560004", 900, 250, 0.04, 0.12,  "Parafusos e Fixadores"),
    ("Bucha de Nylon S8",           "7891234560005", 500, 150, 0.10, 0.30,  "Parafusos e Fixadores"),
    ("Martelo Cabo Madeira 500g",   "7891234561001", 20,  6,   22.00, 55.90, "Ferramentas Manuais"),
    ("Chave Philips N2",            "7891234561002", 45,  12,  5.00,  12.90, "Ferramentas Manuais"),
    ("Alicate Universal 8\"",       "7891234561003", 18,  6,   28.00, 64.90, "Ferramentas Manuais"),
    ("Trena Emborrachada 5m",       "7891234561004", 25,  8,   12.00, 29.90, "Ferramentas Manuais"),
    ("Serrote 22\" Plástico",       "7891234561005", 12,  4,   18.00, 44.90, "Ferramentas Manuais"),
    ("Furadeira 3/8\" 500W Vonder", "7891234562001", 7,   3,   98.00, 239.90,"Ferramentas Elétricas"),
    ("Serra Circular 7.1/4\" 1200W","7891234562002", 4,   2,   185.00,449.90,"Ferramentas Elétricas"),
    ("Lixadeira Orbital 200W",      "7891234562003", 5,   2,   88.00, 214.90,"Ferramentas Elétricas"),
    ("Tinta Acrílica Branca 18L",   "7891234563001", 12,  4,   118.00,279.90,"Tintas e Vernizes"),
    ("Tinta Esmalte Branco 3,6L",   "7891234563002", 10,  4,   42.00, 99.90, "Tintas e Vernizes"),
    ("Massa Corrida PVA 25kg",      "7891234563003", 14,  5,   48.00, 115.90,"Tintas e Vernizes"),
    ("Rolo de Lã 23cm",             "7891234563004", 35,  10,  8.50,  19.90, "Tintas e Vernizes"),
    ("Lixa Massa Grão 120",         "7891234563005", 100, 30,  1.20,  2.90,  "Tintas e Vernizes"),
    ("Torneira Parede 1/2\" Deca",  "7891234564001", 14,  5,   38.00, 89.90, "Hidráulica"),
    ("Registro Gaveta 1/2\" Deca",  "7891234564002", 8,   3,   42.00, 98.90, "Hidráulica"),
    ("Cano PVC 25mm barra 6m",      "7891234564003", 30,  10,  12.00, 28.90, "Hidráulica"),
    ("Joelho PVC 25mm 90°",         "7891234564004", 80,  25,  1.20,  3.20,  "Hidráulica"),
    ("Fita Veda Rosca 18mm x 10m",  "7891234564005", 90,  25,  2.20,  5.50,  "Hidráulica"),
    ("Tomada 2P+T 10A Tramontina",  "7891234565001", 50,  15,  5.80,  14.90, "Elétrica"),
    ("Interruptor Simples",         "7891234565002", 45,  15,  4.80,  12.90, "Elétrica"),
    ("Disjuntor 20A Monopolar",     "7891234565003", 18,  6,   16.00, 38.90, "Elétrica"),
    ("Cabo Flexível 2,5mm 100m",    "7891234565004", 5,   2,   98.00, 235.90,"Elétrica"),
    ("Lâmpada LED 9W E27",          "7891234565005", 35,  12,  5.90,  14.90, "Elétrica"),
    ("Luva de Raspa CA",            "7891234566001", 25,  8,   12.00, 28.90, "Segurança do Trabalho"),
    ("Óculos de Segurança Incolor", "7891234566002", 20,  8,   5.50,  13.90, "Segurança do Trabalho"),
    ("Cimento CP-II 50kg Votoran",  "7891234567001", 50,  20,  32.00, 49.90, "Construção e Cimento"),
    ("Argamassa AC-II 20kg",        "7891234567002", 35,  15,  14.00, 29.90, "Construção e Cimento"),
    ("Mangueira Trançada 1/2\" 50m","7891234568001", 10,  4,   55.00, 129.90,"Jardim e Irrigação"),
    ("Regador Plástico 10L",        "7891234568002", 10,  4,   18.00, 42.90, "Jardim e Irrigação"),
    ("Silicone Neutro Transp. 280g","7891234569001", 22,  8,   10.00, 24.90, "Peças e Vedação"),
    ("WD-40 Desengripante 300ml",   "7891234570001", 20,  8,   18.00, 42.90, "Limpeza e Manutenção"),
]

for nome, cod, est_at, est_min, p_compra, p_venda, cat_nome in produtos_data:
    p = Produto(
        nome=nome,
        codigo_barra=cod,
        estoque_atual=est_at,
        estoque_minimo=est_min,
        preco_compra=p_compra,
        preco_venda=p_venda,
        categoria_id=cats[cat_nome],
        unidade_medida=UnitMeasure.UNIT,
        ativo=True,
    )
    db.add(p)

db.commit()
db.close()
print("✅ Banco populado com sucesso!")
print(f"   {len(categorias_data)} categorias | {len(produtos_data)} produtos")