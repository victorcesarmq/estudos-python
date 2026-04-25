import random

NMB = int(input("Digite o numero mais baixo:"))
NMA = int(input("Agora digite o numero mais alto:"))
NUMEROESCOLHIDO = int(input(f"Escolha um numero que esta entre {NMB} e {NMA}: "))

#USUARIO ESCOLHE NUMERO FORA DO LIMITE
if NUMEROESCOLHIDO < NMB:
        print("O numero escolhido e menor que o limite")
        exit()

elif NUMEROESCOLHIDO > NMA:
        print("O numero escolhido e maior do que o limite")
        exit()

else:
    numeroaleatorio = random.randint(NMB, NMA)
#---------------------------------------------------------------------------------------
    print()
#---------------------------------------------------------------------------------------
    print (f"O numero sorteado foi {numeroaleatorio} e o seu numero é {NUMEROESCOLHIDO}")

