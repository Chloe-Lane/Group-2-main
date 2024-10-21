import datetime

AWS_ACCESS_KEY_ID = "AKIAQSOI4C3H4DJ4SQ2C"
AWS_SECRET_ACCESS_KEY = "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"
AWS_FILE_EXPIRE = 200
AWS_PRELOAD_METADATA = True
AWS_QUERYSTRING_AUTH = True

STORAGES = {
     "default": {"BACKEND": "storages.backends.s3boto3.S3StaticStorage"},
     "staticfiles": {"BACKEND": "storages.backends.s3boto3.S3StaticStorage"},
 }

AWS_STORAGE_BUCKET_NAME = 'pyple201-bucket'
S3DIRECT_REGION = 'ap-southeast-2'
S3_URL = '//%s.s3.amazonaws.com/' % AWS_STORAGE_BUCKET_NAME
MEDIA_URL = '//%s.s3.amazonaws.com/media/' % AWS_STORAGE_BUCKET_NAME
MEDIA_ROOT = MEDIA_URL
STATIC_URL = S3_URL + 'static/'
ADMIN_MEDIA_PREFIX = STATIC_URL + 'admin/'

two_months = datetime.timedelta(days=61)
date_two_months_later = datetime.date.today() + two_months
expires = date_two_months_later.strftime("%A, %d %B %Y 20:00:00 GMT")

AWS_HEADERS = {
    'Expires': expires,
    'Cache-Control': 'max-age=%d' % (int(two_months.total_seconds()), ),
}

AUTH_PASSWORD_VALIDATORS = True