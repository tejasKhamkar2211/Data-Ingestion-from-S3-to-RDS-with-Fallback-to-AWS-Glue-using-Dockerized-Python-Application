# Data-Ingestion-from-S3-to-RDS-with-Fallback-to-AWS-Glue-using-Dockerized-Python-Application

1. Python Script Development

create a RDS & connect with ec2 instance

<img width="960" height="540" alt="Image" src="https://github.com/user-attachments/assets/d637e611-0591-4449-9837-d6f4c776eba0" />

Create a s3 bucket 

<img width="960" height="540" alt="Image" src="https://github.com/user-attachments/assets/f95320ae-6441-4a03-8466-b84ba27bf7c2" />

Creating a table in AWS Glue Data Catalog

<img width="960" height="540" alt="Image" src="https://github.com/user-attachments/assets/6b671616-eea4-421b-9e4e-fe22c4af939a" />

Registering the dataset location in S3

<img width="960" height="540" alt="Image" src="https://github.com/user-attachments/assets/8c6f49f7-cdb1-434d-b367-a7ebd5e2c5ae" />

2. Dockerfile Creation

Build a Dockerfile that:
o Uses a Python 3.9+ base image
o Installs all necessary libraries (boto3, pandas, sqlalchemy, pymysql)
o Copies the Python script into the container
o Runs the script on container startup

Require files
i. main.py
ii.  Dockerfile
iii. Requirements.txt

3. Image Build and Container Run:
 Build the Docker image:
 Run the container using environment variables for AWS credentials

<img width="960" height="540" alt="Image" src="https://github.com/user-attachments/assets/9be97983-2e33-4088-a53c-6ead4037de28" />

4. Configuration Parameters (Replace with actual values):
 S3 Bucket Name
 CSV File Key
 RDS DB Endpoint, Username, Password, DB Name, Table Name
 Glue Database Name, Table Name, and S3 Location

docker run  \
-e AWS_ACCESS_KEY_ID=---------------------- \
-e AWS_SECRET_ACCESS_KEY=----------------------------- \
-e AWS_DEFAULT_REGION=us-east-1 \
-e S3_BUCKET=python-project3 \
-e CSV_KEY=students.csv \
-e RDS_HOST=database-forbackup-project-1.ccv2yuoumhxt.us-east-1.rds.amazonaws.com \
-e RDS_PORT=3306 \
-e RDS_USER=root \
-e RDS_PASSWORD=Satara123 \
-e RDS_DB=python_project \
-e RDS_TABLE=students \
-e GLUE_DB=student_glue_db \
-e GLUE_TABLE=studentstudents_csv \
-e GLUE_S3_PATH=s3://python-project3/ \
s3-to-rds-fallback


5. 
