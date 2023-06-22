import nltk
from nltk.tag import pos_tag
from pyswip import Prolog

def extract_relationship(sentence):
    # Tokenize the sentence
    tokens = nltk.word_tokenize(sentence)

    # Perform part-of-speech tagging
    tagged_tokens = pos_tag(tokens)

    # Extract the first and last noun tags
    nouns = [tagged_token for tagged_token in tagged_tokens if tagged_token[1].startswith('NN')]
    if len(nouns) >= 2:
        first_noun = nouns[0][0]
        last_noun = nouns[-1][0]
    else:
        return None
    # Determine the relationship based on the "is" keyword and subsequent tag
    is_index = -1
    for i in range(len(tagged_tokens) - 1):
        if tagged_tokens[i][0].lower() == 'is':
            is_index = i
            break
    if is_index != -1 and is_index < len(tagged_tokens) - 1:
        relationship = (first_noun, tagged_tokens[is_index + 1][0], last_noun)
        print(relationship)
        return relationship

    return None

def create_family_knowledge_base(relationship):
    prolog = Prolog()
    prolog.consult("family_relations.pl")
    prolog.assertz(f"{relationship[1]}('{relationship[0].lower()}', '{relationship[2].lower()}')")
    print(prolog)
    c=list(prolog.query(f"{relationship[1]}('{relationship[0].lower()}', '{relationship[2].lower()}')"))
    print (c)
    prolog.save("family_relations.pl")
    # You can add more family relationships here using similar prolog.assertz statements

    return prolog

# Example usage
sentence = input("Enter a sentence: ")
relationship = extract_relationship(sentence)

if relationship:
    family_kb = create_family_knowledge_base(relationship)
    print("Family knowledge base created successfully!")
else:
    print("No relationship found in the sentence.")
