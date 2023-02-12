from datetime import datetime

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
      array.append(i, j, bk)
      print(f"Étape {j}, Match {i}\nBankroll : {int(bk)}")
  return array

#calculer le nombre de jours d'écart entre deux dates
def days_between(d1, d2):
  try:
    d1 = datetime.strptime(d1, "%d/%m/%y")
    d2 = datetime.strptime(d2, "%d/%m/%y")
    return abs((d2 - d1).days)
  except:
    return None

#imprimer un array de notes de matchs
def print_array_notes(array):
  for i in range(len(array)):
    print(f"{i} - {array[i][0]} - {array[i][1]}")
  print("\n")

#impriner un array d'équipes
def print_array_equipes(array):
  for i in range(len(array)):
    print(f"{i} - {array[i]}")

#calculer la cote nécessaire pour être au seuil de rentabilité
def break_even(pourcDepart, pourcFin, increment):
  array = []
  i = pourcDepart
  while i < pourcFin:
    print(f"Pourcentage de victoires : {i}")
    print(f"Cote nécessaire : {100 / i}")
    print("\n")
    array.append([i, 100 / i])
    i += increment
  return array