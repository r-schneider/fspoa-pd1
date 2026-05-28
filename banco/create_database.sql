-- ============================================================
--  Ferragem Pro — Script de Criação do Banco de Dados
--  PostgreSQL 14+
--  Execute como superusuário ou com permissões de CREATE
-- ============================================================

-- Criação do banco (opcional — execute separado se necessário)
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
-- TABELA: USUARIOS
-- ============================================================

CREATE TABLE IF NOT EXISTS "USUARIOS" (
    "ID"              SERIAL PRIMARY KEY,
    "NOME"            VARCHAR(200)  NOT NULL,
    "EMAIL"           VARCHAR(254)  NOT NULL UNIQUE,
    "SENHA_HASH"      VARCHAR(255)  NOT NULL,
    "ATIVO"           BOOLEAN       NOT NULL DEFAULT TRUE,
    "DATA_CRIACAO"    TIMESTAMP     NOT NULL DEFAULT NOW(),
    "DATA_ATUALIZACAO" TIMESTAMP    NOT NULL DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_usuarios_email ON "USUARIOS" ("EMAIL");

-- ============================================================
-- TABELA: CATEGORIAS
-- ============================================================

CREATE TABLE IF NOT EXISTS "CATEGORIAS" (
    "ID"              SERIAL PRIMARY KEY,
    "NOME"            VARCHAR(100)  NOT NULL UNIQUE,
    "DESCRICAO"       TEXT,
    "ATIVO"           BOOLEAN       NOT NULL DEFAULT TRUE,
    "DATA_CRIACAO"    TIMESTAMP     NOT NULL DEFAULT NOW(),
    "DATA_ATUALIZACAO" TIMESTAMP    NOT NULL DEFAULT NOW()
);

-- ============================================================
-- TABELA: PRODUTOS
-- ============================================================

CREATE TABLE IF NOT EXISTS "PRODUTOS" (
    "ID"              SERIAL PRIMARY KEY,
    "NOME"            VARCHAR(200)  NOT NULL,
    "DESCRICAO"       TEXT,
    "CODIGO_BARRAS"   VARCHAR(50)   UNIQUE,
    "SKU"             VARCHAR(50)   NOT NULL UNIQUE,
    "ESTOQUE_ATUAL"   INTEGER       NOT NULL DEFAULT 0,
    "ESTOQUE_MINIMO"  INTEGER       NOT NULL DEFAULT 0,
    "ESTOQUE_MAXIMO"  INTEGER,
    "PRECO_VENDA"     NUMERIC(10,2) NOT NULL,
    "PRECO_CUSTO"     NUMERIC(10,2),
    "UNIDADE_MEDIDA"  unit_measure_enum NOT NULL,
    "ATIVO"           BOOLEAN       NOT NULL DEFAULT TRUE,
    "URL_IMAGEM"      VARCHAR(500),
    "DATA_CRIACAO"    TIMESTAMP     NOT NULL DEFAULT NOW(),
    "DATA_ATUALIZACAO" TIMESTAMP    NOT NULL DEFAULT NOW(),
    "ID_CATEGORIA"    INTEGER REFERENCES "CATEGORIAS"("ID") ON DELETE SET NULL
);

CREATE INDEX IF NOT EXISTS idx_produtos_sku        ON "PRODUTOS" ("SKU");
CREATE INDEX IF NOT EXISTS idx_produtos_categoria  ON "PRODUTOS" ("ID_CATEGORIA");
CREATE INDEX IF NOT EXISTS idx_produtos_ativo      ON "PRODUTOS" ("ATIVO");

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
    "ID_USUARIO"           INTEGER       REFERENCES "USUARIOS"("ID") ON DELETE SET NULL
);

CREATE INDEX IF NOT EXISTS idx_mov_produto    ON "MOVIMENTACOES_ESTOQUE" ("ID_PRODUTO");
CREATE INDEX IF NOT EXISTS idx_mov_usuario    ON "MOVIMENTACOES_ESTOQUE" ("ID_USUARIO");
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

-- Trigger em USUARIOS
DROP TRIGGER IF EXISTS trg_usuarios_update ON "USUARIOS";
CREATE TRIGGER trg_usuarios_update
    BEFORE UPDATE ON "USUARIOS"
    FOR EACH ROW EXECUTE FUNCTION fn_update_timestamp();

-- Trigger em CATEGORIAS
DROP TRIGGER IF EXISTS trg_categorias_update ON "CATEGORIAS";
CREATE TRIGGER trg_categorias_update
    BEFORE UPDATE ON "CATEGORIAS"
    FOR EACH ROW EXECUTE FUNCTION fn_update_timestamp();

-- Trigger em PRODUTOS
DROP TRIGGER IF EXISTS trg_produtos_update ON "PRODUTOS";
CREATE TRIGGER trg_produtos_update
    BEFORE UPDATE ON "PRODUTOS"
    FOR EACH ROW EXECUTE FUNCTION fn_update_timestamp();

-- ============================================================
-- DADOS INICIAIS: Categorias padrão para ferragens
-- ============================================================

INSERT INTO "CATEGORIAS" ("NOME", "DESCRICAO") VALUES
    ('Parafusos e Porcas',  'Parafusos, porcas, arruelas e fixadores em geral'),
    ('Ferramentas Manuais', 'Martelos, chaves, alicates, serras e similares'),
    ('Ferramentas Elétricas','Furadeiras, esmerilhadeiras, parafusadeiras etc.'),
    ('Tintas e Vernizes',   'Tintas, vernizes, primers e complementos'),
    ('Hidráulica',          'Conexões, tubos, registros e materiais hidráulicos'),
    ('Elétrica',            'Cabos, disjuntores, tomadas e materiais elétricos'),
    ('Madeiras e Compensados','Tábuas, compensados, MDF e similares'),
    ('Cimento e Argamassa', 'Cimentos, argamassas, rejuntes e concretos'),
    ('EPI',                 'Equipamentos de Proteção Individual'),
    ('Outros',              'Demais produtos')
ON CONFLICT ("NOME") DO NOTHING;

-- ============================================================
-- USUÁRIO ADMIN PADRÃO
-- Senha: admin123  (hash bcrypt — troque em produção!)
-- ============================================================

INSERT INTO "USUARIOS" ("NOME", "EMAIL", "SENHA_HASH") VALUES (
    'Administrador',
    'admin@ferragempro.com',
    '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQyCgd8C2bSMnHjsJxgCqBjUy'
) ON CONFLICT ("EMAIL") DO NOTHING;

-- ============================================================
-- FIM DO SCRIPT
-- ============================================================
