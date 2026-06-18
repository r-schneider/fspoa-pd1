# 📄 Status Report – Sprint 5

## 👥 Equipe

* **Nome do projeto:** StockMaster
* **Integrantes:** Mauricio T. Welter, Vítor Saraiva de Souza, Nicollas G. Garcia e Rodrigo Monte
* **Scrum Master da Sprint:** Vítor Saraiva de Souza
* **Product Owner:** Mauricio T. Welter

---

## 📅 Informações da Sprint

* **Número da Sprint:** 5
* **Período:** 12/06 – 18/06 (Data atual de fechamento)
* **Objetivo da Sprint:**

> Iniciar a fase de testes e polimento do sistema, mapear correções de erros e implementar a interface e lógica da tela de login para proteção do ambiente em nuvem.

---

## 📌 1. Resumo Executivo

Nesta sprint, o cronograma da equipe foi severamente impactado pela escassez de tempo disponível dos integrantes para avançar no ritmo planejado. Diante dessa restrição, o grupo priorizou os esforços na camada visual, resultando na conclusão do front-end da tela de login do sistema. O desenvolvimento do back-end correspondente a essa autenticação ficou pendente e sua implementação dependerá estritamente do tempo remanescente. Devido a essas pendências e ao adiamento da rodada massiva de testes de consistência, a sprint foi classificada como parcialmente concluída. O grupo focará a próxima semana, onde haverá maior disponibilidade de tempo, para executar de forma intensiva as rotas de testes funcionais, correções de falhas e o polimento fino do StockMaster.

* **A sprint foi:**

  * ( ) Concluída com sucesso
  * (X) Parcialmente concluída
  * ( ) Não concluída

* **Principais entregas:**

  * Interface visual (Front-End) da nova Tela de Login totalmente estruturada e integrada ao layout.
  * Mapeamento prévio dos pontos críticos que passarão pela bateria de testes funcionais.

* **Principais dificuldades:**

  * Intensa falta de tempo hábil por parte dos integrantes da equipe para conciliar as demandas de código com as rotinas externas, travando o avanço do back-end da autenticação e a execução dos testes programados.

---

## ✅ 2. Itens Planejados vs Entregues

**Status possíveis (utilizar apenas estes):**

* 🟢 Concluído
* 🟡 Em andamento
* 🔴 Não iniciado
* ⚫ Bloqueado

| User Story / Tarefa | Responsável | Story Points | Status | Observações |
| ------------------- | ----------- | ------------ | ------ | ----------- |
| US10 – Interface da Tela de Login (Front) | Vítor | 5 | 🟢 | Tela construída e integrada esteticamente |
| US11 – Lógica de Autenticação (Back-End) | Rodrigo | 5 | 🟡 | Dependendo de tempo hábil para o fechamento |
| US12 – Bateria de Testes de Integração | Nicollas | 5 | 🔴 | Postergada para a semana de maior foco |
| US13 – Correção de Bugs e Ajustes de Regras | Mauricio | 4 | 🟡 | Revisões pontuais iniciadas; correções finais na próxima semana |

---

## 🚀 3. Entregas da Sprint

### Funcionalidades implementadas

* **Front-End da Autenticação:** Criação visual do fluxo de acesso do usuário, preparando o StockMaster para deixar de ser totalmente exposto na nuvem.
* **Estabilização do Deploy (Render/Supabase):** Manutenção do ambiente online operando de forma estável enquanto as novas features de interface eram acopladas.

### Evidências (obrigatório)

* **Link do repositório:** https://github.com/r-schneider/fspoa-pd1
* **Link do quadro Kanban:** https://github.com/users/r-schneider/projects/3
* **Prints ou GIFs:**
  ![Login StockMaster](./imagem_login.png)
  *Figura 1: Nova interface da tela de login projetada para restrição de acessos no ambiente em nuvem.*
* **Link do deploy:** https://fspoa-pd1-1.onrender.com/

---

## 🧪 4. Qualidade e Testes

* **Tipos de testes realizados:**

  * (X) Manual (Apenas testes básicos de renderização e responsividade da nova tela de login)
  * ( ) Automatizado
  * ( ) Unitário
  * ( ) Integração

* **Cobertura (se aplicável):** Não aplicável nesta etapa devido ao adiamento dos testes de carga.

* **Bugs encontrados:** 0 (Fase oficial de testes não iniciada).

* **Bugs corrigidos:** 0.

---

## 🔧 5. Processo e Ferramentas

* **Controle de versão utilizado:** Git + GitHub
* **Estratégia de branch:** feature branches + main
* **Uso de CI/CD:** Deploy contínuo ativo via Render
* **Ferramentas utilizadas:** VS Code, Supabase, Node.js, Render, GitHub Projects.

---

## ⚠️ 6. Impedimentos

| Impedimento | Impacto | Solução adotada |
| ----------- | ------- | --------------- |
| Escassez severa de tempo disponível da equipe durante o período da sprint. | Bloqueou a execução dos testes e empurrou o back-end da autenticação para o status de risco. | Postergar a massa de testes de homologação e as correções para a semana seguinte, onde a equipe terá maior dedicação. |

---

## 🔄 7. Retrospectiva da Sprint

### 👍 O que funcionou bem

* O Vítor conseguiu adiantar e isolar todo o front-end da tela de login de forma limpa, sem quebrar as telas de movimentação já publicadas no Render.

### 👎 O que pode melhorar

* A gestão do tempo em semanas de alta sobrecarga externa precisa ser revista para que o desenvolvimento de funcionalidades críticas (como o back-end de segurança) não fique ameaçado.

### 🔁 Ações para próxima sprint

* Aproveitar a maior janela de tempo disponível na próxima semana para concentrar todos os integrantes na varredura de erros.
* Avaliar se haverá tempo útil para codificar o back-end da autenticação ou se o foco será mantido no polimento do core do sistema.

---

## 📊 8. Métricas da Sprint

* **Story Points planejados:** 20

* **Story Points concluídos:** 5

* **Velocidade da equipe:**

> 5 story points concluídos de 19 planejados (26% de entrega focado exclusivamente no front-end do login)

* **% Entrega:**

> (5 / 19) × 100 = 26.3%

* **Nº de tarefas concluídas:** 1
* **Nº de tarefas não concluídas:** 3 (Tarefas de back-end, testes e correções movidas para a reta final)
* **Nº de commits:** (Preencher com o total acumulado atualizado do repositório)
* **Nº de PRs:** 0 (Contribuições diretas via branch)

---

## 🎯 9. Planejamento Inicial da Próxima Sprint (Reta Final de Homologação)

* **Principais objetivos:**

  * Executar a fase oficial e intensiva de testes funcionais e de consistência com os 1.500 itens.
  * Realizar as correções de quaisquer erros e bugs que forem encontrados durante os testes da semana.
  * Efetuar pequenos ajustes, refinamentos visuais e alterações necessárias no sistema.
  * Definir e implementar o back-end de autenticação (caso haja tempo hábil disponível).

* **Itens já priorizados:**

  * Execução e documentação dos Casos de Testes Finais do Sistema.
  * Manutenção corretiva de falhas mapeadas em ambiente de produção (Render/Supabase).
  * Polimento estético de UI/UX e finalização dos artefatos para apresentação ao professor Luciano Zanuz.