db = []

running = True

def create_name(first, last):
    first = first.capitalize()
    last = last.capitalize()
    return first + " " + last

while running:
    first = input("Qual o seu primeiro nome: ")
    last = input("Qual o seu ultimo nome: ")

    full_name = create_name(first, last)
    db.append(full_name)

    sair = input("Digite (q) para sair ou ENTER para continuar: ")

    if sair.lower() == "q":
        running = False

print("Lista de nomes:")
for nome in db:
    print(nome)
