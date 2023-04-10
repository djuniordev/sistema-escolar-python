# Routes do Sistema Escolar Simples

# Importação das Bibliotecas

from flask import Flask, render_template, request, flash, redirect, url_for, session
import pandas as pd
from datetime import datetime
import os
from Sistema import app

# Definindo os caminhos

# Pagina Inicial > Portais


@app.route('/')
def portais():
    return render_template('portais.html')

# Portal do Aluno e Portal do Professor


@app.route('/portal_aluno')
def portal_aluno():
    return render_template('portal_aluno.html')


@app.route('/portal_professor')
def portal_professor():
    return render_template('portal_professor.html')

# Home do Aluno e do Professor


@app.route('/home_aluno', methods=['POST', 'GET'])
def home_aluno():
    table_students = pd.read_excel("tables/students.xlsx")
    try:
        matricula = request.form['matricula']
        password = request.form['password']
        session['matricula'] = request.form['matricula']
        session['password'] = request.form['password']
    except:
        matricula = session.get('matricula')
        password = session.get('password')
    for i in range(len(table_students)):
        if table_students['matricula'][i] == matricula and str(table_students['senha'][i]) == password:
            idres = table_students['id'][i]
            return render_template('home_aluno.html', matricula=matricula, password=password, idres=idres)
            break
    else:
        return "Usuario Não cadastrado!"


@app.route('/home_professor', methods=['POST', 'GET'])
def home_professor():
    table_users = pd.read_excel("tables/users.xlsx")
    try:
        user = request.form['user']
        password = request.form['password']
        session['user'] = request.form['user']
        session['password'] = request.form['password']
    except:
        user = session.get('user')
        password = session.get('password')
    for i in range(len(table_users)):
        if table_users['user'][i] == user and str(table_users['password'][i]) == password:
            idres = table_users['id'][i]
            return render_template('home_professor.html', user=user, password=password, idres=idres)
            break
    else:
        return "Usuario Não cadastrado!"

# Pagina de Boletim do Aluno


@app.route('/boletim', methods=["POST"])
def boletim():
    table_students = pd.read_excel("tables/students.xlsx")
    table_classes = pd.read_excel("tables/classes.xlsx")
    table_subjects = pd.read_excel("tables/subjects.xlsx")
    matricula = request.form['matricula']
    idres = request.form['idres']
    idres = int(idres)
    for i in range(len(table_students)):
        if table_students['id'][i] == idres:
            turma = table_students['turma'][i]

    try:
        presenca = pd.read_excel('tables/presenca_{}.xlsx'.format(turma))
    except:
        presenca = pd.DataFrame()
        n_faltas = 0

    for i in range(len(presenca)):
        if presenca['id'][i] == idres:
            linha = presenca.loc[i]
            n_faltas = linha.str.contains('falta').sum()
    size_table_subjects = len(table_subjects)
    size_table_students = len(table_students)
    size_table_classes = len(table_classes)
    bimestre = ['1', '2', '3', '4']
    notas_1 = pd.DataFrame()
    notas_2 = pd.DataFrame()
    notas_3 = pd.DataFrame()
    notas_4 = pd.DataFrame()
    try:
        notas_1 = pd.read_excel(
            'tables/notas/nota_{}EF_1BI.xlsx'.format(turma[0]))
        notas_2 = pd.read_excel(
            'tables/notas/nota_{}EF_2BI.xlsx'.format(turma[0]))
        notas_3 = pd.read_excel(
            'tables/notas/nota_{}EF_3BI.xlsx'.format(turma[0]))
        notas_4 = pd.read_excel(
            'tables/notas/nota_{}EF_4BI.xlsx'.format(turma[0]))
    except:
        pass

    try:
        size_notas_1 = len(notas_1)
        size_notas_2 = len(notas_2)
        size_notas_3 = len(notas_3)
        size_notas_4 = len(notas_4)
    except:
        pass

    media_final = [0] * len(table_subjects)

    for i in range(len(table_subjects)):
        materia = table_subjects['materia'][i]
        notas_materia = []
        if materia in notas_1:
            for j in range(len(notas_1[materia])):
                if notas_1['id'][j] == idres:
                    notas_materia.append(notas_1[materia][j])
        if materia in notas_2:
            for j in range(len(notas_2[materia])):
                if notas_2['id'][j] == idres:
                    notas_materia.append(notas_2[materia][j])
        if materia in notas_3:
            for j in range(len(notas_3[materia])):
                if notas_3['id'][j] == idres:
                    notas_materia.append(notas_3[materia][j])
        if materia in notas_4:
            for j in range(len(notas_4[materia])):
                if notas_4['id'][j] == idres:
                    notas_materia.append(notas_4[materia][j])
        if len(notas_materia) > 0:
            media_final[i] = sum(notas_materia) / 4
    size_media_final = len(media_final)
    return render_template('boletim.html', table_subjects=table_subjects, table_students=table_students,
                           table_classes=table_classes, size_table_subjects=size_table_subjects,
                           size_table_students=size_table_students, size_table_classes=size_table_classes,
                           idres=idres, matricula=matricula, n_faltas=n_faltas, notas_1=notas_1,
                           size_notas_1=size_notas_1, notas_2=notas_2, size_notas_2=size_notas_2,
                           notas_3=notas_3, size_notas_3=size_notas_3, notas_4=notas_4,
                           size_notas_4=size_notas_4, media_final=media_final, size_media_final=size_media_final)

# Área para Lançamento de Nota e Chamada/Frequência de Alunos, mostra as turmas cadastradas com o ID do Professor.


