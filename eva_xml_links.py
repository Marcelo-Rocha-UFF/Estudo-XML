from platform import node
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
        # Eu pensei que esse caso não funcionasse, mas ele funcionou tanto no robô quanto no EvaSIM
        # # CASO ESPECIAL: <switch> conectando a outro <switch>
        # # ISSO NÃO PODE OCORRER, pois os cases de um <switch> são conectados (tem como origem) a UM elemento.
        # # e um <switch> tem como saida mais de um elemento.
        # if node_to.tag == "switch":
        #     print('  Error -> Due to robot VPL limitations, using two consecutive <switch> commands is not allowed.')
        #     exit(1)
        # vamos percorrer os elementos case e default do switch
        for case_elem in node_from:
            qtd = len(case_elem)
            # só precisamos do ultimo elemento de cada bloco case/default
            if (qtd == 0): # case vazio, conecta o <case> ao node_to
                #lista_links.append(case_elem.attrib["key"] + "," + node_to.attrib["key"])
                cria_link(case_elem, node_to)
            else:
                # caso do <stop> e do <goto>. Nesses casos ocorre um bypass
                if (case_elem[qtd -1].tag == "stop") or (case_elem[qtd -1].tag == "goto"):
                    pass
                else: # caso seja outro comando, cria a conexao do comando com o node_to
                    cria_link(case_elem[qtd -1], node_to)
        return

    # node <goto> com node_to. O node_to, é substituido pelo nó indicado no atrib. "target" do <goto>
    if node_to.tag == "goto":
        target_found = False # indica se o id referenciado no target foi encontrado
        for elem in script_node.iter(): # procura por target na interação
            if elem.get("id") != None:
                if elem.attrib["id"] == node_to.attrib["target"]:
                    # cria um link entre o no que queria se conectar ao goto (node_from) e o no para o qual o goto aponta
                    # isso trás mais flexibilidade à conexão de nós que se conectam a elementos goto
                    # com isso, um switch passou a poder ter o atributo id
                    cria_link(node_from, elem)
                    # lista_links.append(node_from.attrib["key"] + "," + elem.attrib["key"])
                    target_found = True
        if not (target_found):
            # target id not found
            print('  Error -> The "target" attribute from <goto> was not found:', node_to.attrib["target"])
            exit(1) # termina com erro
        return

    # "node_to" e' uma folha, que nao contem filhos. ex.: <wait>, <light>, <case> vazio e etc
    if len(node_to) == 0:
        lista_links.append(node_from.attrib["key"] + "," + node_to.attrib["key"])
        
    # trata os nodes com filhos
    elif (node_to.tag == "switch"): # trata o node "switch"
        for case_elem in node_to:

            # todas os cases passam a ter o atrib. "var" igual ao "var" do switch (node_to)
            # verifica se ha o atrib. "var", senão emite o sinal de erro e pára.
            if node_to.get("var") != None:
                case_elem.attrib["var"] = node_to.attrib["var"] # existe "var" no switch, então transfere para o <case>
            else:
                print('  Error -> There is a <switch> without attribute "var", please fix it.')
                exit(1)

            if case_elem.tag == "default": # preenche o default com os parametros default
                case_elem.attrib["value"] = ""
                case_elem.attrib["op"] = "exact"

            # gera o link de node_from (que veio na chamada) com o elem. (case ou default)
            #lista_links.append(node_from.attrib["key"] + "," + case_elem.attrib["key"])
            cria_link(node_from, case_elem)
            
            if (len(case_elem) == 0): # case o <case> seja vazio
                # nao conecta o <case>
                pass
            else: # caso o case não seja vazio, gera o link entre o <case> e o primeiro elemento e depois processa o conteudo do <case>
                cria_link(case_elem, case_elem[0]) # conecta o <case> com o seu primeiro elemento filho
                link_process(case_elem) # processa a lista de elem. do <case>
    # processa os node_to do tipo <case>            
    elif (node_to.tag == "case") or (node_to.tag == "default"):
        lista_links.append(node_from.attrib["key"] + "," + node_to.attrib["key"])


def link_process(node_list):

    qtd = len(node_list)

    for i in range(0, qtd-1): # processa uma lista de nós (dois a dois) A->B, B->C,...,Y->Z
        node_from = node_list[i]
        node_to = node_list[i+1]

        # emite um aviso caso haja elemento(s) após um <goto>
        # se esse elemento não for referenciado em outra parte do script, ele poderá ficar desconectado do fluxo.
        if node_from.tag == "goto":
            print("  Warning - there are elements after the <goto>. These elements may not be reached." + node_list[i+1].tag + ">")

        # case especifico da tag <stop> que deve interromper a conexao dos do fluxo sendo processado
        # todos os elem. após um <stop> são removidos. O parser emite um aviso de remoção e os exibe no terminal.
        if (node_from.tag == "stop"):
            for s in range(i, qtd-1):
                print("  Warning - removing unused commands ... <" + node_list[i+1].tag + ">")
                node_list.remove(node_list[i+1])
            break
        else:
            cria_link(node_from, node_to)
        

def saida_links():
    # insere a tag links como ultimo elemento de root (<evaml>)
    # len(root) retorna o valor que sera o indice para o ultimo elemento
    tag_links = ET.Element("links") # cria a tag links (mae de varios links)
    root.insert(len(root), tag_links) #

    for i in range(len(lista_links)): # insere cada link como os atributos from e to, dentro do elemento <links>
        tag_link = ET.Element("link", attrib={"from" : lista_links[i].split(",")[0], "to" : lista_links[i].split(",")[1]})
        root[len(root) - 1].insert(i, tag_link)

# inserindo o elemento voice como primeiro elemento do script_node a ser processado
# neste caso, o elem. voice é inserido (temporriamente) para que ele seja sempre o primeiro elemento a ser processado
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
