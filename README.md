
# The Line - Sistema de Gestão Comercial (SGC)

## 📌 Sobre o Projeto

Este projeto consiste no desenvolvimento de um **Sistema de Gestão Comercial (SGC)** aplicado a um contexto real de comércio eletrônico. O sistema foi projetado para atender às necessidades da **The Line**, uma empresa especializada na venda de roupas e acessórios de moda para todo o Brasil.

A plataforma tem como objetivo oferecer uma gestão eficiente integrando as áreas de:

* **Diretoria:** Visão estratégica e relatórios consolidados de vendas.
* **Catálogo e Produtos:** Gestão de estoque, preços e cadastro de peças.
* **Vendas:** Registro de pedidos e atualização automática de estoque.

---

## ⚙️ Tecnologias e Arquitetura

O sistema foi desenvolvido seguindo uma **Arquitetura em Camadas (App Único)** garantindo organização e alta coesão, utilizando as seguintes tecnologias:

* **Backend:** Django (Python)
* **API:** Django REST Framework (DRF)
* **Comunicação:** API REST (JSON)
* **Banco de Dados:** SQLite 3

---

## 🛠 Diferenciais Técnicos e Robustez

### ⚠️ Tratamento de Exceções Personalizadas

O sistema utiliza exceções customizadas e capturas globais para garantir que as regras de negócio sejam respeitadas, retornando mensagens claras na interface e na API em vez de erros genéricos de servidor (Erro 500):

* **ProtectedError:** Implementado nas *Views*. Impede a exclusão de clientes ou produtos que possuam vendas registradas, exibindo alertas visuais amigáveis ao usuário.
* **EstoqueInsuficiente:** Interrompe a venda na API caso a quantidade solicitada seja maior que a disponível.
* **VendaSemItens:** Impede a criação de registros de venda vazios.

### 📊 Integridade de Dados

* **Proteção de Deleção (Integridade Referencial):** Clientes e produtos vinculados ao histórico de vendas estão protegidos com JWT.

---

## 🚀 Funcionalidades Principais

* **👤 Gestão de Clientes:** Cadastro, validação de CPF/E-mail e histórico de vínculos.
* **📦 Gestão de Produtos:** Cadastro, controle rigoroso de estoque e gestão de preços.
* **🛒 Registro de Vendas:** Registro de pedidos via API, cálculo automático de valor total e baixa instantânea de estoque.
* **📈 Relatórios Gerenciais:** Endpoint exclusivo que consolida dados e calcula automatiamente *cliente*, *produtos* e e *Quantidade de Vendas*.

---

## 🚀 Como Executar o Projeto

**1️⃣ Clonar o Repositório**

```bash
git clone <URL_DO_REPOSITORIO>

```

**2️⃣ Entrar na Pasta do Projeto**

```bash
cd theline

```

**3️⃣ Criar e Ativar o Ambiente Virtual**

* **Windows:**
```bash
python -m venv venv
venv\Scripts\activate

```


* **Linux/Mac:**
```bash
python3 -m venv venv
source venv/bin/activate

```



**4️⃣ Instalar as Dependências**

```bash
pip install -r requirements.txt

```

**5️⃣ Executar as Migrações**

```bash
python manage.py migrate

```

**6️⃣ Iniciar o Servidor**

```bash
python manage.py runserver
```


🌐 **Acesso:** Com o servidor iniciado, acesse `http://127.0.0.1:8000/`

---

## 📋 Passo a Passo da Demonstração (API REST)

Este roteiro demonstra o funcionamento completo do sistema e a integração das regras de negócio.

### 1️⃣ Mostrar os Produtos

* **Acesse:** `/api/produtos/`
* **Objetivo:** Mostrar os produtos cadastrados e o estoque atual.

### 2️⃣ Registrar uma Nova Venda

* **Acesse:** `/api/vendas/`
* **Método:** `POST` (Selecionar a opção *Raw data*)
* **Objetivo:** Demonstrar o cadastro de uma nova venda com itens.

### 3️⃣ Demonstrar a Atualização Automática do Estoque

* **Acesse novamente:** `/api/produtos/`
* **Objetivo:** Comprovar a regra de negócio. O estoque foi reduzido proporcionalmente.
* **Resultado:** O estoque que era `10` passará automaticamente a ser `5`.

### 4️⃣ Demonstrar o Relatório de Vendas

* **Acesse:** `/api/vendas/relatorios/`
* **Objetivo:** Mostrar os agregadores gerenciais calculados em tempo real pelo banco de dados.

---

## 👥 Equipe Desenvolvedora

Projeto desenvolvido por:

* [**Matheus Costa Pessanha**](https://www.google.com/search?q=https://github.com/matheuscostaps)
* [**Tais Döring Freire da Silva**](https://www.google.com/search?q=https://github.com/TaisDF)
* [**Geovana Rodrigues Paz Cruz**](https://www.google.com/search?q=https://github.com/geovanards)
* [**Alysson Kennedy Oliveira de Carvalho**](https://www.google.com/search?q=https://github.com/AlyssonKennedy744)
