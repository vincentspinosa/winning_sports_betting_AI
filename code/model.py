import statistics as stats
from helper_functions import days_between

#can only be used if pandas is already imported in the file calling the function

def obtenir_arrays(df, equipe, depart, HTheader, ATheader, DateHeader):
  df_rev = df.reindex(index=df.index[::-1])
  df_rev = df_rev.iloc[depart:, 0:]
  numbers = [7, 10, 15, 23, 41]
  groups = [[], [], [], [], []]
  matchs = 0
  for i, data in df_rev.iterrows():
    if (data[HTheader] == equipe or data[ATheader] == equipe):
      if (matchs == 0):
        dateMatch1 = data[DateHeader]
      x = days_between(dateMatch1, data[DateHeader])
      if x is not None:
        if x > 600:
          for i in range(5):
            while (len(groups[i]) < numbers[i]):
              groups[i].append(0)
          return groups
      for i in range(5):
        if (len(groups[i]) < numbers[i]):
          if (data['A&H Scored?'] is None):
            groups[i].append(0)
          else:
            groups[i].append(data['A&H Scored?'])
      matchs += 1
      if (matchs > numbers[len(numbers) - 1]):
        return groups
  for i in range(5):
    while (len(groups[i]) < numbers[i]):
      groups[i].append(0)
  return groups


def obtenir_arrays_cote(df, equipe, depart, coteHeader, dateHeader):
  df_rev = df.reindex(index=df.index[::-1])
  df_rev = df_rev.iloc[depart:, 0:]
  numbers = [5, 8, 13, 21]
  groups = [[], [], [], []]
  matchs = 0
  for i, data in df_rev.iterrows():
    if (data[coteHeader] == equipe):
      if (matchs == 0):
        dateMatch1 = data[dateHeader]
      x = days_between(dateMatch1, data[dateHeader])
      if x is not None:
        if x > 600:
          for i in range(4):
            while (len(groups[i]) < numbers[i]):
              groups[i].append(0)
          return groups
      for i in range(4):
        if (len(groups[i]) < numbers[i]):
          if (data['A&H Scored?'] is None):
            groups[i].append(0)
          else:
            groups[i].append(data['A&H Scored?'])
      matchs += 1
      if (matchs > numbers[len(numbers) - 1]):
        return groups
  for i in range(4):
    while (len(groups[i]) < numbers[i]):
      groups[i].append(0)
  return groups


#obtenir la note à partir de l'array retourné par obtenir_arrays() ou obtenir_arrays_cote()
def obtenir_note(array):
  notes = []
  if array is not None:
    for i in array:
      notes.append(stats.mean(i))
    return stats.mean(notes)
  else:
    return None


#obtenir la note d'un match (sans prendre en compte le côté)
def note_match_beta(dtf, equipeA, equipeB, depart, HTheader, ATheader, DateHeader):
  arrayA = obtenir_arrays(dtf, equipeA, depart, HTheader, ATheader, DateHeader)
  arrayB = obtenir_arrays(dtf, equipeB, depart, HTheader, ATheader, DateHeader)
  if arrayA is not None and arrayB is not None:
    noteA = obtenir_note(arrayA)
    noteB = obtenir_note(arrayB)
    return (noteA + noteB) / 2
  return -1


#obtenir la note d'une équipe
def note_equipe(dtf, equipe, depart, coteHeader, HTheader, ATheader, DateHeader):
  array = obtenir_arrays(dtf, equipe, depart, HTheader, ATheader, DateHeader)
  if array is not None:
    arrayCote = obtenir_arrays_cote(dtf, equipe, depart, coteHeader, DateHeader)
    if arrayCote is not None:
      try:
        note = obtenir_note(array)
        note = (note * (1 + obtenir_note(arrayCote))) / 2
        return note
      except:
        return None


#obtenir la note d'un match
def note_match(dtf, equipeA, equipeB, depart, HTheader, ATheader, DateHeader):
  noteA = note_equipe(dtf, equipeA, depart, HTheader, HTheader, ATheader, DateHeader)
  noteB = note_equipe(dtf, equipeB, depart, ATheader, HTheader, ATheader, DateHeader)
  if noteA is not None and noteB is not None:
    return (noteA + noteB) / 2
  return -1


#récupérer les notes pour chaque match du dataframe passé en paramètre
def get_notes(df, HTheader, ATheader, DateHeader, NoteMatchHeader, moduloAffichage):
  for i, data in df.iterrows():
    note = note_match(df, data[HTheader], data[ATheader], df.shape[0] - 1 - i, HTheader, ATheader, DateHeader)
    df.at[i, NoteMatchHeader] = note
    if i % moduloAffichage == 0:
      print(f"{i} - {note}")
  print("\n")
  return df