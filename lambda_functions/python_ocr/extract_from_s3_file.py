# This python code goes on the cloud
import json
import boto3
import re


def lambda_handler(event, context):

    filePath= event;
    # filePath="67491.png"
    
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
    
    details = {
        'name':'',
        'pan':'',
        'dob':''
    }
    name_flag = 0

    # Print detected text
    for item in response["Blocks"]:
        if item["BlockType"] == "LINE":
            if item["Text"].isupper() and not bool(re.search(r'\d', item["Text"])) and (item["Text"] not in ["","INCOME TAX DEPARTMENT","GOVT. OF INDIA","HRT"]) and name_flag==0:
                details['name'] =item["Text"]
                name_flag=1
    
            elif re.findall("[A-Z]{5}[0-9]{4}[A-Z]{1}",item["Text"]):
                details['pan'] =item["Text"]
                
            elif re.findall('\d{2}\/\d{2}\/\d{4}',item["Text"]) :
                details['dob'] = item["Text"]
                
    return {
        "statusCode":200,
        "body":details
    }