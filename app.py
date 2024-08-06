from flask import Flask, render_template, request, url_for, redirect, jsonify
import requests
import boto3

s3 = boto3.client('s3')
bucket_name = 'shlokbloggenerator'
prefix = 'blog_output/'

app = Flask(__name__)

@app.route('/')
def main():
    return render_template('index.html')

@app.route('/blog', methods = ['POST'])
def generate_blog():
    blog_topic = request.form['blogTitle']
    blog_content = f'Generated content for blog title {blog_topic}'
    
    # URL of the AWS Lambda function
    lambda_url = 'https://j7d10659ya.execute-api.ap-south-1.amazonaws.com/dev/blog-generation'

    # The payload to send to the Lambda function
    payload = {
        "blog_topic": blog_topic,
        }

    # hit the API Gateway
    
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
    
    
    # add blog display here
    return render_template('result.html', blog_title=blog_topic, blog_content=blog_topic)


    # try:
    #     # Sending POST request to the Lambda function
    #     response = requests.post(lambda_url, json=payload)

    #     # Check if the request was successful
    #     if response.status_code == 200:
    #         # Process the response from the Lambda function
    #         response_data = response.json()
    #         return jsonify(response_data)
    #     else:
    #         return jsonify({'error': 'Failed to invoke Lambda function', 'status_code': response.status_code})
    # except Exception as e:
    #     return jsonify({'error': str(e)})



if __name__ == '__main__':
    app.run(debug=True)