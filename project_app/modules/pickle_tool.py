import pickle

def save_models(models):
    with open('pickles/models.pickle','wb') as fw:
        pickle.dump(models, fw)
def save_score(score):
    with open('pickles/score.pickle','wb') as fw:
        pickle.dump(score, fw)
 
def load_models():
    with open('pickles/models.pickle', 'rb') as f: 
        return pickle.load(f)

def load_score():
    with open('pickles/score.pickle', 'rb') as f: 
        return pickle.load(f)

