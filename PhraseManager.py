import nltk
from nltk.corpus import wordnet as wn
from nltk.corpus import wordnet_ic
import collections

topics = ("hobbies", "time", "music", "love", "work", "food", "persons", "animals", "learning", "goals", "dreams", "shopping", "money", "politics", "news", "cooking", "sports")


class Phrase:
    def __init__(self):#this is a contrucstor

            pass

    def IsAQuestion(self, strPhrase):
        strPhrase = strPhrase.lower()
        text = nltk.word_tokenize(strPhrase)
        _words = []
        c = 0
        for c , _words in enumerate(nltk.pos_tag(text, tagset = 'universal')):
            if _words[1] == "VERB" and nltk.pos_tag(text, tagset = 'universal')[c-1][1] == "ADV":
                if nltk.pos_tag(text, tagset = 'universal')[c-1][0] == "how":
                    print(c, _words[1][0])
                    return True
                elif nltk.pos_tag(text, tagset = 'universal')[c-1][0] == "where":
                    print(c, _words[1][0])
                    return True
                elif nltk.pos_tag(text, tagset = 'universal')[c-1][0] == "what":
                    print(c, _words[1][0])
                    return True
                elif nltk.pos_tag(text, tagset = 'universal')[c-1][0] == "why":
                    print(c, _words[1][0])
                    return True
                elif nltk.pos_tag(text, tagset = 'universal')[c-1][0] == "when":
                    print(c, _words[1][0])
                    return True
                elif nltk.pos_tag(text, tagset = 'universal')[c-1][0] == "who":
                    print(c, _words[1][0])
                    return True

            if _words[1] == "VERB" and c == 0:
                print(c, _words[1][0])
                return True

            if _words[1] == "VERB" and (nltk.pos_tag(text, tagset = 'universal')[c-1][1] == "PRON" or nltk.pos_tag(text, tagset = 'universal')[c-1][1] == "NOUN"):
                if nltk.pos_tag(text, tagset = 'universal')[c-2][1] == "VERB":
                    print(c, _words[1][0])
                    return True

        return False

    def GuessTopic(self, strPhrase):
        text = nltk.word_tokenize(strPhrase)
        _words = []
        tops = []
        brown_ic = wordnet_ic.ic('ic-brown.dat')
        c = 0
        for c, _words in enumerate(nltk.pos_tag(text, tagset = 'universal')):
            if _words[1] == "NOUN":
                print(_words[0])
                try:
                    _word = wn.synsets(_words[0], 'n')[0]
                    _word.hyponyms()
                except IndexError as e:
                     e.message = "WORD NOT RECOGNISED"
                best_str = ""
                best_f = 0.0
                for _t in topics:
                    _topic = wn.synsets(_t, 'n')[0]
                    _topic.hyponyms()
                    if _topic.lin_similarity(_word, brown_ic) > best_f:
                        best_f = _topic.lin_similarity(_word, brown_ic)
                        best_str = _t
                tops.append(best_str)
        cnt = collections.Counter()
        for _best_in_tops in tops:
            cnt[_best_in_tops] += 1
        print("TOPIC: " + str(cnt.most_common(1)[0][0]))
        return topics.index(str(cnt.most_common(1)[0][0]))
