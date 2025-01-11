from textblob import TextBlob
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.corpus import stopwords
import logging

# Helper functions
def syllable_count(word):
    try:
        vowels = "aeiouy"
        word = word.lower().strip(".:;?!")
        if not word:
            return 0
        count = 0
        if word[0] in vowels:
            count += 1
        for index in range(1, len(word)):
            if word[index] in vowels and word[index - 1] not in vowels:
                count += 1
        if word.endswith("e") and len(word) > 2:
            count -= 1
        return max(1, count)
    except Exception as e:
        logging.error(f"Error calculating syllable count for word '{word}': {e}")
        return 0

def count_complex_words(words):
    try:
        return sum(1 for word in words if syllable_count(word) > 2)
    except Exception as e:
        logging.error(f"Error counting complex words: {e}")
        return 0

# Function to calculate text metrics
def calculate_text_metrics(cleaned_text):
    try:
        if not cleaned_text.strip():
            logging.warning("Empty or whitespace-only text received.")
            return {metric: 0 for metric in [
                "Positive Score", "Negative Score", "Polarity Score", "Subjectivity Score",
                "Average Sentence Length", "Percentage of Complex Words", "Fog Index",
                "Average Number of Words Per Sentence", "Complex Word Count", "Word Count",
                "Syllable Per Word", "Personal Pronouns", "Average Word Length"
            ]}


        sentences = sent_tokenize(cleaned_text)
        words = word_tokenize(cleaned_text)
        words = [word for word in words if word.isalpha()]  # Keep only alphabetic tokens
        stop_words = set(stopwords.words('english'))
        words_without_stopwords = [word for word in words if word.lower() not in stop_words]
        
        # Sentiment Analysis
        analyzer = SentimentIntensityAnalyzer()
        sentiment = analyzer.polarity_scores(cleaned_text)
        blob = TextBlob(cleaned_text)
        
        # Calculations
        positive_score = sentiment['pos']
        negative_score = sentiment['neg']
        polarity_score = blob.sentiment.polarity
        subjectivity_score = blob.sentiment.subjectivity
        avg_sentence_length = len(words) / len(sentences) if len(sentences) > 0 else 0
        complex_word_count = count_complex_words(words)
        percentage_of_complex_words = (complex_word_count / len(words)) * 100 if len(words) > 0 else 0
        fog_index = 0.4 * (avg_sentence_length + percentage_of_complex_words)
        avg_number_of_words_per_sentence = len(words) / len(sentences) if len(sentences) > 0 else 0
        word_count = len(words)
        syllable_per_word = sum(syllable_count(word) for word in words) / len(words) if len(words) > 0 else 0
        personal_pronouns = len([word for word in words if word.lower() in ['i', 'we', 'my', 'ours', 'us']])
        avg_word_length = sum(len(word) for word in words) / len(words) if len(words) > 0 else 0
        
        # Return results
        return {
            "Positive Score": positive_score,
            "Negative Score": negative_score,
            "Polarity Score": polarity_score,
            "Subjectivity Score": subjectivity_score,
            "Average Sentence Length": avg_sentence_length,
            "Percentage of Complex Words": percentage_of_complex_words,
            "Fog Index": fog_index,
            "Average Number of Words Per Sentence": avg_number_of_words_per_sentence,
            "Complex Word Count": complex_word_count,
            "Word Count": word_count,
            "Syllable Per Word": syllable_per_word,
            "Personal Pronouns": personal_pronouns,
            "Average Word Length": avg_word_length
        }
    except Exception as e:
        logging.error(f"Error calculating text metrics: {e}")
        return {metric: None for metric in [
            "Positive Score", "Negative Score", "Polarity Score", "Subjectivity Score",
            "Average Sentence Length", "Percentage of Complex Words", "Fog Index",
            "Average Number of Words Per Sentence", "Complex Word Count", "Word Count",
            "Syllable Per Word", "Personal Pronouns", "Average Word Length"
        ]}

