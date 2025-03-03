import csv

cyrillicLetters = {}
cyrillicUppercaseLookup = {}
cyrillicLowercaseLookup = {}

bestCyrillicLetters = {}

russianLetters = []
ignoreWordsWithTheseLetters = ['.', '-']

with open('Russian Cyrillic Letters comapred to English Latin Leters.csv', encoding='utf8') as csvfile:
    reader = csv.reader(csvfile, delimiter=',', quotechar='|')
    rowNumber = 0
    for row in reader:
        if rowNumber != 0:
            cyrillicLetter = row[0]
            cyrillicLowercaseLetter = row[1][1]
            cyrillicUppercaseLookup[cyrillicLowercaseLetter] = cyrillicLetter
            cyrillicLowercaseLookup[cyrillicLetter] = cyrillicLowercaseLetter
            russianLetters.append(cyrillicLetter)
            russianLetters.append(cyrillicLowercaseLetter)
            lookSoundMismatch = float(row[6])
            looksLikeLatinAlphabet = float(row[8])
            points = (lookSoundMismatch*1.5)+looksLikeLatinAlphabet
            bestCyrillicLetters[cyrillicLetter] = points
            cyrillicLetters[cyrillicLetter] = {
                'similarLooking': row[3],
                'soundsLike': row[4],
                'lookSoundMismatch': lookSoundMismatch,
                'looksLikeLatinAlphabet': looksLikeLatinAlphabet,
                'points': points
            }           #'lowercase': cyrillicLowercaseLetter, 'identicalLooking': row[2],
        rowNumber += 1

#print(russianLetters)

bestCyrillicLetters = {k: v for k, v in sorted(bestCyrillicLetters.items(), key=lambda item: item[1])[::-1]}

#print(bestCyrillicLetters)

mismatchSoundThreshold = 0      #Threshold for how different the words sound, I'll increase it later
acceptableThreshold = 0.3       #Threshold for Cyrillic looking similar to Latin letters, it doesn't consider Russian words with Cyrillic letters below this threshold

#FIND SIMILAR LOOKING
#ANY
#Synonyms
#Antonyms

englishWords = {}

f = open("english-sanitized.txt", "r", encoding='utf8')
for word in f:
    word = word.strip().lower()
    englishWords[word] = "" #Faster than a list
f.close()

f = open("russian-sanitized.txt", "r", encoding='utf8')

russianWordsRated = {}
looksLikeActualEnglishWords = []

for word in f:
    word = word.strip()
    englishLookingWord = ""
    totalPoints = 0
    letterMismatchSoundsPoints = 0
    looksLikeLatinPoints = 0
    skipWord = False
    for letter in word:
        letterKey = letter
        if letter in cyrillicLetters:
            pass
        elif letter in cyrillicUppercaseLookup:
            letterKey = cyrillicUppercaseLookup[letter]
        else:
            print(letter)
            CRASH()
        englishLookingLetter = cyrillicLetters[letterKey]["similarLooking"]
        if not englishLookingLetter:
            skipWord = True
        englishLookingWord += englishLookingLetter
        totalPoints += cyrillicLetters[letterKey]["points"]
        letterMismatchSoundsPoints += cyrillicLetters[letterKey]["lookSoundMismatch"]
        looksLikeLatinPoints += cyrillicLetters[letterKey]["looksLikeLatinAlphabet"]
    russianWordsRated[word] = {"russianWord": word, "englishLookingWord": englishLookingWord, "englishLookingWordLowercase": englishLookingWord.lower(), "totalPoints": totalPoints, "letterMismatchSoundsPoints": letterMismatchSoundsPoints, "looksLikeLatinPoints": looksLikeLatinPoints}
    if not skipWord and englishLookingWord.lower() in englishWords:
        looksLikeActualEnglishWords.append(russianWordsRated[word])
        #print(russianWordsRated[word])

f.close()

looksLikeActualEnglishWords = sorted(looksLikeActualEnglishWords, key=lambda x: x['totalPoints'], reverse=True) #Sort by most points to least
for wordLine in looksLikeActualEnglishWords[:200]:
    print(wordLine)

#RESULTS
# щедрой looks like weapon  means generous
# сядь  looks like  creb    means sit down
# фрей  looks like  open    means Norse god of fertility?
# везя  looks like  BEER    means carrying
# ново  looks like  HOBO    means new
# веер  looks like  Beep    means fan
# мочит looks like  MOUNT   means wets
# суди  looks like CYAN     means judge (verb)