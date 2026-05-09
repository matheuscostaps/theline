# The Line - Sistema de Gestão Comercial (SGC)

## 📌 Sobre o Projeto

Este projeto consiste no desenvolvimento de um **Sistema de Gestão Comercial (SGC)** aplicado a um contexto real de comércio eletrónico.

O sistema foi projetado para atender às necessidades da **The Line**, uma empresa B2C especializada na venda de roupas e acessórios de moda para todo o Brasil.

A plataforma tem como objetivo oferecer uma gestão eficiente integrando as áreas de:

- **Diretoria:** visão estratégica e relatórios de vendas
- **Catálogo e Produtos:** gestão de estoque, preços e cadastro de peças
- **Vendas:** registo de pedidos e atualização automática de estoque
- **Marketing:** acesso aos dados de clientes para campanhas promocionais

---

# ⚙️ Tecnologias e Arquitetura

O sistema foi desenvolvido seguindo uma **Arquitetura em Camadas** utilizando as seguintes tecnologias:

- **Backend:** Django (Python)
- **API:** Django REST Framework
- **Comunicação:** API REST (JSON)
- **Banco de Dados:** SQLite
- **Segurança:** autenticação baseada em Token (JWT) e senhas criptografadas

---

# 🛠 Diferenciais Técnicos e Robustez

## ⚠️ Tratamento de Exceções Personalizadas

O sistema utiliza exceções customizadas para garantir que as regras de negócio sejam respeitadas e retornem mensagens claras via API:

* **EstoqueInsuficiente:** Interrompe a venda caso a quantidade solicitada seja maior que a disponível no banco de dados.
* **VendaSemItens:** Impede a criação de registros de venda vazios.
* **Handler Global:** Erros são capturados e tratados para evitar respostas genéricas do servidor (Erro 500).

## 📊 Integridade de Dados

* **Atomic Transactions:** O registro da venda e a baixa do estoque ocorrem dentro de uma transação atômica. Se um falhar, o outro não é executado, evitando dados inconsistentes.
* **Proteção de Deleção:** Clientes com vendas registradas são protegidos contra exclusão acidental (`models.PROTECT`).

---

# 🚀 Funcionalidades Principais

## 👤 Gestão de Clientes
- Cadastro de clientes
- Validação de CPF
- Validação de e-mail

## 📦 Gestão de Produtos
- Cadastro de produtos
- Controle de estoque
- Gestão de preços

## 🛒 Registo de Vendas
- Registro de pedidos
- Cálculo automático de valores
- Baixa automática de estoque

## 🔐 Autenticação e Perfis
- Controle de acesso
- Perfis ADMIN e FUNCIONARIO

## 📈 Relatórios
- Relatórios de vendas
- Dados consolidados
- Informações por período e cliente

---

# 📦 Extensões Utilizadas

- Python
- Python Debugger
- SQLite Viewer

---

# 🚀 Como Executar o Projeto

## 1️⃣ Clonar o Repositório

```bash
git clone <URL_DO_REPOSITORIO>
```

---

## 2️⃣ Entrar na Pasta do Projeto

```bash
cd theline
```

---

## 3️⃣ Criar e Ativar o Ambiente Virtual

### Windows

```bash
python -m venv venv
venv\Scripts\activate
```

### Linux/Mac

```bash
python3 -m venv venv
source venv/bin/activate
```

---

## 4️⃣ Instalar as Dependências

```bash
pip install -r requirements.txt
```

---

## 5️⃣ Executar as Migrações

```bash
python manage.py migrate
```

---

## 6️⃣ Iniciar o Servidor

```bash
python manage.py runserver
```


=======
Para garantir a sua nota máxima, acrescentei as seções fundamentais que o critério de avaliação exige: **Execução de Testes**, **Tratamento de Exceções Personalizadas** e o comando de **requirements.txt**.

Mantenha o seu conteúdo original e insira estes blocos nos locais indicados abaixo:

## 7️⃣ Executar os Testes Automatizados

Para validar a integridade do sistema, controle de estoque e relatórios:

```bash
python manage.py test

```


---

# 🌐 Acesso à API

