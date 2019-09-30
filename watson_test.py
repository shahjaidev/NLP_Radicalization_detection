import json
from ibm_watson import NaturalLanguageUnderstandingV1
from ibm_watson.natural_language_understanding_v1 \
    import Features, EntitiesOptions, KeywordsOptions, EmotionOptions

natural_language_understanding = NaturalLanguageUnderstandingV1(
    version='2019-07-12',
    iam_apikey='oRW-WiI73HQMQxq0mVZnPJzN3UFwX4-9oD-XpjLjqUNi',
    url='https://gateway-wdc.watsonplatform.net/natural-language-understanding/api')


response = natural_language_understanding.analyze(
    text="Trump is a stupid fucker",
    features=Features(
        EmotionOptions(document=True)) 
    ).get_result()

print(json.dumps(response, indent=2))



"""
response = natural_language_understanding.analyze(
    text='IBM is an American multinational technology company '
    'headquartered in Armonk, New York, United States, '
    'with operations in over 170 countries.',
    features=Features(
        entities=EntitiesOptions(emotion=True, sentiment=True, limit=2),
        keywords=KeywordsOptions(emotion=True, sentiment=True,
                                 limit=2))).get_result()

print(json.dumps(response, indent=2))




"""