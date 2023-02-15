import matplotlib.pyplot as plt

#Fonctions exécutables seulement si pandas est déjà importé par le fichier appelant les fonctions

#Récupérer la data des sous-resultats
#arrayPrecis : array de sous-résultats
#arrayDatesPourc : array avec date du dernier match et % réussite
#dataSousResultats : array pour stocker l'ensemble 
def data_sous_resultat(dt, dateHeader, arrayPrecis, arrayDatesPourc, dataSousResultats):
  print(arrayPrecis)
  l = 0
  m = 0
  for i in arrayPrecis:
    if i == 1:
      l += 1
    m += 1
  sousPourc = int((l / m) * 10000) / 100
  arrayDatesPourc.append([dt[dateHeader], sousPourc])
  dataSousResultats.append(arrayPrecis)
  try:
    print(f"Sous-résultat : {l}/{m}, {sousPourc}% de réussite")
  except:
    pass



def creer_array_paris(df, note):
  arrayParis = []
  for i, data in df.iterrows():
    nb = data['Note_Match_Beta'] * 100
    if (nb >= note):
      arrayParis.append(df.iloc[i])
  return arrayParis

#pour une note :
#récupérer les % de réussites, total de la bankroll, matchs réussis / matchs perdus pour une équipe
#récupérer les sous-arrays de résultats
#a besoin d'une dataframe, d'une note, d'un pourcentage de la bankroll parié et d'une côte moyenne
#a besoin de la longeur maximale des arrays de sous-resultats
#la note en param est passée multipliée par 100 (ex : on reçoit 62 pour 0.62)
def data_note(df, dateHeader, maxLenArrayPrecis, note, pourcentage, cote):
  n = note / 100
  print(f"Note : {n}")
  print(f"{pourcentage}% à chaque pari")
  arrayParis = creer_array_paris(df, note)
  x = 0
  y = 0
  bankroll = 100
  arrayPrecis = []
  arrayDatesPourc = []
  dataSousResultats = []
  #on parcoure les résultats
  for dt in arrayParis:
    pari = (bankroll / 100) * pourcentage
    bankroll -= pari
    #si le pari est réussi, on multiplie le % de la BK parié par la côte moyenne
    if dt['HA_Scored'] == 1:
      x += 1
      bankroll += pari * cote
    arrayPrecis.append(dt['HA_Scored'])
    if len(arrayPrecis) == maxLenArrayPrecis:
      data_sous_resultat(dt, dateHeader, arrayPrecis, arrayDatesPourc, dataSousResultats)
      arrayPrecis = []
    y += 1
    dateDernierMatch = dt[dateHeader]
  if len(arrayPrecis) > 0:
      data_sous_resultat(dt, dateHeader, arrayPrecis, arrayDatesPourc, dataSousResultats)
      arrayPrecis = []
  #si il y a au moins 1 pari réussi, on renvoie les résultats
  if x > 0:
    bankroll = int(bankroll)
    pourcReussite = int((x / y) * 10000) / 100
    array = [n, x, y, bankroll, pourcReussite]
    print(f"Résultat : {x}/{y}")
    print(f"Bankroll : {bankroll}")
    print(f"Pourcentage réussite : {pourcReussite}")
    print(f"Dernier match : {dateDernierMatch}")
    print("\n")
    return [array, arrayDatesPourc, dataSousResultats]

#effectuer la fonction data_note() sur un ensemble de notes
#noteDepart : la note de match de départ à récupérer
#noteFin : la note qui déclenchera l'arrêt de la boucle
#increment : l'increment à ajouter dans les notes
#pourcentageBKdepart : pour chaque note, le % de la BK parié de départ
#pourcentageBKfin : pour chaque note, le % de la BK qui déclenchera l'arrêt de la boucle
#incrementPourc : l'incrément à utiliser pour les % de la BK à parier
def get_data(df, dateHeader, maxLenArrayPrecis, noteDepart, noteFin, cote, increment, pourcentageBKdepart, pourcentageBKfin, incrementPourc):
  arrayResultats = []
  x = noteDepart
  while x < noteFin:
    i = pourcentageBKdepart
    while i < pourcentageBKfin:
      array = data_note(df, dateHeader, maxLenArrayPrecis, x, i, cote)
      arrayResultats.append(array)
      i += incrementPourc
    x += increment
  return arrayResultats


#get 2D plots for a strategy result
#data : array of results from get_data()
def get_plots(data, lenMatchGroups):
  for i in data:
    array = []
    try:
      for j in range(len(i[1]) - 1):
        array.append(i[1][j][1])
    except:
      pass
    print(f"Note : {i[0][0]}")
    plt.plot(array)
    plt.ylabel(f"% réussite")
    plt.xlabel(f"Groupes de {lenMatchGroups} paris")
    plt.show()