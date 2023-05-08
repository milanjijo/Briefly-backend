import numpy as np     
import networkx as nx 
import nltk 
from nltk.corpus import stopwords
from nltk.cluster.util import cosine_distance

STOP_WORDS = []
try:
    STOP_WORDS = stopwords.words('english')
    if not STOP_WORDS:
        nltk.download('stopwords')
except LookupError:
    nltk.download('stopwords')

class SummariserCosine:
    # Generate clean sentences
    def read_text(self, text):
        split_text = text.split(". ")

        sentences = []

        for sentence in split_text:
            sentences.append(sentence.replace("[^a-zA-Z]", " ").split(" "))

        sentences.pop()

        return sentences

    def extract_vector(self, sentence, all_words, stop_words):
        
        extracted_vector = [0] * len(all_words)

        # build the vector for the sentence
        for word in sentence:
            if word in stop_words:
                continue
            extracted_vector[all_words.index(word)] += 1

        return extracted_vector

    # Checking the similarity of the two sentences(adjacent)
    def sentence_similarity(self, first_sentence, second_sentence, stop_words=None):
        
        if stop_words is None:
            stop_words = []

        #print(first_sentence)
        first_sentence = [word.lower() for word in first_sentence]
    
        second_sentence = [word.lower() for word in second_sentence]

        all_words = list(set(first_sentence + second_sentence))

        first_vector = self.extract_vector(first_sentence, all_words, stop_words)
        second_vector = self.extract_vector(second_sentence, all_words, stop_words)

        return 1 - cosine_distance(first_vector, second_vector)

    # Similarity matrix
    def build_similarity_matrix(self, sentences, stop_words):
        
        # Create an empty similarity matrix
        similarity_matrix = np.zeros((len(sentences), len(sentences)))

        for this_sentence_index, this_sentence in enumerate(sentences):
            for another_sentence_index, another_sentence in enumerate(sentences):
                if this_sentence == another_sentence: 
                    #ignore if both are same sentences
                    continue
                similarity_matrix[this_sentence_index][another_sentence_index] = \
                    self.sentence_similarity(this_sentence, another_sentence, stop_words)

        return similarity_matrix

    # Construct the summarised text from the ranked sentences
    def summarise_text(self,sentences, ranked_sentences, top_n_sentences):
        
        summarised_text = []
        top_sen= []
        
        if top_n_sentences > len(ranked_sentences):
            top_n_sentences = len(ranked_sentences)
        
        for index in range(top_n_sentences):
            top_sen.append(ranked_sentences[index][1])

        for l in sentences:
          if l in top_sen:
            summarised_text.append(" ".join(l))

        # for index in range(top_n_sentences):
        #     summarised_text.append(" ".join(ranked_sentences[index][1]))

        summarised_text = ". ".join(summarised_text)

        return summarised_text

    # Sort sentences to surface top ranked ones from the similarity matrix
    def sort_sentences_to_surface_top_ranked_sentences(self, scores, sentences):
        
        return sorted(((scores[index], sentence) \
            for index, sentence in enumerate(sentences)), reverse=True)

    # Rank the sentences using networkx's pagerank() function
    def rank_sentences(self, sentence_similarity_martix):
       
        sentence_similarity_graph = nx.from_numpy_array(sentence_similarity_martix)
        scores = nx.pagerank(sentence_similarity_graph)
        return sentence_similarity_graph, scores

    # Generating Summary Method
    def generate_summary(self, text, top_n_sentences=3):
      

        sentences = self.read_text(text)
        print(sentences)
        #Generate Similary Martix across sentences
        sentence_similarity_martix = self.build_similarity_matrix(sentences, STOP_WORDS)

        #Rank sentences in similarity martix
        sentence_similarity_graph, scores = self.rank_sentences(sentence_similarity_martix)

        ranked_sentences = self.sort_sentences_to_surface_top_ranked_sentences(scores, sentences)

        summarised_text = self.summarise_text(sentences, ranked_sentences, top_n_sentences)
        return summarised_text, ranked_sentences


n= SummariserCosine()
test="""There are many techniques available to generate extractive summarization to keep it simple, I will be using an unsupervised learning approach to find the sentences similarity and rank them. Summarization can be defined as a task of producing a concise and fluent summary while preserving key information and overall meaning. One benefit of this will be, you don’t need to train and build a model prior start using it for your project. It’s good to understand Cosine similarity to make the best use of the code you are going to see. Cosine similarity is a measure of similarity between two non-zero vectors of an inner product space that measures the cosine of the angle between them. Its measures cosine of the angle between vectors. The angle will be 0 if sentences are similar."""
# s, r =n.generate_summary(test)
# print(s)
# print(r)