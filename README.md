## kanvas

- [Sobre](#sobre)
- [Instalação](#instalação)
- [Documentação](#documentação)
- [Termos de uso](#termos-de-uso)

<br>

# Sobre

<b>kanvas</b> é uma API de gerenciamento de usuários e cursos semelhante à plataforma [Canvas](https://www.canvas.net/). Esta aplicação utiliza o framework Django.
<br>

# Instalação

<h5>0. Primeiramente, é necessário já ter instalado na própria máquina:</h5>

- Um <b>editor de código</b>, conhecido também como <b>IDE</b>. Por exemplo, o <b>[Visual Studio Code (VSCode)](https://code.visualstudio.com/)</b>.

- Uma <b>ferramenta cliente de API REST</b>. Por exemplo, o <b>[Insomnia](https://insomnia.rest/download)</b> ou o <b>[Postman](https://www.postman.com/product/rest-client/)</b>.

- <p> E versionar o diretório para receber o clone da aplicação:</p>

```
git init
```

<br>
<h5>1. Fazer o clone do reposítório <span>Kanvas</span> na sua máquina pelo terminal do computador ou pelo do IDE:</h5>

```
git clone https://github.com/AndreKuratomi/kanvas.git
```

<p>Entrar na pasta criada:</p>

```
cd kanvas
```

Após feito o clone do repositório Kanvas, instalar:

O ambiente virtual e atualizar suas dependências com o seguinte comando:

```
python -m venv venv --upgrade-deps
```

Ative o seu ambiente virtual com o comando:

```
source/venv/bin/activate
```

Instalar suas dependências:

```
pip install -r requirements.txt
```

E rodar a aplicação:

```
code .
```

# Documentação

Para ter acesso às descrições, detalhes das rotas e seus retornos, conferir documentação completa no link a seguir:

https://kanvas-documentation.vercel.app/

# Termos de uso

Esse projeto atende a fins exclusivamente didáticos e sem nenhum intuito comercial.
