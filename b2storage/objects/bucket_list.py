from ..b2_exceptions import B2InvalidBucketName, B2InvalidBucketConfiguration, B2BucketCreationError
from bucket import B2Bucket


class B2Buckets:

    def __init__(self, connector):
        self.connector = connector
        self._buckets_by_name = {}
        self._buckets_by_id = {}

    @property
    def all(self):
        path = '/b2_list_buckets'
        response = self.connector.make_request(path=path, method='post', account_id_required=True)
        if response.status_code == 200:
            response_json = response.json()
            print(response_json)
            buckets = []
            for bucket_json in response_json['buckets']:
                new_bucket = B2Bucket(connector=self.connector, **bucket_json)
                buckets.append(new_bucket)
                self._buckets_by_name[bucket_json['bucketName']] = new_bucket
                self._buckets_by_id[bucket_json['bucketId']] = new_bucket
            print(self._buckets_by_id)
            print(self._buckets_by_name)
            return buckets
        else:
            print(response.json())
        return response.json()

    def get(self, bucket_name=None, bucket_id=None):
        if bucket_name is not None:
            return self._buckets_by_name.get(bucket_name, None)
        else:
            return self._buckets_by_id.get(bucket_id, None)

    def create(self, bucket_name, configuration=None):
        path = '/b2_create_bucket'
        if type(bucket_name) != str or type(bucket_name) != bytes:
            raise B2InvalidBucketName
        if type(configuration) != dict and configuration is not None:
            raise B2InvalidBucketConfiguration
        params = {
            'bucketName': bucket_name,
            'bucketType': 'allPublic',
            #TODO: bucketInfo
            #TODO: corsRules
            #TODO: lifeCycleRules
        }
        response = self.connector.make_request(path=path, method='post', params=params, account_id_required=True)
        if response.status_code == 200:
            bucket_json = response.json()
            print(bucket_json)
            new_bucket = B2Bucket(connector=self.connector, **bucket_json)
            self._buckets_by_name[bucket_json['bucketName']] = new_bucket
            self._buckets_by_id[bucket_json['bucketId']] = new_bucket
            return new_bucket
        else:
            print(response.status_code)
            raise B2BucketCreationError(str(response.json()))