@app.route('/<user>/classes/lancamento', methods=['POST'])
def classes_lancamento(user):
    table_classes = pd.read_excel('tables/classes.xlsx')
    table_subjects = pd.read_excel('tables/subjects.xlsx')
    size_table_classes = len(table_classes)
    size_table_subjects = len(table_subjects)
    idres = request.form['idres']
    idres = int(idres)
    return render_template('classes_lancamento.html', user=user, table_classes=table_classes, size_table_classes=size_table_classes, table_subjects=table_subjects, size_table_subjects=size_table_subjects, idres=idres)


@app.route('/<user>/classes/chamada', methods=["POST"])
def classes_chamada(user):
    table_classes = pd.read_excel('tables/classes.xlsx')
    size_table_classes = len(table_classes)
    idres = request.form['idres']
    idres = int(idres)
    return render_template('classes_chamada.html', user=user, table_classes=table_classes, size_table_classes=size_table_classes, idres=idres)

# Área para a realização de Chamada/Frequência


@app.route('/chamada', methods=["POST"])
def chamada():
    table_students = pd.read_excel('tables/students.xlsx')
    size_table_students = len(table_students)
    turma = request.form['turma']
    data = datetime.now()
    data = data.strftime("%d/%m/%Y")
    return render_template('chamada.html', turma=turma, table_students=table_students, size_table_students=size_table_students, data=data)

# Área para a realização de Lançamento de Nota


@app.route('/lancar_nota', methods=["POST"])
def lancar_nota():
    table_students = pd.read_excel('tables/students.xlsx')
    size_table_students = len(table_students)
    turma = request.form['turma']
    materia = request.form['materia']
    bimestre = request.form['bimestre']
    return render_template('lancar_nota.html', materia=materia, turma=turma, table_students=table_students, size_table_students=size_table_students, bimestre=bimestre)

# Envio de Notas e Chamada/Frequência


@app.route('/enviar_chamada', methods=["POST"])
def enviar_chamada():
    turma = request.form['turma']
    table_students = pd.read_excel('tables/students.xlsx')
    dados = []
    data = request.form['data']
    data_obj = datetime.strptime(data, '%Y-%m-%d')
    data_br = data_obj.strftime("%d/%m/%Y")
    presenca = []
    if os.path.exists('tables/presenca_{}.xlsx'.format(turma)):
        turma_presente = pd.read_excel('tables/presenca_{}.xlsx'.format(turma))
        for i in range(len(table_students)):
            if table_students['turma'][i] == turma:
                dados.append({'id': table_students['id'][i],
                              'nome': table_students['nome'][i]})
        for i in range(len(table_students)):
            if table_students['turma'][i] == turma:
                estado_presente = request.form[table_students['nome'][i]]
                presenca.append(estado_presente)
        turma_presente.loc[:, data_br] = presenca
        turma_presente.to_excel(
            'tables/presenca_{}.xlsx'.format(turma), index=False)
    else:
        for i in range(len(table_students)):
            if table_students['turma'][i] == turma:
                dados.append({'id': table_students['id'][i],
                              'nome': table_students['nome'][i]})
        for i in range(len(table_students)):
            if table_students['turma'][i] == turma:
                estado_presente = request.form[table_students['nome'][i]]
                presenca.append(estado_presente)
        df = pd.DataFrame(dados)
        df.loc[:, data_br] = presenca
        df.to_excel('tables/presenca_{}.xlsx'.format(turma), index=False)

    return render_template('enviado.html')


@app.route('/enviar_nota', methods=["POST"])
def enviar_nota():
    table_students = pd.read_excel('tables/students.xlsx')
    turma = request.form['turma']
    materia = request.form['materia']
    bimestre = request.form['bimestre']
    notas = []
    nova_tabela = []

    if os.path.exists('tables/notas/nota_{}EF_{}BI.xlsx'.format(turma[0], bimestre[0])):
        atualizar = pd.read_excel(
            'tables/notas/nota_{}EF_{}BI.xlsx'.format(turma[0], bimestre[0]))
        for i in range(len(table_students)):
            if table_students['turma'][i] == turma:
                nova_tabela.append(
                    {'id': table_students['id'][i], 'nome': table_students['nome'][i]})
        for i in range(len(table_students)):
            if table_students['turma'][i] == turma:
                nota = request.form[table_students['nome'][i]]
                nota = nota.replace(',', '.')
                nota = '{:.1f}'.format(float(nota))
                notas.append(float(nota))
        atualizar.loc[:, materia] = notas
        atualizar.to_excel(
            'tables/notas/nota_{}EF_{}BI.xlsx'.format(turma[0], bimestre[0]), index=False)
    else:
        for i in range(len(table_students)):
            if table_students['turma'][i] == turma:
                nova_tabela.append({'id': table_students['id'][i],
                                    'nome': table_students['nome'][i]})
        for i in range(len(table_students)):
            if table_students['turma'][i] == turma:
                nota = request.form[table_students['nome'][i]]
                nota = nota.replace(',', '.')
                nota = '{:.1f}'.format(float(nota))
                notas.append(float(nota))
        df = pd.DataFrame(nova_tabela)
        df.loc[:, materia] = notas
        df.to_excel(
            'tables/notas/nota_{}EF_{}BI.xlsx'.format(turma[0], bimestre[0]), index=False)

    return render_template('enviado.html')

# Redirecionamento para voltar para as paginas anteriores


@app.route('/voltar_professor', methods=['POST', 'GET'])
def voltar_professor():

    return redirect(url_for('home_professor'))


@app.route('/voltar_aluno', methods=['POST', 'GET'])
def voltar_aluno():

    return redirect(url_for('home_aluno'))
