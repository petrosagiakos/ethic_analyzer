import config
import pandas as pd

def allowed_file(filename):
    ext=filename.split('.')[-1]
    if ext in config.FILE_EXTENSIONS:
        return True
    return False
def preview(file):
    words=[]
    df=pd.read_csv(file)
    words.append(df.dtypes)
    words.append(df.head(10).to_html())
    words.append(df.columns)
    words.append(df.shape[1])
    words.append(df.shape[0])
    return words
    
#db()