import config
import pandas as pd
import os

def allowed_file(filename):
    ext=filename.split('.')[-1]
    if ext in config.FILE_EXTENSIONS:
        return True
    return False

def preview(file):
    words = []

    ext = os.path.splitext(file)[1].lower()

    if ext == ".csv":
        df = pd.read_csv(file)
    elif ext == ".xlsx":
        df = pd.read_excel(file)
    else:
        raise ValueError("Unsupported file type")

    words.append(df.dtypes.astype(str))   # safer for JSON/templates
    words.append(df.head(10).to_html(classes="table table-striped", index=False))
    words.append(df.columns.tolist())
    words.append(df.shape[1])
    words.append(df.shape[0])

    return words