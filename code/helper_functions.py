from model import note_match

#récupérer les équipes d'un championnat
#a besoin d'un point de départ, du nombre d'équipes à récupérer, du column header des équipes dom et ext
def get_equipes(df, depart, nbEquipes, HTheader, ATheader):
  array = []
  df_rev = df.reindex(index=df.index[::-1])
  df_rev = df_rev.iloc[depart:, 0:]
  for i, data in df_rev.iterrows():
    if data[HTheader] not in array:
      array.append(data[HTheader])
    if data[ATheader] not in array:
      array.append(data[ATheader])
    if len(array) == nbEquipes:
      return array

#afficher et récupérer la note d'un match
def afficher_note_match(df, equipeA, equipeB, depart, HTheader, ATheader, PariHeader, DateHeader):
  note = note_match(df, equipeA, equipeB, depart, HTheader, ATheader, PariHeader, DateHeader)
  print(f"Match : {equipeA} - {equipeB}")
  print(f"Note : {note}\n")
  return [equipeA, equipeB, note]

def add_match(df, date, equipeA, equipeB):
  df.loc[len(df.index)] = [date, equipeA, equipeB, 0, 0, 0]


#impriner un array d'équipes
def print_array_equipes(array):
  for i in range(len(array)):
    print(f"{i} - {array[i]}")

#imprimer un array de notes de matchs
""" def print_array_notes(array):
  for i in range(len(array)):
    print(f"{i} - {array[i][0]} - {array[i][1]}")
  print("\n") """

#calculer la somme d'un pari
def calcul_somme(bankroll, pourcentage):
  return bankroll * pourcentage

#faire des projections de la bankroll selon un multiplicateur
#a besoin de :
  #une bankroll de départ
  #un nombre de matchs
  #du nombre de matchs par étapes du multiplicateur
  #du multiplicateur
def projections(bk, matchs, etapes, mul):
  array = []
  j = 0
  for i in range(matchs):
    if i % etapes == 0 and i > 0:
      bk *= mul
      j += 1
      array.append([i, j, bk])
      print(f"Étape {j}, Match {i}\nBankroll : {int(bk)}")
  return array

#calculer la cote nécessaire pour être au seuil de rentabilité
def break_even(pourcDepart, pourcFin, increment):
  array = []
  for i in range(pourcDepart, pourcFin, increment):
    print(f"Pourcentage de victoires : {i}")
    print(f"Cote nécessaire : {100 / i}")
    print("\n")
    array.append([i, 100 / i])
  return array