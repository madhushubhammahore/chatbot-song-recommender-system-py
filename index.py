#Class for Item similarity based Recommender System model
class similarity_recommender():
    def __init__(self):
        self.t_data = None
        self.u_id = None
        self.i_id = None
        self.co_matrix = None
        self.songs_dic = None
        self.rev_songs_dic = None
        self.i_similarity_recommendations = None
        
    #Get unique songs corresponding to a given user
    def get_u_items(self, u):
        u_data = self.t_data[self.t_data[self.u_id] == u]
        u_items = list(u_data[self.i_id].unique())
        
        return u_items
        
    #Get unique users for a given song
    def get_i_users(self, i):
        i_data = self.t_data[self.t_data[self.i_id] == i]
        i_users = set(i_data[self.u_id].unique())
            
        return i_users
        
    #Get unique songs in the training data
    def get_all_items_t_data(self):
        all_items = list(self.t_data[self.i_id].unique())
            
        return all_items
        
    #Construct cooccurence matrix
    def construct_co_matrix(self, u_songs, a_songs):
            
        #Get users for all songs in user_songs.
        u_songs_users = []        
        for i in range(0, len(u_songs)):
            u_songs_users.append(self.get_i_users(u_songs[i]))
            
        #Initialize the item cooccurence matrix of size len(user_songs) X len(songs)
        co_matrix = np.matrix(np.zeros(shape=(len(u_songs), len(a_songs))), float)
           
        #Calculate similarity between songs listened by the user and all unique songs in the training data
        for i in range(0,len(a_songs)):
            #Calculate unique listeners (users) of song (item) i
            songs_i_data = self.t_data[self.t_data[self.i_id] == a_songs[i]]
            users_i = set(songs_i_data[self.u_id].unique())
            
            for j in range(0,len(u_songs)):       
                    
                #Get unique listeners (users) of song (item) j
                users_j = u_songs_users[j]
                    
                #Calculate the songs which are in common listened by users i & j
                users_intersection = users_i.intersection(users_j)
                
                #Calculate cooccurence_matrix[i,j] as Jaccard Index
                if len(users_intersection) != 0:
                    #Calculate all the songs listened by i & j
                    users_union = users_i.union(users_j)
                    
                    co_matrix[j,i] = float(len(users_intersection))/float(len(users_union))
                else:
                    co_matrix[j,i] = 0
                    
        
        return co_matrix
    
    #Use the cooccurence matrix to make top recommendations
    def generate_top_r(self, user, cooccurence_matrix, a_songs, u_songs):
        print("Non zero values in cooccurence_matrix :%d" % np.count_nonzero(cooccurence_matrix))
        
        #Calculate the average of the scores in the cooccurence matrix for all songs listened by the user.
        user_sim_scores = cooccurence_matrix.sum(axis=0)/float(cooccurence_matrix.shape[0])
        user_sim_scores = np.array(user_sim_scores)[0].tolist()
 
        #Sort the indices of user_sim_scores based upon their value also maintain the corresponding score
        s_index = sorted(((e,i) for i,e in enumerate(list(user_sim_scores))), reverse=True)
    
        #Create a dataframe from the following
        columns = ['user_id', 'song', 'score', 'rank']
        #index = np.arange(1) # array of numbers for the number of samples
        df1 = pandas.DataFrame(columns=columns)
         
        #Fill the dataframe with top 10 songs
        rank = 1 
        for i in range(0,len(s_index)):
            if ~np.isnan(s_index[i][0]) and a_songs[s_index[i][1]] not in u_songs and rank <= 10:
                df1.loc[len(df1)]=[user,a_songs[s_index[i][1]],s_index[i][0],rank]
                rank = rank+1
        
        #Handle the case where there are no recommendations
        if df1.shape[0] == 0:
            print("The current user don't have any song for similarity based recommendation model.")
            return -1
        else:
            return df1
 
    #Create the system model
    def create_s(self, t_data, u_id, i_id):
        self.t_data = t_data
        self.u_id = u_id
        self.i_id = i_id
    #Use the model to make recommendations
    def recommend_s(self, u):
        
        #A. Get all unique songs for this user
        u_songs = self.get_u_items(u)    
            
        print("No. of songs for the user: %d" % len(u_songs))
    
        #B. Get all the songs in the data
        a_songs = self.get_all_items_t_data()
        
        print("No. of songs in the list: %d" % len(a_songs))
         
        #C. Make the cooccurence matrix of size len(user_songs) X len(songs)
        co_matrix = self.construct_co_matrix(u_songs, a_songs)
        
        #D. Use the matrix to make recommended songs
        df_r = self.generate_top_r(u, co_matrix, a_songs, u_songs)
        return df_r
    
    #Create a function to get similar songs
    def similar_items(self, i_list):
        
        u_songs = i_list
        
        #A. Get all the songs from the data
        a_songs = self.get_all_items_t_data()
        
        print("no. of unique songs in the set: %d" % len(a_songs))
         
        #B. Make the cooccurence matrix of size len(user_songs) X len(songs)
        co_matrix = self.construct_co_matrix(u_songs, a_songs)
        
        #C. Use the matrix to make recommendations
        u = ""
        df_r = self.generate_top_r(u, co_matrix, a_songs, u_songs)
         
        return df_r