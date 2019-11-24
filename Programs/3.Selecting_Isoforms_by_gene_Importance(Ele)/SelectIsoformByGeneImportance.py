import pandas as pd
import os
import shutil
import argparse

parser = argparse.ArgumentParser(description = "Genis_importantibus prende un file di geni rankati (es lista di open target) e ritorna una cartella con i risultati delle espanioni di NESSRA tenendo conto del rank della lista."
                                               "PER FUNZIONARE NECESSITA DI AVERE ALL'INTERNO DELLA CARTELLA DOVE VIENE AVVIATO IL FILE DI ANNOTAZIONE :"
                                               "hgnc_cc_zero_filtered_anno.csv")



parser.add_argument("-b", "--BOINC_file" , help = "The update file from boinc")
parser.add_argument("-max","--Maximum", type = int, help = "The maximum genes to take for the most importance gene")
parser.add_argument("-s","--Step", type = int,  help = "The difference of genes to take between 2 different ranked genes")
parser.add_argument("-min", "--Minimum", type = int, help = "The minimum value of genes to take in case of emergency")
parser.add_argument("-open", "--OpenTarget_Genes", help = "A list of genes ranked by importance")
parser.add_argument("-i", "--Expansion_folder", help = "The folder that contains the expasnions")

args = parser.parse_args()

OpenTarget = args.OpenTarget_Genes
maximum = args.Maximum
minimum = args.Minimum
step = args.Step
Boinc_History = args.BOINC_file
Folder_expansion = args.Expansion_folder

# Creazione di un dizionario con chiave: isoforma, valore gene
phantom_anno = "hgnc_cc_zero_filtered_anno.csv" #fissa

phantom_anno_DF = pd.read_csv(phantom_anno, sep ="\t", header = 0, error_bad_lines =  False)
df = {"ID": phantom_anno_DF["Unnamed: 0"], "Gene": phantom_anno_DF["short_description"]}
annotation = pd.DataFrame(df)

D = {} #Dizionario {isoforma: gene}  x tutti i geni nella filtered
for el in range(len(annotation)):
    gene = annotation.iloc[el][1]
    id = annotation.iloc[el][0]

    gene = gene.split("@")
    gene = gene[1]

    if not id in D:
        D[id] = gene





# Creazione dizionario assocatio agli id di BOINC
#Boinc_History = "Boinc_History.csv" #variabile da inserire ogni volta aggionrata


D_id = {} #{isoforma : [gene, id]}
boinc = pd.read_csv(Boinc_History, sep = ",", header = 0)

for el in range(6,len(boinc)):
    matrice = boinc.iloc[el][3]
    if matrice == "hgnc_cc_zf_mat.csv":
        id = boinc.iloc[el][0]
        lgn = boinc.iloc[el][2].split("-")
        isoform = lgn[0]
        gene = lgn[1]

        for el in D:
            if isoform == el and gene == D[el]:
                if not isoform in D_id:
                    D_id[isoform] = [gene, id]




# Creazione dizionario con chiave nome gene e valore id da cercare nella cartella Expansion
boinctionary = {} #{gene : [id,id, id..]

for key in D_id:
    isoform = key
    id = D_id[key][1]
    gene = D_id[key][0]

    if not gene in boinctionary:
        boinctionary[gene] = [id]

    else:
        boinctionary[gene].append(id)



# Lista dei file nella cartella con le espansioni
#Folder_expansion = "Expansion" #variabile con nome della cartella con i risultati

expansion_in_folder = []
for file in os.listdir(Folder_expansion):
    if file[0] in "1234567890": # mini controllo
        expansion_in_folder.append(file)



# Cerco i file nella cartella expansion, confronto con open target e taglio dei geni
#maximum = 500 #parametro da inserire a piacere
#minimum = 5 #parametro da inserire a piacere
#step = 5 #parametro da inserire a piacere




#OpenTarget = "Prova_PAX.csv" # da inserire con il rank dei geni di open target


Open_Target = pd.read_csv(OpenTarget, sep = ",", header = 0, index_col= None)

Result = "Result_with_max:{}_min:{}_step:{}".format(maximum, minimum, step)
shutil.rmtree(Result, ignore_errors= True)
os.makedirs(Result, exist_ok = False)
count = 0

i = 0
while i in range(len(Open_Target)):
    rank = Open_Target.iloc[i][0]
    gene = Open_Target.iloc[i][1]

    i = i + 1

    id_tosearch = []
    if gene in boinctionary:
        for el in boinctionary[gene]:
            id_tosearch.append(str(el))


    for exp in expansion_in_folder:
        expansion_id = exp.split("_")[0]
        if expansion_id in id_tosearch:
            count = count + 1
            expansion = pd.read_table("{}/{}".format(Folder_expansion, exp), sep=",", header=1, index_col = 0)

            Line = pd.read_table("{}/{}".format(Folder_expansion, exp), sep=",", header=0)
            StringaLine = (str(Line.iloc[0]).split(" "))
            Gene_Isoform = StringaLine[3]
            Isoform_name = Gene_Isoform.split("-")[0]
            title = Gene_Isoform.split("-")[1] + "-" + Gene_Isoform.split("-")[0]

            with open("{}/{}".format(Result, title), "w") as fh:
                fh.write("{}\nresult from expansion with number of genes  {}\n".format(Gene_Isoform, maximum))
                fh.write("{} rank in Open_Target:{}\n".format(title, i))
                fh.write("rank\tgene\tisoform\n")

                SelectionGenes = expansion.iloc[0:maximum]

                for j in range(len(SelectionGenes)):
                    gene_related = SelectionGenes.iloc[j][0].replace("t", "T")

                    if gene_related in D:
                        fh.write("{}\t{}\t{}\n".format(j, D[gene_related], gene_related))

    maximum = maximum - (step * i)

    if maximum < 0:
        maximum = minimum


print("FINISH WITH NO ERRORS!😎")
print("You find your results in the folder {}".format(Result))
print("There are {} file inside".format(count))

