# 🏦 Sistema Bancário em Python - Otimizado e Modularizado

Este projeto consiste na evolução de um sistema bancário simples para uma versão estruturada, modular e escalável. O objetivo foi aplicar boas práticas de programação em Python, saindo de um script monolítico para uma arquitetura baseada em funções e estruturas de dados.

## 🚀 Evolução Técnica

O projeto passou por uma refatoração completa para atender a requisitos de **manutenibilidade** e **organização**.

### 📉 De: Ponto Inicial (Versão 1)
* **Estrutura Monolítica:** Todo o código em um único bloco de execução.
* **Variáveis Globais:** Dificuldade em rastrear o estado das variáveis.
* **Sem Persistência de Dados:** Apenas variáveis simples para controle.
* **Limitação:** Apenas 3 operações básicas (Saque, Depósito, Extrato).

### 📈 Para: Transformação Aplicada (Versão 2)
O sistema foi reescrito adotando **Modularização Funcional** e **Separação de Responsabilidades**.

#### 1. Modularização e Argumentos Especiais
Uso avançado de definição de funções para garantir clareza nas chamadas:
* `depositar(saldo, valor, extrato, /)`: Implementação de **Positional-Only Arguments** para forçar a passagem de valores por posição.
* `sacar(*, saldo, valor...)`: Implementação de **Keyword-Only Arguments** para obrigar a nomeação de argumentos, evitando erros em chamadas com muitos parâmetros.
* `exibir_extrato(saldo, /, *, extrato)`: Uso híbrido para flexibilidade e legibilidade.

#### 2. Estruturas de Dados Dinâmicas
Substituição de variáveis soltas por coleções robustas:
* **Usuários:** Lista de dicionários (`{'nome': ..., 'cpf': ...}`) permitindo múltiplos clientes.
* **Contas:** Lista de dicionários com vínculo ao usuário (Relacionamento 1:N).
* **Validações:** Verificação de unicidade de CPF para impedir duplicatas.

#### 3. Novas Funcionalidades
* **Cadastro de Usuários:** Coleta de dados com validação de existência.
* **Criação de Contas:** Geração automática de número de conta e agência fixa "0001".
* **Listagem de Contas:** Exibição formatada dos dados vinculados.

---

## 🏗️ Arquitetura do Sistema

### Fluxo de Dados
```mermaid
graph LR
    Input[Entrada do Usuário] --> Menu
    Menu --> Funcoes[Funções Especializadas]
    Funcoes --> Validacao[Validações CPF/Saldo]
    Validacao --> Estruturas[Listas e Dicionários]
    Estruturas --> Output[Exibição Formatada]
