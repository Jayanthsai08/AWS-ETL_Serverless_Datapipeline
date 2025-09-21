# AWS Serverless ETL Pipeline with S3, Lambda, Glue, and Athena

This project demonstrates a serverless ETL pipeline on AWS that processes nested JSON order data from S3, flattens and converts it to Parquet, catalogs with Glue Crawler, and enables querying with Athena.

## Architecture

- **AWS S3:** Store raw JSON files and processed Parquet files.
- **AWS Lambda:** Triggered by S3 uploads, flattens JSON, writes Parquet to S3, triggers Glue Crawler.
- **AWS Glue Crawler:** Crawls Parquet files and updates Data Catalog.
- **Amazon Athena:** Allows SQL querying of the processed data.

## Prerequisites

- AWS Account and CLI or Console access
- IAM role with S3, Glue, Lambda permissions
- Python 3.8+ for Lambda

## Setup Instructions

### 1. Create S3 Bucket and Folders
- Create a bucket: e.g., `your-bucket-name`
- Create folders:
  - `orders_etl.json/` — upload JSON files here
  - `orders_parquet_datalake/` — Lambda will output Parquet here

### 2. Prepare Sample JSON Files
- Use nested JSON orders with customers and products structure

### 3. Create Lambda Function
- Runtime: Python 3.8 or newer
- Add packages: `pandas`, `pyarrow`, `boto3`
- Add a new Layer in the lambda function and add pandas
- Use the provided Lambda code to flatten JSON and convert to Parquet
- Set role with permissions for S3 read/write and Glue crawler start
- Add an S3 trigger on `orders_etl.json/` folder

### 4. Configure Glue Crawler
- Set data source to S3 path: `s3://your-bucket-name/orders_parquet_datalake/`
- Set to crawl all sub-folders
- Specify the appropriate IAM role
- Attach to a Glue database or create a new one
- Run the crawler to create/update tables

### 5. Query Data in Athena
- Open Athena Console
- Select the Glue database and crawler-created table
- Run SQL queries on flattened Parquet data

## Troubleshooting

- Ensure Lambda processes and uploads valid Parquet files
- Glue crawler must run after Parquet files arrive
- Athena returns no rows if no data or schema mismatch
- Verify file structure and role permissions

---

Customize this README according to your project’s needs and deployment practices.
