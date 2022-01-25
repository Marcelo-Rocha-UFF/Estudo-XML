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

    # um switch, uma macro, um goto ou um stop nunca podem ser node_from
    if node_from.tag == "switch": return
    # if node_from.tag == "macro": return
    if node_from.tag == "stop": return
    if node_from.tag == "goto": return

    # node goto com node_to
    if node_to.tag == "goto":
        for elem in script_node.iter(): # procura por target na interação
            if elem.get("id") != None:
                if elem.attrib["id"] == node_to.attrib["target"]:
                    lista_links.append(node_from.attrib["key"] + "," + elem.attrib["key"])
        return

    # "node_to" e' uma folha, que nao contem filhos
    if len(node_to) == 0:
        lista_links.append(node_from.attrib["key"] + "," + node_to.attrib["key"])
        
    # trata os nodes com filhos
    elif (node_to.tag == "switch"): # trata o node "switch"
        for switch_elem in node_to:
            # todas os cases passam a ter o atrib. "var" igual ao "var" do switch
            switch_elem.attrib["var"] = node_to.attrib["var"] 
            if switch_elem.tag == "default": # preenche o default com os parametros default
                switch_elem.attrib["value"] = ""
                switch_elem.attrib["op"] = "exact"
            lista_links.append(node_from.attrib["key"] + "," + switch_elem.attrib["key"])
            link_process(switch_elem, switch_elem)
    elif (node_to.tag == "case"): # trata o node "case"
        lista_links.append(node_from.attrib["key"] + "," + node_to.attrib["key"])
        link_process(node_to, node_to)
    ### foi retirado pois nesta etapa, não existem mais macros
    #elif (node_to.tag == "macro"): # trata de node "macro" 
    #    link_process(node_from, node_to)


def link_process(node_from, node_list):
    # o caso inicial é o que node_from é o elemento voice que é passado na primeira chamada de link_process()
    # neste caso, o elem. voice é inserido (temporriamente) em node_list para que ele seja sempre o primeiro elemento a ser processado.
    # if node_from.tag == "voice": 
    #     node_list.insert(0, node_from)
        
    qtd = len(node_list)

    if qtd != 0: # a ideia é tratar os casos dos blocos vazios, como o dos <cases>
        node_to = node_list[0] # blocos vazios não tem o elemento[0]
        cria_link(node_from, node_to) # se um bloco tem elemento, então tudo ok


    for i in range(0, qtd-1):
        node_from = node_list[i]
        node_to = node_list[i+1]
        ########################################
        if node_to.tag == "switch":
            if (i+1 != qtd-1): # verifica se existe algum node, dentro do fluxo corrente, depois do switch
                for p in range(0, len(node_to)): # empilhando no' depois do switch
                    # a qtd de empilhamentos e' igual ao numero de cases dentro do switch
                    pilha.append(node_list[i+2])
            else: # quando não ha no' depois do switch
                if len(pilha) != 0: # um switch com uma pilha nao vazia e' um switch interno a outro switch
                    no_aux = pilha.pop() # pega o no mais exterior da pilha fica com -1)
                    for p in range(0, len(node_to)+1): # nao entendi o porque do + 1.
                        pilha.append(no_aux) 
                    #print("num de elem. empilhados:", len(node_to))
                    #print("pilha: ", spilha)               # o ou os cases deverao se conectar a no mais externo

        ########################################
        cria_link(node_from, node_to)

    if (len(pilha) != 0): # esse cara cria os links nos finais dos fluxos dos cases, ou do fluxo principal
        if qtd == 0:
            cria_link(node_from, pilha.pop())
        else:
            cria_link(node_to, pilha.pop())
        

def saida_links():
    # insere a tag links como ultimo elemento de root (<evaml>)
    # len(root) retorna o valor que sera o indice para o ultimo elemento
    tag_links = ET.Element("links") # cria a tag links (mae de varios links)
    root.insert(len(root), tag_links) #

    for i in range(len(lista_links)): # insere cada link como os atributos from e to, dentro do elemento <links>
        tag_link = ET.Element("link", attrib={"from" : lista_links[i].split(",")[0], "to" : lista_links[i].split(",")[1]})
        root[len(root) - 1].insert(i, tag_link)


# gera os links na lista de links auxiliar
link_process(root.find("settings").find("voice"), script_node)

# gera os links no arquivo xml
saida_links()

print("step 03 - Creating the Elements <link>...")

# O elemento voice foi inserido ao script_node (list) para processamento, somente. 
# Agora será removido da seção script
# script_node.remove(root.find("script").find("voice"))

# arquivo de saida
tree.write(root.attrib['name'] + "_EvaML.xml", "UTF-8") # versao para o EvaSIM

#tree.write("_xml_links.xml", "UTF-8") # versao para a etapa 4 do parser
