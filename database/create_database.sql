-- ============================================================
--  Stockmaster — Script de Criação e Dados do Banco
--  PostgreSQL 14+
--  Execute como superusuário ou com permissões de CREATE
-- ============================================================

-- CREATE DATABASE ferragem_pro;
-- \c ferragem_pro;

-- ============================================================
-- TIPOS ENUM
-- ============================================================

DO $$ BEGIN
    CREATE TYPE unit_measure_enum AS ENUM (
        'UNIDADE', 'METRO', 'LITRO', 'QUILOGRAMA',
        'CAIXA', 'PACOTE', 'ROLO', 'PAR'
    );
EXCEPTION WHEN duplicate_object THEN NULL;
END $$;

DO $$ BEGIN
    CREATE TYPE movement_type_enum AS ENUM (
        'ENTRADA_COMPRA',
        'SAIDA_VENDA',
        'SAIDA_BAIXA',
        'ENTRADA_AJUSTE',
        'SAIDA_AJUSTE',
        'ENTRADA_DEVOLUCAO'
    );
EXCEPTION WHEN duplicate_object THEN NULL;
END $$;

DO $$ BEGIN
    CREATE TYPE movement_direction_enum AS ENUM (
        'ENTRADA',
        'SAIDA'
    );
EXCEPTION WHEN duplicate_object THEN NULL;
END $$;

-- ============================================================
-- TABELA: CATEGORIAS
-- ============================================================

CREATE TABLE IF NOT EXISTS "CATEGORIAS" (
    "ID"               SERIAL PRIMARY KEY,
    "NOME"             VARCHAR(100)  NOT NULL UNIQUE,
    "DESCRICAO"        TEXT,
    "ATIVO"            BOOLEAN       NOT NULL DEFAULT TRUE,
    "DATA_CRIACAO"     TIMESTAMP     NOT NULL DEFAULT NOW(),
    "DATA_ATUALIZACAO" TIMESTAMP     NOT NULL DEFAULT NOW()
);

-- ============================================================
-- TABELA: FORNECEDORES
-- ============================================================

