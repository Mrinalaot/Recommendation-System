
import pandas as pd
import numpy as np
import warnings
warnings.simplefilter("ignore", DeprecationWarning)

# --- Read Data --- #
data = pd.read_csv('groceries_2.csv')

series = pd.Series([0 for i in range(len(set(data['Person']))) ])
df = pd.DataFrame()
df['Person'] = pd.Series([i for i in range(1,len(set(data['Person']))+1)])

for i in range(0, len(data)):
  df[data['item'][i]] = series
   
k=-1
l = []
for i in range(0, len(data)):
  if data['Person'][i] in l:
    s = data['item'][i]
    df[s][k] = 1
  else:
    print(data['Person'][i],sep='\n')
    l.append(data['Person'][i])
    s = data['item'][i]
    df[s][k+1] = 1
    k=k+1
    

################################################################################
  
from scipy.spatial.distance import cosine

# --- Start Item Based Recommendations --- #
df1 = df.drop('Person', 1)
# Create a placeholder dataframe listing item vs. item
data_ibs = pd.DataFrame(index=df1.columns,columns=df1.columns)
 
# Lets fill in those empty spaces with cosine similarities
# Loop through the columns
lenx = len(data_ibs.columns)
for i in range(0, lenx) :
    # Loop through the columns for each column
    for j in range(0, lenx) :
      # Fill in placeholder with cosine similarities
      print('running...')
      data_ibs.iloc[i,j] = 1-cosine(df1.iloc[:,i],df1.iloc[:,j])
print('Completed!!')

# Create a placeholder items for closes neighbours to an item
l = [i for i in range(1,11)]
data_neighbours = pd.DataFrame(index = data_ibs.columns, columns = l)
 
# Loop through our similarity dataframe and fill in neighbouring item names
for i in range(0,len(data_ibs.columns)):
    data_neighbours.iloc[i,:10] = data_ibs.iloc[0:,i].sort_values(ascending=False)[:10].index
 


#############################################################################
def itemBased(s):  
  #s = input('Enter Item name : ')
  for i in s:
    print(list(data_neighbours.ix[i][2:7].values))
##############################################################################
# --- Start User Based Recommendations --- #

# Helper function to get similarity scores
def getScore(history, similarities):
   return sum(history*similarities)/sum(similarities)
 
  

# Create a place holder matrix for similarities, and fill in the user name column
data_sims = pd.DataFrame(index = df.index, columns = df.columns)
data_sims.iloc[:,:1] = df.iloc[:,:1]

#Loop through all rows, skip the user column, and fill with similarity scores
x1 = len(data_sims.index)
x2 = len(data_sims.columns)

for i in range(0, x1):
  print('running...',i)
  for j in range(1, x2):
    user = data_sims.index[i]
    product = data_sims.columns[j]
    
    if df.ix[i][j] == 1:
      data_sims.ix[i][j] = 0
    else:
      product_top_names = data_neighbours.ix[product][1:10]
      product_top_sims = data_ibs.ix[product].sort_values(ascending=False)[1:10]
      user_purchases = df1.ix[user,product_top_names]
      data_sims.ix[i][j] = getScore(user_purchases,product_top_sims)
 
# Get the top Items
data_recommend = pd.DataFrame(index=data_sims.index, columns=['Person','1','2','3','4','5','6'])
data_recommend.iloc[0:,0] = data_sims.iloc[:,0]
 
# Instead of top song scores, we want to see names
for i in range(0, x1):
    data_recommend.iloc[i,1:] = data_sims.iloc[i,:].sort_values(ascending=False).ix[1:7,].index.transpose()
 
###########################################################
def userBased():
  print(list(data_recommend.ix[x-1][1:].values))

###########################################################
data_neighbours.to_csv('data_neighbours.csv',index=True, header=True)
data_sims.to_csv('data_sims.csv', index=True, header=True)
data_recommend.to_csv('data_recommend.csv',index=True,header=True) 
##################################################################


