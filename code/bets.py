from model import obtenir_arrays, obtenir_note, obtenir_arrays_cote, note_match

#récupérer les équipes d'un championnat
#a besoin d'un point de départ, du nombre d'équipes à récupérer, du column header des équipes dom et ext
def get_equipes(df, depart, nbEquipes, HTheader, ATheader):
  array = []
  df_rev = df.reindex(index=df.index[::-1])
  df_rev = df_rev.iloc[depart:, 0:]
  for i, data in df_rev.iterrows():
    if data[HTheader] not in array:
      #print(data[HTheader])
      array.append(data[HTheader])
    if data[ATheader] not in array:
      #print(data[ATheader])
      array.append(data[ATheader])
    if len(array) == nbEquipes:
      return array

#récupérer les équipes d'un championnat et leurs notes
""" def notes_equipes_futur(df, array, HTheader, ATheader, DateHeader, coteHeader):
  arrayNotes = []
  for i in range(len(array)):
    note = [array[i], obtenir_note(obtenir_arrays(df, array[i], 0, HTheader, ATheader, DateHeader))]
    note[1] *= obtenir_note(obtenir_arrays_cote(df, array[i], ))
    arrayNotes.append(note)
  return arrayNotes """

#afficher et récupérer la note d'un match
def afficher_note_match(dtf, equipeA, equipeB, depart, HTheader, ATheader, DateHeader):
  note = note_match(dtf, equipeA, equipeB, depart, HTheader, ATheader, DateHeader)
  print(f"Match : {equipeA} - {equipeB}")
  print(f"Note : {note}\n")
  return [equipeA, equipeB, note]

#calculer la somme d'un pari
def calcul_somme(bankroll, pourcentage):
  return bankroll * pourcentage