# Sistema Escolar Simples

## Sobre:

O Sistema Escolar Simples é uma aplicação web desenvolvida com o objetivo de aprimorar o processo de lançamento de notas de alunos, processo de chamada e também ao acesso ao boletim do aluno de forma virtual. O sistema consegue fazer a leitura de planilhas do Excel e caso não existem, ele as cria, e com as informações da planilha, ele consegue atualizar os dados de uma pagina html.

## Ferramentas:

Para sua criação, foi utilizado o framework Flask para desenvolvimento web, sem a utilização de CSS, com foco na prática e no desenvolvimento de habilidades em programação e sistemas online. Biblioteca Pandas para fazer consultoria de base de dados do Excel.

## Como utilizar

Para utilizar o Sistema de Escolar Simples, basta executar o arquivo "main.py" e acessar o endereço "127.0.0.1/5000" em seu navegador. Na página inicial, temos duas opções, a de Portal do Aluno e Portal do Professor, caso você seja algum dos dois, você clica em algum dos dois e ele o redicionará para a pagina de Login, onde o usuário deve informar seu nome de usuário e senha cadastrados ou se caso for aluno, a matricula e a senha que estão previamente no sistema. O aluno tem acesso ao seu boletim e o Professor tem acesso a área de Lançamento de Notas e a área de Chamada da Turma. Cada uma delas o professor consegue escolher a turma correspondente ao seu id, bimestre, e a sua matéria.

## Observações

Este Sistema é simples, portanto não há complexidade nos códigos e na estruturação do Sistema.

## Usuários para testar

Professor:
* usuario: daniel
* senha: 123

Aluno: 
* 2023-1-98
* senha: 123

Caso você queria acessar outros usuários e outros alunos, basta acessar as planilhas users.xlsx e students.xlsx

