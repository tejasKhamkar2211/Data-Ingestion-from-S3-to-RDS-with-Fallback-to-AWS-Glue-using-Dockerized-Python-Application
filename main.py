import os
import boto3
import pandas as pd
from sqlalchemy import create_engine
import pymysql
from botocore.exceptions import ClientError

def load_csv_from_s3():
    s3 = boto3.client('s3')
    bucket = os.environ['S3_BUCKET']
    key = os.environ['CSV_KEY']
    obj = s3.get_object(Bucket=bucket, Key=key)
    return pd.read_csv(obj['Body'])

def insert_into_rds(df):
    try:
        engine = create_engine(
            f"mysql+pymysql://{os.environ['RDS_USER']}:{os.environ['RDS_PASSWORD']}@{os.environ['RDS_HOST']}:{os.environ['RDS_PORT']}/{os.environ['RDS_DB']}"
        )
        df.to_sql(os.environ['RDS_TABLE'], con=engine, if_exists='replace', index=False)
        print("✅ Data inserted into RDS successfully.")
    except Exception as e:
        print("❌ RDS insert failed, triggering Glue fallback...\n", e)
        fallback_to_glue(df)

def fallback_to_glue(df):
    glue = boto3.client('glue')
    db_name = os.environ['GLUE_DB']
    table_name = os.environ['GLUE_TABLE']
    s3_path = os.environ['GLUE_S3_PATH']

    # Step 1: Create database if it doesn't exist
    try:
        glue.create_database(DatabaseInput={'Name': db_name})
        print(f"✅ Glue database '{db_name}' created.")
    except glue.exceptions.AlreadyExistsException:
        print(f"ℹ️ Glue database '{db_name}' already exists.")

    # Step 2: Build schema from DataFrame
    columns = []
    for col in df.columns:
        dtype = df[col].dtype
        if pd.api.types.is_integer_dtype(dtype):
            glue_type = 'int'
        elif pd.api.types.is_float_dtype(dtype):
            glue_type = 'double'
        else:
            glue_type = 'string'
        columns.append({'Name': col, 'Type': glue_type})

    # Step 3: Create table
    try:
        glue.create_table(
            DatabaseName=db_name,
            TableInput={
                'Name': table_name,
                'StorageDescriptor': {
                    'Columns': columns,
                    'Location': s3_path,
                    'InputFormat': 'org.apache.hadoop.mapred.TextInputFormat',
                    'OutputFormat': 'org.apache.hadoop.hive.ql.io.HiveIgnoreKeyTextOutputFormat',
                    'SerdeInfo': {
                        'SerializationLibrary': 'org.apache.hadoop.hive.serde2.lazy.LazySimpleSerDe',
                        'Parameters': {'field.delim': ','}
                    }
                },
                'TableType': 'EXTERNAL_TABLE',
            }
        )
        print(f"📚 Glue table '{table_name}' created successfully in database '{db_name}'.")
    except glue.exceptions.AlreadyExistsException:
        print(f"ℹ️ Glue table '{table_name}' already exists.")

if __name__ == "__main__":
    df = load_csv_from_s3()
    insert_into_rds(df)
