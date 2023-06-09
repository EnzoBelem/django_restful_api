# Documentação da API
Caso ainda não saiba como executar este projeto em sua máquina local confira o arquivo **README.md**.<br>
> **Dica:** para facilitar os seus testes com esta API você pode usar alguma ferramenta de desenvolvimento e teste de APIs. Algumas opções válidas são o **Postman** e o **Insomnia**.
# Entendo as regras de negócio
Assumindo que essa API seria usada num contexto fictício por uma loja, algumas regras de negócio foram criadas.
## Grupos de usuários
Os usuários desta API podem ser categorizados em três grupos:
* ### Cliente
    * Usuário com permissão limitada as rotas e funcionalidades da API. Possuem acesso a:
        * `GET/POST/PATCH/DELETE` de seu próprio perfil.
        * `GET` itens.
        * `GET/POST` de seus próprios pedidos.
* ### Funcionário
    * Usuário com menos restrições as rotas e funcionalidades da API. Possuem acesso a:
        * `GET/POST/PATCH/DELETE` do perfil de usuários do grupo *Cliente*.
        * `GET/POST/PATCH/DELETE` itens.
        * `GET/POST` pedidos.
* ### Gerência
    * Usuário sem restrições as rotas e funcionalidades da API.
# Rotas da API
## Recurso: Usuário
A autenticação de usuários na API é feita por meio de Token, esse Token deve ser incluido no cabeçalho em todas as requisições que exigem autenticação.
## Autenticação
Retorna o Token de autenticação do usuário.<br>
> Não exige Token de autenticação no cabeçalho da requisição.
* Rota: `/auth/`
* Método: `POST` 

Parâmetros do Corpo (JSON)
```
{
	"username": "cliente",
	"password": "1234"
}
```
Resposta
```
{
	"token": <token>
}
```
## Cadastro de clientes
Criar um novo usuário do grupo Cliente.<br>
> Não exige Token de autenticação no cabeçalho da requisição.
* Rota: `/usuarios/signup/`
* Método: `POST` 

Parâmetros do Corpo (JSON)
```
{
	"username": "cliente",
	"password": "1234",
	"first_name": "Enzo",
	"last_name": "Belém",
	"email": "enzo@email.com"
}
```
Resposta
```
{
	"username": "cliente",
	"first_name": "Enzo",
	"last_name": "Belém",
	"email": "enzo@email.com"
}
```
## Listagem total/restrita de usuários
Retorna uma lista total/restrita dos usuários criados.
> Grupo Cliente não tem acesso a dados além do seus própios. <br>
Outros grupos tem acesso completo.

* Rota: `/usuarios/`
* Método: `GET`

Parâmetros do Cabeçalho
```
Authorization: Token <token>
```
Resposta 

Grupo: Cliente
```
{
	"username": "cliente",
	"first_name": "Enzo",
	"last_name": "Belém",
	"email": "enzo@email.com"
}
```
Grupo: Funcionário, Gerência
```
[
	{
		"id": 6,
		"username": "admin",
		"first_name": "Admin",
		"last_name": "Admin",
		"email": "admin@email.com",
		"groups": []
	},
	{
		"id": 48,
		"username": "cliente",
		"first_name": "Enzo",
		"last_name": "Belém",
		"email": "enzo@email.com",
		"groups": [
			"Cliente"
		]
	}
]
```
## Criação de usuários
Criação de usuários de todos os grupos.<br>
> Grupo Cliente não tem acesso a essa rota.<br>
> Grupo Funcionário tem acesso restrito para criar apenas usuários do grupo Cliente.<br>

* Rota: `/usuarios/`
* Método: `POST`

Parâmetros do Cabeçalho
```
Content-Type: application/json
Authorization: Token <token>
```
Parâmetros do Corpo (JSON)
```
{
	"username": "funcionario",
	"password": "1234",
	"first_name": "Jonas",
	"last_name": "Silva",
	"email": "funcionario@email.com",
	"group": "Funcionário"
}
```
Resposta 
```
{
	"id": 49,
	"username": "funcionario",
	"first_name": "Jonas",
	"last_name": "Silva",
	"email": "funcionario@email.com"
}
```
## Obter dados do usuário específico
Retorna os detalhes de um usuário específico. <br>
> Grupo Cliente tem acesso restrito a seus próprios dados.<br>
> Outros grupos tem acesso completo.

* Rota: `/usuarios/{username}/`
* Método: `GET`

Parâmetros da URL

* `{username}` (obrigatório): O username do usuário.

