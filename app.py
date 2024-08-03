import boto3
import json
import botocore.client
import botocore.config
import response

def generate_blog(topic:str) -> str:
   
    prompt = """ <s>[INST]Human: Write a 200 words blog on the topic {topic}
    Assistant:[/INST] """
    
    body = {
        'prompt' : prompt,
        'mag_gen_len' : 512,
        'temperature' : 0.5,
        'top_p' : 0.9
    }
    
    try:
        bedrock = boto3.client('bedrock-runtime',
                                region_name = 'ap-south-1',
                                config = botocore.config.Config(read_timeout = 300, retries = {'max_attempts':3}))
        bedrock.invoke(body = json.dumps(body),
                       modelID = 'meta.llama3-8b-instruct-v1:0')
        
        response_content = response.get('body').read()
        response_data = json.loads(response_content)
        print(response_data)
        
        blog_details = response_data['generation']
        return blog_details
    except Exception as e:
        print(f'Error generating the blog, {e}')
        return('')
    
# continue at 24:50
# https://www.youtube.com/watch?v=3OP39y4dO_Y

        