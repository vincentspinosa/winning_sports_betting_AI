#get all zeros and ones for a dataframe
#need a dataframe, a Home Goals column header, a Away Goals column header
def get_zeros_and_ones(df, HG, AG):
  for i, data in df.iterrows():
    try:
      if (int(data[HG]) > 0 and int(data[AG]) > 0):
        df.at[i, 'A&H Scored?'] = 1
      else:
        df.at[i, 'A&H Scored?'] = None
    except:
        df.at[i, 'A&H Scored?'] = None
  return df