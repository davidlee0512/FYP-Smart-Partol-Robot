import nltk

nltk.download('punkt', download_dir=os.path.join(os.path.dirname(__file__),"./nltk_data"))
nltk.download('averaged_perceptron_tagger', download_dir=os.path.join(os.path.dirname(__file__),"./nltk_data"))
nltk.download('maxent_ne_chunker', download_dir=os.path.join(os.path.dirname(__file__),"./nltk_data"))
nltk.download('words', download_dir=os.path.join(os.path.dirname(__file__),"./nltk_data"))
nltk.download('stopwords', download_dir=os.path.join(os.path.dirname(__file__),"./nltk_data"))
nltk.download('wordnet', download_dir=os.path.join(os.path.dirname(__file__),"./nltk_data"))
