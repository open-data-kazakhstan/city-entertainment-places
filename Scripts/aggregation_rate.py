import pandas as pd 

df1 = pd.read_csv('./data/output1.csv')
df2 = pd.read_csv('./archive/city_population.csv')

region_replacements = {
    'Zhambyl Region': 'Jambyl Region',
    'Zhetysu Region': 'Jetisu Region',
    'Abay Region': 'Abai Region',
    'Turkestan Region': 'Turkistan Region',
    'Туркестанская ':'Turkistan Region',
    'The Republic of Kazakhstan': 'The Republic Of Kazakhstan',
    'Shymkent City': 'Shymkent city',
    'Almaty City': 'Almaty city',
    'Astana City': 'Astana city',
    'The Republic Kazakhstan': 'The Republic Of Kazakhstan',
    'Область Абай': 'Abai Region',
    'Ulytau Region Region': 'Ulytau Region',
    'Актюбинская ': 'Aktobe Region',
    'Zhetisu Region': 'Jetisu Region',
    'Karagandy Region': 'Karaganda Region',
    'Astana city Region': 'Astana city'
}

df2['Region'] = df2['Region'].replace(region_replacements)
df1['Region'] = df1['Region'].replace(region_replacements)

df2 = df2.drop(df2.columns[2:], axis=1)
df2.rename(columns={'Total': 'Population'}, inplace=True)

columns_to_fillna = ['Theaters', 'Museums', 'Cultural and leisure facilities', 'Cinemas', 'Libraries', 'Concert organizations', 'Parks', 'Zoos', 'Circuses']
df1[columns_to_fillna] = df1[columns_to_fillna].fillna(0)
df1['Cultural and leisure facilities'] = df1['Cultural and leisure facilities'].replace('3 102', 3102)
df1['Libraries'] = df1['Libraries'].replace('3 917', 3917)
df1['Zoos'] = df1['Zoos'].replace('х', 0)

df1[columns_to_fillna] = df1[columns_to_fillna].astype(int)
df1['number of entertainment places'] = df1[columns_to_fillna].sum(axis=1)
df1 = df1.drop(columns_to_fillna, axis=1)

df3=pd.merge(df1,df2,on='Region', how='outer')
df3['Entertainment-places-rate'] = ((df3['number of entertainment places']*1000)/df3['Population'])

df3.to_csv('./data/Entertainment-places-rate.csv')

print(df3)