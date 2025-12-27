# Flask Auth API

Uma API REST desenvolvida em Flask para gerenciamento de usuários e snacks (lanches), com sistema de autenticação e autorização utilizando Flask-Login.

## 📋 Descrição

Esta API permite que usuários se registrem, façam login e gerenciem seus próprios snacks. Cada snack possui nome, descrição, data da dieta e um flag indicando se é dietético. A API garante que cada usuário só possa acessar e modificar seus próprios snacks.

## 🛠️ Tecnologias Utilizadas

- **Flask** 3.1.2 - Framework web
- **Flask-SQLAlchemy** 3.1.1 - ORM para banco de dados
- **Flask-Login** 0.6.3 - Gerenciamento de autenticação
- **bcrypt** 5.0.0 - Hash de senhas
- **SQLAlchemy** 2.0.45 - ORM
- **SQLite** - Banco de dados

## 📦 Pré-requisitos

- Python 3.7 ou superior
- pip (gerenciador de pacotes do Python)

## 🚀 Instalação

1. Clone o repositório:
```bash
git clone <url-do-repositorio>
cd flask_auth_api
```

2. Crie um ambiente virtual (recomendado):
```bash
python -m venv venv
```

3. Ative o ambiente virtual:

   **Windows (PowerShell):**
   ```powershell
   .\venv\Scripts\Activate.ps1
   ```

   **Windows (CMD):**
   ```cmd
   venv\Scripts\activate.bat
   ```

   **Linux/Mac:**
   ```bash
   source venv/bin/activate
   ```

4. Instale as dependências:
```bash
pip install -r requirements.txt
```

## 🏃 Como Executar

1. Certifique-se de que o ambiente virtual está ativado
2. Execute a aplicação:
```bash
python app.py
```

A API estará disponível em `http://127.0.0.1:5000`


## 📁 Estrutura do Projeto

```
flask_auth_api/
│
├── app.py              # Arquivo principal da aplicação com todas as rotas
├── database.py         # Configuração do SQLAlchemy
├── requirements.txt    # Dependências do projeto
├── route.http          # Exemplos de requisições HTTP
├── Readme.md          # Este arquivo
│
├── model/
│   ├── User.py        # Modelo de usuário
│   └── Snack.py       # Modelo de snack
│
└── instance/
    └── database.db    # Banco de dados SQLite (criado automaticamente)
```

## 🔌 Endpoints da API

### Autenticação

#### POST `/register`
Registra um novo usuário.

**Body (JSON):**
```json
{
    "name": "João Silva",
    "email": "joao@example.com",
    "password": "senha123"
}
```

**Resposta (201):**
```json
{
    "message": "User created successful",
    "user": {
        "id": 1,
        "name": "João Silva",
        "email": "joao@example.com",
        "created_at": "2024-01-15T10:30:00"
    }
}
```

#### POST `/login`
Autentica um usuário existente.

**Body (JSON):**
```json
{
    "email": "joao@example.com",
    "password": "senha123"
}
```

**Resposta (200):**
```json
{
    "message": "Login successful"
}
```

#### GET `/logout`
Encerra a sessão do usuário autenticado.

**Headers:**
- Requer autenticação (sessão ativa)

**Resposta (200):**
```json
{
    "message": "Logout success"
}
```

### Snacks

#### POST `/snacks`
Cria um novo snack.

**Headers:**
- Requer autenticação (sessão ativa)
- `Content-Type: application/json`

**Body (JSON):**
```json
{
    "name": "Hambúrguer",
    "description": "Hambúrguer artesanal com queijo",
    "diet_date": "2024-01-20T16:00:00",
    "diet": false
}
```

**Resposta (200):**
```json
{
    "message": "Snack created sucessful",
    "snack": {
        "id": 1,
        "name": "Hambúrguer",
        "description": "Hambúrguer artesanal com queijo",
        "diet": false,
        "user_id": 1,
        "created_at": "2024-01-15T10:35:00"
    }
}
```

#### GET `/snacks`
Lista todos os snacks do usuário autenticado.

**Headers:**
- Requer autenticação (sessão ativa)

**Resposta (200):**
```json
{
    "snacks": [
        {
            "id": 1,
            "name": "Hambúrguer",
            "description": "Hambúrguer artesanal com queijo",
            "diet": false,
            "user_id": 1,
            "created_at": "2024-01-15T10:35:00"
        }
    ]
}
```

#### GET `/snacks/<id>`
Retorna um snack específico.

**Headers:**
- Requer autenticação (sessão ativa)

**Resposta (200):**
```json
{
    "snack": {
        "id": 1,
        "name": "Hambúrguer",
        "description": "Hambúrguer artesanal com queijo",
        "diet": false,
        "user_id": 1,
        "created_at": "2024-01-15T10:35:00"
    }
}
```

#### PUT `/snacks/<id>`
Atualiza um snack existente.

**Headers:**
- Requer autenticação (sessão ativa)
- `Content-Type: application/json`

**Body (JSON):**
```json
{
    "name": "Hambúrguer Editado",
    "description": "Nova descrição",
    "diet_date": "2024-01-21T16:00:00",
    "diet": true
}
```

**Resposta (200):**
```json
{
    "message": "Snack update successfully",
    "snack": {
        "id": 1,
        "name": "Hambúrguer Editado",
        "description": "Nova descrição",
        "diet": true,
        "user_id": 1,
        "created_at": "2024-01-15T10:35:00"
    }
}
```

#### DELETE `/snacks/<id>`
Remove um snack.

**Headers:**
- Requer autenticação (sessão ativa)

**Resposta (200):**
```json
{
    "message": "Snack remove successfully"
}
```

## ⚠️ Códigos de Status HTTP

- `200` - Sucesso
- `201` - Criado com sucesso
- `400` - Requisição inválida
- `401` - Não autenticado
- `403` - Não autorizado
- `404` - Recurso não encontrado


