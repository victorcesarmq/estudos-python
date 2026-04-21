valores = {"dolar": 1,"real": 5.23,"euro": 0.86,"gbp": 1.23}

# Funcao para converter as moedas
def conversao(moeda1, moeda2):
    conversaodollar = caixa / valores.get(moeda1)
    conversaofinal = conversaodollar * valores.get(moeda2)
    return conversaofinal

print()
print("-----------------------------------------------------")
print("OPCOES".center(50))
print("Dolar".center(50))
print("Real".center(50))
print("Euro".center(50))
print("Gbp".center(50))
print("-----------------------------------------------------")
print()

while True:
    moeda1 = input("Qual a sua moeda inicial: ").lower()
    if moeda1 not in valores.keys():
        print("Essa moeda não esta disponivel para conversão ou não existe")
    else:
        break

while True:
        try:
            caixa = float(input(f"Digite quantos você tem em {moeda1} para conversão:"))
            break
        except ValueError:
            print("Digite um valor valido")

while True:
    moeda2 = input("Digite para qual moeda você deseja trocar: ")
    if moeda2 not in valores.keys():
        print("A moeda nao e valida ou nao esta disponivel")
    else:
        break

if moeda2 in ("dolar", "euro", "gbp"):
    print(f"O valor final que voce vai ter em {moeda2} é de: ${conversao(moeda1, moeda2):.2f}")
else:
    print(f"O valor final que voce vai ter em {moeda2} é de: R${conversao(moeda1, moeda2):.2f}")
