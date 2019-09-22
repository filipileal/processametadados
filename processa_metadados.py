import publicacoes_com_metadados as publicacao
import funcoes as func

total_publicacoes = 0

for entrada in publicacao.publicacoes:
    total_publicacoes += 1
    #importando conteudo.
    conteudo = entrada.conteudo
    #importando metadados.
    metadados = entrada.metadados.keys()
    #processando conteudo dos metadados
    result = func.procura_metadado(metadados, conteudo)
    print("Publicação", total_publicacoes)
    for keys, values in result.items():
        print(keys,": [")
        for x in values:
            print("    ", x)
        print("]")
    print()