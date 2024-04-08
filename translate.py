""" Translate text between two languages with Amazon Translate. """

import boto3

translation_client = boto3.client(service_name="translate", region_name="us-east-1", use_ssl=True)


def translate_text(input_text, source_language, target_language):
    result = translation_client.translate_text(Text=input_text, SourceLanguageCode=source_language,
                                               TargetLanguageCode=target_language)
    
    return result.get("TranslatedText")
