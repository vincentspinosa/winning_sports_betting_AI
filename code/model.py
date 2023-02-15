import numpy as np
import statistics as stats
from datetime import datetime

def days_between(d1, d2):
  try:
    d1 = datetime.strptime(d1, "%d/%m/%y")
    d2 = datetime.strptime(d2, "%d/%m/%y")
    return abs((d2 - d1).days)
  except:
    return None

def rev_and_place(df, depart):
  df = df.reindex(index=df.index[::-1])
  df = df.iloc[depart:, 0:]
  return df

def date_valide(v1, v2, ecartMax):
  x = days_between(v1, v2)
  if x is not None:
    if x > ecartMax:
      return False
  return True

def set_ones(data, dtHeader, array, numbers, matchs):
  if data[dtHeader] == 1:
    for i in range(len(numbers)):
      if matchs < len(array[i]):
        array[i][matchs] = 1
  return array
  


#can only be used if pandas is already imported in the file calling the function

def obtenir_arrays(df, numbersArray, equipe, depart, HTheader, ATheader, PariHeader, DateHeader):
  df_rev = rev_and_place(df, depart)
  groups = np.empty(len(numbersArray), dtype=object)
  for i in range(len(numbersArray)):
    groups[i] = np.zeros([numbersArray[i]])
  matchs = 0
  for i, data in df_rev.iterrows():
    if data[HTheader] == equipe or data[ATheader] == equipe:
      if matchs == 0:
        dateMatch1 = data[DateHeader]
      if date_valide(dateMatch1, data[DateHeader], 600) == False:
        break
      groups = set_ones(data, PariHeader, groups, numbersArray, matchs)
      matchs += 1
      if (matchs > numbersArray[len(numbersArray) - 1]):
        break
  return groups


def obtenir_arrays_cote(df, numbersArray, equipe, depart, coteHeader, PariHeader, dateHeader):
  df_rev = rev_and_place(df, depart)
  groups = np.empty(len(numbersArray), dtype=object)
  for i in range(len(numbersArray)):
      groups[i] = np.zeros([numbersArray[i]])
  matchs = 0
  for i, data in df_rev.iterrows():
    if data[coteHeader] == equipe:
      if matchs == 0:
        dateMatch1 = data[dateHeader]
      if date_valide(dateMatch1, data[dateHeader], 600) == False:
        break
      groups = set_ones(data, PariHeader, groups, numbersArray, matchs)
      matchs += 1
      if (matchs > numbersArray[len(numbersArray) - 1]):
        break
  return groups


#obtenir la note à partir de l'array retourné par obtenir_arrays() ou obtenir_arrays_cote()
def obtenir_note(array):
  if array is not None:
    notes = []
    for i in array:
      notes.append(stats.mean(i))
    return stats.mean(notes)
  return None


#obtenir la note d'une équipe
def note_equipe(dtf, equipe, depart, coteHeader, HTheader, ATheader, PariHeader, DateHeader):
  array = obtenir_arrays(dtf, [7, 10, 15, 23, 41], equipe, depart, HTheader, ATheader, PariHeader, DateHeader)
  if array is not None:
    arrayCote = obtenir_arrays_cote(dtf, [5, 8, 13, 21], equipe, depart, coteHeader, PariHeader, DateHeader)
    if arrayCote is not None:
      try:
        note = obtenir_note(array)
        note = (note * (1 + obtenir_note(arrayCote))) / 2
        return note
      except:
        return None


#obtenir la note d'un match
def note_match(dtf, equipeA, equipeB, depart, HTheader, ATheader, PariHeader, DateHeader):
  noteA = note_equipe(dtf, equipeA, depart, HTheader, HTheader, ATheader, PariHeader, DateHeader)
  noteB = note_equipe(dtf, equipeB, depart, ATheader, HTheader, ATheader, PariHeader, DateHeader)
  if noteA is not None and noteB is not None:
    return (noteA + noteB) / 2
  return -1


#récupérer les notes pour chaque match du dataframe passé en paramètre
def get_notes(df, HTheader, ATheader, DateHeader, NoteHeader, PariHeader, moduloAffichage):
  for i, data in df.iterrows():
    note = note_match(df, data[HTheader], data[ATheader], df.shape[0] - 1 - i, HTheader, ATheader, PariHeader, DateHeader)
    df.at[i, NoteHeader] = note
    if i % moduloAffichage == 0:
      print(f"{i} - {note}")
  print("\n")
  return df