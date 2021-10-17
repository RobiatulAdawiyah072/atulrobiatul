# import Sastrawi package
import string
import csv
import re #regex library
from Sastrawi.Stemmer.StemmerFactory import StemmerFactory
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize 
from nltk.probability import FreqDist

from modulenorm.modNormalize import normalize
from modulenorm.modTokenizing import tokenize



# sentence input
sentence = "Siang bunda benar adeknya bernama fahmi benar dok untuk imunisasi ya iya dok apakah nanti badanya panas dok bunda gak perlu kawatir nanti panasnya cuman sebentar kok bisa dikompres biar cepet reda panasnya terima kasih dok"




# ------ Case Folding --------
# gunakan fungsi .lower()
lowercase_sentence = sentence.lower()

print('Case Folding Result : \n')
print(lowercase_sentence)
print('\n\n\n')

#normalisasi text
def normalisasi(text):
	text = text.encode("utf-8")
	text_decode = str(text.decode("utf-8"))

	# isisialisasi modul normalisasi dari folder modulnorm/modNormalize
	# isinya normalisasi: lower, repeat char, space char, link, emoticon, ellipsis, spell
	usenorm = normalize()

	# normalisasi enter, 1 revw 1 baris
	text_norm = usenorm.enterNormalize(text_decode) 
	# normalisasi spesial char
	text_norm = "".join([x for x in text_norm if ord(x)<128])
	# normalisasi titik yang berulang
	text_norm = usenorm.repeatcharNormalize(text_norm) 
	# normalisasi link dalam text
	text_norm = usenorm.linkNormalize(text_norm) 
	# normalisasi spasi karakter
	text_norm = usenorm.spacecharNormalize(text_norm)
	# normalisasi karakter elepsis (…) 
	text_norm = usenorm.ellipsisNormalize(text_norm)
	# hapus kutip jika ada
	text_norm = text_norm.replace("'", "")

	# panggil modul tokenisasi untuk persiapan tokenisasi
	tok = tokenize() 
	# pisah tiap kata pada kalimat
	text_norm = tok.WordTokenize(text_norm) 

	# cek spell dari kata perkata
	text_norm = usenorm.spellNormalize(text_norm) 
	# menyambung kata (malam-malam) (param: textlist, jmlh_loop)
	text_norm = usenorm.wordcNormalize(text_norm,2) 
	# menggabung kalimat tokenize dengan separate spasi
	text_norm = ' '.join(text_norm) 
	# menggabung struktur emoticon yang terpisah ([: - )] = [:-)])
	text_norm = usenorm.emoticonNormalize(text_norm) 

	# kembalikan hasil normalisasi
	return text_norm
# Eksekusi #
# inisialisasi file yang akan dinormalisasi
target = "normalisasi.csv";

# buka file csv
with open(target, encoding = "ISO-8859-1") as csvfile:
	# beritahu, kolom dalam csv dipisah dengan pipe (|)
	readCSV = csv.reader(csvfile, delimiter='|')
	# untuk tiap baris data dalam csv lakukan perulangan
	for text in readCSV:

		# ambil text asli
		text_asli = text[0]
		# lakukan normalisasi dari text asli
		text_normalized = normalisasi(text_asli)

		# tampilkan hasil normalisasi text
		print("Word Normalisation")
		#print("text asli: "+text_asli)
		print("text normalisasi: "+text_normalized)
# ------ Tokenizing ---------
#remove angka
lowercase_sentence = re.sub(r"\d+", "", lowercase_sentence)

#remove punctuation
lowercase_sentence = lowercase_sentence.translate(str.maketrans("","",string.punctuation))

#remove whitespace leading & trailing
lowercase_sentence = lowercase_sentence.strip()

#remove multiple whitespace into single whitespace
lowercase_sentence = re.sub('\s+',' ',lowercase_sentence)


tokens = word_tokenize(lowercase_sentence)

#print('Tokenizing Result : \n') 
#print(tokens)
#print('\n\n\n')

freq_tokens = FreqDist(tokens)

#print('Frequency Tokens : \n') 
#print(freq_tokens.most_common())

# get Indonesian stopword 
list_stopwords = set(stopwords.words('indonesian'))

#remove stopword pada list token
tokens_without_stopword = [word for word in freq_tokens if not word in list_stopwords]


#print(tokens_without_stopword)
# create stemmer
factory = StemmerFactory()
stemmer = factory.create_stemmer()

# token without stopword
list_tokens = tokens_without_stopword

# stem
output   = [(token + " : " + stemmer.stem(token)) for token in list_tokens]
print ("***************")
print("Hasil stem :",output)

#Stopword removal

def stopwordremove():
    stop = set(stopwords.words('indonesian'))
    
    print ("--------Stop word removal from raw text---------")
    print (" ".join([i for i in sentence.lower().split() if i not in stop]))

if __name__ == "__main__":
    stopwordremove()
