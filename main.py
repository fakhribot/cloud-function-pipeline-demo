import os
from google.cloud import bigquery

def load_gcs_to_bigquery(event, context):
    """Triggered by a change to a Cloud Storage bucket.
    Args:
         event (dict): Event payload.
         context (google.cloud.functions.Context): Metadata for the event.
    """
    
    # Konfigurasi dari Environment Variable
    dataset_id = os.environ.get('DATASET_ID') # Contoh: 'demo_dataset'
    table_id = os.environ.get('TABLE_ID')     # Contoh: 'sales_data'
    
    file_name = event['name']
    bucket_name = event['bucket']

    # Hanya proses file CSV
    if not file_name.endswith('.csv'):
        print(f"File {file_name} bukan CSV, skip.")
        return

    print(f"Processing file: {file_name} from bucket: {bucket_name}")

    client = bigquery.Client()
    table_ref = client.dataset(dataset_id).table(table_id)

    job_config = bigquery.LoadJobConfig()
    job_config.source_format = bigquery.SourceFormat.CSV
    job_config.skip_leading_rows = 1 # Skip header row
    job_config.autodetect = True     # Otomatis deteksi tipe data (Int/String)

    uri = f"gs://{bucket_name}/{file_name}"

    try:
        load_job = client.load_table_from_uri(
            uri, table_ref, job_config=job_config
        )
        
        print(f"Starting job {load_job.job_id}")
        load_job.result()  # Menunggu job selesai
        
        print(f"Job selesai. {load_job.output_rows} baris telah dimuat ke {dataset_id}.{table_id}.")
        
    except Exception as e:
        print(f"Error loading data: {e}")