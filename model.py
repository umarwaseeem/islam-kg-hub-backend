import nltk
import spacy
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer

# Download necessary NLTK data
nltk.download('punkt', quiet=True)
nltk.download('stopwords', quiet=True)
nltk.download('wordnet', quiet=True)

# Try to load spaCy model, use a flag if it's not available
try:
    nlp = spacy.load("en_core_web_sm")
    spacy_available = True
except IOError:
    print("Warning: spaCy model 'en_core_web_sm' not found. Some features will be limited.")
    spacy_available = False

class NLPModel:
    def __init__(self):
        self.stop_words = set(stopwords.words('english'))
        self.lemmatizer = WordNetLemmatizer()
        self.analytics_keywords = ['how many', 'how much', 'count', 'number of']
        self.subject_keywords = ['hadith', 'narration', 'saying', 'tradition']

    def preprocess_text(self, text):
        # Tokenize the text
        tokens = word_tokenize(text.lower())
        
        # Remove stopwords and lemmatize
        tokens = [self.lemmatizer.lemmatize(token) for token in tokens if token not in self.stop_words]
        
        return tokens

    def extract_entities(self, text):
        if spacy_available:
            doc = nlp(text)
            entities = [(ent.text, ent.label_) for ent in doc.ents]
        else:
            # Fallback to a simple approach if spaCy is not available
            tokens = self.preprocess_text(text)
            entities = [(token, 'UNKNOWN') for token in tokens if token[0].isupper()]
        return entities

    def extract_query_info(self, user_query):
        tokens = self.preprocess_text(user_query)
        entities = self.extract_entities(user_query)

        # Extract relevant information
        narrator = None
        count_hadith = False
        analytics_question = False
        subject = None

        # Check for analytics keywords
        for keyword in self.analytics_keywords:
            if keyword in user_query.lower():
                analytics_question = True
                break

        # Identify subject
        for token in tokens:
            if token in self.subject_keywords:
                subject = token
                break

        # Identify narrator and count_hadith
        for i, token in enumerate(tokens):
            if token in ['narrate', 'narrated', 'narrator']:
                count_hadith = True
                # Check the next token as a potential narrator
                if i + 1 < len(tokens):
                    narrator = tokens[i + 1]
                break

        # If narrator not found, check entities
        if not narrator:
            for entity, label in entities:
                if label == 'PERSON' or (not spacy_available and self.is_potential_name(entity, user_query)):
                    narrator = entity
                    break

        return {
            'narrator': narrator,
            'count_hadith': count_hadith or analytics_question,
            'subject': subject,
            'analytics_question': analytics_question
        }

    def is_potential_name(self, word, context):
        # Check if the word is capitalized (for non-Arabic/Urdu names)
        if word[0].isupper():
            return True
        
        # Check for common name indicators in the context
        name_indicators = ['narrated by', 'reported by', 'according to']
        for indicator in name_indicators:
            if indicator + ' ' + word.lower() in context.lower():
                return True
        
        return False

def build_sparql_query(query_info):
    narrator = query_info['narrator']
    count_hadith = query_info['count_hadith']
    subject = query_info['subject']
    analytics_question = query_info['analytics_question']

    if narrator and (count_hadith or analytics_question):
        return f"""
        PREFIX : <http://www.semantichadith.com/ontology/>
        PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
        SELECT (COUNT (?hadith) AS ?num)
        WHERE {{
            ?hadith rdf:type :Hadith .
            ?hadith :hasNarratorChain ?o .
            ?o :hasNarratorSegment ?x .
            ?x :refersToNarrator+ ?y .
            ?y :name ?name .
            FILTER(REGEX(?name, "{narrator}", "i"))
        }}
        """
    elif subject and analytics_question:
        return f"""
        PREFIX : <http://www.semantichadith.com/ontology/>
        PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
        SELECT (COUNT (?hadith) AS ?num)
        WHERE {{
            ?hadith rdf:type :Hadith .
        }}
        """
    else:
        return None