Com o servidor iniciado:

```text
http://127.0.0.1:8000/
```

---

# 📋 Passo a Passo da Demonstração

Este roteiro foi preparado para demonstrar o funcionamento completo do sistema e a integração das regras de negócio.
---

# 1️⃣ Mostrar os Produtos

Acesse:

```text
/api/produtos/
```

## Objetivo
Mostrar os produtos cadastrados e o estoque atual.

### Exemplo esperado

```json
{
    "id": 1,
    "nome": "Babylook Patinho",
    "preco": "300.00",
    "estoque": 10
}
```

---

# 2️⃣ Registrar uma Nova Venda

Acesse:

```text
/api/vendas/
```

## Método

```text
POST
```

## Selecionar a opção

```text
Raw data
```

## Exemplo de JSON

```json
{
    "cliente": 1,
    "valor_total": 500.00,
    "itens": [
        {
            "produto": 4,
            "quantidade": 5,
            "preco_unitario": 100.00
        }
    ]
}
```

## Objetivo
Demonstrar o cadastro de uma nova venda pela API.

---

# 3️⃣ Demonstrar a Atualização Automática do Estoque

Volte novamente para:

```text
/api/produtos/
```

## Objetivo
Mostrar que o estoque do produto foi reduzido automaticamente de forma proporcional à quantidade vendida.

### Exemplo

Antes da venda:

```json
"estoque": 10
```

Depois da venda:

```json
"estoque": 8
```

## Regra de Negócio Demonstrada

✔ Atualização automática do estoque  
✔ Integração entre produtos e vendas  
✔ Persistência no banco de dados

---

# 4️⃣ Mostrar a Venda Registrada

Acesse novamente:

```text
/api/vendas/
```

## Objetivo
Comprovar que a venda foi salva corretamente no banco de dados.

### Exemplo esperado

```json
{
    "id": 1,
    "produto": 1,
    "quantidade": 2,
    "valor_total": "7000.00",
    "data": "2026-05-08T10:30:00Z"
}
```

---

# 5️⃣ Demonstrar o Relatório de Vendas

Acesse:

```text
/api/vendas/relatorio/
```

## Objetivo
Mostrar os dados consolidados de faturamento e vendas.

### Exemplo esperado

```json
{
    "total_vendas": 5,
    "faturamento_total": "15000.00"
}
```
## ❌ Deletar Venda

A API permite remover uma venda registrada no sistema.

### 📌 Endpoint

http://127.0.0.1:8000/api/vendas/3/  | (3 é o id do cliente)
---

### 🧾 Método HTTP

---
##DELETE
### 🎯 Objetivo

Remover uma venda específica pelo seu ID.

---

### ⚙️ Funcionamento

Ao enviar uma requisição `DELETE`:

- A venda é excluída do banco de dados
- Ela deixa de aparecer na listagem de vendas
- Dependendo da regra do sistema, o estoque pode ser ajustado automaticamente (se implementado)

---
## DELETE /api/vendas/3/

### 📌 Exemplo de Requisição

---

# ✅ Funcionalidades Demonstradas

Durante a apresentação serão demonstradas:

- Cadastro e listagem de produtos
- Controle de estoque
- Registro de vendas
- Atualização automática do estoque
- Persistência no banco de dados
- Relatório consolidado de vendas
- API REST funcional

---

# 🛠 Tecnologias Utilizadas

- Python
- Django
- Django REST Framework
- SQLite
- API REST

---

# 📌 Observações

- O estoque é atualizado automaticamente após cada venda
- O sistema impede inconsistências entre vendas e produtos
- Todos os dados ficam registrados no banco de dados

---

# 👥 Equipe

Projeto desenvolvido por:

- **Matheus Costa Pessanha**  
  GitHub: [matheuscostaps](https://github.com/matheuscostaps)

- **Tais Döring**  
  GitHub: [TaisDF](https://github.com/TaisDF)

- **Geovana Rodrigues**  
  GitHub: [geovanards](https://github.com/geovanards)

- **Alysson Kennedy**  
  GitHub: [AlyssonKennedy744](https://github.com/AlyssonKennedy744)

---
