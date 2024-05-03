import pandas as pd
from pymongo import MongoClient
from sklearn.preprocessing import LabelEncoder, StandardScaler


def preprocess_data():
    client = MongoClient('mongodb://localhost:27017/')
    db = client['flaskdatabase']
    collection = db['data']

    df = pd.DataFrame(list(collection.find()))
    df.drop('_id', axis=1, inplace=True)
    df = df.dropna(subset=['Year', 'Publisher'], axis=0)
    data = df.drop(['Rank', 'Name', 'Year', 'JP_Sales', 'Other_Sales', 'Global_Sales'], axis=1)

    le = LabelEncoder()
    data['Platform'] = le.fit_transform(data['Platform'].astype('str'))
    data['Genre'] = le.fit_transform(data['Genre'].astype('str'))
    data['Publisher'] = le.fit_transform(data['Publisher'].astype('str'))

    y = df['Global_Sales']
    scaler = StandardScaler()
    scaler.fit(data)
    data = scaler.transform(data)

    return data, y


from sklearn.model_selection import train_test_split
from sklearn.ensemble import GradientBoostingRegressor
from sklearn.metrics import mean_squared_error, r2_score


def train_model(X, y):
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.30)
    gbr = GradientBoostingRegressor()
    gbr.fit(X_train, y_train)

    pred_gbr = gbr.predict(X_test)

    results = {
        'Accuracy_Train': gbr.score(X_train, y_train),
        'Accuracy_Test': gbr.score(X_test, y_test),
        'MSE': mean_squared_error(y_test, pred_gbr),
        'Variance_Score': r2_score(y_test, pred_gbr)
    }
    return results

def save_to_db(results):
    client = MongoClient('mongodb://localhost:27017/')
    db = client['results_db']
    collection = db['model_results']
    collection.insert_one(results)


def retrieve_results():
    client = MongoClient('mongodb://localhost:27017/')
    db = client['results_db']
    collection = db['model_results']

    results = list(collection.find({}, {'_id': 0}))
    return results
