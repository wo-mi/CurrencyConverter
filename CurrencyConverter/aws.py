import os
import json
import boto3
import botocore


class AWS:
    def __init__(self):
        self._get_credentials()
        self._filename = "log.txt"

    def append_data(self, data):
        self._download_data()

        with open(self._filename, "r") as f:
            input = json.load(f)

        if data not in input:
            output = json.dumps(input + [data])

            with open(self._filename, "w") as f:
                f.write(output)

            self._upload_data()

        os.remove(self._filename)

    def _get_credentials(self):
        try:
            with open("aws_credentials", "r") as f:
                parsed_json = json.load(f)
        except Exception:
            raise Exception("Can't parse json.")

        if "aws_access_key_id" not in parsed_json or "aws_secret_access_key" not in parsed_json:
            raise Exception("Can't read credentials.")

        self.bucket_name = parsed_json["bucket"]
        self.aws_access_key_id = parsed_json["aws_access_key_id"]
        self.aws_secret_access_key = parsed_json["aws_secret_access_key"]

    def _download_data(self):
        try:
            self.bucket.download_file(self._filename, self._filename)

        except botocore.exceptions.ClientError as e:
            if e.response["Error"]["Code"] == "404":  # file doesn't exist on S3
                with open(self._filename, "w") as f:
                    f.write("[]")
            else:
                raise ConnectionError("Can't establish AWS S3 connection")

    def _upload_data(self):
        with open(self._filename, "rb") as f:
            self.bucket.upload_file(self._filename, self._filename)

    @property
    def bucket(self):
        session = boto3.Session(
            aws_access_key_id=self.aws_access_key_id, aws_secret_access_key=self.aws_secret_access_key
        )

        s3 = session.resource("s3")

        try:
            s3.meta.client.head_bucket(Bucket=self.bucket_name)

        except botocore.exceptions.ClientError:
            raise ValueError("Bucket doesn't exist.")

        return s3.Bucket(self.bucket_name)
