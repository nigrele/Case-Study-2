"""Take the files from Expension Results folder
Create a Dictionary with the isoforms count : {isoform: counts} that contains the count for every file in experiment results

Output:
a file containing ranked(by score) isoforms translated in genes"""




import os
import pandas as pd
import argparse


parser = argparse.ArgumentParser(description = "Prende la cartella con all'interno le espansioni, somma i gli score delle isoforme presenti. Ritorna un file contenente tutte le isoforme ordinate per importanza")

parser.add_argument("-i", "--input" , help = "inserire la cartella con le espansioni")
parser.add_argument("-o", "--output", help = "inserire il nome dell'output contenente le isoforme")

args = parser.parse_args()

folder_Experiment_Results = args.input
output = args.output

# Dizionario con score
D = {}
num_file = 0

for file in os.listdir(folder_Experiment_Results):
    if file[0] in "1234567890":
        num_file = num_file + 1
        #print(file)
        with open("{}/{}".format(folder_Experiment_Results, file), "r") as fh:
            for line in fh:
                if line[0] in "123456789":
                    relation_line = line.split(",")
                    isoform = relation_line[1].replace("t", "T")
                    rank = int(relation_line[0])
                    score = float(relation_line[3])

                    if isoform not in D:
                         D[isoform] = [score]
                    else :
                         D[isoform].append(score)

D_sum = {}
for key in D:
    sum_score = sum(D[key])
    D_sum[key] = sum_score	



#print("Dizionario score:\n{}".format(D["T147981"]))

#print("Dizioanrio medie:\n{}".format(D_sum["T147981"]))


ranked = pd.Series([key for key in D_sum], index = [D_sum[x] for x in D_sum])

ranked = ranked.sort_index(ascending = False)
ranked.to_csv("{}.txt".format(output), sep = "\t")
#
# print("Ho finito!😎")
# print("Le isoforme nella lista sono: {}".format(len(ranked)))
# print("Trovi i risultati nel file {}".format(output))
# print("🦎🦎🦎🦎🦎🦎🦎🦎🦎🦎🦎🦎🦎🦎🦎🦎🦎")
