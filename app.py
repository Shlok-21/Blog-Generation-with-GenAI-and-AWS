from flask import Flask, render_template, request, url_for, redirect, jsonify
import requests
import os
import boto3

s3 = boto3.client(
    's3',
    aws_access_key_id='AWS_ACCESS_KEY',
    aws_secret_access_key='AWS_SECRET_ACCESS_KEY',
    region_name='ap-south-1'
)

bucket_name = 'shlokbloggenerator'
prefix = 'blog_output/'

app = Flask(__name__)

@app.route('/')
def main():
    return render_template('index.html')

@app.route('/blog', methods = ['POST'])
def generate_blog():
    blog_topic = request.form['blogTitle']
    
    # URL of the AWS Lambda function
    lambda_url = 'https://j7d10659ya.execute-api.ap-south-1.amazonaws.com/dev/blog-generation'

    # The payload to send to the Lambda function
    payload = {
        "blog_topic": blog_topic,
        }
    
    try:
        response = requests.post(lambda_url, json = payload)
        if response.status_code==200:
            response_data = response.json()
            response_status = jsonify(response_data)
            print(response_status)
        else:
            print(jsonify({'error': 'Failed to invoke Lambda function', 'status_code': response.status_code}))
    except Exception as e:
        return jsonify({'error': str(e)})    
    
    try:
        response = s3.list_objects_v2(Bucket=bucket_name, Prefix=prefix)
        if 'Contents' in response:
            # Find the latest file based on LastModified timestamp
            latest_file = max(response['Contents'], key=lambda obj: obj['LastModified'])['Key']
            print(f"Latest file found: {latest_file}")
            
            # Retrieve the object
            obj = s3.get_object(Bucket=bucket_name, Key=latest_file)
            
            # Read the content of the file
            file_content = obj['Body'].read().decode('utf-8')
            
            # Store the content in a variable
            blog_content = file_content
        else:
            blog_content = 'No files found in the bucket.'
    except Exception as e:
        return jsonify({'error': str(e)})
    
    # Display the blog content in the result.html template
    return render_template('result.html', blog_title=blog_topic, blog_content=blog_content)



if __name__ == '__main__':
    app.run(debug=True)