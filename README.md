# **Panduan Demo Lanjutan: Automasi Pipeline Data (GCS ke BigQuery)**

## **Langkah 1: Persiapan BigQuery**

Kita butuh dataset dan tabel kosong (atau biarkan Cloud Function yang membuat tabel, tapi lebih aman buat dataset dulu).

1. **Buat Dataset**  
   bq \--location=asia-southeast2 mk \-d demo\_dataset

## **Langkah 2: Deploy Cloud Function**

Fungsi ini akan "mendengarkan" (listen) setiap kali ada file baru masuk ke bucket yang kita buat sebelumnya.

1. Pastikan Anda berada di luar folder function\_source (sejajar).  
2. Jalankan perintah deploy:  
   *(Ganti \[NAMA\_BUCKET\_ANDA\] dengan nama bucket dari demo sebelumnya)*  
   gcloud functions deploy gcs-to-bigquery-loader \\  
       \--source ./function\_source \\  
       \--runtime python39 \\  
       \--trigger-resource \[NAMA\_BUCKET\_ANDA\] \\  
       \--trigger-event google.storage.object.finalize \\  
       \--region asia-southeast2 \\  
       \--set-env-vars DATASET\_ID=demo\_dataset,TABLE\_ID=sales\_data \\  
       \--entry-point load\_gcs\_to\_bigquery

   **Penjelasan untuk Engineer & Analyst:**  
   * \--trigger-event google.storage.object.finalize: Ini adalah "Event". Artinya, jalankan kode TEPAT saat upload file selesai.

## **Langkah 3: Setup IAM (Penting\!)**

Cloud Function butuh izin untuk menulis ke BigQuery.

1. Dapatkan email service account Cloud Function (biasanya App Engine default service account):  
   gcloud projects describe $GOOGLE\_CLOUD\_PROJECT \--format="value(projectNumber)"

   Emailnya: \[PROJECT\_NUMBER\]@cloudbuild.gserviceaccount.com atau \[PROJECT\_ID\]@appspot.gserviceaccount.com. Cek di UI Cloud Functions \> Details untuk pastinya.  
2. Berikan role BigQuery Data Editor dan BigQuery Job User.

## **Langkah 4: Demo Time\!**

1. Siapkan file CSV dummy sederhana di komputer Anda, misal transaksi.csv:

```csv  
   id,product,amount,city  
   1,Laptop,15000000,Jakarta  
   2,Mouse,200000,Bandung  
   3,Monitor,3000000,Surabaya
```

2. Buka Web App (Demo 1\) dan Upload file CSV tersebut.  
3. Buka **Cloud Console \> BigQuery**.  
4. Cek dataset demo\_dataset, buka tabel sales\_data.  
5. Klik **Preview**. Data sudah masuk\!
