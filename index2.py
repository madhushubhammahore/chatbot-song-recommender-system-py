#Read user_id, song_id, listen_count 
#This step might take time to download data from external sources
triplets = 'https://static.turi.com/datasets/millionsong/10000.txt'
songs_metadata = 'https://static.turi.com/datasets/millionsong/song_data.csv'

song_df_a = pandas.read_table(triplets,header=None)
song_df_a.columns = ['user_id', 'song_id', 'listen_count']

#Read song  metadata
song_df_b =  pandas.read_csv(songs_metadata)

#Merge the two dataframes above to create input dataframe for recommender systems
song_df1 = pandas.merge(song_df_a, song_df_b.drop_duplicates(['song_id']), on="song_id", how="left")
song_df1.head()