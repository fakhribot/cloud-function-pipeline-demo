# **Automasi Pipeline Data (GCS ke BigQuery)**

## **Langkah 1: Persiapan BigQuery**

Kita butuh dataset dan tabel kosong (atau biarkan Cloud Function yang membuat tabel, tapi lebih aman buat dataset dulu).

1. **Buat Dataset**  
   ```
   bq --location=asia-southeast2 mk -d demo_dataset
   ```

## **Langkah 2: Deploy Cloud Function**

Fungsi ini akan "mendengarkan" (listen) setiap kali ada file baru masuk ke bucket yang kita buat sebelumnya.

1. Pastikan Anda berada di luar folder function\_source (sejajar).  
2. Jalankan perintah deploy:    
   ```
   gcloud functions deploy gcs-to-bigquery-loader2 \
    --source ./function_source \
    --runtime python311 \
    --no-gen2 \
    --trigger-resource $BUCKET_NAME \
    --trigger-event google.storage.object.finalize \
    --region asia-southeast2 \
    --set-env-vars DATASET_ID=demo_dataset,TABLE_ID=sales_data \
    --entry-point load_gcs_to_bigquery
   ```


## **Langkah 3: Setup IAM (Penting\!)**

Cloud Function (Gen 1) berjalan menggunakan App Engine Default Service Account. Akun ini butuh izin untuk menulis data (Data Editor), menjalankan proses upload (Job User), dan membaca file dari bucket (Storage Viewer).

1. Set Variable Service Account
Secara default, Cloud Functions Gen 1 menggunakan App Engine default service account.

```
export PROJECT_ID=$(gcloud config get-value project)
export SERVICE_ACCOUNT="${PROJECT_ID}@appspot.gserviceaccount.com"
```

2. Berikan Role BigQuery & Storage (Eksekusi 3 Perintah Ini)
Tanpa roles/bigquery.jobUser, error jobs.create. Tanpa roles/storage.objectViewer, error Access Denied: File gs://....

```
# 1. Izin untuk mengedit data BigQuery (Insert rows/Create Tables)
gcloud projects add-iam-policy-binding $PROJECT_ID \
    --member="serviceAccount:${SERVICE_ACCOUNT}" \
    --role="roles/bigquery.dataEditor"

# 2. Izin untuk menjalankan Job BigQuery (Load Job)
gcloud projects add-iam-policy-binding $PROJECT_ID \
    --member="serviceAccount:${SERVICE_ACCOUNT}" \
    --role="roles/bigquery.jobUser"

# 3. Izin untuk membaca file dari GCS
gcloud projects add-iam-policy-binding $PROJECT_ID \
    --member="serviceAccount:${SERVICE_ACCOUNT}" \
    --role="roles/storage.objectViewer"
```


## **Langkah 4: Demo Time\!**

1. Siapkan file CSV dummy sederhana di komputer Anda, misal transaksi.csv:

```csv  
   id,product,amount,city  
   1,Laptop,15000000,Jakarta  
   2,Mouse,200000,Bandung  
   3,Monitor,3000000,Surabaya
```

2. Buka Web App dan Upload file CSV tersebut.  
3. Buka **Cloud Console > BigQuery**.  
4. Cek dataset demo_dataset, buka tabel sales\_data.  
5. Klik **Preview**. Data sudah masuk!
