
linha1 = list(map(float, input().split()))
linha2 = list(map(float, input().split()))

print(linha1,linha2)

x_um, y_um = linha1
x_dois, y_dois = linha2

distancia = (((x_um - x_dois)**2) + ((y_dois - y_um)**2)) ** (1/2)
print(distancia)