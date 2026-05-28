# 📄 Status Report – Sprint 3

## 👥 Equipe

* **Nome do projeto:** StockMaster
* **Integrantes:** Mauricio T. Welter, Vítor Saraiva de Souza, Nicollas G. Garcia e Rodrigo Monte (Observação: Leandro Mandela trancou o curso e foi removido da equipe)
* **Scrum Master da Sprint:** Rodrigo Monte
* **Product Owner:** Mauricio T. Welter

---

## 📅 Informações da Sprint

* **Número da Sprint:** 3
* **Período:** 15/05 – 28/05
* **Objetivo da Sprint:**

> Finalizar a estrutura do banco de dados e suas regras de negócio core, evoluir o desenvolvimento das APIs do back-end e preparar o sistema para o deploy.

---

## 📌 1. Resumo Executivo

Nesta sprint, a equipe alcançou marcos importantes na fundação estrutural do sistema. O banco de dados e as regras de negócio core foram 100% finalizados e estruturados pelo integrante Mauricio. Na camada visual, o front-end avançou sob a responsabilidade do Vítor, consolidando a interface do sistema web para registro de saídas com histórico integrado. No back-end, os demais integrantes (Rodrigo e Nicollas) focaram no desenvolvimento dos endpoints de integração, levando a API a um estágio de aproximadamente 45% de conclusão. A ideia inicial previa a realização do deploy nesta etapa, porém, a equipe optou por segurar a publicação até que o sistema esteja correndo perfeitamente em ambiente local. Por conta disso, e somado ao desfalque pelo trancamento de curso do ex-integrante Leandro Mandela, a sprint foi classificada como parcialmente concluída.

* **A sprint foi:**

  * ( ) Concluída com sucesso
  * (X) Parcialmente concluída
  * ( ) Não concluída

* **Principais entregas:**

  * Banco de dados totalmente pronto e estruturado com as chaves e relacionamentos necessários.
  * Regras de negócio essenciais do sistema mapeadas e implementadas na base de dados.
  * Interface web estável para a tela de "Registrar Saída de Estoque" com histórico em tempo real.
  * Avanço na codificação das APIs de back-end (aproximadamente 40% a 50% concluído).

* **Principais dificuldades:**

  * Necessidade de maior maturidade nas rotas do back-end antes de prosseguir de forma segura com o deploy.
  * Redistribuição da carga de tarefas de codificação do back-end após a saída de um integrante da equipe.

---

## ✅ 2. Itens Planejados vs Entregues

**Status possíveis (utilizar apenas estes):**

* 🟢 Concluído
* 🟡 Em andamento
* 🔴 Não iniciado
* ⚫ Bloqueado

| User Story / Tarefa | Responsável | Story Points | Status | Observações |
| ------------------- | ----------- | ------------ | ------ | ----------- |
| US04 – Finalização do Banco e Regras Core | Mauricio | 5 | 🟢 | Banco de dados e regras de negócio 100% prontos |
| US05 – Desenvolvimento da Interface Web | Vítor | 5 | 🟢 | Tela de saídas e histórico finalizados no front |
| US06 – Construção de Endpoints e APIs | Rodrigo | 5 | 🟡 | Desenvolvimento ativo do back-end (cerca de 45% pronto) |
| US07 – Implementação de Rotas de Integração | Nicollas | 6 | 🟡 | Acoplamento de rotas com a base pronta do banco |
| US08 – Deploy em Produção (Vercel) | Equipe | 3 | 🔴 | Postergado para quando o sistema estiver correndo certo |

---

## 🚀 3. Entregas da Sprint

### Funcionalidades implementadas

* **Persistência de Dados Concluída:** Estrutura relacional do banco pronta para suportar o cadastro completo e a volumetria de 1.500 itens.
* **Componentização do Front-End:** Telas e grids de exibição de dados operacionais (Histórico de Saídas e Cards de Resumo) finalizados no navegador.
* **Camada de Integração:** Início da amarração entre as requisições de backend e os ganchos lógicos do banco.

### Evidências (obrigatório)

