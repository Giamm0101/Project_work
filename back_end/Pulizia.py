import pandas as pd

path = input("Mettere il path del csv da pulire")
df = pd.read_csv(path)
df.rename(columns={'Unnamed: 0': 'index'}, inplace=True)
df_filtrato = df[df['total_reviews_count'] >= 10]
df_filtrato['total_reviews_count'] = df_filtrato['total_reviews_count'].astype(int)
df_filtrato.to_csv('Dataset_ancora_più_pulito.csv', index=False)
print(df_filtrato.head())
print(df)
