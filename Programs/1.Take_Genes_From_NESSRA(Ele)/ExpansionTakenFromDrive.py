import pandas as pd
import subprocess
import os

boinc = "genehome_PC-IM_15Nov.csv" #da cambiare in base al boinc che si usa
isoforme_mandate = "sentIsoforms.csv" #da cambiare in base alle isoforme




def GeniDaCercare(file_nostre_isoforme, boinc):
    """La funzione prende le nostre isoforme  e la matrice di boinc, printa un file con gene, isoforma e id, ritorna una lista di ID """

    matrice = pd.read_table(boinc, sep = ",", header = 0)
    mat = matrice[matrice["exp"] == "hgnc_cc_zf_mat.csv"]

    dizionario_boinc = {}
    # {id : [gene, isoforma]

    for el in range(len(mat)):
        lgn = mat.iloc[el][2]
        gene = lgn.split("-")[1]
        isoforma = lgn.split("-")[0]

        id = mat.iloc[el][0]

        if not id in dizionario_boinc:
            dizionario_boinc[id] = [gene, isoforma]

    dizionario_isoforme = {}
    # {isoforma : gene}

    with open(file_nostre_isoforme, "r") as fh:
        for line in fh:
            line = line.replace("\n", "")

            lista_info = line.split("\t")
            gene = lista_info[0]

            for isoforma in lista_info[1:]:
                if isoforma not in dizionario_isoforme:
                    dizionario_isoforme[isoforma] = gene

    Lista_id = []

    count = 0
    #Controllo i due dizionari
    with open("id_nostre_isoforme", "w") as fh:
        fh.write("Our ids:\n")
        for id in dizionario_boinc:
            isoforma = dizionario_boinc[id][1]
            if isoforma in dizionario_isoforme:
                count = count + 1
                gene = dizionario_isoforme[isoforma]
                Lista_id.append(id)

                fh.write("{}\t{}\t{}\n".format(id, isoforma,gene))

        fh.write("ids found on gene@home: {}".format(count))

    return (Lista_id)


Lista_id = GeniDaCercare(isoforme_mandate, boinc)
#print(len(Lista_id))
print("Number of isoforms to search: {}".format(len(Lista_id)))

count = 0
for expansion in Lista_id:
    count = count + 1
    bashcommand = "rclone copy --drive-shared-with-me remote:experiments_results/" + str(expansion) + "_Hs.expansion remote:"
    print(bashcommand)
    os.system(bashcommand)
    print("{}/{} Done 👍".format(count, len(Lista_id)))

print("Finish!!! See your results in yur Drive! 🎉🎉🎉")


#bashcommand = "rclone copy --drive-shared-with-me remote:experiments_results/146696_Hs.interactions remote:Blanzieri"

#os.system(bashcommand)


