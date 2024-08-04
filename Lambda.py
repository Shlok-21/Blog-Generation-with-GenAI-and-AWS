import boto3
import json
import botocore.client
import botocore.config
from datetime import datetime

def generate_blog(topic:str) -> str:
    prompt = f""" <s>[INST]Human: Write a 200 words blog on the topic {topic}
    Assistant:[/INST] """
    body = {
        'prompt' : prompt,
        'max_gen_len' : 512,
        'temperature' : 0.5,
        'top_p' : 0.9
    }
    
    try:
        bedrock = boto3.client('bedrock-runtime',
                                region_name = 'ap-south-1',
                                config = botocore.config.Config(read_timeout = 300, retries = {'max_attempts':3}))
        response = bedrock.invoke_model(body = json.dumps(body),
                       modelId = 'meta.llama3-8b-instruct-v1:0')
        
        response_content = response.get('body').read()
        response_data = json.loads(response_content)
        print(response_data)
        
        blog_details = response_data['generation']
        return blog_details
    
    except Exception as e:
        print(f'Error generating the blog, {e}')
        return('')

def save_blog_details_in_S3(s3_key, s3_bucket, blog):
    s3 = boto3.client('s3')
    try:
        s3.put_object(Bucket = s3_bucket, Key = s3_key, Body = blog)
        print(f'Blog saved to S3')
    except Exception as e:
        print(f'Error occured while saving Blog to S3 {e}')    


def lambda_handler(event, context):
    event = json.loads(event['body'])
    blog_topic = event['blog_topic']
    blog = generate_blog(topic = blog_topic)
    
    # Save the generated blog in S3 bucket
    if blog:
        current_time = datetime.now().strftime('%H%M%S')
        s3_key = f'blog_output/{blog_topic}-{current_time}.txt'
        s3_bucket_name = 'shlokbloggenerator' #s3 bucket name must be unique and without '_'
        save_blog_details_in_S3(s3_key=s3_key, s3_bucket= s3_bucket_name, blog = blog)
    else:
        print(f'No blog was generated.')
        
    return {
        'statusCode':200,
        'body':json.dumps('Blog generated successfully.')
    }