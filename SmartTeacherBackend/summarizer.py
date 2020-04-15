from gensim.summarization.summarizer import summarize
import boto3

__author__ = "Sumanth Reddy Muni, Priyadarshini Murugan"
__copyright__ = "Copyright 2020, Smart Teacher"
__version__ = "1.0.0"
__maintainer__ = "Sumanth Reddy Muni, Priyadarshini Murugan"
__email__ = "sumanthreddymindia@gmail.com"

text_folder_path = 'Text_Files/'

def get_summary(text):
    num_of_words = len(text.split())
    print('[info] total size: ' + str(num_of_words))
 
    if num_of_words >= 5000:
        return (summarize(text,0.05))
    elif num_of_words >= 3000 and num_of_words < 5000 :
        return (summarize(text,0.1))
    elif num_of_words >= 1000 and num_of_words < 3000 :
        return (summarize(text,0.2))
    else:
        return (summarize(text,0.3))


def get_summary_with_ratio(text, ratio):
 
    return (summarize(text,0.5, split=True))

def get_short_summary(video_id):
    # uses mphasis AWS marketplace model to get short summary in 3 lines

    client = boto3.client('sagemaker-runtime')
    text_file_path = text_folder_path+video_id+'.txt'

    f = open(text_file_path, mode='r')
    data = f.read()
    data = ' '.join(data.split()[:512])

    response = client.invoke_endpoint(
        # add your AWS sagemaker endpoint below
        EndpointName='sample-endpoint-DFDE1C3C-XXXX-XXXX-XXXX-XXXX6C77XXXX-1',
        Body=data,
        ContentType='text/plain',
        Accept='text/plain'
    )

    return response['Body'].read().decode("utf-8").split('\n',1)[0]
