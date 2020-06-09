import boto3
import datetime
from botocore.signers import CloudFrontSigner
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import padding
from django.conf import settings


def rsa_signer(message):
    private_key = serialization.load_pem_private_key(
        settings.CLOUDFRONT_KEY_PRIVATE.encode('ascii'),
        password=None,
        backend=default_backend()
    )
    return private_key.sign(message, padding.PKCS1v15(), hashes.SHA1())


def sign_download(url):
    expire_date = datetime.datetime.utcnow() + datetime.timedelta(hours=1)
    cloudfront_signer = CloudFrontSigner(settings.CLOUDFRONT_KEY_ID, rsa_signer)
    signed_url = cloudfront_signer.generate_presigned_url(url, date_less_than=expire_date)
    return signed_url


def sign_upload(file_id):
    s3 = boto3.client('s3')
    signed_url = s3.generate_presigned_url(
        'put_object',
        Params={'Bucket': settings.S3_BUCKET, 'Key': file_id},
        ExpiresIn=3600,
        HttpMethod='PUT'
    )
    return signed_url


def s3_delete(del_list):
    s3 = boto3.resource('s3')
    bucket = s3.Bucket(settings.S3_BUCKET)
    del_s3_list = []
    for key in del_list:
        del_s3_list.append({'Key': key})
    bucket.delete_objects(Delete={'Objects': del_s3_list})


def s3_copy(file_id, new_file_id):
    s3 = boto3.resource('s3')
    bucket = s3.Bucket(settings.S3_BUCKET)
    copy_source = {
        'Bucket': settings.S3_BUCKET,
        'Key': file_id
    }
    obj = bucket.Object(str(new_file_id))
    obj.copy(copy_source)
