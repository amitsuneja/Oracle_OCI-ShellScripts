# importing libraries
# from oci.config import validate_config

import os
import oci
import io
from oci.config import from_file

data_dir = "D:\\DataScienceAndStats\\artificialintelligence\\CS223A"
files_to_process = [file for file in os.listdir(data_dir) if file.endswith('txt')]
bucket_name = "Sales_Data"

# this is to configure the oci configuration file
my_config = from_file(file_location="C:\\Users\\amits\\Desktop\\Oracle_Cloud\\config_file_oci.txt")
print(my_config)

# Test Configuration file of oci
# print(validate_config(my_config))

"""
Create object storage client and get its namespace
"""
object_storage_client = oci.object_storage.ObjectStorageClient(my_config)
namespace = object_storage_client.get_namespace().data

"""
Create a bucket if it does not exist

"""
try:
	create_bucket_response = object_storage_client.create_bucket(namespace,
		oci.object_storage.models.CreateBucketDetails(name=bucket_name, compartment_id=my_config['tenancy']))

except Exception as e:
	print("Please read below messages")
	print(e.message)
	print(e.status)

"""
Uploading the files

"""
print("uploading files to bucket")
for upload_file in files_to_process:
	print('Uploading file {}'.format(upload_file))
	object_storage_client.put_object(namespace, bucket_name, upload_file, io.open(os.path.join(data_dir, upload_file),
																				'rb'))

"""
Listing a files in the Bucket
"""

object_list = object_storage_client.list_objects(namespace, bucket_name)
for o in object_list.data.objects:
	print(o.name)

"""
Downloading files from Bucket
"""
object_name = "1.txt"
destination_dir = 'D:\\DataScienceAndStats\\artificialintelligence\\CS223A\\moved_files'.format(object_name)
get_obj = object_storage_client.get_object(namespace, bucket_name, object_name)
with open(os.path.join(destination_dir, object_name), 'wb') as f:
	for chunk in get_obj.data.raw.stream(1024 * 1024, decode_content=False):
		f.write(chunk)


"""
Deleting object from Bucket and the deleting Bucket itself
"""
for o in object_list.data.objects:
	print('Deleting object {}'.format(o.name))
	object_storage_client.delete_object(namespace, bucket_name, o.name)
response = object_storage_client.delete_bucket(namespace, bucket_name)
