import json
import boto3
import pandas as pd
import io
from datetime import datetime

def flatten(data):
    orders_data = []
    for order in data:
        for product in order.get('products', []):
            row_orders = {
                "order_id": order.get("order_id"),
                "order_date": order.get("order_date"),
                "total_amount": order.get("total_amount"),
                "customer_id": order["customer"].get("customer_id"),
                "customer_name": order["customer"].get("name"),
                "email": order["customer"].get("email"),
                "address": order["customer"].get("address"),
                "product_id": product.get("product_id"),
                "product_name": product.get("name"),
                "category": product.get("category"),
                "price": product.get("price"),
                "quantity": product.get("quantity")
            }
            orders_data.append(row_orders)
    return pd.DataFrame(orders_data)

def lambda_handler(event, context):
    try:
        bucket_name = event['Records'][0]['s3']['bucket']['name']
        key = event['Records'][0]['s3']['object']['key']

        print(f"Reading file {key} from bucket {bucket_name}...")

        s3 = boto3.client('s3')
        response = s3.get_object(Bucket=bucket_name, Key=key)
        file_content = response['Body'].read().decode('utf-8')
        data = json.loads(file_content)

        df = flatten(data)
        print("Flattened Data Shape:", df.shape)
        print(df.head())

        if df.empty:
            print("DataFrame is empty. Exiting Lambda.")
            return {'statusCode': 200, 'body': 'No data to process.'}

        parquet_buffer = io.BytesIO()
        print("Converting DataFrame to Parquet...")
        df.to_parquet(parquet_buffer, index=False, engine='pyarrow')
        parquet_buffer.seek(0)  
        
        key_staging = f'orders_parquet_datalake/orders_etl_{datetime.now().strftime("%Y%m%d_%H%M%S")}.parquet'
        s3.put_object(Bucket=bucket_name, Key=key_staging, Body=parquet_buffer.getvalue())
        print(f"✅ Parquet file uploaded to {key_staging}")

        # Start Glue Crawler BEFORE return
        glue = boto3.client('glue')
        glue.start_crawler(Name='etl_pipeline_crawler')
        print("✅ Glue crawler started.")

        return {'statusCode': 200, 'body': 'File processed and crawler started successfully!'}

    except Exception as e:
        print(f"Error: {str(e)}")
        raise e