Parâmetros do Cabeçalho
```
Authorization: Token <token>
```
Resposta 
```
{
	"id": 49,
	"username": "funcionario",
	"first_name": "Jonas",
	"last_name": "Silva",
	"email": "funcionario@email.com",
	"groups": [
		"Funcionário"
	]
}
```
## Alterar dados do usuário específico
Permite alterar dados de um usuário específico.<br>
> Grupo Cliente tem acesso restrito para alterar seus próprios dados.<br>
> Grupo Funcionário tem acesso restrito para alterar usuários do grupo Cliente.

* Rota: `/usuarios/{username}/`
* Método: `PATCH`

Parâmetros da URL

* `{username}` (obrigatório): O username do usuário.

Parâmetros do Cabeçalho
```
Content-Type: application/json
Authorization: Token <token>
```
Parâmetros do Corpo (JSON)
```
{
	"username": "funcionario_editado",
	"email": "funcionario_editado@email.com"
}
```
Resposta 
```
{
	"id": 49,
	"username": "funcionario_editado",
	"first_name": "Jonas",
	"last_name": "Silva",
	"email": "funcionario_editado@email.com"
}
```
## Remover usuário específico
Permite remover um usuário específico.<br>
> Grupo Cliente tem acesso restrito para remover a si mesmo.<br>
> Grupo Funcionário tem acesso restrito para remover usuários do grupo Cliente.

* Rota: `/usuarios/{username}/`
* Método: `DELETE`

Parâmetros da URL

* `{username}` (obrigatório): O username do usuário.

Parâmetros do Cabeçalho
```
Content-Type: application/json
Authorization: Token <token>
```
## Obter todos os pedidos do usuário específico
Retorna todos os pedidos de um usuário específico. <br>
> Grupo Cliente tem acesso restrito a seus próprios dados.<br>
> Outros grupos tem acesso completo.

* Rota: `/usuarios/{username}/pedidos/`
* Método: `GET`

Parâmetros da URL

* `{username}` (obrigatório): O username do usuário.

Parâmetros do Cabeçalho
```
Authorization: Token <token>
```
Resposta 
```
[
	{
		"codigo_pedido": "FGPK8KY3",
		"data_criacao": "2023-06-08T23:27:34.854804-03:00"
	},
	{
		"codigo_pedido": "6F67NTF6",
		"data_criacao": "2023-06-08T23:38:45.706682-03:00"
	}
]
```
***
## Recurso: Item
## Listagem de itens
Retorna uma lista de todos os itens cadastrados.
> Não exige Token de autenticação no cabeçalho da requisição.
* Rota: `/itens/`
* Método: `GET`

Resposta 

Requisição sem autenticação/ Grupo: Cliente 
```
[
	{
		"codigo_item": "item_1",
		"nome": "Sapato Masculino",
		"descricao": "Sapato social masculino.",
		"preco": 225.5
	},
	{
		"codigo_item": "item_2",
		"nome": "Meia Infantil",
		"descricao": "Meia Infantil unissex.",
		"preco": 20.2
	}
]
```
Grupo: Funcionário, Gerência
```
[
	{
		"id": 4,
		"codigo_item": "item_1",
		"nome": "Sapato Masculino",
		"descricao": "Sapato social masculino.",
		"preco": 225.5,
		"quantidade_estoque": 13
	},
	{
		"id": 5,
		"codigo_item": "item_2",
		"nome": "Meia Infantil",
		"descricao": "Meia Infantil unissex.",
		"preco": 20.2,
		"quantidade_estoque": 0
	}
]
```
## Criação de itens
Cria um novo item com base nos dados fornecidos.
> Grupo Cliente não tem acesso a rota.<br>
> Outros grupos tem acesso completo.

* Rota: `/itens/`
* Método: `POST`

Parâmetros do Cabeçalho
```
Content-Type: application/json
Authorization: Token <token>
```
Parâmetros do Corpo (JSON)
```
{
	"codigo_item": "item_2",
	"nome": "Meia Infantil",
	"descricao": "Meia Infantil unissex.",
	"preco": 20.2,
	"quantidade_estoque": 5
}
```
Resposta 
```
{
	"id": 5,
	"codigo_item": "item_2",
	"nome": "Meia Infantil",
	"descricao": "Meia Infantil unissex.",
	"preco": 20.2,
	"quantidade_estoque": 5
}
```
## Obter dados do item especifico
Retorna os dados do item especifico.
> Não exige Token de autenticação no cabeçalho da requisição.
* Rota: `/itens/{codigo_item}/`
* Método: `GET`

Parâmetros da URL

* `{codigo_item}` (obrigatório): O código do item.

