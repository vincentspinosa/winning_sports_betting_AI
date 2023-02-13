#get all zeros and ones for a dataframe
#need a dataframe, a Home Goals column header, a Away Goals column header
def get_zeros_and_ones(df, HG, AG):
  for i, data in df.iterrows():
    try:
      if (int(data[HG]) > 0 and int(data[AG]) > 0):
        df.at[i, 'A&H Scored?'] = 1
      else:
        df.at[i, 'A&H Scored?'] = 0
    except:
        df.at[i, 'A&H Scored?'] = 0
  return df

def arrange_data(dataframe):
  dataframe = dataframe.iloc[:, 1:6]
  dataframe = dataframe.dropna()
  dataframe['FTHG'] = dataframe['FTHG'].astype(int)
  dataframe['FTAG'] = dataframe['FTAG'].astype(int)
  dataframe['A&H Scored?'] = ''
  dataframe = dataframe.reset_index(drop=True)
  dataframe = get_zeros_and_ones(dataframe, 'FTHG', 'FTAG')
  dataframe['A&H Scored?'] = dataframe['A&H Scored?'].astype(int)
  return dataframe