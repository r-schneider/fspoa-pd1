content = """# 📄 Status Report – Sprint 2

## 👥 Equipe

* **Nome do projeto:** StockMaster
* **Integrantes:** Mauricio T. Welter, Vítor Saraiva de Souza, Leandro Mandela, Nicollas G. Garcia e Rodrigo Monte
* **Scrum Master da Sprint:** Vítor Saraiva de Souza
* **Product Owner:** Mauricio T. Welter

---

## 📅 Informações da Sprint

* **Número da Sprint:** 2
* **Período:** 08/05 – 22/05 (Estimado)
* **Objetivo da Sprint:**
> Implementar a lógica de leitura de códigos de barras via mobile e integrar o sistema de notificações automáticas via WhatsApp.

---

## 📌 1. Resumo Executivo

Nesta sprint, o foco saiu da modelagem e entrou na funcionalidade operacional. Conseguimos integrar a biblioteca de leitura de câmera para reconhecer os códigos de barras dos produtos da União das Ferragens. Também estruturamos a API de mensageria para os alertas de estoque mínimo. O maior desafio foi a calibração do scanner para ambientes com pouca luz, comum no depósito do Sr. Valdir.

* **A sprint foi:**
    * (X) Concluída com sucesso
    * ( ) Parcialmente concluída
    * ( ) Não concluída

* **Principais entregas:**
    * Módulo de Leitura de Código de Barras (Scanner Mobile)
    * Integração com API de WhatsApp para Alertas
    * Refinamento da tabela de `notificacoes` no banco de dados

* **Principais dificuldades:**
    * Latência na resposta da API de notificações.
    * Ajuste de foco da câmera em códigos de barras danificados ou pequenos.

---

## ✅ 2. Itens Planejados vs Entregues

| User Story / Tarefa | Responsável | Story Points | Status | Observações |
| :--- | :--- | :--- | :--- | :--- |
| US05 – Scanner Mobile | Mauricio | 8 | 🟢 | Funcional em Android e iOS |
| US06 – Disparo WhatsApp | Leandro | 5 | 🟢 | Alerta de nível mínimo configurado |
| US07 – Filtro Categorias | Nicollas | 3 | 🟢 | Busca por localização física ok |
| US08 – Relatório Financeiro | Rodrigo | 5 | 🟢 | Cálculo de lucro bruto implementado |

---

## 🚀 3. Entregas da Sprint

### Funcionalidades implementadas
* Leitura de EAN-13 via câmera para busca automática de produtos.
* Gatilho automático: quando `estoqueAtual < estoqueMinimo`, o sistema gera um registro em `notificacoes` e envia o WhatsApp.
* Interface de filtros por categoria para facilitar a organização física no balcão.

### Evidências
* **Protótipo Atualizado:** Tela de inventário exibindo o ícone de scanner e as etiquetas de "Estoque Baixo" em vermelho.
* **Logs de Sistema:** Registro de notificações pendentes e enviadas com sucesso.

---

## 🧪 4. Qualidade e Testes

* **Tipos de testes realizados:**
    * (X) Manual (Testes de leitura com produtos reais)
    * (X) Integração (Envio de mensagens do sistema para o celular)
    * ( ) Automatizado
    * ( ) Unitário

* **Bugs encontrados:** 3 (Timeout na API e erro de renderização em telas pequenas).
* **Bugs corrigidos:** 3.

---

## 🔧 5. Processo e Ferramentas

* **Controle de versão:** GitHub
* **Ferramentas utilizadas:** VS Code, API de WhatsApp (Twilio/Evolution), Bibliotecas de Scanner (QuaggaJS/Html5-QRCode).

---

## 🔄 6. Retrospectiva da Sprint

### 👍 O que funcionou bem
* A integração do scanner mobile superou a expectativa de velocidade de busca.
* O feedback do Sr. Valdir sobre os alertas de WhatsApp foi extremamente positivo.

### 👎 O que pode melhorar
* A documentação das rotas da API de notificação precisa de mais detalhes para facilitar a manutenção futura.

---

## 🎯 7. Planejamento Inicial da Próxima Sprint

* **Principais objetivos:**
    * Finalizar o Dashboard de "Dinheiro Parado" com gráficos de rotatividade.
    * Realizar o teste de carga com o banco completo de 1.500 itens.
"""