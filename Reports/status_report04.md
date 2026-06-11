# 📄 Status Report – Sprint 4

## 👥 Equipe

* **Nome do projeto:** StockMaster
* **Integrantes:** Mauricio T. Welter, Vítor Saraiva de Souza, Nicollas G. Garcia e Rodrigo Monte
* **Scrum Master da Sprint:** Nicollas G. Garcia
* **Product Owner:** Mauricio T. Welter

---

## 📅 Informações da Sprint

* **Número da Sprint:** 4
* **Período:** 29/05 – 11/06
* **Objetivo da Sprint:**

> Concluir o desenvolvimento do Back-End, unificar a integração com o Front-End e realizar o deploy definitivo da aplicação na nuvem via Render integrado ao banco Supabase.

---

## 📌 1. Resumo Executivo

A Sprint 4 marcou um ponto de virada crucial para o StockMaster, onde todo o cronograma técnico foi colocado em dia. A equipe finalizou com sucesso os 50% restantes das APIs do back-end, permitindo o acoplamento completo com a interface web desenvolvida pelo Vítor. Com o sistema correndo perfeitamente em ambiente local, o grupo executou o deploy definitivo da aplicação na nuvem utilizando a plataforma Render, integrando-a com a base de dados hospedada no Supabase. Com o núcleo do MVP 100% operacional e publicado, o projeto avança agora para a sua última etapa, focada na rodada intensiva de testes, polimento de usabilidade e na criação de uma camada de autenticação segura (tela de login) para proteger o ambiente de produção.

* **A sprint foi:**

  * (X) Concluída com sucesso
  * ( ) Parcialmente concluída
  * ( ) Não concluída

* **Principais entregas:**

  * Conclusão de 100% do desenvolvimento das rotas e lógica do Back-End.
  * Integração total e funcional entre as telas do Front-End e as APIs do sistema.
  * Deploy bem-sucedido e publicação do StockMaster na plataforma Render.
  * Migração e sincronização da base de dados local para o Supabase.
  * Resolução de todas as pendências técnicas acumuladas da sprint anterior.

* **Principais dificuldades:**

  * Ajustes na configuração das variáveis de ambiente de produção no Render para garantir uma conexão segura e estável com o cluster do Supabase.

---

## ✅ 2. Itens Planejados vs Entregues

**Status possíveis (utilizar apenas estes):**

* 🟢 Concluído
* 🟡 Em andamento
* 🔴 Não iniciado
* ⚫ Bloqueado

| User Story / Tarefa | Responsável | Story Points | Status | Observações |
| ------------------- | ----------- | ------------ | ------ | ----------- |
| US06 – Conclusão e Fechamento das APIs | Rodrigo | 5 | 🟢 | 100% do back-end finalizado e funcional |
| US07 – Integração Completa (Front + Back) | Vítor | 5 | 🟢 | Sistema unificado e testado localmente |
| US08 – Deploy de Produção na Nuvem (Render) | Equipe | 5 | 🟢 | Link ativo e aplicação correndo online |
| US09 – Migração e Modelagem em Produção | Mauricio | 4 | 🟢 | Banco de dados e regras validados no Supabase |

---

## 🚀 3. Entregas da Sprint

### Funcionalidades implementadas

* **Aplicação em Nuvem (Deploy):** Sistema totalmente acessível de forma online através do servidor de produção do Render.
* **Persistência Remota (Supabase):** Banco de dados relacional ativo na nuvem processando as transações reais da aplicação.
* **Comunicação Fim a Fim:** O front-end agora consome os dados reais do back-end hospedado, atualizando saldos de estoque e histórico instantaneamente.

### Evidências (obrigatório)

* **Link do repositório:** https://github.com/r-schneider/fspoa-pd1
* **Link do quadro Kanban:** https://github.com/users/r-schneider/projects/3
* **Prints ou GIFs:**
  ![Interface StockMaster](./imagem_telas.png)
  *Figura 1: Sistema StockMaster rodando integrado, exibindo dados dinâmicos salvos e consultados diretamente no Supabase via API no Render.*
* **Link do deploy:** https://fspoa-pd1-1.onrender.com/

---

## 🧪 4. Qualidade e Testes

* **Tipos de testes realizados:**

  * (X) Manual (Navegação completa pelas rotas do sistema após a publicação)
  * ( ) Automatizado
  * ( ) Unitário
  * (X) Integração (Validação do fluxo completo: Interface -> API Render -> Banco Supabase)

* **Cobertura (se aplicável):** Não aplicável nesta etapa.

* **Bugs encontrados:** 2 (Erro de conexão por timeout no banco remoto e problemas de CORS durante as requisições iniciais).

* **Bugs corrigidos:** 2 (Ajuste nas strings de conexão de produção e liberação das políticas de CORS no back-end).

---

## 🔧 5. Processo e Ferramentas

* **Controle de versão utilizado:** Git + GitHub
* **Estratégia de branch:** feature branches + main
* **Uso de CI/CD:** Deploy automatizado integrado via Render + GitHub
* **Ferramentas utilizadas:** VS Code, Supabase (PostgreSQL), Node.js, Render Dashboard, GitHub Projects.

---

## ⚠️ 6. Impedimentos

| Impedimento | Impacto | Solução adotada |
| ----------- | ------- | --------------- |
| Nenhum impedimento travou a equipe nesta sprint. | Nulo | O planejamento conservador permitiu mitigar os riscos e zerar as pendências. |

---

## 🔄 7. Retrospectiva da Sprint

### 👍 O que funcionou bem

* A escolha do Supabase agilizou a visualização e monitoramento das tabelas em tempo real.
* A dedicação em fechar o back-end local antes de subir para o Render evitou quebras em produção.

### 👎 O que pode melhorar

* O sistema ficou exposto publicamente na nuvem logo após o deploy, reforçando que deveríamos ter mapeado a autenticação antes.

### 🔁 Ações para próxima sprint

* Desenhar e implementar imediatamente a tela de login e o middleware de proteção de rotas.
* Iniciar o plano detalhado de testes funcionais.

---

## 📊 8. Métricas da Sprint

* **Story Points planejados:** 19

* **Story Points concluídos:** 19

* **Velocidade da equipe:**

> 19 story points concluídos de 19 planejados (100% de eficiência e cronograma totalmente atualizado)

* **% Entrega:**

> (19 / 19) × 100 = 100%

* **Nº de tarefas concluídas:** 4
* **Nº de tarefas não concluídas:** 0
* **Nº de commits:** 17 (Sendo 16 de código de desenvolvimento e 1 referente ao envio deste relatório)
* **Nº de PRs:** 0

---

## 🎯 9. Planejamento Inicial da Próxima Sprint (Última Sprint - Fase Final)

* **Principais objetivos:**

  * Iniciar e executar a fase oficial de testes funcionais, consistência e validação de dados no Supabase.
  * Realizar a depuração e correção imediata de quaisquer erros (bugs) identificados durante a rotina de testes.
  * Implementar pequenos ajustes e alterações necessárias para otimização do comportamento do sistema.
  * Desenvolver e implementar a **Tela de Login (Autenticação)** para restringir e proteger o acesso à aplicação na nuvem.
  * Realizar o polimento estético final de UI/UX, tratando pequenos detalhes visuais e de usabilidade.

* **Itens já priorizados:**

  * US10 – Tela de Login e Proteção de Rotas (Auth) para ambiente Cloud
  * US11 – Homologação de Usabilidade, Ajustes Finos e Correção de Erros da fase de testes
  * US12 – Execução de Casos de Testes e Validação com a volumetria de 1.500 Itens