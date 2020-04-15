from __future__ import print_function
import time
import boto3

__author__ = "Sumanth Reddy Muni, Priyadarshini Murugan"
__copyright__ = "Copyright 2020, Smart Teacher"
__version__ = "1.0.0"
__maintainer__ = "Sumanth Reddy Muni, Priyadarshini Murugan"
__email__ = "sumanthreddymindia@gmail.com"

transcribe = boto3.client('transcribe')

def speech_to_text(job_name,job_uri):

    transcribe.start_transcription_job(
        TranscriptionJobName=job_name,
        Media={'MediaFileUri': job_uri},
        MediaFormat='wav',
        LanguageCode='en-US'
    )

    while True:
        status = transcribe.get_transcription_job(TranscriptionJobName=job_name)
        if status['TranscriptionJob']['TranscriptionJobStatus'] in ['COMPLETED', 'FAILED']:
            break
        print("Not ready yet...")
        time.sleep(5)

    print(status)
    # if status['TranscriptionJob']['TranscriptionJobStatus']

speech_to_text("job_name_zume", "https://addnv.s3.amazonaws.com/videos/fossils.wav")
