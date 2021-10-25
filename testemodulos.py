
s = "Seus pontos são #x agora e #y e nao #pontos como vc disse antes."

variaveis = {"x":10, "y":20, "pontos":30}
st_nova = s

for i in range(len(s)):
	if s[i] == "#":
		inicio = i
		
		while s[i] != " ":
			i += 1
			if i == len(s):
				break
		if i - inicio > 0:
			for v in variaveis:
				if v == s[inicio + 1: i]:
					st_nova = st_nova.replace(s[inicio: i], str(variaveis[v]))
print(s)
print(st_nova)				