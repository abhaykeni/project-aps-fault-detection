from sensor.entity import config_entity
from sensor.entity import artifact_entity
from sensor.exception import SensorException
from sensor.logger import logging
from sensor import utils
import numpy as np
import os,sys
from sklearn.model_selection import train_test_split

class DataIngestion:

    def __init__(self,data_ingestion_config:config_entity.DataIngestionConfig):
        try:
            self.data_ingestion_config = data_ingestion_config
        except Exception as e:
            raise SensorException(e,sys)

    def initiate_data_ingestion(self)->artifact_entity.DataIngestionArtifact:
        try:
            #Exporting collection data as Pandas Data frame
            logging.info(f"Exporting collection data as pandas dataframe")
            df: pd.DataFrame = utils.get_collection_as_dataframe(
                database_name = self.data_ingestion_config.database_name, 
                collection_name = self.data_ingestion_config.collection_name
                )
            
            logging.info("Save data in feature store")
            
            #Replace na with Nan
            df.replace(to_replace="na",value=np.NAN,inplace=True)

            #Save Data in Feature Store Folder
            logging.info("Create feature store folder if not available")
            #Create feature store folder if not available
            feature_store_dir = os.path.dirname(self.data_ingestion_config.feature_store_file_path)
            os.makedirs(feature_store_dir,exist_ok=True)
            logging.info("Save df to feature store folder")
            #Save df to feature store folder
            df.to_csv(path_or_buf=self.data_ingestion_config.feature_store_file_path,index=False,header=True)

            #Split Dataset into Train and Test
            logging.info("split dataset into train and test set")
            train_df,test_df = train_test_split(df, test_size=self.data_ingestion_config.test_size)

            logging.info("create dataset directory folder if not available")
            #create dataset directory folder if not available
            dataset_dir = os.path.dirname(self.data_ingestion_config.train_file_path)
            os.makedirs(dataset_dir,exist_ok=True)

            logging.info("Save train and test df to dataset folder")
            #Save train and test df to dataset folder
            df.to_csv(path_or_buf=self.data_ingestion_config.train_file_path,index=False,header=True)
            df.to_csv(path_or_buf=self.data_ingestion_config.test_file_path,index=False,header=True)

            #Prepare artifact
            data_ingestion_artifact = artifact_entity.DataIngestionArtifact(
                feature_store_file_path = self.data_ingestion_config.feature_store_file_path,
                train_file_path = self.data_ingestion_config.train_file_path,
                test_file_path = self.data_ingestion_config.test_file_path 
            )

            logging.info(f"Data ingestion artifact: {data_ingestion_artifact}")
            return data_ingestion_artifact

        except Exception as e:
            raise SensorException(e,sys)

    