Parâmetros do Cabeçalho
```
Content-Type: application/json
Authorization: Token <token>
```
Resposta 
```
{
	"codigo_item": "item_1",
	"nome": "Sapato Masculino",
	"descricao": "Sapato social masculino.",
	"preco": 225.5
}
```
## Alterar dados do item especifico
Alterar dados do item especifico com base nos dados fornecidos.
> Grupo Cliente não tem acesso a rota.<br>
> Outros grupos tem acesso completo.

* Rota: `/itens/{codigo_item}/`
* Método: `PATCH`

Parâmetros da URL

* `{codigo_item}` (obrigatório): O código do item.

Parâmetros do Cabeçalho
```
Content-Type: application/json
Authorization: Token <token>
```
Parâmetros do Corpo (JSON)
```
{
	"nome": "Sapato Masculino editado",
	"quantidade_estoque": 15
}
```
Resposta 
```
{
	"id": 4,
	"codigo_item": "item_1",
	"nome": "Sapato Masculino editado",
	"descricao": "Sapato social masculino.",
	"preco": 225.5,
	"quantidade_estoque": 15
}
```
## Remover item específico
Permite remover um item específico.<br>
> Grupo Cliente não tem acesso a rota.<br>
> Outros grupos tem acesso completo.

* Rota: `/itens/{codigo_item}/`
* Método: `DELETE`

Parâmetros da URL

* `{codigo_item}` (obrigatório): O código do item.

Parâmetros do Cabeçalho
```
Content-Type: application/json
Authorization: Token <token>
```
***
## Recurso: Pedido
## Listagem de pedidos
Retorna uma lista de todos os pedidos cadastrados.
> Grupo Cliente tem acesso restrito a seus próprios pedidos.<br>
> Outros grupos tem acesso completo.

* Rota: `/pedidos/`
* Método: `GET`

Parâmetros do Cabeçalho
```
Content-Type: application/json
Authorization: Token <token>
```
Resposta 

Grupo: Cliente 
```
[
	{
		"codigo_pedido": "FGPK8KY3",
		"data_criacao": "2023-06-08T23:27:34.854804-03:00"
	},
	{
		"codigo_pedido": "6F67NTF6",
		"data_criacao": "2023-06-08T23:38:45.706682-03:00"
	}
]
```
Grupo: Funcionário, Gerência
```
[
	{
		"id": 11,
		"codigo_pedido": "21XUKMDN",
		"usuario": "funcionario",
		"data_criacao": "2023-06-08T23:24:28.937239-03:00"
	},
	{
		"id": 12,
		"codigo_pedido": "FGPK8KY3",
		"usuario": "cliente",
		"data_criacao": "2023-06-08T23:27:34.854804-03:00"
	},
	{
		"id": 13,
		"codigo_pedido": "6F67NTF6",
		"usuario": "cliente",
		"data_criacao": "2023-06-08T23:38:45.706682-03:00"
	}
]
```
## Criação de Pedidos
Cria um novo pedido com base nos dados fornecidos. Caso o `username` não seja explicitado no corpo será criado para o usuário que realizou a requisição.
> Grupo Cliente tem acesso restrito para criação de seus próprios pedidos.<br>
> Outros grupos tem acesso completo.

* Rota: `/pedidos/`
* Método: `POST`

Parâmetros do Cabeçalho
```
Content-Type: application/json
Authorization: Token <token>
```
Parâmetros do Corpo (JSON)
```
{
	"usuario": "cliente",
    "itens": [
        {
            "item": "item_1",
            "quantidade": 3
        },
        {
            "item": "item_2",
            "quantidade": 5
        }
    ]
}
```
Resposta 
```
{
	"id": 15,
	"codigo_pedido": "01YHBIUM",
	"usuario": "cliente",
	"data_criacao": "2023-06-09T00:35:43.759289-03:00",
	"itens": [
		{
			"id": 26,
			"item": "item_1",
			"descricao": "Sapato social masculino.",
			"quantidade": 3
		},
		{
			"id": 27,
			"item": "item_2",
			"descricao": "Meia Infantil unissex.",
			"quantidade": 5
		}
	]
}
```
## Obter dados de pedido específico
Retorna os dados completos de um pedido específico. <br>
> Todos os grupos tem acesso.

* Rota: `/pedidos/{codigo_pedido}/`
* Método: `GET`

Parâmetros da URL

* `{codigo_pedido}` (obrigatório): O código do pedido.

Parâmetros do Cabeçalho
```
Authorization: Token <token>
```
Resposta 
```
{
	"codigo_pedido": "FGPK8KY3",
	"data_criacao": "2023-06-08T23:27:34.854804-03:00",
	"itens": [
		{
			"item": "item_1",
			"descricao": "Sapato social masculino.",
			"quantidade": 3
		}
	]
}
```