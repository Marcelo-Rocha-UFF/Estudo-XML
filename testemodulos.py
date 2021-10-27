with open("ibm_cred.txt", "r") as ibm_cred:
	print("i")
	linhas = ibm_cred.read().splitlines()


print(type(linhas))

for linha in linhas:
	print(linha)