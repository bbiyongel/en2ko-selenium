#%% import
from csv import DictReader

#%%
class DataSet():
    def __init__(self, name="train", path="fnc-1"):
        self.path = path

        print("Reading dataset")
        bodies = name+"_bodies.csv"
        stances = name+"_stances.csv"

        self.stances = self.read(stances)
        articles = self.read(bodies)
        self.articles = dict()

        #make the body ID an integer value
        for i,_ in enumerate(self.stances):
            self.stances[i] = dict(self.stances[i])
            try:
                self.stances[i]['Body ID'] = int(self.stances[i]['Body ID'])
            except ValueError:
                pass

        #copy all bodies into a dictionary
        for article in articles:
            self.articles[int(article['Body ID'])] = article['articleBody']

        print("Total stances: " + str(len(self.stances)))
        print("Total bodies: " + str(len(self.articles)))



    def read(self,filename):
        rows = []
        with open(self.path + "/" + filename, "r", encoding='utf-8') as table:
            r = DictReader(table)

            for line in r:
                rows.append(line)
        return rows

#%%
def extract_sub_stances(stances, body_id):
    # extract all headline and stance for the body_id
    # list of {'Headline': '~~', 'Stance': '~~'}
    # type(stances) = list, type(body_id) = int
    return [{'Headline': d['Headline'],'Stance': d['Stance']} 
             for d in stances if d['Body ID'] == body_id]