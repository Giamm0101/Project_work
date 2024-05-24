import csv
import pandas as pd
import pandasgui

dt= {'region': 'str'}
df = pd.read_csv('tripadvisor_european_restaurants.csv', dtype= dt)
colonne_da_eliminare= ['original_location', 'claimed', 'popularity_detailed', 'popularity_generic', 'price_level', 'meals',
'vegetarian_friendly','vegan_options', 'open_days_per_week', 'open_hours_per_week', 'working_shifts_per_week', 'default_language',
'reviews_count_in_default_language', 'excellent', 'very_good', 'average', 'poor', 'terrible', 'food', 'service','value','atmosphere',
'keywords']
df.drop(columns= colonne_da_eliminare, inplace=True)

df_glutenfree= df[df['gluten_free']== 'Y']

df_glutenfree.to_csv('Dataset_pulito', index=True)
pandasgui.show(df_glutenfree)



