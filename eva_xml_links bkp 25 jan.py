import sys
import xml.etree.ElementTree as ET

tree = ET.parse(sys.argv[1])  # arquivo de codigo xml
root = tree.getroot() # evaml root node
script_node = root.find("script")
pilha = [] # pilha de nodes (enderecos)

###############################################################################
# aqui estão os métodos que geram os links que conectam os nós                #
###############################################################################

lista_links = [] # lista provisoria com os links gerados

def cria_link(node_from, node_to):
    # node stop como node_to
    if (node_to.tag == "stop"): # stop nao pode ser node_to
        return

    # a conexão de um switch com outro elemento deve fazer com que o ultimo elemento de cada <case> seu (do switch) se conecte ao node_to
    # a concexão não ocorrerá caso o ultimo elemento de um <case> seja o <stop> ou seja um <goto>
    if node_from.tag == "switch":
        # vamos percorrer os elementos case e default do switch
        for case_elem in node_from:
            qtd = len(case_elem)
            # só precisamos do ultimo elemento de cada bloco case/default
            if (qtd == 0): # case vazio, conecta o <case> ao node_to
                lista_links.append(case_elem.attrib["key"] + "," + node_to.attrib["key"])
            else:
                # caso do <stop> e do <goto>. Nesses casos ocorre um bypass
                if (case_elem[qtd -1].tag == "stop") or (case_elem[qtd -1].tag == "goto"):
                    pass
                else: # caso seja outro comando, cria a conexao do comando com o node_to
                    cria_link(case_elem[qtd -1], node_to)
        return

    # <goto> não pode ser origem
    if node_from.tag == "goto": return

    # node goto com node_to
    if node_to.tag == "goto":
        for elem in script_node.iter(): # procura por target na interação
            if elem.get("id") != None:
                if elem.attrib["id"] == node_to.attrib["target"]:
                    lista_links.append(node_from.attrib["key"] + "," + elem.attrib["key"])
                else: # target id not found
                    print('  Error -> The "target" attribute from <goto> was not found:', node_to.attrib["target"])
                    exit(1) # termina com erro
        return

    # "node_to" e' uma folha, que nao contem filhos. ex.: <wait>, <light> e etc
    if len(node_to) == 0:
        lista_links.append(node_from.attrib["key"] + "," + node_to.attrib["key"])
        
    # trata os nodes com filhos
    elif (node_to.tag == "switch"): # trata o node "switch"
        for case_elem in node_to:
            # todas os cases passam a ter o atrib. "var" igual ao "var" do switch (node_to)
            case_elem.attrib["var"] = node_to.attrib["var"] 
            if case_elem.tag == "default": # preenche o default com os parametros default
                case_elem.attrib["value"] = ""
                case_elem.attrib["op"] = "exact"
            # gera o link de node_from (que veio na chamada) com o elem. (case ou default)
            lista_links.append(node_from.attrib["key"] + "," + case_elem.attrib["key"])
            # caso o case não seja vazio, gera o link entre o case e o primeiro elemento
            if (len(case_elem) == 0): # case o <case> seja vazio
                # nao conecta o <case>
                pass
            else:
                cria_link(case_elem, case_elem[0]) # conecta o <case> com o seu primeiro elemento filho
                link_process(case_elem) # processa a lista de elem. do <case>



def link_process(node_list):
    # o caso inicial é o que node_from é o elemento voice que é passado na primeira chamada de link_process()
    # neste caso, o elem. voice é inserido (temporriamente) em node_list para que ele seja sempre o primeiro elemento a ser processado.
        
    qtd = len(node_list)

    # if qtd != 0: # a ideia é tratar os casos dos blocos vazios, como o dos <cases>
    #     node_to = node_list[0] # blocos vazios não tem o elemento[0]
    #     cria_link(node_from, node_to) # se um bloco tem elemento, então tudo ok

    # if (qtd == 1) and (node_list[0].tag != "switch"):
    #     node_to = node_list[0]
    #     cria_link(node_from, node_to)

    for i in range(0, qtd-1): # processa uma lista de nós (dois a dois) A->B, B->C,...,Y->Z
        node_from = node_list[i]
        node_to = node_list[i+1]

        # case especifico da tag <stop> que deve interromper a conexao dos do fluxo sendo processado
        # todos os elem. após um <stop> são removidos. O parser emite um aviso de remoção e os exibe no terminal.
        if (node_from.tag == "stop"):
            for s in range(i, qtd-1):
                print("  Warning - removing unused commands ... <" + node_list[i+1].tag + ">")
                node_list.remove(node_list[i+1])
            break
        else:
            cria_link(node_from, node_to)
        
        # ########################################
        # if node_to.tag == "switch":
        #     if (i+1 != qtd-1): # verifica se existe algum node, dentro do fluxo corrente, depois do switch
        #         for p in range(0, len(node_to)): # empilhando no' depois do switch
        #             # a qtd de empilhamentos e' igual ao numero de cases dentro do switch
        #             pilha.append(node_list[i+2])
        #     else: # quando não ha no' depois do switch
        #         if len(pilha) != 0: # um switch com uma pilha nao vazia e' um switch interno a outro switch
        #             no_aux = pilha.pop() # pega o no mais exterior da pilha fica com -1)
        #             for p in range(0, len(node_to)+1): # nao entendi o porque do + 1.
        #                 pilha.append(no_aux) 
        #             #print("num de elem. empilhados:", len(node_to))
        #             #print("pilha: ", spilha)               # o ou os cases deverao se conectar a no mais externo

        # ########################################
        #cria_link(node_from, node_to)

    # if (len(pilha) != 0): # esse cara cria os links nos finais dos fluxos dos cases, ou do fluxo principal
    #     if qtd == 0:
    #         cria_link(node_from, pilha.pop())
    #     else:
    #         cria_link(node_to, pilha.pop())
        

def saida_links():
    # insere a tag links como ultimo elemento de root (<evaml>)
    # len(root) retorna o valor que sera o indice para o ultimo elemento
    tag_links = ET.Element("links") # cria a tag links (mae de varios links)
    root.insert(len(root), tag_links) #

    for i in range(len(lista_links)): # insere cada link como os atributos from e to, dentro do elemento <links>
        tag_link = ET.Element("link", attrib={"from" : lista_links[i].split(",")[0], "to" : lista_links[i].split(",")[1]})
        root[len(root) - 1].insert(i, tag_link)


# inserindo o elemento voice como primeiro elemento do script_node a ser processado
root.find("script").insert(0, root.find("settings").find("voice"))

# processa os links na lista de links auxiliar
link_process(script_node)

# gera os links no arquivo xml
saida_links()

print("step 03 - Creating the Elements <link>...")

# O elemento voice foi inserido ao script_node (list) para processamento, somente. 
# Agora será removido da seção script
script_node.remove(root.find("script").find("voice"))

# arquivo de saida
tree.write(root.attrib['name'] + "_EvaML.xml", "UTF-8") # versao para o EvaSIM

#tree.write("_xml_links.xml", "UTF-8") # versao para a etapa 4 do parser
