# coding: utf-8


from __future__ import print_function
import os
import oci
from oci.object_storage import UploadManager
from oci.object_storage.models import CreateBucketDetails
from oci.object_storage.transfer.constants import MEBIBYTE
from oci.config import from_file


def progress_callback(bytes_uploaded):
    """
    this function is simple to print message on screen
    :param bytes_uploaded: int
    :return: None
    """
    print("{} additional bytes uploaded".format(bytes_uploaded))

"""
config location defined 
"""
config = from_file(file_location="C:\\Users\\amits\\Desktop\\Oracle_Cloud\\config_file_oci.txt")
compartment_id = config["tenancy"]

"""
Create object storage client and get its namespace
"""
object_storage_client = oci.object_storage.ObjectStorageClient(config)
namespace = object_storage_client.get_namespace().data

"""
define bucket_name and object_name variables
"""
bucket_name = "python-sdk-example-bucket"
object_name = "python-sdk-example-object"

"""
creating a bucket
"""
print("Creating a new bucket {!r} in compartment {!r}".format(bucket_name, compartment_id))
request = CreateBucketDetails()
request.compartment_id = compartment_id
request.name = bucket_name
bucket = object_storage_client.create_bucket(namespace, request)

"""
creating a data file to be uploaded
"""
# create example file to upload
filename = 'multipart_object_content.txt'
file_size_in_mebibytes = 10
sample_content = b'a'
with open(filename, 'wb') as f:
    while f.tell() < MEBIBYTE * file_size_in_mebibytes:
        f.write(sample_content * MEBIBYTE)

"""
uploading file.
"""
print("Uploading new object {!r}".format(object_name))
# upload manager will automatically use multipart uploads if the part size is less than the file size
part_size = 2 * MEBIBYTE  # part size (in bytes)
upload_manager = UploadManager(object_storage_client, allow_parallel_uploads=True, parallel_process_count=3)
response = upload_manager.upload_file(
    namespace, bucket_name, object_name, filename, part_size=part_size, progress_callback=progress_callback)

# To force single part uploads, set "allow_multipart_uploads=False" when creating the UploadManager.
# upload_manager = UploadManager(object_storage_client, allow_multipart_uploads=False)
# response = upload_manager.upload_file(
#    namespace, bucket_name, object_name, filename, part_size=part_size, progress_callback=progress_callback)

# remove file to clean up
os.remove(filename)
