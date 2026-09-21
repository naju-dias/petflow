-- ============================================================
-- PETFLOW
-- Criação dos schemas do projeto
-- ============================================================

-- STAGING
-- Camada utilizada para receber os dados da fonte.
CREATE SCHEMA IF NOT EXISTS staging;


-- WAREHOUSE
-- Camada onde ficará nosso modelo dimensional.
CREATE SCHEMA IF NOT EXISTS warehouse;


-- ANALYTICS
-- Camada destinada às tabelas analíticas utilizadas pelo negócio e pelo Power BI.
CREATE SCHEMA IF NOT EXISTS analytics;