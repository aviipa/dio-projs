# 🤖 Chatbot Inteligente com Leitura de PDFs (RAG)

## 📋 Descrição do Projeto
Este projeto consiste no desenvolvimento de um assistente virtual inteligente capaz de responder perguntas baseadas em documentos internos (PDFs) utilizando técnicas de **RAG (Retrieval-Augmented Generation)**.

A solução foi projetada para integrar o **Azure OpenAI (GPT-4)** com o **Azure AI Search** para indexação vetorial, permitindo que o usuário faça upload de documentos técnicos e obtenha respostas precisas com referência à fonte.

> 🚀 **Status:** MVP (Minimum Viable Product) entregue. A estrutura base de indexação e busca vetorial foi definida.

## 🛠 Arquitetura e Tecnologias
* **Azure OpenAI Service:** Modelo LLM (GPT-3.5-turbo ou GPT-4) para geração de respostas.
* **Azure AI Search:** Motor de busca cognitiva e indexação vetorial dos PDFs.
* **Azure Blob Storage:** Armazenamento dos documentos brutos.
* **Python & LangChain:** Orquestração do fluxo de RAG.
* **Streamlit:** Interface de usuário (Front-end).

## ⚙️ Funcionalidades (Roadmap)
- [x] Configuração do ambiente Azure AI.
- [x] Definição da estratégia de "Chunking" (quebra de texto) dos PDFs.
- [ ] Implementação completa da interface em Streamlit.
- [ ] Otimização dos Prompts do Sistema.

## 📂 Estrutura de Arquivos
* `app.py`: Código principal da aplicação (Streamlit).
* `config.py`: Configurações de conexão com Azure.
* `docs/`: Pasta para upload de arquivos de exemplo.
