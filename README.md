# 📦 Controle de Estoque de Peças

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg?logo=python&logoColor=white)](https://www.python.org/)
[![CustomTkinter](https://img.shields.io/badge/GUI-CustomTkinter-blueviolet)](https://github.com/TomSchimansky/CustomTkinter)
[![Database](https://img.shields.io/badge/Database-SQLite3-lightgrey?logo=sqlite&logoColor=white)](https://www.sqlite.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

Sistema de gestão e controle de estoque de peças desenvolvido em **Python**, com interface gráfica moderna desenvolvida em **CustomTkinter** (suporte a Modo Escuro) e banco de dados **SQLite3**.

---

## 📋 Sumário
- [Sobre o Projeto](#-sobre-o-projeto)
- [✨ Funcionalidades](#-funcionalidades)
- [🛠 Tecnologias Utilizadas](#-tecnologias-utilizadas)
- [📂 Estrutura do Projeto](#-estrutura-do-projeto)
- [🚀 Como Executar](#-como-executar)
- [🤝 Como Contribuir](#-como-contribuir)
- [📄 Licença](#-licença)

---

## 💡 Sobre o Projeto

O **Controle de Estoque** é uma solução voltada para automatizar o gerenciamento de peças, movimentações de estoque (entradas e saídas) e controle financeiro de vendas. O sistema foi desenvolvido com foco em facilidade de uso, visual moderno e sincronização automática com o banco de dados local.

---

## ✨ Funcionalidades

- ⚙️ **Gestão de Peças:** Cadastro, edição, listagem e exclusão de peças com detalhes (descrição, número de série, marca, preço de custo e condição).
- 🔍 **Busca Inteligente:** Localização rápida de peças por descrição ou busca detalhada.
- 🔄 **Entradas e Saídas:** Registro de movimentações de estoque com recálculo automático de saldo.
- 💰 **Registro de Vendas & Lucro:** Vínculo de vendas às saídas de estoque com controle do canal de venda e cálculo de margem de lucro.
- 📜 **Histórico Completo:** Consulta de histórico de movimentações filtrado por período.
- 🚨 **Alertas & Validações:** Controle de integridade para evitar exclusões indevidas e alertas de estoque.
- 🎨 **Interface Moderna:** Desenvolvida em CustomTkinter com suporte nativo ao **Modo Escuro (Dark Mode)** e navegação por janelas.

---

## 🛠 Tecnologias Utilizadas

- **Linguagem:** [Python 3.8+](https://www.python.org/)
- **Interface Gráfica:** [CustomTkinter](https://github.com/TomSchimansky/CustomTkinter) & `tkinter.ttk`
- **Banco de Dados:** SQLite3 (nativo do Python com criação automática de tabelas)
- **Padronização:** Arquitetura organizada no modelo **MVC** (Model-View-Controller)

---

## 📂 Estrutura do Projeto

```text
controle_estoque/
├── src/
│   ├── controller/
│   │   └── Controller.py      # Lógica de negócios e mediação
│   ├── model/
│   │   └── database.py        # Gerenciador de banco SQLite e queries
│   └── view/
│       └── View.py            # Interfaces e telas CustomTkinter
├── main.py                    # Ponto de entrada da aplicação
├── .gitignore                 # Arquivos ignorados pelo Git
└── README.md                  # Documentação do projeto