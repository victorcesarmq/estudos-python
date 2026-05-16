if __name__ == '__main__':
    alunos = []
    notas = []

    for _ in range(int(input())):
        name = input()
        score = float(input())
        alunos.append([name, score])

    for aluno in alunos:
        notas.append(aluno[1])

    notas_unicas = sorted(set(notas))
    segunda_menor_nota = notas_unicas[1]

    resultado = []
    for aluno in alunos:
        if aluno[1] == segunda_menor_nota:
            resultado.append(aluno[0])

    resultado.sort()
    for nome in resultado:
        print(nome)
