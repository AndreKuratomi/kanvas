## KANVAS

- [Sobre](#sobre)
- [Instalação](#instalação)
- [Documentação](#documentação)
- [Termos de uso](#termos-de-uso)

<br>

# Sobre

<p><b>TypeORM_CRUD-de-usuario-JWT</b> é uma aplicação de gerenciamento de usuários com endpoints de pedem autenticação com token. Esta aplicação utiliza o ambiente de execução Node.js e o framework Express.js, além do ORM TypeORM e a plataforma Docker.</p>
<br>

# Instalação

<h5>0. Primeiramente, é necessário já ter instalado na própria máquina:</h5>

- <p> Um <b>editor de código</b>, conhecido também como <b>IDE</b>. Por exemplo, o <b>[Visual Studio Code (VSCode)](https://code.visualstudio.com/)</b>.</p>

- <p> Uma <b>ferramenta cliente de API REST</b>. Por exemplo, o <b>[Insomnia](https://insomnia.rest/download)</b> ou o <b>[Postman](https://www.postman.com/product/rest-client/)</b>.</p>

- <p> E versionar o diretório para receber o clone da aplicação:</p>

```
git init
```

<br>
<h5>1. Fazer o clone do reposítório <span style="text-decoration: underline">Users service</span> na sua máquina pelo terminal do computador ou pelo do IDE:</h5>

```
git clone git@gitlab.com:ABKURA/kanvas.git
```

<p>Entrar na pasta criada:</p>

```
cd kanvas
```

Após feito o clone do repositório Kanvas, instalar:

1. O ambiente virtual e atualizar suas dependências com o seguinte comando:

```
python -m venv venv --upgrade-deps
```

2. Ative o seu ambiente virtual com o comando:

```
source/venv/bin/activate
```

3. E instalar suas dependências:

```
pip install -r requirements.txt
```

3. E rodar a aplicação:

```
code .
```

# Documentação

Para ter acesso ao descrições detalhes das rotas e seus retornos, conferir documentação completa no link a seguir:

https://manual-api-kenziedoc.vercel.app/

# Termos de uso

Esse projeto atende a fins exclusivamente didáticos e sem nenhum intuito comercial.
