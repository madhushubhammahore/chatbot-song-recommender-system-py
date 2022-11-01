class popularity_recommender():
    def __init__(self):
        self.t_data = None                                
        self.u_id = None                             #ID of the user
        self.i_id = None                             #ID of Song the user is listening to
        self.pop_recommendations = None              #getting popularity recommendations according to that
        
    #Create the system model
    def create_p(self, t_data, u_id, i_id):
        self.t_data = t_data
        self.u_id = u_id
        self.i_id = i_id
        #Get the no. of times each song has been listened as recommendation score 
        t_data_grouped = t_data.groupby([self.i_id]).agg({self.u_id: 'count'}).reset_index()
        t_data_grouped.rename(columns = {'user_id': 'score'},inplace=True)
    
        #Sort the songs based upon recommendation score
        t_data_sort = t_data_grouped.sort_values(['score', self.i_id], ascending = [0,1])
    
        #Generate a recommendation rank based upon score
        t_data_sort['Rank'] = t_data_sort['score'].rank(ascending=0, method='first')
        
        #Get the top 10 recommendations
        self.pop_recommendations = t_data_sort.head(10)
    #Use the system model to give recommendations
    def recommend_p(self, u_id):    
        u_recommendations = self.pop_recommendations
        
        #Add user_id column for which the recommended songs are generated
        u_recommendations['user_id'] = u_id
    
        #Bring user_id column to the front
        cols = u_recommendations.columns.tolist()
        cols = cols[-1:] + cols[:-1]
        u_recommendations = u_recommendations[cols]
        
        return u_recommendations