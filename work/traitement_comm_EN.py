#!/usr/bin/python

from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
from nltk.corpus import stopwords
import pandas as pd
import numpy as np 
import spacy
import nltk
import re

nltk.download('averaged_perceptron_tagger')
nltk.download('punkt')
nlp = spacy.load("en_core_web_sm")
lemmer = WordNetLemmatizer()
ex = ["Superbly played film set in 1946 , a bright young New England banker is convicted of the slayings of his spouse and her lover and sentenced to life at a strict State Prison . Introspective and quite Andy (Tim Robbins) gradually befriends inmates and over the next 2 decades wins the trust of prisoners and wardens but in his heart he still yearns for freedom . There he forms a peculiar friendship with Red (Morgan Freeman), the prison fixer , he experiences the brutality of prison life with a sadistic head guard (Clancy Brown), and is also mistreated and raped ; however , he adapts himself and offers financial advice to the guards and the selfish governor (Bob Gunton) , all in a shot 19 years. As two imprisoned men bond over a number of years, finding peace and redemption through acts of common help , friendship and decency . But when the proof of Andy's innocence is ripped away by those who need his services ,we learn that all is not quite what it seems at this State Penitentary , provoking a few susprises in the last two reels .\n\nThis is a very good and serious prison movie with thrills , emotion , exciting scenes , colour-blind relationships , hardnut camaraderie , gang opression , and violent disavowal of any homosexual implications . Prison buffs will find a lot of incidents to relish and the great spiritual resolution takes some swallowing and unexpected surprises . Adapted from the novella \u00a8Rita Hayworth and Shawshank redemption\u00a8 ; the twist here is the upright starring is exceptionally bright , as his ability with accountancy leads to his handling the finances of everyone , from the humblest guard to the prison boss . Wonderful spectacle in watching time-passer while changing the bombshell actresses of the history : Rita Hayworth , Marilyn Monroe , Raquel Welch ."]

# Liste de stopWords par défaut
stopWords = nlp.Defaults.stop_words

