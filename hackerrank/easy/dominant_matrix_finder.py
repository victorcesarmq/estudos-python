matriz = [
    [1, 2, 7],
    [4, 5, 6],
    [8, 8, 9]
]

linhas = len(matriz)
colunas = len(matriz[0])

for linha in range(linhas):
    for elemento in range(colunas):
        valor = matriz[linha][elemento]
        dominante = True

        # verificar vizinhos
        for mov_linha in [-1, 0, 1]:
            for mov_coluna in [-1, 0, 1]:

                # ignorar a própria célula
                if mov_linha == 0 and mov_coluna == 0:
                    continue

                viz_linha = linha + mov_linha
                viz_coluna = elemento + mov_coluna

                # verificar se está dentro da matriz
                if 0 <= viz_linha < linhas and 0 <= viz_coluna < colunas:
                    if matriz[viz_linha][viz_coluna] >= valor:
                        dominante = False

        if dominante:
            print(f"Dominante: {valor} na posição ({linha}, {elemento})")