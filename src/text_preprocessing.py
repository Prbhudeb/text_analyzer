import nltk
import matplotlib.pyplot as plt

# Ensure the necessary NLTK corpora are downloaded
# nltk.download('punkt')
# nltk.download('stopwords')
# nltk.download('wordnet')

import re
from wordcloud import WordCloud
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from textblob import TextBlob
from collections import Counter

# Function to preprocess text
def preprocess_text(text):

    try:
        if not isinstance(text, str) or not text.strip():
            raise ValueError("Input text must be a non-empty string.")

        # 1. Lowercasing
        text = text.lower()

        # 2. Remove URLs, Emails, Special Characters
        text = re.sub(r'https?://\S+|www\.\S+', '', text)
        # Remove emails
        text = re.sub(r'\S+@\S+', '', text)
        # Remove non-alphabetic characters, retaining spaces
        text = re.sub(r'[^a-zA-Z\s]', '', text)
        # Remove extra whitespaces
        text = re.sub(r'\s+', ' ', text).strip()

        # 3. Tokenization
        tokens = word_tokenize(text)

        # 4. Remove stopwords
        stop_words = set(stopwords.words('english'))
        filtered_tokens = [word for word in tokens if word not in stop_words]

        if not filtered_tokens:
            raise ValueError("No meaningful tokens found after removing stopwords.")

        # 5. Lemmatization
        lemmatizer = WordNetLemmatizer()
        lemmatized_tokens = [lemmatizer.lemmatize(word) for word in filtered_tokens]

        word_counts = Counter(lemmatized_tokens)
        print(word_counts.most_common(10))

        # wordcloud = WordCloud().generate(' '.join(lemmatized_tokens))
        # plt.imshow(wordcloud, interpolation='bilinear')
        # plt.axis("off")
        # plt.show()

        cleaned_text = " ".join(lemmatized_tokens)
        
        try:
            blob = TextBlob(cleaned_text)
            corrected_text = str(blob.correct())
        except Exception as e:
            print("Spelling correction failed:", e)
            corrected_text = cleaned_text  # Fall back to the original cleaned text

        return corrected_text
    
    except ValueError as ve:
        print(f"ValueError: {ve}")
        return ""

    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return ""