# On ajoute les notres (liste de countwordsfree spécialisée en text processing)
new_stop_words = ["able","about","above","abroad","according","accordingly","across","actually","adj","after","afterwards","again","against","ago","ahead","ain't","all","allow","allows","almost","alone","along","alongside","already","also","although","always","am","amid","amidst","among","amongst","an","and","another","any","anybody","anyhow","anyone","anything","anyway","anyways","anywhere","apart","appear","appreciate","appropriate","are","aren't","around","as","a's","aside","ask","asking","associated","at","available","away","awfully","back","backward","backwards","be","became","because","become","becomes","becoming","been","before","beforehand","begin","behind","being","believe","below","beside","besides","best","better","between","beyond","both","brief","but","by","came","can","cannot","cant","can't","caption","cause","causes","certain","certainly","changes","clearly","c'mon","co","co.","com","come","comes","concerning","consequently","consider","considering","contain","containing","contains","corresponding","could","couldn't","course","c's","currently","dare","daren't","definitely","described","despite","did","didn't","different","directly","do","does","doesn't","doing","done","don't","down","downwards","during","each","edu","eg","eight","eighty","either","else","elsewhere","end","ending","enough","entirely","especially","et","etc","even","ever","evermore","every","everybody","everyone","everything","everywhere","ex","exactly","example","except","fairly","far","farther","few","fewer","fifth","first","five","followed","following","follows","for","forever","former","formerly","forth","forward","found","four","from","further","furthermore","get","gets","getting","given","gives","go","goes","going","gone","got","gotten","greetings","had","hadn't","half","happens","hardly","has","hasn't","have","haven't","having","he","he'd","he'll","hello","help","hence","her","here","hereafter","hereby","herein","here's","hereupon","hers","herself","he's","hi","him","himself","his","hither","hopefully","how","howbeit","however","hundred","i'd","ie","if","ignored","i'll","i'm","immediate","in","inasmuch","inc","inc.","indeed","indicate","indicated","indicates","inner","inside","insofar","instead","into","inward","is","isn't","it","it'd","it'll","its","it's","itself","i've","just","k","keep","keeps","kept","know","known","knows","last","lately","later","latter","latterly","least","less","lest","let","let's","like","liked","likely","likewise","little","look","looking","looks","low","lower","ltd","made","mainly","make","makes","many","may","maybe","mayn't","me","mean","meantime","meanwhile","merely","might","mightn't","mine","minus","miss","more","moreover","most","mostly","mr","mrs","much","must","mustn't","my","myself","name","namely","nd","near","nearly","necessary","need","needn't","needs","neither","never","neverf","neverless","nevertheless","new","next","nine","ninety","no","nobody","non","none","nonetheless","noone","no-one","nor","normally","not","nothing","notwithstanding","novel","now","nowhere","obviously","of","off","often","oh","ok","okay","old","on","once","one","ones","one's","only","onto","opposite","or","other","others","otherwise","ought","oughtn't","our","ours","ourselves","out","outside","over","overall","own","particular","particularly","past","per","perhaps","placed","please","plus","possible","presumably","probably","provided","provides","que","quite","qv","rather","rd","re","really","reasonably","recent","recently","regarding","regardless","regards","relatively","respectively","right","round","said","same","saw","say","saying","says","second","secondly","see","seeing","seem","seemed","seeming","seems","seen","self","selves","sensible","sent","serious","seriously","seven","several","shall","shan't","she","she'd","she'll","she's","should","shouldn't","since","six","so","some","somebody","someday","somehow","someone","something","sometime","sometimes","somewhat","somewhere","soon","sorry","specified","specify","specifying","still","sub","such","sup","sure","take","taken","taking","tell","tends","th","than","thank","thanks","thanx","that","that'll","thats","that's","that've","the","their","theirs","them","themselves","then","thence","there","thereafter","thereby","there'd","therefore","therein","there'll","there're","theres","there's","thereupon","there've","these","they","they'd","they'll","they're","they've","thing","things","think","third","thirty","this","thorough","thoroughly","those","though","three","through","throughout","thru","thus","till","to","together","too","took","toward","towards","tried","tries","truly","try","trying","t's","twice","two","un","under","underneath","undoing","unfortunately","unless","unlike","unlikely","until","unto","up","upon","upwards","us","use","used","useful","uses","using","usually","v","value","various","versus","very","via","viz","vs","want","wants","was","wasn't","way","we","we'd","welcome","well","we'll","went","were","we're","weren't","we've","what","whatever","what'll","what's","what've","when","whence","whenever","where","whereafter","whereas","whereby","wherein","where's","whereupon","wherever","whether","which","whichever","while","whilst","whither","who","who'd","whoever","whole","who'll","whom","whomever","who's","whose","why","will","willing","wish","with","within","without","wonder","won't","would","wouldn't","yes","yet","you","you'd","you'll","your","you're","yours","yourself","yourselves","you've","zero","a","how's","i","when's","why's","b","c","d","e","f","g","h","j","l","m","n","o","p","q","r","s","t","u","uucp","w","x","y","z","I","www","amount","bill","bottom","call","computer","con","couldnt","cry","de","describe","detail","due","eleven","empty","fifteen","fifty","fill","find","fire","forty","front","full","give","hasnt","herse","himse","interest","itse”","mill","move","myse”","part","put","show","side","sincere","sixty","system","ten","thick","thin","top","twelve","twenty","abst","accordance","act","added","adopted","affected","affecting","affects","ah","announce","anymore","apparently","approximately","aren","arent","arise","auth","beginning","beginnings","begins","biol","briefly","ca","date","ed","effect","et-al","ff","fix","gave","giving","heres","hes","hid","home","id","im","immediately","importance","important","index","information","invention","itd","keys","kg","km","largely","lets","line","'ll","means","mg","million","ml","mug","na","nay","necessarily","nos","noted","obtain","obtained","omitted","ord","owing","page","pages","poorly","possibly","potentially","pp","predominantly","present","previously","primarily","promptly","proud","quickly","ran","readily","ref","refs","related","research","resulted","resulting","results","run","sec","section","shed","shes","showed","shown","showns","shows","significant","significantly","similar","similarly","slightly","somethan","specifically","state","states","stop","strongly","substantially","successfully","sufficiently","suggest","thered","thereof","therere","thereto","theyd","theyre","thou","thoughh","thousand","throug","til","tip","ts","ups","usefully","usefulness","'ve","vol","vols","wed","whats","wheres","whim","whod","whos","widely","words","world","youd","youre"]

for word in new_stop_words:
    stopWords.add(word)

def tokenise(comment):
    # Enlève tout ce qui n'est pas mot ou espace
    comm = re.sub(r"[^\w\s]'",'',comment)
    # Conserve les caractères importants
    comm = re.sub('[^a-zA-Zàèéêîïâäëôö0-9 ]', '', comm)
    # Enlève les caractères en double
    comm = re.sub('(.)\\1{2,}', "\\1", comm)
    # Tout en minuscule
    comm = comm.lower()
    # Tokeniser la phrase
    doc = nlp(comm)
    # Retourner le texte de chaque token
    token_comm =  ' '.join([X.text for X in doc])
    return(token_comm)

# Suppression des stopWords
def stop_word(comment):
    com = word_tokenize(comment)
    words = ''
    for x in com:
        words = ' '.join([word for word in com if x not in set(stopWords)])
    return(words)

# Supprimer les noms propres
def sup_np(comment):
    tag_com = nltk.tag.pos_tag(comment.split())
    com_sup_np = [word for word, tag in tag_com if tag != 'NNP' and tag != 'NNPS']
    com = ' '.join(com_sup_np)
    return(com)

# Lemmatisation
def lemming(comment):
    doc = nlp(comment)
    lemmatized_com = ' '.join([token.lemma_ for token in doc])
    return(lemmatized_com)

def main(comment):
    com = sup_np(comment)
    com = tokenise(com)
    com = lemming(com)
    com = stop_word(com)
    com = ' '.join(com.split())
    return(com)

if __name__ == "__main__":
    main()