from nltk import word_tokenize,pos_tag
def sementics(sen):
    word = word_tokenize(sen)
    pos_tags = pos_tag(word)
    print(word)
    print(pos_tags)
    noun = []
    verb = ""
    for tuple in pos_tags:
        if tuple[1] == 'NNP':
            noun.append(tuple[0])
        if tuple[1] == 'VBZ':
            verb = tuple[0]
    print(noun[0],verb,noun[1])
    if len(noun)>=2:
        return noun[0],verb,noun[1]
    else:
        return "No noun is found"
