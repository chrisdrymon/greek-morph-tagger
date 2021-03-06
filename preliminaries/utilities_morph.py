import os
import tensorflow as tf
from bs4 import BeautifulSoup
import numpy as np
import json
from greek_normalisation.normalise import Normaliser, Norm
from gensim.models import KeyedVectors
from collections import Counter


# Create a custom model saver
class ModelSaver(tf.keras.callbacks.Callback):
    """A custom tensorflow model saver that returns useful information"""
    def __init__(self, morph_title, nn_type, nn_layers, cells, corpus_string):
        super().__init__()
        self.best_val_acc = 0
        self.best_epoch = 0
        self.new_best = False
        self.morph_title = morph_title
        self.nn_type = nn_type
        self.nn_layers = nn_layers
        self.cells = cells
        self.corpus_string = corpus_string

    def on_train_begin(self, logs=None):
        self.best_val_acc = 0
        self.new_best = False

    def on_epoch_end(self, epoch, logs=None):
        # Save the best model based on validation accuracy.
        if logs['val_accuracy'] > self.best_val_acc:
            self.best_val_acc = logs['val_accuracy']
            model_name = os.path.join('models', f'{self.morph_title}-{self.nn_type}-{self.nn_layers}x{self.cells}-'
                                                f'{logs["accuracy"]:.3f}'
                                                f'val{logs["val_accuracy"]:.3f}-{self.corpus_string}.h5')
            tf.keras.models.save_model(self.model, model_name, save_format='h5')
            self.best_epoch = epoch + 1
            self.new_best = True
            print('\nModel saved at epoch', epoch + 1, 'with', self.best_val_acc, 'validation accuracy.\n')

    def on_train_end(self, logs=None):
        if self.new_best:
            print('\nBest Model saved at epoch', self.best_epoch, 'with', self.best_val_acc, 'validation accuracy.')


class Morphs:
    """Hold data for one aspect of morphology."""
    def __init__(self, title, tags, lstm1, dnn):
        self.title = title
        self.tags = tags
        self.lstm1 = lstm1
        self.dnn = dnn


