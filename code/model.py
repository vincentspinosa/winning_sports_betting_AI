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

def set_plus(data, HASheader, array, numbers, matchs):
  if data[HASheader] == 1:
    for i in range(len(numbers)):
      if matchs < len(array[i]):
          array[i][matchs] = 1
  return array

def set_minus(data, HASheader, array, numbers, matchs):
  if data[HASheader] == 0:
    for i in range(len(numbers)):
      if matchs < len(array[i]):
        array[i][matchs] = data['Note']
  return array


#can only be used if pandas is already imported in the file calling the function

def layer(df, vector, equipe, depart, Headers, PariHeader, dateHeader, function):
  df_rev = rev_and_place(df, depart)
  array = np.empty(len(vector), dtype=object)
  for i in range(len(vector)):
    array[i] = np.zeros([vector[i]])
  matchs = 0
  for i, data in df_rev.iterrows():
    equipeIn = False
    for hd in Headers:
      if data[hd] == equipe:
        equipeIn = True
    if equipeIn == True:
      if matchs == 0:
        dateMatch1 = data[dateHeader]
        matchs += 1
        continue
      if date_valide(dateMatch1, data[dateHeader], 365) == False:
        break
      array = function(data, PariHeader, array, vector, matchs)
      matchs += 1
      if (matchs > vector[len(vector) - 1]):
        break
  return array


#obtenir la note à partir de l'array retourné par layer()
def obtenir_note(array):
  if array is not None:
    notes = []
    for i in array:
      notes.append(stats.mean(i))
    return stats.mean(notes)
  return None


#obtenir la note d'une équipe
def note_equipe(df, equipe, depart, Headers, PariHeader, DateHeader, function):
  
  vector = [1, 2, 3, 5]
  array = layer(df, vector, equipe, depart, Headers, PariHeader, DateHeader, function)
  try:
    return obtenir_note(array)
  except:
    return 0


#obtenir la note d'un match
def note_match(df, equipeA, equipeB, depart, HTheader, ATheader, PariHeader, DateHeader, function):
  #noteEqAFull = note_equipe(df, equipeA, depart, [HTheader, ATheader], PariHeader, DateHeader, function)
  #noteEqBFull = note_equipe(df, equipeB, depart, [HTheader, ATheader], PariHeader, DateHeader, function)
  noteEqA = note_equipe(df, equipeA, depart, [HTheader], PariHeader, DateHeader, function)
  noteEqB = note_equipe(df, equipeB, depart, [ATheader], PariHeader, DateHeader, function)
  try:
    return (noteEqA + noteEqB) / 2
    #return (noteEqAFull + noteEqBFull + noteEqA + noteEqB) / 4
  except:
    return 0


#récupérer les notes pour chaque match du dataframe passé en paramètre
def get_notes(df, HTheader, ATheader, DateHeader, NoteHeader, PariHeader, moduloAffichage):
  for i, data in df.iterrows():
    note = note_match(df, data[HTheader], data[ATheader], df.shape[0] - 1 - i, HTheader, ATheader, PariHeader, DateHeader, set_plus)
    df.at[i, NoteHeader] = note
    #note -= note_match(df, data[HTheader], data[ATheader], df.shape[0] - 1 - i, HTheader, ATheader, PariHeader, DateHeader, set_minus)
    #df.at[i, NoteHeader] = note
    if i % moduloAffichage == 0:
      print(f"{i} - {note}")
  print("\n")
  return df