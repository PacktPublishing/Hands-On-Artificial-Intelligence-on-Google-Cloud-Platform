# Importing required Dependencies.
import sqlalchemy
from google.cloud import pubsub_v1
import pandas as pd
import json
from google.cloud import storage
from sqlalchemy.sql import text as sa_text


def validate_aip(event, context):
    """Triggered by a change to a Cloud Storage bucket.
    Args:
         event (dict): Event payload.
         context (google.cloud.functions.Context): Metadata for the event.
    """

    #Setting bucket and file name.
    bucket = event['bucket']
    file_path = event['name']

    #Code block to read file from GCS and load data in json format.
    client = storage.Client()
    bucket = client.get_bucket(bucket)
    blob = bucket.get_blob(file_path)
    contents = blob.download_as_string()
    contents = contents.decode("utf-8")
    data = json.loads(contents)

    #Reading required text field from data.
    output = data['responses'][0]['fullTextAnnotation']['text']
    output = output[:-1]

    #Code setup to convert output data from json file to the required format for loading into invoice table.
    keys = ['Company_Name:', 'Client_Name:', 'Client_Address:', 'SOW_Number:', 'Project_ID:', 'Invoice_Number:', 'Invoice_Date:',
           'Billing_Period:', 'Bank_Account_Number:', 'Bank_Name:', 'Balance_Due:', 'Developer Rate Hours Subtotal']

    other_key = "Developer Rate Hours Subtotal"

    output_list = output.split('\n')
    output_dict = {}
    other_value_list = []

    for op in output_list:
        present = False
        for key in keys:
            if key in op:
                dict_key = key.replace(':', '')
                output_dict[dict_key] = op.replace(key, '')
                present = True
        if not present:
            other_value_list.append(op)
            
    output_dict[other_key] = other_value_list

    df_invoice = pd.DataFrame.from_dict(output_dict)

    df_invoice[['Developer', 'Rate', 'Hours', 'Subtotal']] = df_invoice['Developer Rate Hours Subtotal'].str.split(expand=True)

    df_invoice = df_invoice.drop(columns=['Developer Rate Hours Subtotal'])

    #Establishing connection with Cloud SQL.
    db_con = sqlalchemy.create_engine(
        'mysql+pymysql://root:aip-auto$@/aip?unix_socket=/cloudsql/vsmart-iiot-223813:us-central1:aip-auto'
    )

    #Loading data into Cloud SQL, invoice table.
    db_con.execute(sa_text('truncate table invoice'))
    df_invoice.to_sql('invoice',db_con, if_exists='append',index=False)

    #Reading data from timesheet table.
    df_timesheet = pd.read_sql(f'SELECT * FROM timesheet', con=db_con)
    joined_df = pd.merge(df_invoice, df_timesheet, on=['Company_Name','SOW_Number','Project_ID','Invoice_Number','Invoice_Date','Developer'])

    #Matching data of both tables.
    matched = []
    
    for index, row in joined_df.iterrows():
        
        if row['Rate_x'] == row['Rate_y'] and row['Hours_x'] == row['Hours_y'] and row['Bank_Account_Number_x'] == row['Bank_Account_Number_y']:
            
            matched.append(True)
            
        else:
            
            matched.append(False)

    #Pushing successful message into Pub/Sub.
    if False not in matched:
        data = f"Invoice Matched"
        publisher = pubsub_v1.PublisherClient()
        topic_path = publisher.topic_path('vsmart-iiot-223813', 'aip')
        bdata = data.encode("utf-8")
        future = publisher.publish(topic_path, data=bdata)
    