CREATE TABLE IF NOT EXISTS "FORNECEDORES" (
    "ID"               SERIAL PRIMARY KEY,
    "NOME"             VARCHAR(200)  NOT NULL,
    "CNPJ"             VARCHAR(18)   UNIQUE,
    "TELEFONE"         VARCHAR(20),
    "EMAIL"            VARCHAR(254),
    "ENDERECO"         VARCHAR(500),
    "ATIVO"            BOOLEAN       NOT NULL DEFAULT TRUE,
    "DATA_CRIACAO"     TIMESTAMP     NOT NULL DEFAULT NOW(),
    "DATA_ATUALIZACAO" TIMESTAMP     NOT NULL DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_fornecedores_cnpj  ON "FORNECEDORES" ("CNPJ");
CREATE INDEX IF NOT EXISTS idx_fornecedores_ativo ON "FORNECEDORES" ("ATIVO");

-- ============================================================
-- TABELA: PRODUTOS
-- ============================================================

CREATE TABLE IF NOT EXISTS "PRODUTOS" (
    "ID"               SERIAL PRIMARY KEY,
    "NOME"             VARCHAR(200)       NOT NULL,
    "DESCRICAO"        TEXT,
    "CODIGO_BARRAS"    VARCHAR(50)        UNIQUE,
    "SKU"              VARCHAR(50)        NOT NULL UNIQUE,
    "ESTOQUE_ATUAL"    INTEGER            NOT NULL DEFAULT 0,
    "ESTOQUE_MINIMO"   INTEGER            NOT NULL DEFAULT 0,
    "ESTOQUE_MAXIMO"   INTEGER,
    "PRECO_VENDA"      NUMERIC(10,2)      NOT NULL,
    "PRECO_CUSTO"      NUMERIC(10,2),
    "UNIDADE_MEDIDA"   unit_measure_enum  NOT NULL,
    "ATIVO"            BOOLEAN            NOT NULL DEFAULT TRUE,
    "URL_IMAGEM"       VARCHAR(500),
    "DATA_CRIACAO"     TIMESTAMP          NOT NULL DEFAULT NOW(),
    "DATA_ATUALIZACAO" TIMESTAMP          NOT NULL DEFAULT NOW(),
    "ID_CATEGORIA"     INTEGER REFERENCES "CATEGORIAS"("ID") ON DELETE SET NULL
);

CREATE INDEX IF NOT EXISTS idx_produtos_sku       ON "PRODUTOS" ("SKU");
CREATE INDEX IF NOT EXISTS idx_produtos_categoria ON "PRODUTOS" ("ID_CATEGORIA");
CREATE INDEX IF NOT EXISTS idx_produtos_ativo     ON "PRODUTOS" ("ATIVO");

-- ============================================================
-- TABELA: MOVIMENTACOES_ESTOQUE
-- ============================================================

CREATE TABLE IF NOT EXISTS "MOVIMENTACOES_ESTOQUE" (
    "ID"                   SERIAL PRIMARY KEY,
    "TIPO_MOVIMENTACAO"    movement_type_enum      NOT NULL,
    "DIRECAO"              movement_direction_enum NOT NULL,
    "QUANTIDADE"           INTEGER       NOT NULL CHECK ("QUANTIDADE" > 0),
    "CUSTO_UNITARIO"       NUMERIC(10,2),
    "PRECO_UNITARIO"       NUMERIC(10,2),
    "ESTOQUE_ANTES"        INTEGER       NOT NULL,
    "ESTOQUE_DEPOIS"       INTEGER       NOT NULL,
    "MOTIVO"               TEXT,
    "DOCUMENTO_REFERENCIA" VARCHAR(100),
    "DATA_CRIACAO"         TIMESTAMP     NOT NULL DEFAULT NOW(),
    "ID_PRODUTO"           INTEGER       NOT NULL REFERENCES "PRODUTOS"("ID") ON DELETE RESTRICT,
    "ID_FORNECEDOR"        INTEGER       REFERENCES "FORNECEDORES"("ID") ON DELETE SET NULL
);

CREATE INDEX IF NOT EXISTS idx_mov_produto    ON "MOVIMENTACOES_ESTOQUE" ("ID_PRODUTO");
CREATE INDEX IF NOT EXISTS idx_mov_fornecedor ON "MOVIMENTACOES_ESTOQUE" ("ID_FORNECEDOR");
CREATE INDEX IF NOT EXISTS idx_mov_data       ON "MOVIMENTACOES_ESTOQUE" ("DATA_CRIACAO");
CREATE INDEX IF NOT EXISTS idx_mov_tipo       ON "MOVIMENTACOES_ESTOQUE" ("TIPO_MOVIMENTACAO");

-- ============================================================
-- FUNÇÃO: atualiza DATA_ATUALIZACAO automaticamente
-- ============================================================

CREATE OR REPLACE FUNCTION fn_update_timestamp()
RETURNS TRIGGER AS $$
BEGIN
    NEW."DATA_ATUALIZACAO" = NOW();
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

DROP TRIGGER IF EXISTS trg_categorias_update ON "CATEGORIAS";
CREATE TRIGGER trg_categorias_update
    BEFORE UPDATE ON "CATEGORIAS"
    FOR EACH ROW EXECUTE FUNCTION fn_update_timestamp();

DROP TRIGGER IF EXISTS trg_fornecedores_update ON "FORNECEDORES";
CREATE TRIGGER trg_fornecedores_update
    BEFORE UPDATE ON "FORNECEDORES"
    FOR EACH ROW EXECUTE FUNCTION fn_update_timestamp();

DROP TRIGGER IF EXISTS trg_produtos_update ON "PRODUTOS";
CREATE TRIGGER trg_produtos_update
    BEFORE UPDATE ON "PRODUTOS"
    FOR EACH ROW EXECUTE FUNCTION fn_update_timestamp();

-- ============================================================
-- DADOS: CATEGORIAS (15)
-- ============================================================

INSERT INTO "CATEGORIAS" ("NOME", "DESCRICAO") VALUES
    ('Parafusos e Porcas',     'Parafusos, porcas, arruelas e fixadores em geral'),
    ('Ferramentas Manuais',    'Martelos, chaves, alicates, serras e similares'),
    ('Ferramentas Elétricas',  'Furadeiras, esmerilhadeiras, parafusadeiras etc.'),
    ('Tintas e Vernizes',      'Tintas, vernizes, primers e complementos'),
    ('Hidráulica',             'Conexões, tubos, registros e materiais hidráulicos'),
    ('Elétrica',               'Cabos, disjuntores, tomadas e materiais elétricos'),
    ('Madeiras e Compensados', 'Tábuas, compensados, MDF e similares'),
    ('Cimento e Argamassa',    'Cimentos, argamassas, rejuntes e concretos'),
    ('EPI',                    'Equipamentos de Proteção Individual'),
    ('Jardim e Paisagismo',    'Mangueiras, regadores, ferramentas de jardim'),
    ('Construção Civil',       'Telas, arames, pregos e materiais gerais de obra'),
    ('Iluminação',             'Lâmpadas, luminárias e acessórios de iluminação'),
    ('Adesivos e Vedantes',    'Colas, silicones, veda-rosca e fitas adesivas'),
    ('Fixadores e Ancoragem',  'Buchas, ganchos, suportes e ancoragem em geral'),
    ('Outros',                 'Demais produtos não classificados')
ON CONFLICT ("NOME") DO NOTHING;

-- ============================================================
-- DADOS: FORNECEDORES (12)
-- ============================================================

INSERT INTO "FORNECEDORES" ("NOME", "CNPJ", "TELEFONE", "EMAIL", "ENDERECO") VALUES
    ('Brasal Distribuidora de Ferragens',      '11.222.333/0001-44', '(51) 3333-1111', 'compras@brasal.com.br',           'Av. Industrial, 1500 — Porto Alegre/RS'),
    ('Construfort Materiais de Construção',    '22.333.444/0001-55', '(51) 3444-2222', 'vendas@construfort.com.br',        'Rua da Construção, 800 — Canoas/RS'),
    ('Elétrica Nordeste Distribuidora',        '33.444.555/0001-66', '(51) 3555-3333', 'pedidos@eletricanordeste.com.br',  'Rua Elétrica, 450 — São Leopoldo/RS'),
    ('Aqua Hidráulica Distribuições',          '44.555.666/0001-77', '(51) 3666-4444', 'vendas@aquahidraulica.com.br',     'Av. Hidráulica, 200 — Novo Hamburgo/RS'),
    ('Madeireira São Paulo Ltda',              '55.666.777/0001-88', '(51) 3777-5555', 'comercial@madeireirasp.com.br',    'Rodovia BR-116, 2200 — Sapucaia do Sul/RS'),
    ('Tintas Brasil Indústria e Comércio',     '66.777.888/0001-99', '(51) 3888-6666', 'vendas@tintasbrasil.com.br',       'Rua das Tintas, 350 — Esteio/RS'),
    ('EPI Master Equipamentos de Segurança',   '77.888.999/0001-00', '(51) 3999-7777', 'vendas@epimaster.com.br',          'Av. Segurança, 1100 — Cachoeirinha/RS'),
    ('Ferramenta Mão Distribuidora',           '88.999.000/0001-11', '(51) 3100-8888', 'pedidos@ferramentamao.com.br',     'Rua das Ferramentas, 650 — Gravataí/RS'),
    ('Iluminar Soluções em Luz',               '99.000.111/0001-22', '(51) 3211-9999', 'comercial@iluminar.com.br',        'Av. da Luz, 780 — Alvorada/RS'),
    ('Jardim Total Distribuidora',             '10.111.222/0001-33', '(51) 3322-0000', 'vendas@jardimtotal.com.br',        'Rua do Verde, 420 — Viamão/RS'),
    ('Cimentech Materiais de Construção',      '21.222.333/0001-44', '(51) 3433-1110', 'compras@cimentech.com.br',         'Av. do Cimento, 1800 — Eldorado do Sul/RS'),
    ('Global Ferragens Importação e Comércio', '32.333.444/0001-55', '(51) 3544-2221', 'imports@globalferragens.com.br',   'Av. Internacional, 900 — Porto Alegre/RS')
ON CONFLICT ("CNPJ") DO NOTHING;

-- ============================================================
-- DADOS: PRODUTOS (50)
-- Campos: NOME, DESCRICAO, CODIGO_BARRAS, SKU,
--         ESTOQUE_ATUAL, ESTOQUE_MINIMO, ESTOQUE_MAXIMO,
--         PRECO_VENDA, PRECO_CUSTO, UNIDADE_MEDIDA, ID_CATEGORIA
-- ============================================================

INSERT INTO "PRODUTOS"
    ("NOME","DESCRICAO","CODIGO_BARRAS","SKU",
     "ESTOQUE_ATUAL","ESTOQUE_MINIMO","ESTOQUE_MAXIMO",
     "PRECO_VENDA","PRECO_CUSTO","UNIDADE_MEDIDA","ID_CATEGORIA")
VALUES

-- === PARAFUSOS E PORCAS ===
('Parafuso Phillips M5x30 Zincado',
 'Parafuso cabeça chata Phillips M5x30 zincado — caixa c/ 100 un',
 '7891234560001','PAF-001', 500,100,2000,  8.90,  5.50,'CAIXA',
 (SELECT "ID" FROM "CATEGORIAS" WHERE "NOME"='Parafusos e Porcas')),

('Parafuso Phillips M8x50 Zincado',
 'Parafuso cabeça chata Phillips M8x50 zincado — caixa c/ 50 un',
 '7891234560002','PAF-002', 320, 50,1000, 18.50, 11.00,'CAIXA',
 (SELECT "ID" FROM "CATEGORIAS" WHERE "NOME"='Parafusos e Porcas')),

('Porca Sextavada M8 Zincada',
 'Porca sextavada M8 zincada — caixa c/ 100 un',
 '7891234560003','PAF-003', 400, 50,1500, 12.00,  7.20,'CAIXA',
 (SELECT "ID" FROM "CATEGORIAS" WHERE "NOME"='Parafusos e Porcas')),

('Arruela Lisa M8 Zincada',
 'Arruela lisa M8 zincada — pacote c/ 200 un',
 '7891234560004','PAF-004', 600,100,2000,  5.50,  3.00,'PACOTE',
 (SELECT "ID" FROM "CATEGORIAS" WHERE "NOME"='Parafusos e Porcas')),

('Parafuso Chipboard 4x40 Bicromatizado',
 'Parafuso chipboard cabeça chata 4x40 bicromatizado — caixa c/ 200',
 '7891234560005','PAF-005', 250, 50, 800, 22.00, 13.00,'CAIXA',
 (SELECT "ID" FROM "CATEGORIAS" WHERE "NOME"='Parafusos e Porcas')),

('Parafuso Sextavado M10x70',
 'Parafuso sextavado M10x70 zincado — caixa c/ 25 un',
 '7891234560006','PAF-006', 180, 30, 500, 28.00, 16.50,'CAIXA',
 (SELECT "ID" FROM "CATEGORIAS" WHERE "NOME"='Parafusos e Porcas')),

-- === FERRAMENTAS MANUAIS ===
('Martelo de Borracha 300g',
 'Martelo de borracha preta 300g cabo em madeira',
 '7891234561001','FMN-001',  47,  5, 200, 35.00, 20.00,'UNIDADE',
 (SELECT "ID" FROM "CATEGORIAS" WHERE "NOME"='Ferramentas Manuais')),

('Chave Phillips #2 200mm',
 'Chave de fenda Phillips #2 haste de 200mm aço cromo-vanádio',
 '7891234561002','FMN-002',  80, 10, 300, 12.00,  6.50,'UNIDADE',
 (SELECT "ID" FROM "CATEGORIAS" WHERE "NOME"='Ferramentas Manuais')),

('Alicate Universal 8"',
 'Alicate universal boca reta 8 polegadas aço inox',
 '7891234561003','FMN-003',  30,  5, 150, 45.00, 26.00,'UNIDADE',
 (SELECT "ID" FROM "CATEGORIAS" WHERE "NOME"='Ferramentas Manuais')),

('Nível de Bolha 60cm',
 'Nível de bolha alumínio 60cm 3 bolhas de precisão',
 '7891234561004','FMN-004',  25,  5, 100, 28.00, 16.00,'UNIDADE',
 (SELECT "ID" FROM "CATEGORIAS" WHERE "NOME"='Ferramentas Manuais')),

('Trena de Aço 5m',
 'Trena de aço fita 25mm com trava e gancho 5 metros',
 '7891234561005','FMN-005',  60, 10, 200, 22.00, 12.00,'UNIDADE',
 (SELECT "ID" FROM "CATEGORIAS" WHERE "NOME"='Ferramentas Manuais')),

('Colher de Pedreiro 9"',
 'Colher de pedreiro inox 9 polegadas cabo plástico antiderrapante',
 '7891234561006','FMN-006',  55, 10, 200, 18.00, 10.00,'UNIDADE',
 (SELECT "ID" FROM "CATEGORIAS" WHERE "NOME"='Ferramentas Manuais')),

('Espátula Aço 3"',
 'Espátula de aço inox 3 polegadas para massa corrida e texturas',
 '7891234561007','FMN-007',  70, 10, 250, 14.00,  7.50,'UNIDADE',
 (SELECT "ID" FROM "CATEGORIAS" WHERE "NOME"='Ferramentas Manuais')),

-- === FERRAMENTAS ELÉTRICAS ===
('Furadeira de Impacto 750W',
 'Furadeira de impacto 750W 13mm bivolt com maleta e acessórios',
 '7891234562001','FEL-001',  12,  3,  50,289.00,170.00,'UNIDADE',
 (SELECT "ID" FROM "CATEGORIAS" WHERE "NOME"='Ferramentas Elétricas')),

('Parafusadeira a Bateria 18V',
 'Parafusadeira/furadeira a bateria 18V 13mm 2 baterias e carregador',
 '7891234562002','FEL-002',   8, 10,  30,389.00,228.00,'UNIDADE',
 (SELECT "ID" FROM "CATEGORIAS" WHERE "NOME"='Ferramentas Elétricas')),

('Lixadeira Orbital 300W',
 'Lixadeira orbital 300W base 115x115mm bivolt com coletor de pó',
 '7891234562003','FEL-003',   6,  8,  30,189.00,110.00,'UNIDADE',
 (SELECT "ID" FROM "CATEGORIAS" WHERE "NOME"='Ferramentas Elétricas')),

('Serra Circular 1400W 7.1/4"',
 'Serra circular 1400W disco 7 1/4 polegadas bivolt com guia paralelo',
 '7891234562004','FEL-004',   3,  8,  20,459.00,268.00,'UNIDADE',
 (SELECT "ID" FROM "CATEGORIAS" WHERE "NOME"='Ferramentas Elétricas')),

('Esmerilhadeira Angular 900W 4.1/2"',
 'Esmerilhadeira angular 900W disco 4.1/2 polegadas bivolt',
 '7891234562005','FEL-005',  10,  3,  40,249.00,146.00,'UNIDADE',
 (SELECT "ID" FROM "CATEGORIAS" WHERE "NOME"='Ferramentas Elétricas')),

-- === TINTAS E VERNIZES ===
('Tinta Acrílica Branca 18L',
 'Tinta acrílica premium fosca branco gelo 18 litros — uso interno/externo',
 '7891234563001','TIN-001',  43, 10, 150,189.00,110.00,'UNIDADE',
 (SELECT "ID" FROM "CATEGORIAS" WHERE "NOME"='Tintas e Vernizes')),

('Tinta Esmalte Cinza Médio 3.6L',
 'Esmalte sintético brilhante cinza médio 3.6 litros — ferro e madeira',
 '7891234563002','TIN-002',  30,  8, 100, 65.00, 38.00,'UNIDADE',
 (SELECT "ID" FROM "CATEGORIAS" WHERE "NOME"='Tintas e Vernizes')),

('Verniz Marítimo Brilhante 900ml',
 'Verniz marítimo brilhante resistente UV 900ml — uso externo',
 '7891234563003','TIN-003',  20,  5,  80, 55.00, 32.00,'UNIDADE',
 (SELECT "ID" FROM "CATEGORIAS" WHERE "NOME"='Tintas e Vernizes')),

('Primer Spray Cinza 400ml',
 'Primer spray cinza auto nivelante 400ml secagem rápida — multipropósito',
 '7891234563004','TIN-004',  50, 10, 200, 28.00, 16.00,'UNIDADE',
 (SELECT "ID" FROM "CATEGORIAS" WHERE "NOME"='Tintas e Vernizes')),

('Massa Corrida PVA 25kg',
 'Massa corrida PVA para interior 25kg balde — rendimento 80m²/demão',
 '7891234563005','TIN-005',  25,  5,  80,125.00, 73.00,'UNIDADE',
 (SELECT "ID" FROM "CATEGORIAS" WHERE "NOME"='Tintas e Vernizes')),

-- === HIDRÁULICA ===
('Tubo PVC Soldável 25mm 6m',
 'Tubo PVC rígido soldável 25mm barra 6 metros PN 15 água fria',
 '7891234564001','HID-001',  80, 15, 300, 32.00, 18.50,'UNIDADE',
 (SELECT "ID" FROM "CATEGORIAS" WHERE "NOME"='Hidráulica')),

('Registro de Gaveta Latão 1/2"',
 'Registro de gaveta latão cromado 1/2 polegada com volante',
 '7891234564002','HID-002',  35,  8, 120, 48.00, 28.00,'UNIDADE',
 (SELECT "ID" FROM "CATEGORIAS" WHERE "NOME"='Hidráulica')),

('Joelho PVC Soldável 25mm',
 'Joelho 90° PVC soldável 25mm — caixa c/ 50 unidades',
 '7891234564003','HID-003', 200, 30, 600, 15.00,  8.50,'CAIXA',
 (SELECT "ID" FROM "CATEGORIAS" WHERE "NOME"='Hidráulica')),

('Cano Galvanizado 1" 6m',
 'Cano galvanizado rosca BSP 1 polegada barra 6 metros',
 '7891234564004','HID-004',  30,  5, 100, 95.00, 55.00,'UNIDADE',
 (SELECT "ID" FROM "CATEGORIAS" WHERE "NOME"='Hidráulica')),

('Fita Veda Rosca 18mm 50m',
 'Fita veda rosca PTFE 18mm x 50 metros — alta resistência',
 '7891234564005','HID-005', 120, 20, 400,  8.00,  4.50,'UNIDADE',
 (SELECT "ID" FROM "CATEGORIAS" WHERE "NOME"='Hidráulica')),

-- === ELÉTRICA ===
('Fio Elétrico Flexível 2.5mm 100m',
 'Fio elétrico flexível 2.5mm² vermelho rolo 100 metros — ABNT NBR 6812',
 '7891234565001','ELE-001',  25,  5,  80,185.00,108.00,'ROLO',
 (SELECT "ID" FROM "CATEGORIAS" WHERE "NOME"='Elétrica')),

('Disjuntor Bipolar 32A',
 'Disjuntor termomagnético bipolar 32A curva C 220V — trilho DIN',
 '7891234565002','ELE-002',  40,  8, 150, 45.00, 26.00,'UNIDADE',
 (SELECT "ID" FROM "CATEGORIAS" WHERE "NOME"='Elétrica')),

('Tomada 2P+T 10A',
 'Tomada 2P+T 10A com aterramento padrão NBR 14136',
 '7891234565003','ELE-003',  90, 15, 300, 12.00,  6.80,'UNIDADE',
 (SELECT "ID" FROM "CATEGORIAS" WHERE "NOME"='Elétrica')),

('Interruptor Simples 10A',
 'Interruptor de linha simples 10A 250V branco — padrão NBR 14136',
 '7891234565004','ELE-004', 100, 20, 400,  8.50,  4.80,'UNIDADE',
 (SELECT "ID" FROM "CATEGORIAS" WHERE "NOME"='Elétrica')),

('Quadro de Distribuição 12 DIN',
 'Quadro de distribuição de embutir 12 disjuntores DIN — com barramento',
 '7891234565005','ELE-005',  15,  3,  50,125.00, 73.00,'UNIDADE',
 (SELECT "ID" FROM "CATEGORIAS" WHERE "NOME"='Elétrica')),

-- === MADEIRAS E COMPENSADOS ===
('Compensado 12mm Pinus 2.20x1.10m',
 'Compensado estrutural pinus 12mm 2200x1100mm lixado — uso interno',
 '7891234566001','MAD-001',  40,  5, 150,145.00, 85.00,'UNIDADE',
 (SELECT "ID" FROM "CATEGORIAS" WHERE "NOME"='Madeiras e Compensados')),

('MDF Cru 15mm 2.75x1.84m',
 'MDF cru 15mm 2750x1840mm — chapa lixada em ambas as faces',
 '7891234566002','MAD-002',  20,  3,  60,220.00,128.00,'UNIDADE',
 (SELECT "ID" FROM "CATEGORIAS" WHERE "NOME"='Madeiras e Compensados')),

('Pinus Aparelhado 2.5x5cm 3m',
 'Pinus aparelhado 4 faces 2.5x5cm barra 3 metros — uso estrutural',
 '7891234566003','MAD-003', 150, 20, 500, 18.00, 10.00,'UNIDADE',
 (SELECT "ID" FROM "CATEGORIAS" WHERE "NOME"='Madeiras e Compensados')),

('Eucatex 3mm Chapa 2.44x1.22m',
 'Eucatex eucaplac madeira 3mm 2440x1220mm — acabamento e forro',
 '7891234566004','MAD-004',  30,  5, 100, 65.00, 38.00,'UNIDADE',
 (SELECT "ID" FROM "CATEGORIAS" WHERE "NOME"='Madeiras e Compensados')),

-- === CIMENTO E ARGAMASSA ===
('Cimento CP-II 32 50kg',
 'Cimento Portland Composto CP-II 32 saco 50kg — uso geral',
 '7891234567001','CIM-001', 200, 30, 800, 38.00, 22.00,'UNIDADE',
 (SELECT "ID" FROM "CATEGORIAS" WHERE "NOME"='Cimento e Argamassa')),

('Argamassa AC-II 20kg',
 'Argamassa colante AC-II para assentamento de cerâmica saco 20kg',
 '7891234567002','CIM-002', 150, 20, 500, 28.00, 16.00,'PACOTE',
 (SELECT "ID" FROM "CATEGORIAS" WHERE "NOME"='Cimento e Argamassa')),

('Rejunte Cinza Chumbo 1kg',
 'Rejunte em pó cinza chumbo para piso e parede 1kg — resistente à umidade',
 '7891234567003','CIM-003',  80, 15, 300, 12.00,  7.00,'UNIDADE',
 (SELECT "ID" FROM "CATEGORIAS" WHERE "NOME"='Cimento e Argamassa')),

('Concreto Pré-Misturado 40kg',
 'Concreto pré-misturado traço 1:3 saco 40kg — uso em fundações',
 '7891234567004','CIM-004',  60, 10, 200, 45.00, 26.00,'PACOTE',
 (SELECT "ID" FROM "CATEGORIAS" WHERE "NOME"='Cimento e Argamassa')),

-- === EPI ===
('Capacete de Segurança ABA Frontal',
 'Capacete ABA frontal classe A/B HDPE branco com carneira ajustável CA 31469',
 '7891234568001','EPI-001',  45, 10, 200, 25.00, 14.50,'UNIDADE',
 (SELECT "ID" FROM "CATEGORIAS" WHERE "NOME"='EPI')),

('Luvas de Raspa Boi Punho 10"',
 'Luvas de raspa de boi punho de 10 polegadas — proteção mecânica CA 11068',
 '7891234568002','EPI-002',  60, 10, 250, 18.00, 10.00,'PAR',
 (SELECT "ID" FROM "CATEGORIAS" WHERE "NOME"='EPI')),

('Óculos de Proteção Incolor',
 'Óculos de proteção anti-risco lente incolor CA 26126 — ampla visão',
 '7891234568003','EPI-003',  80, 15, 300, 15.00,  8.50,'UNIDADE',
 (SELECT "ID" FROM "CATEGORIAS" WHERE "NOME"='EPI')),

('Protetor Auditivo Plug 25dB',
 'Protetor auditivo tipo plug espuma moldável NRR 25dB — par CA 5674',
 '7891234568004','EPI-004', 100, 20, 400,  8.00,  4.50,'PAR',
 (SELECT "ID" FROM "CATEGORIAS" WHERE "NOME"='EPI')),

-- === JARDIM E PAISAGISMO ===
('Mangueira PVC Bicolor 1/2" 25m',
 'Mangueira PVC bicolor 1/2 polegada 25 metros enrolada — 3 camadas',
 '7891234569001','JAR-001',  35,  8, 120, 68.00, 39.00,'ROLO',
 (SELECT "ID" FROM "CATEGORIAS" WHERE "NOME"='Jardim e Paisagismo')),

('Tesoura de Poda 8" Aço Carbono',
 'Tesoura de poda aço carbono 8 polegadas anti-oxidante cabo ergonômico',
 '7891234569002','JAR-002',  20,  5,  80, 45.00, 26.00,'UNIDADE',
 (SELECT "ID" FROM "CATEGORIAS" WHERE "NOME"='Jardim e Paisagismo')),

('Regador Plástico 10L',
 'Regador plástico resistente UV 10 litros com crivo removível',
 '7891234569003','JAR-003',  25,  5,  80, 32.00, 18.50,'UNIDADE',
 (SELECT "ID" FROM "CATEGORIAS" WHERE "NOME"='Jardim e Paisagismo')),

-- === CONSTRUÇÃO CIVIL ===
('Tela de Alambrado 50x50mm 2m',
 'Tela alambrado galvanizado fio 12 malha 50x50mm largura 2m — por metro',
 '7891234570001','OBR-001', 300, 50,1000,  8.50,  4.80,'METRO',
 (SELECT "ID" FROM "CATEGORIAS" WHERE "NOME"='Construção Civil')),

('Arame Recozido 1.60mm',
 'Arame recozido trefilado 1.60mm para amarração — rolo 1kg',
 '7891234570002','OBR-002', 150, 30, 600, 12.00,  7.00,'QUILOGRAMA',
 (SELECT "ID" FROM "CATEGORIAS" WHERE "NOME"='Construção Civil')),

('Prego com Cabeça 13x15',
 'Prego aço polido com cabeça 13x15mm — pacote 1kg',
 '7891234570003','OBR-003', 200, 50, 800,  8.00,  4.50,'QUILOGRAMA',
 (SELECT "ID" FROM "CATEGORIAS" WHERE "NOME"='Construção Civil')),

-- === ILUMINAÇÃO ===
('Lâmpada LED Bulbo 9W E27 Bivolt',
 'Lâmpada LED bulbo 9W E27 6500K luz branca fria bivolt — 810 lúmens',
 '7891234571001','ILU-001', 120, 20, 500, 18.00, 10.00,'UNIDADE',
 (SELECT "ID" FROM "CATEGORIAS" WHERE "NOME"='Iluminação')),

('Luminária Sobrepor LED 40W',
 'Luminária sobrepor LED 40W 4000K branco neutro 120cm bivolt — IP20',
 '7891234571002','ILU-002',  30, 10,  80, 85.00, 49.00,'UNIDADE',
 (SELECT "ID" FROM "CATEGORIAS" WHERE "NOME"='Iluminação'))

ON CONFLICT ("SKU") DO NOTHING;

-- ============================================================
-- MOVIMENTACOES_ESTOQUE
-- Aviso: re-executar este bloco em banco existente vai
--        duplicar movimentações. Use apenas em banco limpo.
-- ============================================================

-- ============================================================
-- BLOCO A — Compras iniciais (abertura de estoque)
-- ============================================================

INSERT INTO "MOVIMENTACOES_ESTOQUE"
    ("TIPO_MOVIMENTACAO","DIRECAO","QUANTIDADE","CUSTO_UNITARIO",
     "ESTOQUE_ANTES","ESTOQUE_DEPOIS","MOTIVO","DOCUMENTO_REFERENCIA",
     "DATA_CRIACAO","ID_PRODUTO","ID_FORNECEDOR")
SELECT
    'ENTRADA_COMPRA','ENTRADA', v.qtd, v.custo,
    0, v.qtd,
    'Compra inicial — abertura de estoque', v.nf,
    NOW() - INTERVAL '1 day' * v.dias,
    p."ID", f."ID"
FROM (VALUES
    ('PAF-001', 600,  5.50::NUMERIC, 'NF-2024/001', 180, '11.222.333/0001-44'),
    ('PAF-002', 370, 11.00::NUMERIC, 'NF-2024/001', 178, '11.222.333/0001-44'),
    ('PAF-003', 500,  7.20::NUMERIC, 'NF-2024/001', 178, '11.222.333/0001-44'),
    ('PAF-004', 700,  3.00::NUMERIC, 'NF-2024/001', 176, '11.222.333/0001-44'),
    ('PAF-005', 300, 13.00::NUMERIC, 'NF-2024/001', 176, '11.222.333/0001-44'),
    ('PAF-006', 200, 16.50::NUMERIC, 'NF-2024/002', 175, '11.222.333/0001-44'),
    ('FMN-001',  60, 20.00::NUMERIC, 'NF-2024/010', 170, '88.999.000/0001-11'),
    ('FMN-002', 100,  6.50::NUMERIC, 'NF-2024/010', 170, '88.999.000/0001-11'),
    ('FMN-003',  40, 26.00::NUMERIC, 'NF-2024/010', 168, '88.999.000/0001-11'),
    ('FMN-004',  30, 16.00::NUMERIC, 'NF-2024/010', 168, '88.999.000/0001-11'),
    ('FMN-005',  80, 12.00::NUMERIC, 'NF-2024/010', 166, '88.999.000/0001-11'),
    ('FMN-006',  70, 10.00::NUMERIC, 'NF-2024/011', 165, '88.999.000/0001-11'),
    ('FMN-007',  90,  7.50::NUMERIC, 'NF-2024/011', 164, '88.999.000/0001-11'),
    ('FEL-001',  20,170.00::NUMERIC, 'NF-2024/020', 160, '88.999.000/0001-11'),
    ('FEL-002',  15,228.00::NUMERIC, 'NF-2024/020', 158, '88.999.000/0001-11'),
    ('FEL-003',  10,110.00::NUMERIC, 'NF-2024/020', 156, '88.999.000/0001-11'),
    ('FEL-004',   8,268.00::NUMERIC, 'NF-2024/020', 155, '88.999.000/0001-11'),
    ('FEL-005',  15,146.00::NUMERIC, 'NF-2024/021', 154, '88.999.000/0001-11'),
    ('TIN-001',  60,110.00::NUMERIC, 'NF-2024/030', 150, '66.777.888/0001-99'),
    ('TIN-002',  50, 38.00::NUMERIC, 'NF-2024/030', 148, '66.777.888/0001-99'),
    ('TIN-003',  30, 32.00::NUMERIC, 'NF-2024/030', 146, '66.777.888/0001-99'),
    ('TIN-004',  70, 16.00::NUMERIC, 'NF-2024/031', 145, '66.777.888/0001-99'),
    ('TIN-005',  35, 73.00::NUMERIC, 'NF-2024/031', 144, '66.777.888/0001-99'),
    ('HID-001', 100, 18.50::NUMERIC, 'NF-2024/040', 140, '44.555.666/0001-77'),
    ('HID-002',  50, 28.00::NUMERIC, 'NF-2024/040', 138, '44.555.666/0001-77'),
    ('HID-003', 250,  8.50::NUMERIC, 'NF-2024/040', 136, '44.555.666/0001-77'),
    ('HID-004',  40, 55.00::NUMERIC, 'NF-2024/041', 135, '44.555.666/0001-77'),
    ('HID-005', 150,  4.50::NUMERIC, 'NF-2024/041', 134, '44.555.666/0001-77'),
    ('ELE-001',  35,108.00::NUMERIC, 'NF-2024/050', 130, '33.444.555/0001-66'),
    ('ELE-002',  60, 26.00::NUMERIC, 'NF-2024/050', 128, '33.444.555/0001-66'),
    ('ELE-003', 120,  6.80::NUMERIC, 'NF-2024/050', 126, '33.444.555/0001-66'),
    ('ELE-004', 150,  4.80::NUMERIC, 'NF-2024/051', 125, '33.444.555/0001-66'),
    ('ELE-005',  20, 73.00::NUMERIC, 'NF-2024/051', 124, '33.444.555/0001-66'),
    ('MAD-001',  50, 85.00::NUMERIC, 'NF-2024/060', 120, '55.666.777/0001-88'),
    ('MAD-002',  30,128.00::NUMERIC, 'NF-2024/060', 118, '55.666.777/0001-88'),
    ('MAD-003', 200, 10.00::NUMERIC, 'NF-2024/060', 116, '55.666.777/0001-88'),
    ('MAD-004',  40, 38.00::NUMERIC, 'NF-2024/061', 115, '55.666.777/0001-88'),
    ('CIM-001', 250, 22.00::NUMERIC, 'NF-2024/070', 110, '21.222.333/0001-44'),
    ('CIM-002', 180, 16.00::NUMERIC, 'NF-2024/070', 108, '21.222.333/0001-44'),
    ('CIM-003', 100,  7.00::NUMERIC, 'NF-2024/070', 106, '21.222.333/0001-44'),
    ('CIM-004',  80, 26.00::NUMERIC, 'NF-2024/071', 105, '21.222.333/0001-44'),
    ('EPI-001',  60, 14.50::NUMERIC, 'NF-2024/080', 100, '77.888.999/0001-00'),
    ('EPI-002',  80, 10.00::NUMERIC, 'NF-2024/080',  98, '77.888.999/0001-00'),
    ('EPI-003', 100,  8.50::NUMERIC, 'NF-2024/080',  96, '77.888.999/0001-00'),
    ('EPI-004', 120,  4.50::NUMERIC, 'NF-2024/081',  95, '77.888.999/0001-00'),
    ('JAR-001',  50, 39.00::NUMERIC, 'NF-2024/090',  90, '10.111.222/0001-33'),
    ('JAR-002',  30, 26.00::NUMERIC, 'NF-2024/090',  88, '10.111.222/0001-33'),
    ('JAR-003',  35, 18.50::NUMERIC, 'NF-2024/090',  86, '10.111.222/0001-33'),
    ('OBR-001', 300,  4.80::NUMERIC, 'NF-2024/100',  85, '22.333.444/0001-55'),
    ('OBR-002', 150,  7.00::NUMERIC, 'NF-2024/100',  84, '22.333.444/0001-55'),
    ('OBR-003', 200,  4.50::NUMERIC, 'NF-2024/100',  82, '22.333.444/0001-55'),
    ('ILU-001', 150, 10.00::NUMERIC, 'NF-2024/110',  80, '99.000.111/0001-22'),
    ('ILU-002',  40, 49.00::NUMERIC, 'NF-2024/110',  78, '99.000.111/0001-22')
) AS v(sku, qtd, custo, nf, dias, cnpj_forn)
JOIN "PRODUTOS"     p ON p."SKU"  = v.sku
JOIN "FORNECEDORES" f ON f."CNPJ" = v.cnpj_forn;

-- ============================================================
-- BLOCO B — Vendas (saídas de venda — primeiro lote)
-- ============================================================

INSERT INTO "MOVIMENTACOES_ESTOQUE"
    ("TIPO_MOVIMENTACAO","DIRECAO","QUANTIDADE","PRECO_UNITARIO",
     "ESTOQUE_ANTES","ESTOQUE_DEPOIS","MOTIVO","DOCUMENTO_REFERENCIA",
     "DATA_CRIACAO","ID_PRODUTO")
SELECT
    'SAIDA_VENDA','SAIDA', v.qtd, v.preco,
    v.antes, v.depois,
    'Venda balcão', v.pdv,
    NOW() - INTERVAL '1 day' * v.dias,
    p."ID"
FROM (VALUES
    ('PAF-001', 100,  8.90::NUMERIC,  600, 500, 'PDV-2024/0101',  90),
    ('PAF-002',  50, 18.50::NUMERIC,  370, 320, 'PDV-2024/0102',  88),
    ('PAF-003', 100, 12.00::NUMERIC,  500, 400, 'PDV-2024/0103',  86),
    ('PAF-004', 100,  5.50::NUMERIC,  700, 600, 'PDV-2024/0104',  84),
    ('PAF-005',  50, 22.00::NUMERIC,  300, 250, 'PDV-2024/0105',  82),
    ('PAF-006',  20, 28.00::NUMERIC,  200, 180, 'PDV-2024/0106',  80),
    ('FMN-001',  15, 35.00::NUMERIC,   60,  45, 'PDV-2024/0201',  75),
    ('FMN-002',  20, 12.00::NUMERIC,  100,  80, 'PDV-2024/0202',  73),
    ('FMN-003',  10, 45.00::NUMERIC,   40,  30, 'PDV-2024/0203',  71),
    ('FMN-004',   5, 28.00::NUMERIC,   30,  25, 'PDV-2024/0204',  69),
    ('FMN-005',  20, 22.00::NUMERIC,   80,  60, 'PDV-2024/0205',  67),
    ('FMN-006',  15, 18.00::NUMERIC,   70,  55, 'PDV-2024/0206',  65),
    ('FMN-007',  20, 14.00::NUMERIC,   90,  70, 'PDV-2024/0207',  63),
    ('FEL-001',   8,289.00::NUMERIC,   20,  12, 'PDV-2024/0301',  60),
    ('FEL-002',   7,389.00::NUMERIC,   15,   8, 'PDV-2024/0302',  58),
    ('FEL-003',   4,189.00::NUMERIC,   10,   6, 'PDV-2024/0303',  56),
    ('FEL-004',   3,459.00::NUMERIC,    8,   5, 'PDV-2024/0304',  55),
    ('FEL-005',   5,249.00::NUMERIC,   15,  10, 'PDV-2024/0305',  53),
    ('TIN-001',  17,189.00::NUMERIC,   60,  43, 'PDV-2024/0401',  50),
    ('TIN-002',  20, 65.00::NUMERIC,   50,  30, 'PDV-2024/0402',  48),
    ('TIN-003',  10, 55.00::NUMERIC,   30,  20, 'PDV-2024/0403',  46),
    ('TIN-004',  20, 28.00::NUMERIC,   70,  50, 'PDV-2024/0404',  44),
    ('TIN-005',  10,125.00::NUMERIC,   35,  25, 'PDV-2024/0405',  42),
    ('HID-001',  20, 32.00::NUMERIC,  100,  80, 'PDV-2024/0501',  40),
    ('HID-002',  15, 48.00::NUMERIC,   50,  35, 'PDV-2024/0502',  38),
    ('HID-003',  50, 15.00::NUMERIC,  250, 200, 'PDV-2024/0503',  36),
    ('HID-004',  10, 95.00::NUMERIC,   40,  30, 'PDV-2024/0504',  34),
    ('HID-005',  30,  8.00::NUMERIC,  150, 120, 'PDV-2024/0505',  32),
    ('ELE-001',  10,185.00::NUMERIC,   35,  25, 'PDV-2024/0601',  30),
    ('ELE-002',  20, 45.00::NUMERIC,   60,  40, 'PDV-2024/0602',  28),
    ('ELE-003',  30, 12.00::NUMERIC,  120,  90, 'PDV-2024/0603',  26),
    ('ELE-004',  50,  8.50::NUMERIC,  150, 100, 'PDV-2024/0604',  24),
    ('ELE-005',   5,125.00::NUMERIC,   20,  15, 'PDV-2024/0605',  22),
    ('MAD-001',  10,145.00::NUMERIC,   50,  40, 'PDV-2024/0701',  20),
    ('MAD-002',  10,220.00::NUMERIC,   30,  20, 'PDV-2024/0702',  18),
    ('MAD-003',  50, 18.00::NUMERIC,  200, 150, 'PDV-2024/0703',  16),
    ('MAD-004',  10, 65.00::NUMERIC,   40,  30, 'PDV-2024/0704',  14),
    ('CIM-001',  50, 38.00::NUMERIC,  250, 200, 'PDV-2024/0801',  12),
    ('CIM-002',  30, 28.00::NUMERIC,  180, 150, 'PDV-2024/0802',  10),
    ('CIM-003',  20, 12.00::NUMERIC,  100,  80, 'PDV-2024/0803',   9),
    ('CIM-004',  20, 45.00::NUMERIC,   80,  60, 'PDV-2024/0804',   8),
    ('EPI-001',  15, 25.00::NUMERIC,   60,  45, 'PDV-2024/0901',   7),
    ('EPI-002',  20, 18.00::NUMERIC,   80,  60, 'PDV-2024/0902',   6),
    ('EPI-003',  20, 15.00::NUMERIC,  100,  80, 'PDV-2024/0903',   5),
    ('EPI-004',  20,  8.00::NUMERIC,  120, 100, 'PDV-2024/0904',   4),
    ('JAR-001',  15, 68.00::NUMERIC,   50,  35, 'PDV-2024/1001',   3),
    ('JAR-002',  10, 45.00::NUMERIC,   30,  20, 'PDV-2024/1002',   2),
    ('JAR-003',  10, 32.00::NUMERIC,   35,  25, 'PDV-2024/1003',   1)
) AS v(sku, qtd, preco, antes, depois, pdv, dias)
JOIN "PRODUTOS" p ON p."SKU" = v.sku;

-- ============================================================
-- BLOCO C — Vendas adicionais (produtos com maior giro)
-- ============================================================

INSERT INTO "MOVIMENTACOES_ESTOQUE"
    ("TIPO_MOVIMENTACAO","DIRECAO","QUANTIDADE","PRECO_UNITARIO",
     "ESTOQUE_ANTES","ESTOQUE_DEPOIS","MOTIVO","DOCUMENTO_REFERENCIA",
     "DATA_CRIACAO","ID_PRODUTO")
SELECT 'SAIDA_VENDA','SAIDA', v.qtd, v.preco, v.antes, v.depois,
       'Venda balcão — segundo lote', v.pdv,
       NOW() - INTERVAL '1 day' * v.dias,
       p."ID"
FROM (VALUES
    ('PAF-001',  50,  8.90::NUMERIC, 550, 500, 'PDV-2024/1101', 45),
    ('CIM-001',  30, 38.00::NUMERIC, 230, 200, 'PDV-2024/1201', 15),
    ('HID-003',  30, 15.00::NUMERIC, 230, 200, 'PDV-2024/1301', 20),
    ('ELE-003',  20, 12.00::NUMERIC, 110,  90, 'PDV-2024/1401', 10),
    ('MAD-003',  30, 18.00::NUMERIC, 180, 150, 'PDV-2024/1501', 11),
    ('EPI-003',  15, 15.00::NUMERIC,  95,  80, 'PDV-2024/1601',  6),
    ('PAF-003',  50, 12.00::NUMERIC, 450, 400, 'PDV-2024/1701', 30),
    ('TIN-001',  17,189.00::NUMERIC,  60,  43, 'PDV-2024/1801', 25),
    ('EPI-004',  20,  8.00::NUMERIC, 120, 100, 'PDV-2024/1901',  4),
    ('HID-001',  20, 32.00::NUMERIC, 100,  80, 'PDV-2024/2001', 20),
    ('OBR-001',  50,  8.50::NUMERIC, 300, 250, 'PDV-2024/2101', 17),
    ('OBR-003',  50,  8.00::NUMERIC, 200, 150, 'PDV-2024/2201', 14),
    ('ILU-001',  30, 18.00::NUMERIC, 150, 120, 'PDV-2024/2301', 12),
    ('ELE-002',  20, 45.00::NUMERIC,  60,  40, 'PDV-2024/2401',  9)
) AS v(sku, qtd, preco, antes, depois, pdv, dias)
JOIN "PRODUTOS" p ON p."SKU" = v.sku;

-- ============================================================
-- BLOCO D — Devoluções de clientes (ENTRADA_DEVOLUCAO)
-- ============================================================

INSERT INTO "MOVIMENTACOES_ESTOQUE"
    ("TIPO_MOVIMENTACAO","DIRECAO","QUANTIDADE","CUSTO_UNITARIO",
     "ESTOQUE_ANTES","ESTOQUE_DEPOIS","MOTIVO","DOCUMENTO_REFERENCIA",
     "DATA_CRIACAO","ID_PRODUTO")
VALUES
(
    'ENTRADA_DEVOLUCAO','ENTRADA', 2, 20.00,
    45, 47,
    'Devolução cliente — produto adquirido sem defeito, desistência',
    'DEV-2024/001',
    NOW() - INTERVAL '62 days',
    (SELECT "ID" FROM "PRODUTOS" WHERE "SKU" = 'FMN-001')
),
(
    'ENTRADA_DEVOLUCAO','ENTRADA', 3, 110.00,
    43, 46,
    'Devolução cliente — cor diferente do esperado',
    'DEV-2024/002',
    NOW() - INTERVAL '18 days',
    (SELECT "ID" FROM "PRODUTOS" WHERE "SKU" = 'TIN-001')
),
(
    'ENTRADA_DEVOLUCAO','ENTRADA', 1, 268.00,
    5, 6,
    'Devolução cliente — comprou modelo incorreto',
    'DEV-2024/003',
    NOW() - INTERVAL '7 days',
    (SELECT "ID" FROM "PRODUTOS" WHERE "SKU" = 'FEL-004')
);

-- Atualiza estoque com devoluções
UPDATE "PRODUTOS" SET "ESTOQUE_ATUAL" = 47 WHERE "SKU" = 'FMN-001';
UPDATE "PRODUTOS" SET "ESTOQUE_ATUAL" = 46 WHERE "SKU" = 'TIN-001';
UPDATE "PRODUTOS" SET "ESTOQUE_ATUAL" =  6 WHERE "SKU" = 'FEL-004';

-- ============================================================
-- BLOCO E — Ajuste de inventário positivo (ENTRADA_AJUSTE)
-- ============================================================

INSERT INTO "MOVIMENTACOES_ESTOQUE"
    ("TIPO_MOVIMENTACAO","DIRECAO","QUANTIDADE","CUSTO_UNITARIO",
     "ESTOQUE_ANTES","ESTOQUE_DEPOIS","MOTIVO","DOCUMENTO_REFERENCIA",
     "DATA_CRIACAO","ID_PRODUTO")
VALUES
(
    'ENTRADA_AJUSTE','ENTRADA', 20, 11.00,
    300, 320,
    'Ajuste inventário — divergência encontrada na contagem mensal',
    'AJU-2024/001',
    NOW() - INTERVAL '40 days',
    (SELECT "ID" FROM "PRODUTOS" WHERE "SKU" = 'PAF-002')
),
(
    'ENTRADA_AJUSTE','ENTRADA', 10, 8.50,
    70, 80,
    'Ajuste inventário — lote encontrado no armazém auxiliar',
    'AJU-2024/002',
    NOW() - INTERVAL '22 days',
    (SELECT "ID" FROM "PRODUTOS" WHERE "SKU" = 'EPI-003')
),
(
    'ENTRADA_AJUSTE','ENTRADA', 15, 26.00,
    60, 75,
    'Ajuste inventário — diferença apurada na contagem física',
    'AJU-2024/003',
    NOW() - INTERVAL '15 days',
    (SELECT "ID" FROM "PRODUTOS" WHERE "SKU" = 'FMN-003')
);

-- Atualiza estoque com ajustes de entrada
UPDATE "PRODUTOS" SET "ESTOQUE_ATUAL" = 320 WHERE "SKU" = 'PAF-002';
UPDATE "PRODUTOS" SET "ESTOQUE_ATUAL" =  80 WHERE "SKU" = 'EPI-003';
UPDATE "PRODUTOS" SET "ESTOQUE_ATUAL" =  75 WHERE "SKU" = 'FMN-003';

-- ============================================================
-- BLOCO F — Ajuste negativo / baixa (SAIDA_AJUSTE / SAIDA_BAIXA)
-- ============================================================

INSERT INTO "MOVIMENTACOES_ESTOQUE"
    ("TIPO_MOVIMENTACAO","DIRECAO","QUANTIDADE",
     "ESTOQUE_ANTES","ESTOQUE_DEPOIS","MOTIVO","DOCUMENTO_REFERENCIA",
     "DATA_CRIACAO","ID_PRODUTO")
VALUES
(
    'SAIDA_AJUSTE','SAIDA', 5,
    50, 45,
    'Ajuste negativo — capacetes com defeito de fabricação retirados',
    'AJU-2024/004',
    NOW() - INTERVAL '35 days',
    (SELECT "ID" FROM "PRODUTOS" WHERE "SKU" = 'EPI-001')
),
(
    'SAIDA_AJUSTE','SAIDA', 4,
    34, 30,
    'Ajuste negativo — diferença encontrada na contagem trimestral',
    'AJU-2024/005',
    NOW() - INTERVAL '12 days',
    (SELECT "ID" FROM "PRODUTOS" WHERE "SKU" = 'FMN-004')
),
(
    'SAIDA_BAIXA','SAIDA', 2,
    8, 6,
    'Baixa — produto danificado em queda de prateleira',
    'BAX-2024/001',
    NOW() - INTERVAL '8 days',
    (SELECT "ID" FROM "PRODUTOS" WHERE "SKU" = 'FEL-004')
),
(
    'SAIDA_BAIXA','SAIDA', 5,
    50, 45,
    'Baixa — embalagens danificadas por umidade no depósito',
    'BAX-2024/002',
    NOW() - INTERVAL '5 days',
    (SELECT "ID" FROM "PRODUTOS" WHERE "SKU" = 'TIN-004')
);

-- Atualiza estoque com saídas de ajuste e baixa
UPDATE "PRODUTOS" SET "ESTOQUE_ATUAL" = 45 WHERE "SKU" = 'EPI-001';
UPDATE "PRODUTOS" SET "ESTOQUE_ATUAL" = 30 WHERE "SKU" = 'FMN-004';
UPDATE "PRODUTOS" SET "ESTOQUE_ATUAL" =  4 WHERE "SKU" = 'FEL-004';
UPDATE "PRODUTOS" SET "ESTOQUE_ATUAL" = 45 WHERE "SKU" = 'TIN-004';

-- ============================================================
-- BLOCO G — Reposição de estoque (segunda compra)
-- ============================================================

INSERT INTO "MOVIMENTACOES_ESTOQUE"
    ("TIPO_MOVIMENTACAO","DIRECAO","QUANTIDADE","CUSTO_UNITARIO",
     "ESTOQUE_ANTES","ESTOQUE_DEPOIS","MOTIVO","DOCUMENTO_REFERENCIA",
     "DATA_CRIACAO","ID_PRODUTO","ID_FORNECEDOR")
SELECT
    'ENTRADA_COMPRA','ENTRADA', v.qtd, v.custo,
    v.antes, v.depois,
    'Reposição de estoque — segunda compra', v.nf,
    NOW() - INTERVAL '1 day' * v.dias,
    p."ID", f."ID"
FROM (VALUES
    ('ELE-001',  15,108.00::NUMERIC,  25,  40, 'NF-2024/201', 5, '33.444.555/0001-66'),
    ('FEL-005',  10,146.00::NUMERIC,  10,  20, 'NF-2024/202', 4, '88.999.000/0001-11'),
    ('CIM-001',  50, 22.00::NUMERIC, 200, 250, 'NF-2024/203', 3, '21.222.333/0001-44'),
    ('PAF-004',  50,  3.00::NUMERIC, 600, 650, 'NF-2024/204', 2, '11.222.333/0001-44'),
    ('HID-005',  30,  4.50::NUMERIC, 120, 150, 'NF-2024/205', 1, '44.555.666/0001-77'),
    ('ILU-001',  30, 10.00::NUMERIC, 120, 150, 'NF-2024/206', 2, '99.000.111/0001-22'),
    ('OBR-001', 100,  4.80::NUMERIC, 250, 350, 'NF-2024/207', 1, '22.333.444/0001-55')
) AS v(sku, qtd, custo, antes, depois, nf, dias, cnpj_forn)
JOIN "PRODUTOS"     p ON p."SKU"  = v.sku
JOIN "FORNECEDORES" f ON f."CNPJ" = v.cnpj_forn;

-- Atualiza estoque com reposições
UPDATE "PRODUTOS" SET "ESTOQUE_ATUAL" =  40 WHERE "SKU" = 'ELE-001';
UPDATE "PRODUTOS" SET "ESTOQUE_ATUAL" =  20 WHERE "SKU" = 'FEL-005';
UPDATE "PRODUTOS" SET "ESTOQUE_ATUAL" = 250 WHERE "SKU" = 'CIM-001';
UPDATE "PRODUTOS" SET "ESTOQUE_ATUAL" = 650 WHERE "SKU" = 'PAF-004';
UPDATE "PRODUTOS" SET "ESTOQUE_ATUAL" = 150 WHERE "SKU" = 'HID-005';
UPDATE "PRODUTOS" SET "ESTOQUE_ATUAL" = 150 WHERE "SKU" = 'ILU-001';
UPDATE "PRODUTOS" SET "ESTOQUE_ATUAL" = 350 WHERE "SKU" = 'OBR-001';

-- ============================================================
-- FIM DO SCRIPT
--
-- Totais inseridos (banco limpo):
--   Categorias    : 15
--   Fornecedores  : 12
--   Produtos      : 50
--   Movimentações : ~130
--     Bloco A (compras iniciais) : 53
--     Bloco B (vendas lote 1)    : 47
--     Bloco C (vendas lote 2)    : 14
--     Bloco D (devoluções)       :  3
--     Bloco E (ajustes entrada)  :  3
--     Bloco F (ajustes saída)    :  4
--     Bloco G (reposições)       :  7
-- ============================================================