def create_morph_classes():
    """Create a class instance for each part of speech aspect."""
    pos_lstm1 = tf.keras.models.load_model(os.path.join('models', 'pos-lstm1-3x128-0.927val0.939-AGDTfirst26last7.h5'))
    pos_dnn = tf.keras.models.load_model(os.path.join('models', 'pos-dnn-2x20-0.939val0.942-AGDTfirst26last7.h5'))
    person_lstm1 = tf.keras.models.load_model(os.path.join('models',
                                                           'person-lstm1-3x128-0.983val0.990-AGDTfirst26last7.h5'))
    person_dnn = tf.keras.models.load_model(os.path.join('models', 'person-dnn-2x20-0.994val0.992-AGDTfirst26last7.h5'))
    number_lstm1 = tf.keras.models.load_model(os.path.join('models',
                                                           'number-lstm1-3x128-0.955val0.980-AGDTfirst26last7.h5'))
    number_dnn = tf.keras.models.load_model(os.path.join('models', 'number-dnn-2x20-0.977val0.981-AGDTfirst26last7.h5'))
    tense_lstm1 = tf.keras.models.load_model(os.path.join('models',
                                                          'tense-lstm1-3x128-0.976val0.990-AGDTfirst26last7.h5'))
    tense_dnn = tf.keras.models.load_model(os.path.join('models', 'tense-dnn-2x20-0.990val0.992-AGDTfirst26last7.h5'))
    mood_lstm1 = tf.keras.models.load_model(os.path.join('models',
                                                         'mood-lstm1-3x128-0.981val0.992-AGDTfirst26last7.h5'))
    mood_dnn = tf.keras.models.load_model(os.path.join('models', 'mood-dnn-2x20-0.994val0.992-AGDTfirst26last7.h5'))
    voice_lstm1 = tf.keras.models.load_model(os.path.join('models',
                                                          'voice-lstm1-3x128-0.978val0.991-AGDTfirst26last7.h5'))
    voice_dnn = tf.keras.models.load_model(os.path.join('models', 'voice-dnn-2x20-0.992val0.993-AGDTfirst26last7.h5'))
    gender_lstm1 = tf.keras.models.load_model(os.path.join('models',
                                                           'gender-lstm1-3x128-0.923val0.934-AGDTfirst26last7.h5'))
    gender_dnn = tf.keras.models.load_model(os.path.join('models', 'gender-dnn-2x20-0.952val0.937-AGDTfirst26last7.h5'))
    case_lstm1 = tf.keras.models.load_model(os.path.join('models',
                                                         'case-lstm1-3x128-0.934val0.962-AGDTfirst26last7.h5'))
    case_dnn = tf.keras.models.load_model(os.path.join('models', 'case-dnn-2x20-0.957val0.963-AGDTfirst26last7.h5'))
    degree_lstm1 = tf.keras.models.load_model(os.path.join('models',
                                                           'degree-lstm1-3x128-0.998val0.999-AGDTfirst26last7.h5'))
    degree_dnn = tf.keras.models.load_model(os.path.join('models', 'degree-dnn-2x20-0.999val0.999-AGDTfirst26last7.h5'))

    # The possible tags for each item of morphology
    pos_tags = ('l', 'n', 'a', 'r', 'c', 'i', 'p', 'v', 'd', 'm', 'g', 'u')
    person_tags = ('1', '2', '3')
    number_tags = ('s', 'p', 'd')
    tense_tags = ('p', 'i', 'r', 'l', 't', 'f', 'a')
    mood_tags = ('i', 's', 'n', 'm', 'p', 'o')
    voice_tags = ('a', 'p', 'm', 'e')
    gender_tags = ('m', 'f', 'n')
    case_tags = ('n', 'g', 'd', 'a', 'v')
    degree_tags = ('p', 'c', 's')

    # Create a class instance for each aspect of morphology
    pos = Morphs('pos', pos_tags, pos_lstm1, pos_dnn)
    person = Morphs('person', person_tags, person_lstm1, person_dnn)
    number = Morphs('number', number_tags, number_lstm1, number_dnn)
    tense = Morphs('tense', tense_tags, tense_lstm1, tense_dnn)
    mood = Morphs('mood', mood_tags, mood_lstm1, mood_dnn)
    voice = Morphs('voice', voice_tags, voice_lstm1, voice_dnn)
    gender = Morphs('gender', gender_tags, gender_lstm1, gender_dnn)
    case = Morphs('case', case_tags, case_lstm1, case_dnn)
    degree = Morphs('degree', degree_tags, degree_lstm1, degree_dnn)

    return pos, person, number, tense, mood, voice, gender, case, degree


def return_all_treebank_annotators():
    """Search all Greek treebanks and return a list of its annotators' names and abbreviated names."""
    agdt_folder = os.path.join('data', 'corpora', 'greek', 'annotated', 'perseus-771dca2', 'texts')
    gorman_folder = os.path.join('data', 'corpora', 'greek', 'annotated', 'gorman')
    ignore_names = ['arethusa']
    all_files = []
    annotators = []
    short_annotators = {}
    for file in os.listdir(agdt_folder):
        all_files.append(os.path.join(agdt_folder, file))
    for file in os.listdir(gorman_folder):
        all_files.append(os.path.join(gorman_folder, file))
    file_count = 0
    for file in all_files:
        if file[-4:] == '.xml':
            file_count += 1
            print(file_count, file)
            xml_file = open(file, 'r', encoding='utf-8')
            soup = BeautifulSoup(xml_file, 'xml')
            responsibility_statement = soup.find_all('respStmt')
            for responsible in responsibility_statement:
                if 'annotator' in responsible.find('resp').text:
                    person_name = responsible.find('persName')
                    name = person_name.find('name')
                    short = person_name.find('short')
                    if short:
                        short_annotators[short.text] = name.text
                    if name.text not in ignore_names:
                        if short:
                            print(f'{short.text}: {name.text}')
                        if name.text not in annotators:
                            annotators.append(name.text)
            annots = soup.find_all('annotator')
            for annotator in annots:
                try:
                    name = annotator.find('name').text
                    short = annotator.find('short').text
                    if name:
                        print(f'{short}: {name}')
                        if name not in ignore_names and name not in annotators:
                            annotators.append(name)
                except AttributeError:
                    pass
    return annotators, short_annotators


