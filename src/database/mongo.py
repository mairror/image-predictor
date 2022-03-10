from typing import Any, Dict, List, Union

from config.settings import (
    MONGO_COLLECTION_FACES,
    MONGO_COLLECTION_PREDICT,
    MONGO_DATABASE,
    MONGO_URI,
)
from pymongo import MongoClient
from utils.logging import image_predictor

client = MongoClient(MONGO_URI)
database = client[MONGO_DATABASE]


def insert_mongo(document: Dict) -> Union[bool, None]:
    """
    Name: insert_mongo
    Description:
        This function inserts a partial document into MongoDB
        of the bucket and the key of the object.
    Inputs:
        key: The compound string bucket/key_name
    Outputs:
        The object from MongoDB
    """
    collection = database[MONGO_COLLECTION_PREDICT]
    try:
        query_response = collection.insert_one(document)
        return query_response.acknowledged
    except Exception as e:
        image_predictor.error(
            f"There was an error inserting the document into mongo: {e}"
        )


def query_mongo(key: str) -> List[Any]:
    """
    Name: query_mongo
    Description:
        This function query a mongo collection to return
        the numpy array cut by the image processor.
    Inputs:
        key: The compound string bucket/key_name
    Outputs:
        The object from MongoDB
    """
    collection = database[MONGO_COLLECTION_FACES]
    data = {"key": key}
    project = {"_id": 0, "faces": 1}
    try:
        query_response = collection.find_one(data, project)
        return query_response["faces"]
    except Exception as e:
        image_predictor.error(f"There was an error finding the key {key}: {e}")
