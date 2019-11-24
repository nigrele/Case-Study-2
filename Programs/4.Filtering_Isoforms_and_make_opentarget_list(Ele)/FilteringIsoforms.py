"""Il programma prende i file generati con GenisRankibus (o score) e i file ottenuti precedentemente con il rank e tira fuori una lista contenente le info di importanza e le traduce in geni"""


import pandas as pd
import os
import argparse

parser = argparse.ArgumentParser(description = "Prende la cartella dei risultati con le isoforme ordinate in base all'importanza."
                                               "prende il risultato calcolato in base al rank (o in base allo score)."
                                               "Ritorna una lista di geni da mettere in OpenTarge"
                                               ""
                                               "Si deve specificare se la lista in input è di score o di rank"
                                 )


parser.add_argument("-folder", "--folder", help = "La cartella con i file risultanti dopo aver preso le isofomre considerate più importanti")
parser.add_argument("-i", "--genes", help = "file con liste di isoforme rankate o per rank o per score")
parser.add_argument("-o", "--output", help = "Nome del file di output per la lista da mettere in opentarget")
#parser.add_argument("-n", "--number", default = 150, help = "Quanto deve essere lunga la lista, di default è 150 (liste che possono essere caricate su opentarget)")
parser.add_argument("-method", "--method", help = "bisogna dire se la lista in input è basata sul rank o sullo score: scrivere rank o score" )

args = parser.parse_args()

Folder = args.folder
isoform_ranked = args.genes
lista = args.output
#n_isoform = int(args.number)
method = args.method



# Dizionario dai file nella cartella
#Folder = "Prova" #da Argparsare
Genes_inda_folder = {}

for file in os.listdir(Folder):

    fh = pd.read_csv("{}/{}".format(Folder, file), sep = "\t", header = 3)

    for i in range(len(fh)):
        gene = fh.iloc[i]["gene"]
        isoform = fh.iloc[i]["isoform"]

        if not isoform in Genes_inda_folder:
            Genes_inda_folder[isoform] = gene





# Troviamo i geni nei nostri file nel file rankato

#ranktionary : Dizionario contenente {isofomra : rank}

#isoform_ranked = "Prova_Ranked" # Da Arg_parsare
isoform_ranked_series = pd.read_csv(isoform_ranked, sep = "\t", header = None  )


ranktionary = {}

for i in range(len(isoform_ranked_series)):
    rank = isoform_ranked_series.iloc[i][0]
    isoform = isoform_ranked_series.iloc[i][1]

    ranktionary[isoform] = rank


# ranked_result = {isoforma : [rank, gene ]
ranked_result = {}

for i in Genes_inda_folder:
    if i in ranktionary:
            ranked_result[i] =  [ranktionary[i], Genes_inda_folder[i]]

print(len(ranked_result))

# Scriviamo su output
#lista = "lista_prova" #lista dei geni da Arparsare per il nome
#n_isoform = len(ranked_result) #anche qui scegliere quanto


ranked = []
gened = []
isoformed = []
count = 0

for key in ranked_result:

    count = count + 1
    
    rank = ranked_result[key][0]
    gene = ranked_result[key][1]
    isoform = key

    ranked.append(rank)
    gened.append(gene)
    isoformed.append(isoform)

result = pd.DataFrame({"rank ": ranked , "gene": gened, "isoform": isoformed})
#print(result.head())

if method == "score":
    result = result.sort_values(by = "rank " , ascending = False)
    to_write = result

    to_write["gene"].to_csv("{}.txt".format(lista), index = None)

else:
    result = result.sort_values(by = "rank " , ascending = True)
    to_write = result
    to_write["gene"].to_csv("{}.txt".format(lista), index = None)




print("FINITO!!!🤩")
print("Puoi trovare i geni da mettere in open_target nel file {}.txt".format(lista))



