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


def sign(url):
    expire_date = datetime.datetime(2020, 6, 10)
    cloudfront_signer = CloudFrontSigner(settings.CLOUDFRONT_KEY_ID, rsa_signer)
    signed_url = cloudfront_signer.generate_presigned_url(url, date_less_than=expire_date)
    return signed_url
