import requests
import json
from sentence_transformers import SentenceTransformer, util
import spacy 
from collections import OrderedDict

def IdentificaAzioneFirst(sentence):
    model = SentenceTransformer('bert-base-nli-mean-tokens')
    nlp = spacy.load("en_core_web_sm")
    testo = sentence
    doc = nlp(testo)
    reference_sentences = []
    for frase in doc.sents:
        reference_sentences.append(frase.text)

    sentences_to_compare = {
    "Hello": ["Zora say hello","Greet me","Extend your greetings to me","Give me a shoutout","Say hello","Say hi","Greet","Wave hello",
    "Give your regards","Send your best wishes","Extend greetings","Offer a greeting","Acknowledge","Bid farewell","Convey your salutations",
    "Send a warm welcome","Exchange pleasantries","Wish them well","Say hey","Salute"],
    "RaiseArmRight": ["Raise your arm","Raise your right arm", "Can you please raise your right arm","Please raise your right arm","Lift your right arm","Elevate your right arm",
    "Hoist your right arm","Pick up your right arm","Extend your right arm","Hold up your right arm","Lift your right hand","Extend your right hand","Reach your right arm up","Up with your right arm",
    "Raise your right hand high","Elevate your right hand","Extend your right hand upward","Hoist your right hand","Lift your right hand into the air"],
    "RaiseArmLeft": ["Raise your left arm ", "Can you please raise your left arm?","Please raise your left arm","Lift your left arm","Elevate your left arm",
    "Hoist your left arm","Pick up your left arm","Extend your left arm","Hold up your left arm","Lift your left hand","Extend your left hand",
    "Reach your left arm up","Up with your left arm","Raise your left hand high","Elevate your left hand","Extend your left hand upward",
    "Hoist your left hand","Lift your left hand into the air"],
    "GiveFive": ["Give me the high-five","High five","Slap me some skin","Up top","Hit me up top","Let's high-five","Gimme a high-five",
    "Slap hands","Let's do a high five","Give me five"]
    }

    closest_keys_with_similarity = {}

    for reference_sentence in reference_sentences:
        reference_embedding = model.encode(reference_sentence, convert_to_tensor=True)
        closest_key = None
        highest_similarity = -1.0

        for key, sentences in sentences_to_compare.items():
            for sentence in sentences:
                embedding = model.encode(sentence, convert_to_tensor=True)
                cosine_similarity = util.pytorch_cos_sim(reference_embedding, embedding)
                similarity = cosine_similarity.item()
                if similarity > highest_similarity:
                    highest_similarity = similarity
                    closest_key = key

    closest_keys_with_similarity[reference_sentence] = (closest_key, highest_similarity)

    gptres=0
    movementres = 0
    
    for reference_sentence, (closest_key, similarity) in closest_keys_with_similarity.items():
        if(similarity>0.8):
            movementres = movementres+1
            print(closest_key)
            return closest_key
        else:
            gptres = gptres +1

    if(gptres>0):
        print("Similarity: ", similarity)
        print("Indirizzo la frase a chatgpt")
        azione = ''
        return azione


def IdentificaAzioneSecond(sentence):
    tresh = 0.8
    model = SentenceTransformer('bert-base-nli-mean-tokens')
    nlp = spacy.load("en_core_web_sm")
    testo = sentence
    testo = testo.replace(",", ".")
    doc = nlp(testo)
    reference_sentences = []
    #frasi
    for frase in doc.sents:
        reference_sentences.append(frase.text)
    #dizionario
    sentences_to_compare = {
        "Hello":["Hello","What's up"],
        "Think":["I think","It seems to me","Maybe"],
        "Donthink": ["I don't think","I doubt","I'm not sure",],
        "No": ["No","Impossible"],
        "Yes":["Yes","I will","I'll do"],
        "Explain":["Explain","Here's how it works","Here's what you need to know","First, let me clarify","To begin with"]
    }
    closest_keys_with_similarity = {}
    for reference_sentence in reference_sentences:
        reference_embedding = model.encode(reference_sentence, convert_to_tensor=True)
        closest_key = None
        highest_similarity = -1.0

        for key, sentences in sentences_to_compare.items():
            for sentence in sentences:
                embedding = model.encode(sentence, convert_to_tensor=True)
                cosine_similarity = util.pytorch_cos_sim(reference_embedding, embedding)
                similarity = cosine_similarity.item()
                if similarity > highest_similarity:
                    highest_similarity = similarity
                    closest_key = key
            closest_keys_with_similarity[reference_sentence] = (closest_key, highest_similarity)
    gptres=0
    movementres = 0
    reply = {}
    for reference_sentence, (closest_key, similarity) in closest_keys_with_similarity.items():
        for reference_sentence, (closest_key, similarity) in closest_keys_with_similarity.items():
            if(similarity>tresh):
                movementres = movementres+1
                reply[reference_sentence]=closest_key
            else:
                reply[reference_sentence]="AnimatedSay"
                gptres = gptres +1
    # Trova le chiavi di una sola parola con valore 'AnimatedSay'
    animated_say_keys = [key for key, value in reply.items() if value == "AnimatedSay" and len(key.split()) == 1]

    new_dict = reply.copy()

    for i in range(0, len(animated_say_keys), 2):
        if i + 1 < len(animated_say_keys):
            new_key = f"{animated_say_keys[i].replace('.', ',')} {animated_say_keys[i + 1].replace('.', ',')}"
            new_dict[new_key] = "Explain"
            del new_dict[animated_say_keys[i]]
            del new_dict[animated_say_keys[i + 1]]
        else:
            new_dict[animated_say_keys[i]] = "Explain"
    
    original_ordered_dict = OrderedDict(new_dict)
    print("OrderedDict")
    print(original_ordered_dict)
    new_ordered_dict = {'sentences': list(original_ordered_dict.keys()),'movements': list(original_ordered_dict.values())}
    print(new_ordered_dict)
    return new_ordered_dict

