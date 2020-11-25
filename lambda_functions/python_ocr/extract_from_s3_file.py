# This python code goes on the cloud
import json
import boto3
import re

def lambda_handler(event, context):

    filePath= event;
    bad_chars = [';', ':', '!', "*", ']', "[" ,'"', "{" , "}" , "'",","]
    
    s3BucketName = "react-info-extractor-images"
    documentName = filePath
    textract = boto3.client('textract')
    
    # Call Amazon Textract
    response = textract.detect_document_text(
        Document={
            'S3Object': {
                'Bucket': s3BucketName,
                'Name': documentName
            }
        })
    
    details = []
    name_flag,pan_flag,dob_flag = 0,0,0

    # Print detected text
    for item in response["Blocks"]:
        if item["BlockType"] == "LINE":
    
            if "Name" in item["Text"] and name_flag==0:
                name_flag=1
                continue
            elif "Permanent Account" in item["Text"] and pan_flag==0:
                pan_flag=1
                continue
            elif "Date of Birth" in item["Text"] and dob_flag==0:
                dob_flag=1
                continue
    
            if pan_flag == 1:
                details.append(item["Text"])
                pan_flag = 2
            if name_flag == 1:
                details.append(item["Text"])
                name_flag = 2
            if dob_flag == 1:
                details.append(item["Text"])
                dob_flag = 2
    
    return {
        "statusCode":200,
        "body":details
    }