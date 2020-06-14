import boto3
from django.conf import settings


def sign_download(file_id):
    s3 = boto3.client('s3')
    signed_url = s3.generate_presigned_url(
        'get_object',
        Params={'Bucket': settings.S3_BUCKET, 'Key': file_id},
        ExpiresIn=3600,
        HttpMethod='GET'
    )
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


def s3_update_and_return_size(file_id, name):
    s3 = boto3.resource('s3')
    s3_object = s3.Object(settings.S3_BUCKET, file_id)
    s3_object.copy_from(CopySource={'Bucket': settings.S3_BUCKET, 'Key': file_id},
                        ContentType='application/octet-stream',
                        ContentDisposition='attachment; filename=%s' % name,
                        MetadataDirective='REPLACE')
    return s3_object.content_length
