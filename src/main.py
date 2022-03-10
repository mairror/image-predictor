from http.client import HTTPException

import boto3
from aws_utils.sqs import delete_message, get_queue_url, receive_message
from config.settings import SQS_PREDICT_QUEUE_NAME
from database.mongo import insert_mongo, query_mongo
from faces_predict.predict_faces import make_prediction
from utils.logging import image_predictor


def main() -> None:
    """
    Name: main
    Description:
        Main principal function to run the event listener and send the images predictions.
    Inputs:
        None
    Outputs:
        None
    S3 received object:
        s3_object = {
            "key": "",
            "bucket_name": "",
            "checksum": ""
        }
    """

    while True:
        try:
            image_predictor.info("Waiting for messages...")
            s3_object, receipt_handle, message_id = receive_message(
                sqs_client, predict_queue_url
            )

            query_result = query_mongo(s3_object["key"])
            prediction = make_prediction(s3_object["key"], query_result)
            response = insert_mongo(prediction)

            if response:
                image_predictor.info("Prediction succesfully inserted in the DB.")
            else:
                image_predictor.error(
                    "Something was wrong inserting the prediction in the DB."
                )

            s3_deleted_object = delete_message(
                sqs_client, predict_queue_url, receipt_handle
            )

            if s3_deleted_object == 200:
                image_predictor.info(f"Deleted from queue event {message_id}")
            else:
                image_predictor.error(f"Error deleting from queue event {message_id}")

        except KeyError as key_error:
            image_predictor.error(f"KeyError: No key {key_error} found")
            continue
        except TypeError as type_error:
            image_predictor.error(f"NoneType: No key {type_error} found")
            continue
        except HTTPException as http_exception:
            image_predictor.error(f"{http_exception}")
            continue
        except Exception as exception:
            image_predictor.error(f"{exception}")
            continue


if __name__ == "__main__":
    try:
        image_predictor.info("Start the SQS client to receive messages...")
        sqs_client = boto3.client("sqs")
        predict_queue_url = get_queue_url(sqs_client, SQS_PREDICT_QUEUE_NAME)
    except Exception as e:
        image_predictor.error(
            "There was an error connecting to aws. "
            "Check the aws credentials and the default region. "
            f"{e}"
        )
    main()