def return_file_annotators(soup):
    """Search this treebank and return a list of its annotators' names and abbreviated names."""
    annotators = []
    ignore_names = ['arethusa']
    responsibility_statement = soup.find_all('respStmt')
    for responsible in responsibility_statement:
        if 'annotator' in responsible.find('resp').text:
            person_name = responsible.find('persName')
            name = person_name.find('name')
            if name.text not in ignore_names and name.text not in annotators:
                annotators.append(name.text)
    annots = soup.find_all('annotator')
    for annotator in annots:
        try:
            name = annotator.find('name').text
            if name:
                if name not in ignore_names and name not in annotators:
                    annotators.append(name)
        except AttributeError:
            pass
    return annotators


def return_sentence_annotators(sentence, short_annotators):
    """Return a list of this sentence's annotators"""
    sentence_annotators = []
    xml_sen_ann = sentence.find_all(['annotator', 'primary', 'secondary'])
    for annotator in xml_sen_ann:
        try:
            sentence_annotators.append(short_annotators[annotator.text])
        except KeyError:
            sentence_annotators.append(annotator.text)
    return sentence_annotators


def elision_normalize(s):
    """Turn unicode characters which look similar to 2019 into 2019."""
    return s.replace("\u02BC", "\u2019").replace("\u1FBF", "\u2019").replace("\u0027", "\u2019").\
        replace("\u1FBD", "\u2019")


def return_all_normalized_treebank_characters():
    """Return a list of each unique character which occurs in the treebanks. Prints character counts."""
    agdt_folder = os.path.join('data', 'corpora', 'greek', 'annotated', 'perseus-771dca2', 'texts')
    gorman_folder = os.path.join('data', 'corpora', 'greek', 'annotated', 'gorman')
    all_files = []
    all_characters = []
    character_count = Counter()

    for file in os.listdir(agdt_folder):
        all_files.append(os.path.join(agdt_folder, file))
    for file in os.listdir(gorman_folder):
        all_files.append(os.path.join(gorman_folder, file))
    with open(os.path.join('data', 'jsons', 'short_annotators.json'), encoding='utf-8') as json_file:
        short_annotators = json.load(json_file)
    with open(os.path.join('data', 'jsons', 'annotators.json'), encoding='utf-8') as json_file:
        all_annotators = json.load(json_file)

    # Create the normaliser
    normalise = Normaliser().normalise

    file_count = 0
    for file in all_files[11:]:
        if file[-4:] == '.xml':
            file_count += 1
            print(file_count, file)
            xml_file = open(file, 'r', encoding='utf-8')
            soup = BeautifulSoup(xml_file, 'xml')
            sentences = soup.find_all('sentence')
            for sentence in sentences:
                tokens = sentence.find_all(['word', 'token'])
                for token in tokens:
                    if token.has_attr('form') and token.has_attr('postag') and token.has_attr('artificial') is False:
                        normalized_form = normalise(elision_normalize(token['form']))
                        for character in normalized_form[0]:
                            if character not in all_characters:
                                all_characters.append(character)
                                print(f'{character} in {token["form"]}')
    print(character_count)
    return all_characters


def return_similar_words(one_word):
    """Return a list of words which Word2Vec finds similar to the input."""
    wv = KeyedVectors.load('models/word2vec.wordvectors')
    normalise = Normaliser().normalise
    return wv.most_similar(normalise(elision_normalize(one_word))[0])


def remove_greek_punctuation(word):
    """Return the Greek input without punctuation."""
    return word.replace(',', '').replace('·', '').replace(';', '').replace('.', '').replace('?', '').replace('»', '').\
        replace('«', '').replace('“', '').replace('„', '')


def isolate_greek_punctuation(fsentence):
    return fsentence.replace(',', ' , ').replace('·', ' · ').replace(';', ' ; ').replace('.', ' . ').\
        replace('?', ' ? ').replace('»', ' » ').replace('«', ' « ').replace('“', ' “ ').replace('„', ' „ ')