import pymongo
import json
import pandas as pd
from sensor.config import mongo_client

from dotenv import load_dotenv
print(f"Loading environment variable from .env file")
load_dotenv()

DATABASE_NAME = 'aps'
COLLECTION_NAME = 'sensor'
DATABASE_FILE_PATH = '/config/workspace/aps_failure_training_set1.csv'



if __name__=="__main__":

    #Read CSV File as Pandas Data Frame
    df = pd.read_csv(DATABASE_FILE_PATH)
    print(df.shape)

    #Delete Index Row
    df.reset_index(drop =True, inplace= True)

    #Conver Pandas Data Frame to JSON Format
    json_record = list(json.loads(df.T.to_json()).values())
    print(json_record[0])

    #Store Records in MongoDB
    mongo_client['aps']['sensor'].insert_many(json_record)

    
