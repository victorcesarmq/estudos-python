# O programa deve conter o nome do aluno, a série em que o mesmo esta e tambem a nota nas respectivas matérias.
import json
from pathlib import Path

materias_validas = ("portugues",
                    "matematica",
                    "ingles",
                    "historia",
                    "geografia")

semestres_validos = ("1 Semestre",
                     "2 Semestre",
                     "3 Semestre",
                     "4 Semestre")

id_aluno = 0


def DB_PATH():
    dbpath = path("alunos.json")
    return dbpath

def calcular_media():
    print()


def cadastrar_aluno():
    nome_aluno(pnome_aluno, sobrenome_aluno)
    return aluno


def nome_aluno():
    pnome = input("Digite o primeiro nome do aluno: ")
    unome = input("Digite o sobrenome do aluno: ")
    return pnome.capitalize() + " " + unome.capitalize()


DB_ALUNOS = {}

while True:
    #MENU INICIAL
    print("--------------------------------------------------")
    print("1. Ver notas de alunos")
    print("2. Cadastrar novo aluno")
    print("3. Alterar nota de aluno")
    print("4. Ver Alunos cadastrados")
    print("5. Sair")
    print("--------------------------------------------------")
    #-----------------------------------------------------------------
    opcao = int(input("Escolha uma opcao: "))
    if opcao == 1:
        print(f"Escolha um aluno: {aluno[0,]}")
    # -----------------------------------------------------------------
    #CADASTRO DE ALUNOS
    elif opcao == 2: #NÃO MEXER

        print("-------CADASTRO DE ALUNOS-------")
        nome = nome_aluno()
        notas = {}
        id_aluno += 1
        idade = int(input("Digite a idade do aluno: "))

        print()
    # -----------------------------------------------------------------
        for s in semestres_validos:
            atualsemestre = {}
            print(s)
            for i in materias_validas:
                print(f"Digite a nota da materia: {i.capitalize()}")
                nota = float(input("Nota: "))
                print()
                atualsemestre[i] = nota
            notas[s] = atualsemestre
    # ----------------------------------------------------------------

        aluno = {"Nome": nome,
                 "Idade": idade,
                  "Notas": notas}

        DB_ALUNOS[id_aluno] = aluno
    # -----------------------------------------------------------------
    elif opcao == 3:
        print()

    elif opcao == 4:
        for aluno in DB_ALUNOS.items():
            print(aluno["Nome"])
            print(aluno[atualsemestre(aluno)])
            print(aluno["Notas"])

    else:
        break
