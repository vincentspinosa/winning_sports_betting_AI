#get all zeros and ones for a dataframe
#need a dataframe, a Home Goals column header, a Away Goals column header
def get_zeros_and_ones(df, HG, AG, HASheader):
  for i, data in df.iterrows():
    if (data[HG] > 0 and data[AG] > 0):
      df.at[i, HASheader] = 1
    else:
      df.at[i, HASheader] = 0
  return df

def arrange_data(df, HGheader, AGheader, HASheader):
  df = df.iloc[:, 1:6]
  df = df.dropna()
  df[HGheader] = df[HGheader].astype(int)
  df[AGheader] = df[AGheader].astype(int)
  df[HASheader] = ''
  df = df.reset_index(drop=True)
  df = get_zeros_and_ones(df, HGheader, AGheader, HASheader)
  df[HASheader] = df[HASheader].astype(int)
  return df