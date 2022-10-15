import json

from fastapi import APIRouter, Depends, HTTPException, Query, Body, status
import requests
from schemas import report
from api import deps
import crud
import utils
from core.config import settings
from core.logger_config import ErrorType, log_handler, logger
import os
from fastapi import File, UploadFile
import boto3
import json
from botocore.exceptions import ClientError
from boto3.exceptions import S3UploadFailedError
from fastapi_jwt_auth import AuthJWT
import fastapi_jwt_auth
import boto3
from boto3.s3.transfer import TransferConfig
from api.api_v1.services.multipart_s3_upload import upload_with_chunksize_and_meta


MB = 1024 * 1024
s3 = boto3.resource("s3")


router = APIRouter()

sqs = boto3.resource("sqs", region_name=settings.LIMS_REGION)
s3_client = boto3.client("s3", region_name=settings.LIMS_REGION)

temp_dir = "/tmp"


@router.post("/lims")
async def test():
    push_to_queue()
    return {"message": "Hello World"}
 
@router.post("/upload_file/")
async def create_upload_file(
    file: UploadFile,
    Authorize: AuthJWT = Depends(),
    token: bool = Depends(deps.token_filter),
):
    try:
        Authorize.jwt_required()

        lims_output_folder_name = settings.OUTPUT_FOLDER
        file_name = file.filename
        try:
            contents = file.file.read()
            file_path = f"{temp_dir}/{file_name}"
            with open(file_path, "wb") as f:
                f.write(contents)
        except Exception:
            return {"message": "There was an error uploading the file"}
        finally:
            file.file.close()
        upload_to_s3(file_path, file_name, lims_output_folder_name)
        # upload_multipart_to_s3(file_path, file_name, lims_output_folder_name)
        listdir = os.listdir(temp_dir)
        logger.info(listdir)
        # Get the queue. This returns an SQS.Queue instance
        # queue = sqs.get_queue_by_name(QueueName=settings.ML_QUEUE_NAME)
        # queue.send_message(MessageBody=json.dumps({"filename": file_name}))
        return {"filename": file_name}
    except fastapi_jwt_auth.exceptions.RevokedTokenError:
        raise HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail="Token has been revoked",
    )


def push_to_queue() -> None:

    # Get the queue. This returns an SQS.Queue instance
    print("queue")
    print(settings.ML_QUEUE_NAME)
    queue = sqs.get_queue_by_name(QueueName=settings.ML_QUEUE_NAME)
    queue.send_message(MessageBody=json.dumps({"grs_file": "test", "ped_file_dir": "test_ped"}))


def upload_to_s3(file_path: str, file_name: str, lims_output_folder_name) -> bool:
    try:
        s3_client.upload_file(
            file_path, settings.LIMS_OUTPUT_BUCKET_NAME, f"{lims_output_folder_name}/{file_name}"
        )
        logger.info(
            f"File has been uploaded successfully. File path {lims_output_folder_name}/{file_name}"
        )
        os.remove(file_path)
        return True
    except S3UploadFailedError as e:
        logger.error(e)
        os.remove(file_path)
        return False
    except ClientError as e:
        logger.error(e)
        os.remove(file_path)
        return False


def upload_multipart_to_s3(file_path: str, file_name: str, lims_output_folder_name):
    presigned_url_response = create_presigned_url(f"{lims_output_folder_name}/{file_name}")
    print(presigned_url_response)

    with open(file_path, "rb") as file_to_upload:
        files = {"file": (file_name, file_to_upload)}
        requests.post(
            presigned_url_response["url"], data=presigned_url_response["fields"], files=files
        )


def create_presigned_url1(file_path: str, expiration: int = 10 * 3600):
    s3_client = boto3.client(
        "s3",
        region_name=settings.LIMS_REGION,
    )
    try:
        return s3_client.generate_presigned_post(
            settings.LIMS_OUTPUT_BUCKET_NAME, file_path, ExpiresIn=expiration
        )
    except ClientError as e:
        logger.error(e)
        return None


def create_presigned_url(file_path: str, expiration: int = 10 * 3600):
    s3_client = boto3.client(
        "s3",
        region_name=settings.LIMS_REGION,
    )
    try:
        return s3_client.generate_presigned_url(
            "put_object",
            Params={
                "Bucket": settings.LIMS_OUTPUT_BUCKET_NAME,
                "Key": file_path,
            },
            ExpiresIn=expiration,
        )
    except ClientError as e:
        logger.error(e)
        return None