* **Link do repositório:** https://github.com/r-schneider/fspoa-pd1
* **Link do quadro Kanban:** https://github.com/users/r-schneider/projects/3
* **Prints ou GIFs:**
  ![Interface StockMaster](./imagem_telas.png)
  *Figura 1: Tela de controle operacional e registro de saídas integrada à estrutura de dados do sistema.*
* **Link do deploy (se houver):** Não disponível (Postergado para a próxima sprint)

---

## 🧪 4. Qualidade e Testes

* **Tipos de testes realizados:**

  * (X) Manual (Validação visual do fluxo de dados na tela construída pelo Vítor)
  * ( ) Automatizado
  * ( ) Unitário
  * (X) Integração (Testes de inserção direta no banco através de chamadas manuais de API)

* **Cobertura (se aplicável):** Não aplicável nesta etapa do projeto.

* **Bugs encontrados:** 1 (Inconsistência de tipagem de dados ao enviar requisições do back-end para as tabelas do banco).

* **Bugs corrigidos:** 1 (Ajuste rápido feito pelo Mauricio na validação das chaves das regras de negócio).

---

## 🔧 5. Processo e Ferramentas

* **Controle de versão utilizado:** Git + GitHub
* **Estratégia de branch:** feature branches + main
* **Uso de CI/CD:** Não utilizado nesta sprint
* **Ferramentas utilizadas:** VS Code, MySQL / brModelo, Node.js, GitHub Projects.

---

## ⚠️ 6. Impedimentos

| Impedimento | Impacto | Solução adotada |
| ----------- | ------- | --------------- |
| Perda de força de trabalho devido ao trancamento de curso do integrante Leandro Mandela. | Risco de sobrecarga no cronograma de rotas que os colegas do back-end precisavam desenvolver. | O grupo focou em priorizar o núcleo do back-end web, deixando os testes em bloco e a portabilidade para o fechamento. |
| Necessidade de refinar o fluxo de dados local. | Bloqueou a subida do sistema para a nuvem nesta sprint. | Decisão estratégica de adiar o deploy para a Vercel até que o back-end esteja totalmente estável. |

---

## 🔄 7. Retrospectiva da Sprint

### 👍 O que funcionou bem

* Ter o banco de dados e as regras finalizadas pelo Mauricio deu autonomia para o Vítor avançar no front sabendo exatamente quais campos exibir.
* A divisão clara de tarefas (Mauricio no banco/regras e Vítor no front) evitou conflitos de código.

### 👎 O que pode melhorar

* O ritmo de desenvolvimento das APIs do back-end foi sobrecarregado pela ausência de um membro, demandando mais tempo do que o previsto.

### 🔁 Ações para próxima sprint

* Concentrar esforços do grupo para apoiar a conclusão do back-end.
* Definir uma janela de tempo específica para realizar os testes de ponta a ponta e garantir o sucesso do deploy.

---

## 📊 8. Métricas da Sprint

* **Story Points planejados:** 24

* **Story Points concluídos:** 10

* **Velocidade da equipe:**

> 10 story points totalmente concluídos e 14 pendentes/em andamento (Foco concentrado na infraestrutura e lógica do sistema)

* **% Entrega:**

> (10 / 24) × 100 = 41.6% de tarefas totalmente fechadas (com o restante do back-end bem encaminhado)

* **Nº de tarefas concluídas:** 2
* **Nº de tarefas não concluídas:** 3 (Desenvolvimento contínuo do back-end e deploy pendente)
* **Nº de commits:** 15 (Sendo 14 de código de desenvolvimento e 1 referente ao envio deste relatório)
* **Nº de PRs:** 0 (Contribuições integradas diretamente via commit nas branches locais de desenvolvimento)

---

## 🎯 9. Planejamento Inicial da Próxima Sprint (Última Sprint)

* **Principais objetivos:**

  * Concluir em 100% o desenvolvimento das APIs e endpoints do back-end.
  * Realizar o deploy definitivo do sistema completo na plataforma Vercel assim que estiver correndo corretamente.
  * Executar a rodada final de testes de integração e testes funcionais de ponta a ponta.

* **Itens já priorizados:**

  * Finalização das rotas pendentes de relatórios e controle de saldos.
  * Configuração do ambiente de produção e pipeline na Vercel.
  * Homologação do MVP integrado e preparação dos artefatos de entrega para o professor Luciano Zanuz.