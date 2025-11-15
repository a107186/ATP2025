#TPC7:


##TPC1:


##a) 

lista1 = [1, 2, 3, 4, 5]
lista2 = [4, 5, 6, 7, 8]  
ncomuns = []

for n in lista1:
    if n not in lista2:
        ncomuns.append(n)

for n in lista2:
    if n not in lista1:
        ncomuns.append(n)

print(ncomuns)

###b) 

texto = """Insistir na igualdade de direitos não é sobre tirar privilégios, 
mas sim sobre garantir que todos tenham as mesmas oportunidades de viver com dignidade e respeito."""
lista = []
palavras = texto.split()
for n in palavras:
    if len(n) > 3:
        lista.append(n)

print(lista)


###c
lista = ['cobra', 'burro', 'harry', 'texugo']
listaRes = []
indice = 1
for n in lista:
    listaRes.append((indice,n))
    indice += 1

print(listaRes)

##TPC2

###a)

def strCount(s, subs):
    countador = 0
    posição = 0
    while posição != -1:
        posição = s.find(subs, posição)
        if posição != -1:
            countador += 1
            posição += len(subs)

    return countador

print(strCount("cãoburrogato", "gato")) # --> 1
print(strCount("cãocãocão", "cow")) # --> 3
print(strCount("gatoburrogato", "dog")) # --> 0

###b)
def produtoM3(lista):
    min1 = lista[0]
    min2 = lista [0]
    min3 = lista [0]
    for n in lista:
        if n < min1:
            min3 = min2
            min2 = min1
            min1 = n
        else:
            if n < min2:
                min3 = min2
                min2 = n
            else:
                if n < min3:
                    min3 = n
    if min1 > min2:
        min1, min2 = min2, min1
    if min1 > min3:
        min1, min3 = min3, min1
    if min2 > min3:
        min2, min3 = min3, min2


    produto = min1*min2*min3
    return  produto

print(produtoM3([12,3,7,10,12,8,9]))

###c)
def reduxInt(n):
    somafinal=100
    while somafinal > 9:
        soma=0
        digito =[int(d) for d in str(n)]
        for h in digito:
            soma += h
        somafinal = soma
        n = soma

    return soma

reduxInt(6)

###d)
def myIndexOf(s1, s2):
    posição=-1
    if s2 in s1:
        for n in range(len(s1)):
            if s1[n:n+len(s2)] == s2:
                posição = n
    return posição

myIndexOf("Hoje o dia está lindo!", "está")


## tpc3
### a)
def quantosPost(redeSocial):
    return len(redeSocial)

### b)
def postsAutor(redeSocial, autor):
    lista = []
    for post in redeSocial:
        if autor == post["autor"]:
            lista.append(post)
    return lista

### c)
def autores(redeSocial): 
    lista=[]
    for post in redeSocial:
        if "autor" in post:
            lista.append(post["autor"])
    return  lista

### d)
def insPost(redeSocial, conteudo, autor, dataCriacao, comentarios):
    id = f"p{len(redeSocial)+1}"
    post = {"id" : id, "conteudo" : conteudo, "autor" : autor, 'dataCriacao': dataCriacao, 'comentarios': comentarios}
    return redeSocial.append(post)

### e)
def remPost(redeSocial, id):
    redeSocial = [post for post in redeSocial if post["id"] != id]
    return redeSocial


###f)
def postsPorAutor(redeSocial):
    distrib = {}
    for post in redeSocial:
        autor = post.get("autor")
        if autor in distrib:
            distrib[autor] += 1
        else:
            distrib[autor] = 1
    return distrib

###g)
def comentadoPor(redeSocial, autor):
    lista = []
    for post in redeSocial:
        if "comentarios" in post:
            for comentario in post["comentarios"]:
                if comentario.get("autor") == autor:
                    lista.append(post)
    return lista 


