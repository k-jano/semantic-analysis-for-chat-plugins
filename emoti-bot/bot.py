import discord
import pickle, re, string
import nltk
from nltk.tokenize import word_tokenize
from nltk.stem.wordnet import WordNetLemmatizer
from nltk.tag import pos_tag
from nltk.corpus import stopwords

stop_words = stopwords.words('english')
f = open('../sentiment_classifier.pickle', 'rb')
classifier = pickle.load(f)
f.close()

client = discord.Client()

def lemmatize(tokens):
    lemmatizer = WordNetLemmatizer()
    lem_sentence = []
    for word, tag in pos_tag(tokens):
        if tag.startswith('NN'): #noun
            sen_type = 'n'
        elif tag.startswith('VB'): #verb
            sen_type = 'v'
        else:
            sen_type = 'a'
        lem_sentence.append(lemmatizer.lemmatize(word, sen_type))
    return lem_sentence


def remove_noise(tokens):
    cleaned_tokens = []
    for token in tokens:
        token = re.sub('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+#]|[!*\(\),]|'\
                       '(?:%[0-9a-fA-F][0-9a-fA-F]))+','', token)
        token = re.sub("(@[A-Za-z0-9_]+)","", token)
        
        if len(token) > 0 and token not in string.punctuation and token.lower() not in stop_words:
            cleaned_tokens.append(token.lower())
    
    return cleaned_tokens


@client.event
async def on_message(message):
    if message.author == client.user:
        return

    tokens = lemmatize(remove_noise(word_tokenize(message.content)))
    emotion = classifier.classify(dict([token, True] for token in tokens))
    await message.channel.send('Emotion: %s' % emotion)


client.run('insert-bot-token-here')