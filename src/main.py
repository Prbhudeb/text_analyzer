import pandas as pd
import src.data_extractor as de
import src.calculate_metrics as cm
import src.text_preprocessing as tp
import src.utils as ut
import logging

def main():
    try:
        input_file = '../data/raw/Output.xlsx'
        output_file = '../data/processed/Output.xlsx'
        output_new_file = '../data/processed/Output_new.xlsx'
        
        logging.info(f"Loading data from {input_file}")
        data = pd.read_excel(input_file)

        if 'URL' not in data.columns or data['URL'].isnull().all():
            raise ValueError("The 'URL' column is missing or empty in the input file.")

        new_data = pd.DataFrame(columns=['URL','POSITIVE SCORE', 'NEGATIVE SCORE', 'POLARITY SCORE', 'SUBJECTIVITY SCORE',
                                         'AVG SENTENCE LENGTH', 'PERCENTAGE OF COMPLEX WORDS', 'FOG INDEX',
                                         'AVG NUMBER OF WORDS PER SENTENCE', 'COMPLEX WORD COUNT', 'WORD COUNT',
                                         'SYLLABLE PER WORD', 'PERSONAL PRONOUNS', 'AVG WORD LENGTH'])

        logging.info("Extracting data from the URLs")
        for index, link in enumerate(data['URL']):
            if not isinstance(link, str) or not link.strip():
                logging.warning(f"Skipping invalid or empty URL at index {index}")
                continue
            
            try:
                logging.info(f"Processing URL at index {index}: {link}")
                raw_text = de.extract_data(link)  # Extract raw text
                cleaned_text = tp.preprocess_text(raw_text)  # Preprocess text
                metrics = cm.calculate_text_metrics(cleaned_text)  # Calculate metrics

                if new_data.empty:
                    new_data = pd.DataFrame(columns=['URL','POSITIVE SCORE', 'NEGATIVE SCORE', 'POLARITY SCORE', 'SUBJECTIVITY SCORE',
                                         'AVG SENTENCE LENGTH', 'PERCENTAGE OF COMPLEX WORDS', 'FOG INDEX',
                                         'AVG NUMBER OF WORDS PER SENTENCE', 'COMPLEX WORD COUNT', 'WORD COUNT',
                                         'SYLLABLE PER WORD', 'PERSONAL PRONOUNS', 'AVG WORD LENGTH'])

                row_df = pd.DataFrame([{
                    'URL': link,
                    'POSITIVE SCORE': float(metrics['Positive Score']),
                    'NEGATIVE SCORE': float(metrics['Negative Score']),
                    'POLARITY SCORE': float(metrics['Polarity Score']),
                    'SUBJECTIVITY SCORE': float(metrics['Subjectivity Score']),
                    'AVG SENTENCE LENGTH': float(metrics['Average Sentence Length']),
                    'PERCENTAGE OF COMPLEX WORDS': float(metrics['Percentage of Complex Words']),
                    'FOG INDEX': float(metrics['Fog Index']),
                    'AVG NUMBER OF WORDS PER SENTENCE': float(metrics['Average Number of Words Per Sentence']),
                    'COMPLEX WORD COUNT': float(metrics['Complex Word Count']),
                    'WORD COUNT': int(metrics['Word Count']),  # Ensure integer conversion
                    'SYLLABLE PER WORD': float(metrics['Syllable Per Word']),
                    'PERSONAL PRONOUNS': float(metrics['Personal Pronouns']),
                    'AVG WORD LENGTH': float(metrics['Average Word Length'])
                }])

                new_data = pd.concat([new_data, row_df], ignore_index=True)


            except Exception as e:
                logging.error(f"Error processing URL at index {index}: {e}")
                continue

        # logging.info(f"Saving processed data to {output_file}")
        # data.to_excel(output_file, index=False)
        logging.info(f"Saving processed data to {output_new_file}")
        new_data.to_excel(output_new_file, index=False)

    except FileNotFoundError as fnf_error:
        logging.error(f"Input file not found: {fnf_error}")
    except ValueError as ve:
        logging.error(f"Data validation error: {ve}")
    except Exception as e:
        logging.error(f"An unexpected error occurred: {e}")    


if __name__ == "__main__":
    main()
    