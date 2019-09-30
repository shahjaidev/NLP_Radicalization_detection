#Comparison


from deepsegment import DeepSegment
from get_emotions import *
segmenter = DeepSegment('en')

 
import json
from ibm_watson import ToneAnalyzerV3

tone_analyzer = ToneAnalyzerV3(
    version='2017-09-21',
    iam_apikey='0DWwlEM6RsPb0nnawbE3Rzbpmrg9OOLcLA5xJOel17wN',
    url='https://gateway-syd.watsonplatform.net/tone-analyzer/api'
)

#text_A = 'Team, I know that times are tough! Product sales have been disappointing for the past three quarters. We have a competitive product, but we need to do a better job of selling it!'


"""
tone_analysis_A = tone_analyzer.tone(
    {'text': text_A},
    content_type='application/json'
).get_result()

print("A: \n")
print(tone_analysis_A)
print("\n")
print(json.dumps(tone_analysis_A, indent=2))

"""

li_B= ['since 1990 the number of gun deaths', 'worldwide has reached six point five', 'million three quarters of gun deaths', 'occur in just 15 countries Latin America', "is home to some of the world's most", 'violent countries by murder rate El', 'Salvador Venezuela and Guatemala are the', 'top three countries for deaths caused by', 'guns per population these Latin American', 'countries are marred by corruption', 'organized crime and a dysfunctional', 'criminal justice system that further', 'fuels the problem the availability of', 'guns in the United States is another', 'concern for these countries an estimated', '200,000 guns a year that were first sold', 'in the United States are smuggled over', 'the southern border and used in violent', 'crimes in Latin America and the', 'Caribbean in the United States the', 'constitutional right to bear arms has', 'led to looser regulations and easier', 'access to firearms this contributes to', 'the 30,000 men women and children who', 'were killed with guns each year mass', 'shootings attract their headlines but in', 'fact these make up only 0.2% of gun', 'deaths 60% of gun related deaths are in', 'fact suicide', "America's suicide rate increased by 25", 'percent between 1999 and 2015 of nearly', '45,000 taking their own lives in 2015', 'alone half of these suicides were', "carried out with guns though guns aren't", 'the most common method of suicide they', 'are the most lethal other wealthy', 'countries have far lower rates of gun', 'violence in Japan if you want to own a', 'gun you must pass a written exam and a', 'shooting range test alongside a series', 'of mental health drug in criminal record', 'tests', 'it has virtually eradicated gun crime', 'after a mass shooting in 1996 Australia', 'introduced an effective buyback scheme', 'of firearms in the 20 years following', 'the bag there was an accelerated decline', 'in total gun deaths but in America the', 'House of Representatives has not voted', 'on a single measure to prevent gun', 'violence and in some states such as', 'Texas where students at public colleges', 'can now carry concealed handguns the law', 'has actually loosened easy access to', 'firearms will continue to be the main', "driver of America's gun debt"]


segmented_li= segmenter.segment(" ".join(li_B))

text_B= ". ".join(segmented_li)



tone_analysis_B = tone_analyzer.tone(
    {'text': text_B},
    content_type='application/json'
).get_result()

print("B: \n")
print(tone_analysis_B)
print("\n")
print(json.dumps(tone_analysis_B, indent=2))



#NRC Emotions

print("\n"+ "Raw NRC counts")
res_A= get_emotion_counts_with_vader(segmented_li)

print(res_A)

print("\n"+ " Softmaxed and Normalized NRC:")
print(softmaxed_normalized_emotion_counts(segmented_li,1) )



