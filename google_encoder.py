import tensorflow as tf
import tensorflow_hub as hub
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity



embed = hub.Module("jd")
# Compute a representation for each message, showing various lengths supported.
s1 = "Jun.21 -- The U.S. called off military strikes against Iran on Thursday night that were approved by President Donald Trump, according to an administration official, abandoning a move that would have dramatically escalated tensions that are already running high between the two countries. Annmarie Hordern reports on Bloomberg Daybreak: Europe."
s2 = "Jordan Peterson: The Left's new public enemy No. 1. Clinical psychologist Jordan Peterson hates what the Left loves - identity politics - and has whipped liberals into a frenzy with his new book, '12 Rules for Life.'"
s3 = "The truth about global warming. Dr. Patrick Michaels, director of the Center for the Study of Science at the Cato Institute, provides insight into the debate over climate change and the political games played to create policy."
s4= "Bongino calls on Congress to fix immigration laws. Dan Bongino said it's time for Congress to put aside politics and come up with solutions to the border crisis."
s5= "The Atlantic slave trade: What too few textbooks told you - Anthony Hazard. Slavery has occurred in many forms throughout the world, but the Atlantic slave trade -- which forcibly brought more than 10 million Africans to the Americas -- stands out for both its global scale and its lasting legacy. Anthony Hazard discusses the historical, economic and personal impact of this massive historical injustice.  "


s6= "Does Islam Have a Violent Extremism Problem? Ayaan Hirsi Ali and Manal Omar square off over Hirsi Ali’s new book ‘Heretic.’"

s7= "Town Hall Debate: Should Americans Fear Islam? Christiane Amanpour moderates a special 'This Week' town hall debate.  For more, click here: "


s8= "Piers Morgan Debates Headscarf Ban With Muslim Women | Good Morning Britain "

s9= "How to Destroy Christianity With One Easy Step... | IMPACT Whiteboard Videos"

s10= "You are a rude, terrible person' : Trump attacks CNN reporter"


messages = [s1, s2, s3,s4,s5, s6, s7, s8, s9,s10]
# Reduce logging output.
tf.logging.set_verbosity(tf.logging.ERROR)
with tf.Session() as session:
    session.run([tf.global_variables_initializer(), tf.tables_initializer()])
    message_embeddings = session.run(embed(messages))


for i, message_embedding in enumerate(np.array(message_embeddings).tolist()):
        print("Message: {}".format(messages[i]))
        print("Embedding size: {}".format(len(message_embedding)))
        message_embedding_snippet = ", ".join((str(x) for x in        message_embedding[:3]))
        print("Embedding[{},...]\n".format(message_embedding_snippet))



print("s1,s2: ")
s0_embed= message_embeddings[0].reshape(1,512) 
s1_embed= message_embeddings[1].reshape(1,512) 
print(cosine_similarity(s0_embed, s1_embed ) )

print("s2,s3: ")
s2_embed= message_embeddings[1].reshape(1,512) 
s3_embed= message_embeddings[2].reshape(1,512) 
print(cosine_similarity(s2_embed, s3_embed ) )

print("s1,s3: ")
s1_embed= message_embeddings[0].reshape(1,512) 
s3_embed= message_embeddings[2].reshape(1,512) 
print(cosine_similarity(s1_embed, s3_embed ) )

print("s1,s4: ")
s1_embed= message_embeddings[0].reshape(1,512) 
s4_embed= message_embeddings[3].reshape(1,512) 
print(cosine_similarity(s1_embed, s4_embed ) )

print("s1,s5: ")
s1_embed= message_embeddings[0].reshape(1,512) 
s5_embed= message_embeddings[4].reshape(1,512) 
print(cosine_similarity(s1_embed, s5_embed ) )

print("s6,s7: ")
s6_embed= message_embeddings[5].reshape(1,512) 
s7_embed= message_embeddings[6].reshape(1,512) 
print(cosine_similarity(s6_embed, s7_embed ) )

print("s7,s8: ")
s8_embed= message_embeddings[7].reshape(1,512) 
print(cosine_similarity(s7_embed, s8_embed ) )

print("s9,s7: ")
s9_embed= message_embeddings[8].reshape(1,512) 
print(cosine_similarity(s7_embed, s9_embed ) )


print("s6,s10:")
s10_embed= message_embeddings[9].reshape(1,512) 
print(cosine_similarity(s6_embed, s10_embed ) )

