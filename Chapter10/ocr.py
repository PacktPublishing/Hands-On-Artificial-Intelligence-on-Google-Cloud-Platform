def async_detect_document(source_path_gcs, destination_path_gcs):
   
    import re
    from google.cloud import vision
    from google.cloud import storage
    from google.protobuf import json_format
    
    mime_type = 'application/pdf'

    # PDF Pages grouping - In our example, we are going to 
    # have single page invoice and hence value is set to 1
    batch_size = 1

    client = vision.ImageAnnotatorClient()

    feature = vision.types.Feature(
        type=vision.enums.Feature.Type.DOCUMENT_TEXT_DETECTION)

    gcs_source = vision.types.GcsSource(uri=source_path_gcs)
    input_config = vision.types.InputConfig(
        gcs_source=gcs_source, mime_type=mime_type)

    output_location = vision.types.GcsDestination(uri=destination_path_gcs)
    output_config = vision.types.OutputConfig(
        output_location=output_location, batch_size=batch_size)

    async_request = vision.types.AsyncAnnotateFileRequest(
        features=[feature], input_config=input_config,
        output_config=output_config)

    operation = client.async_batch_annotate_files(
        requests=[async_request])

    # Setting a timeout value in order to wait for the asynchronous
    # call to return
    operation.result(timeout=180)

    # Once the request has completed and the output has been
    # written to GCS, we can list all the output files.
    storage_client = storage.Client()

    match = re.match(r'gs://([^/]+)/(.+)', destination_path_gcs)
    bucket_name = match.group(1)
    prefix = match.group(2)

    bucket = storage_client.get_bucket(bucket_name)

    # List objects with the given prefix.
    output_files_list = list(bucket.list_blobs(prefix=prefix))
    print('Output files:')
    for output_file in output_files_list:
        print(output_file.name)
