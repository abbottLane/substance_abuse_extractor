from FeatureExtractor.FeatureExtractor import FeatureExtractor
from Classification import Globals
import subprocess
# from nltk.tag import StanfordNERTagger


features = [
    "useClassFeature=true",
    "useWord=true",
    "useNGrams=true",
    "noMidNGrams=true",
    "useDisjunctive=true",
    "maxNGramLeng=6",
    "usePrev=true",
    "useNext=true",
    "useSequences=true",
    "usePrevSequences=true",
    "maxLeft=1",
    "useTypeSeqs=true",
    "useTypeSeqs2=true",
    "useTypeySequences=true",
    "wordShape=chris2useLC"
]

entity_types = [
    "Status",
    "Temporal",
    "Method",
    "Type",
    "Amount",
    "Frequency",
    "History"
]


def classify(training_doc_objs,
             stanford_ner_path="/Users/Martin/stanford-ner-2015-04-20/stanford-ner.jar",
             train_file_name="train-file.tsv",
             prop_file_name="attr_extract.prop",
             model_name="ner-model.ser.gz",
             test_file_name="test-file.tsv",
             train_script_name="train_model.sh",
             test_script_name="test_classify.sh"):
    '''
    This classifies.
    :return: list of sent_objs with attributes filled
    '''
    global features
    create_train_file(training_doc_objs, train_file_name)
    create_prop_file(prop_file_name, train_file_name, features, model_name)
    train_model(stanford_ner_path, prop_file_name, train_script_name)
    test_model(stanford_ner_path, model_name, test_file_name, test_script_name)


def train(training_doc_objs, path="EntityExtractor/",
          stanford_ner_path="/Users/Martin/stanford-ner-2015-04-20/stanford-ner.jar",
          train_script_name="train_model.sh"):
    global features
    global entity_types
    for type in entity_types:
        train_file_name = path + "train-" + type + ".tsv"
        prop_file_name = path + type + ".prop"
        model_name = path + type + "-model.ser.gz"
        create_train_file(training_doc_objs, train_file_name)
        create_prop_file(prop_file_name, train_file_name, features, model_name)
        train_model(stanford_ner_path, prop_file_name, train_script_name)


def test_model(stanford_ner_path, model_name, test_file_name, test_script_name):
    subprocess.call(["./" + test_script_name + " " + stanford_ner_path + " " + model_name + " " + test_file_name], shell=True)


def train_model(stanford_ner_path, prop_file_name, train_script_name):
    subprocess.call(["./"+train_script_name+" "+stanford_ner_path+" "+prop_file_name], shell=True)


def create_train_file(training_doc_objs, train_file_name):
    train_file = open(train_file_name, 'w')
    for doc in training_doc_objs:
        doc_obj = training_doc_objs[doc]
        for sent_obj in doc_obj.get_sentence_obj_list():
            if sent_obj.has_substance_abuse_entity():
                sentence = sent_obj.sentence
                entity_set = sent_obj.set_entities
                for entity in entity_set:
                    attr_dict = entity.dict_of_attribs
                    for attr in attr_dict:
                        for word in attr_dict[attr].text.strip().split():
                            train_file.write(word + "\t" + attr_dict[attr].type + "\n")
                        # print(attr_dict[attr])
    train_file.close()


def create_prop_file(prop_file_name, train_file_name, features, model_name):
    prop_file = open(prop_file_name, 'w')
    prop_file.write("trainFile = " + train_file_name + "\n")
    prop_file.write("serializeTo = " + model_name + "\n")
    # prop_file.write("map = word=0,answer=1,temp=2,method=3,type=4,amount=5,freq=6,hist=7\n")
    prop_file.write("map = word=0,answer=1\n")
    for feat in features:
        prop_file.write(feat + "\n")
    prop_file.close()


if __name__ == "__main__":
    stanford_ner_path = "/Users/Martin/stanford-ner-2015-04-20/stanford-ner.jar"
    # train_file_name = "jane-austen-emma-ch1.tsv"
    # train_file_name = "dummy-train.tsv"
    train_file_name = "dummer.tsv"
    test_file_name = "dummer-test.tsv"
    # test_file_name = "dummy-train.tsv"
    # prop_file_name = "austen.prop"
    prop_file_name = "attr_extract.prop"
    model_name = "ner-model.ser.gz"
    train_script_name = "train_model.sh"
    test_script_name = "test_classify.sh"
    # classify(stanford_ner_path, train_file_name, prop_file_name, model_name,
    #          test_file_name, train_script_name, test_script_name)
