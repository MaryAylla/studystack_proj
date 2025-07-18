# 📖 StudyStack: Sua Base de Conhecimento Pessoal com Python e Flask

StudyStack é uma aplicação web completa, inspirada em ferramentas como o Notion, projetada para ser uma base de conhecimento pessoal onde usuários podem criar, gerenciar e pesquisar resumos de estudo. Construída com **Python** e **Flask**, a aplicação utiliza **PostgreSQL** como banco de dados e uma arquitetura modular para demonstrar práticas de desenvolvimento de software robustas.

Este projeto é uma demonstração aprofundada de conceitos full-stack, incluindo:

* **Backend (Python, Flask & SQLAlchemy):**
    * **Arquitetura Modular:** Separação de responsabilidades com arquivos dedicados (`app.py`, `models.py`).
    * **CRUD Completo:** Implementação de todas as operações (Create, Read, Update, Delete) para os resumos.
    * **Modelagem de Dados Avançada:**
        * Uso de um banco de dados relacional (PostgreSQL).
        * Implementação de um relacionamento **Muitos-para-Muitos (N:N)** entre Resumos e Tags, utilizando uma tabela de associação.
        * Lógica de "Find or Create" para gerenciar entidades relacionadas (Matérias e Tags) de forma eficiente, evitando duplicatas.
    * **Consultas Complexas:** Construção de queries dinâmicas com SQLAlchemy para implementar filtros e uma busca textual (case-insensitive com `ilike` e `or_`).

* **Frontend (HTML, CSS & JavaScript):**
    * **Templates com Jinja2:** Uso de herança (`{% extends %}`), blocos (`{% block %}`) e estruturas de controle (`{% for %}`, `{% if %}`) para renderizar páginas dinâmicas.
    * **Design Responsivo com CSS:** Layout moderno de "cards" utilizando Flexbox, com uma paleta de cores consistente gerenciada por variáveis CSS.
    * **Interatividade com JavaScript:**
        * **Editor de Texto Rico (WYSIWYG):** Integração da biblioteca **TinyMCE** para permitir a formatação de texto (negrito, itálico, listas, etc.).
        * **Modo Claro/Escuro:** Implementação de um seletor de tema que altera o visual da aplicação e salva a preferência do usuário no `localStorage` do navegador.

* **Segurança:**
    * **Prevenção de XSS:** Sanitização do conteúdo HTML gerado pelo editor de texto usando a biblioteca **Bleach** para remover tags e atributos maliciosos antes da exibição.
    * **Gerenciamento de Credenciais:** Uso de um arquivo `.env` e da biblioteca `python-dotenv` para manter as credenciais do banco de dados seguras e fora do controle de versão.

-----

## ✨ Funcionalidades Principais

* **CRUD Completo de Resumos:** Crie, visualize, edite e exclua seus resumos de estudo.
* **Organização com Matérias e Tags:** Cada resumo é associado a uma Matéria (relação 1:N) e a múltiplas Tags (relação N:N).
* **Busca Global:** Uma barra de busca no cabeçalho permite pesquisar por palavras-chave no título e no conteúdo de todos os resumos.
* **Filtros Dinâmicos:** Filtre a visualização de resumos por Matéria ou por uma Tag específica.
* **Editor de Texto Rico:** Crie resumos com formatação de texto (negrito, itálico, listas, etc.) graças à integração com o editor TinyMCE.
* **Modo Claro/Escuro:** Alterne entre um tema visual claro ou escuro para uma experiência de leitura mais confortável. A sua preferência é salva no navegador.

-----

## 🔧 Tecnologias Utilizadas

* **Backend:** Python, Flask, SQLAlchemy (ORM)
* **Banco de Dados:** PostgreSQL
* **Driver do DB:** psycopg2
* **Frontend:** HTML5, CSS3 (Flexbox, Variáveis), JavaScript
* **Bibliotecas Python:** Bleach (Segurança), python-dotenv (Configuração)
* **Bibliotecas JavaScript:** TinyMCE (Editor WYSIWYG)

-----

## 🚀 Como Executar Localmente

Para rodar este projeto em sua máquina, você precisará ter o **Python 3** e o **PostgreSQL** instalados e rodando.

1.  **Clone o repositório:**
    ```bash
    git clone [https://github.com/MaryAylla/studystack_proj.git](https://github.com/MaryAylla/studystack_proj.git)
    cd nome-do-repositorio
    ```

2.  **Crie e ative um ambiente virtual:**
    ```bash
    # Windows
    python -m venv venv
    venv\Scripts\activate

    # macOS/Linux
    python3 -m venv venv
    source venv/bin/activate
    ```

3.  **Instale as dependências:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Configure o Banco de Dados:**
    * No PostgreSQL, crie um novo banco de dados (ex: `studystack_db`).
    * Crie uma cópia do arquivo `.env.example` (se houver) ou crie um novo arquivo chamado `.env`.

5.  **Configure as Variáveis de Ambiente:**
    * Abra o arquivo `.env` e adicione a sua URL de conexão com o banco:
        ```
        DATABASE_URL="postgresql://SEU_USUARIO:SUA_SENHA@localhost/studystack_db"
        ```
    * *(Lembre-se de codificar caracteres especiais na sua senha, se houver).*

6.  **Execute a Aplicação:**
    ```bash
    python app.py
    ```
    * Na primeira execução, as tabelas serão criadas automaticamente no seu banco de dados.

7.  **Acesse o Projeto:**
    * Abra seu navegador e acesse: `http://127.0.0.1:5000`
