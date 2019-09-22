import numpy as np

#funçao para limpar cada linha de retorno
def limpa_linha(linha):
    return linha.replace(";","").replace("Dr(a).", "").strip(" ")


#Processa dados "ADV(s)"
def procura_adv(texto):
    retorno_array = []
    metadados = ["Advs", "Adv -"]
    for  met in metadados:
        if texto.find(met) > 0:
            entrada = texto[texto.find(met)+len(met)+1:].replace("\n", "")
            while "  " in entrada:
                entrada = entrada.replace("  ", " ")
            if entrada.find(" - ") > -1:
                retorno_array = entrada.split(" - ")
            else:
                retorno_array = entrada.split(",")
    if retorno_array == []:
        metadado = "adv(s)."
        retorno_array_local = []
        texto = texto.replace("\n", "")
        #ADV(s) do autor
        if texto.lower().find(metadado) > 0:
            substr1 = (texto[texto.lower().find(metadado):])
            if substr1:
                pos = texto.find(substr1)
                entrada = texto[pos+len(metadado):].split(" X ")[0]
                while "  " in entrada:
                    entrada = entrada.replace("  ", " ")
                retorno_array_local = entrada.split(",")
        #ADV(s) do Réu
        textoreu = texto[texto.find(" X "):]
        if textoreu.lower().find(metadado) > 0:
            substr1 = (textoreu[textoreu.lower().find(metadado,1):])
            if substr1:
                pos = textoreu.find(substr1)
                entrada = textoreu[pos+len(metadado):].split("Despacho:")[0]
                while "  " in entrada:
                    entrada = entrada.replace("  ", " ")
                for adv in entrada.split(","):
                    retorno_array_local.append(adv)                
        retorno_array = retorno_array_local
    for x in range(len(retorno_array)):
        retorno_array[x] = limpa_linha(retorno_array[x])
    return np.unique(retorno_array)

#Processa dados dos metadados que não tem função específica.
def procura_geral(metadado, texto):
    entradalist = texto.split('\n')
    retorno_array = []
    for linha in entradalist:
        substr1 = (linha[linha.lower().find(metadado.lower()):linha.find(":")+1])
        if substr1:
            pos = linha.find(substr1)+len(substr1)
            for x in linha[pos:].split(","):
                retorno_array.append(x.strip())       
    for x in range(len(retorno_array)):
        retorno_array[x] = limpa_linha(retorno_array[x])
    return np.unique(retorno_array)

#Processa dados dos metadados "Agravada", "Agravado" e " Agravante"
def procura_agr(metadado, texto):
    retorno_array = []
    if texto.lower().find(metadado.lower()) > 0:
        entrada = texto[texto.lower().find(metadado.lower())+len(metadado)+1:].replace("\n", "")
        while "  " in entrada:
            entrada = entrada.replace("  ", " ")
        if entrada.find("Advogado") > 0:
            retorno_temp = entrada.split("Advogado")[0]
        else:
            retorno_temp = entrada.split(" - ")[0]
        retorno_array = retorno_temp.split(",") 
    else:
        return []
    for x in range(len(retorno_array)):
        retorno_array[x] = limpa_linha(retorno_array[x])
    return np.unique(retorno_array)

#Processa dados dos metadado "Autor"
def procura_autor(texto):
    retorno_array = procura_geral("AUTOR", texto)
    if retorno_array.size == 0:
        retorno_array_local = []
        texto = texto.replace("\n", "")
        if texto.lower().find("proc.") > 0:
            substr1 = (texto[texto.lower().find("proc."):texto.lower().find(" - ")+3])
            if substr1:
                pos = texto.find(substr1)+len(substr1)
                entrada = texto[pos:].split("(Adv(s)")[0]
                while "  " in entrada:
                    entrada = entrada.replace("  ", " ")
                retorno_array_local.append(entrada)
                retorno_array = retorno_array_local
    for x in range(len(retorno_array)):
        retorno_array[x] = limpa_linha(retorno_array[x])
    return np.unique(retorno_array)

#Processa dados do metadado "reu"
def procura_reu(texto):
    retorno_array = procura_geral("REU", texto)
    if retorno_array.size == 0:
        retorno_array_local = []
        texto = texto.replace("\n", "")
        if texto.lower().find("proc.") > 0:
            substr1 = (texto[texto.lower().find("proc."):texto.lower().find(" x ")+3])
            if substr1:
                pos = texto.find(substr1)+len(substr1)
                entrada = texto[pos:].split("(Adv(s)")[0]
                while "  " in entrada:
                    entrada = entrada.replace("  ", " ")
                retorno_array_local.append(entrada)
                retorno_array = retorno_array_local
    for x in range(len(retorno_array)-1):
        retorno_array[x] = limpa_linha(retorno_array[x])
    return np.unique(retorno_array)

#Processa metadados
def procura_metadado(metadado, texto):
    retorno = {}
    for met in metadado:
        if met == "ADV":
            procura = procura_adv(texto)
            if len(procura) > 0: 
                retorno["ADV"] = procura 
        elif met == "AUTOR":
            procura = procura_autor(texto)
            if len(procura) > 0:
                retorno["AUTOR"] = procura
        elif met == "AGRAVANTE":
            procura = procura_agr(met, texto)
            if len(procura) > 0:
                retorno["AGRAVANTE"] = procura
        elif met == "AGRAVADA":
            procura = procura_agr(met, texto)
            if len(procura) > 0:
                retorno["AGRAVADA"] = procura
        elif met == "REU":
            procura = procura_reu(texto)
            if len(procura) > 0:
                retorno["REU"] = procura
        elif met == "AGRAVADO":
            procura = procura_agr(met, texto)
            if len(procura) > 0:
                retorno["AGRAVADO"] = procura
        else:
            procura = procura_geral(met, texto)
            if len(procura) > 0: 
                retorno[met] = procura
    return retorno 