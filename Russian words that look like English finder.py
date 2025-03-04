import csv

from santizeWords import englishLetters

cyrillicLetters = {}
cyrillicUppercaseLookup = {}
cyrillicLowercaseLookup = {}
bestCyrillicLetters = {}

latinLetters = {}
bestEnglishLetters = {}

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
            similarLooking = row[3]
            lookSoundMismatch = float(row[6])
            looksLikeLatinAlphabet = float(row[8])
            points = (lookSoundMismatch*1.5)+looksLikeLatinAlphabet     #Chose 1.5 to give sound mismatch an extra weight to the points total
            bestCyrillicLetters[cyrillicLowercaseLetter] = points
            cyrillicLetters[cyrillicLowercaseLetter] = {
                'similarLooking': similarLooking,
                'soundsLike': row[4],
                'lookSoundMismatch': lookSoundMismatch,
                'looksLikeOtherAlphabet': looksLikeLatinAlphabet,
                'points': points
            }           #'lowercase': cyrillicLowercaseLetter, 'uppercase': cyrillicLetter, 'identicalLooking': row[2],

            #ALSO DOES THE REVERSE FOR ENGLISH TO CYRILLIC
            if similarLooking:
                englishLetter = similarLooking.upper()      #equivalent to cyrillicLetter = row[0]
                englishLowercaseLetter = englishLetter.lower()
                latinLetters[similarLooking] = {
                    'similarLooking': cyrillicLetter,
                    'lookSoundMismatch': lookSoundMismatch,
                    'looksLikeOtherAlphabet': looksLikeLatinAlphabet,
                    'points': points
                }

                       #'lowercase': englishLowercaseLetter


        rowNumber += 1

#print(russianLetters)

bestCyrillicLetters = {k: v for k, v in sorted(bestCyrillicLetters.items(), key=lambda item: item[1])[::-1]}

#print(bestCyrillicLetters)

#I didn't end up using these thresholds, the list of good words was much shorter than I thought it would be.
mismatchSoundThreshold = 0      #Threshold for how different the words sound, I'll increase it later
acceptableThreshold = 0.3       #Threshold for Cyrillic looking similar to Latin letters, it doesn't consider Russian words with Cyrillic letters below this threshold

#Didn't end up doing this because of how few impressive words there are
    #FIND SIMILAR LOOKING
    #ANY
    #Synonyms
    #Antonyms

englishWords = {}
russianWords = {}

f = open("english-sanitized.txt", "r", encoding='utf8')
for word in f:
    word = word.strip()
    englishWords[word.lower()] = word #Faster than a list
f.close()

f = open("russian-sanitized.txt", "r", encoding='utf8')
for word in f:
    word = word.strip()
    russianWords[word.lower()] = word #Faster than a list
f.close()

def findingWordsLookLikeAnotherLanguage(languageOne, words, letters, lowerIsSameAsUpper, languageTwo, anotherLanguageWords):      #words is language 1 (like Russian), anotherLanguageWords is language 2 (like English)

    upperLowerPasses = 2
    if lowerIsSameAsUpper:
        upperLowerPasses = 1

    wordsRated = {}                         #russianWordsRated = {}
    looksLikeAnotherLanguageWords = []      #looksLikeEnglishWords

    for wordKey in words:            #for wordKey in russianWords:
        languageOneWordsAllLowerUpper = {"lower": "", "upper": ""}

        for i in range(upperLowerPasses):  #Does one pass, or two passes for all upper and lowercase
            languageTwoLookingWord = ""         #englishLookingWord
            word = words[wordKey]
            if i == 1:
                word = word.upper()
            totalPoints = 0
            letterMismatchSoundsPoints = 0
            looksLikeAnotherLanguagePoints = 0      #looksLikeLatinPoints
            skipWord = False
            for letter in word:
                #letterKey = letter.upper()      #letterKey = uppercaseLookup[letter]
                letterKey = letter
                if i == 1:
                    letterKey = letter.upper()
                if letterKey not in letters:
                    skipWord = True
                else:
                    languageTwoLookingLetter = letters[letterKey]["similarLooking"]
                    if not languageTwoLookingLetter:
                        skipWord = True
                    languageTwoLookingWord += languageTwoLookingLetter  #englishLookingLEtter
                    totalPoints += letters[letterKey]["points"]
                    letterMismatchSoundsPoints += letters[letterKey]["lookSoundMismatch"]
                    looksLikeAnotherLanguagePoints += letters[letterKey]["looksLikeOtherAlphabet"]      #"looksLikeOtherAlphabet"

            if i == 0:
                languageOneWordsAllLowerUpper["lower"] = languageTwoLookingWord
            else:
                languageOneWordsAllLowerUpper["upper"] = languageTwoLookingWord

            if not skipWord and languageTwoLookingWord.lower() in anotherLanguageWords and word not in wordsRated and (i == 0 or languageOneWordsAllLowerUpper["lower"] == "" or languageOneWordsAllLowerUpper["lower"] != languageOneWordsAllLowerUpper["upper"].lower()):
                ratedWord = {
                    languageOne+"Word": word,
                    languageTwo+"LookingWord": languageTwoLookingWord,
                    languageTwo+"LookingWordLowercase": languageTwoLookingWord.lower(),
                    "totalPoints": totalPoints,
                    "letterMismatchSoundsPoints": letterMismatchSoundsPoints,
                    "looksLike"+languageTwo.capitalize()+"AlphabetPoints": looksLikeAnotherLanguagePoints
                }
                wordsRated[word] = ratedWord
                looksLikeAnotherLanguageWords.append(ratedWord)
                #print(russianWordsRated[word])

    looksLikeAnotherLanguageWords = sorted(looksLikeAnotherLanguageWords, key=lambda x: x['totalPoints'], reverse=True) #Sort by most points to least      #looksLikeActualEnglishWords = []
    return looksLikeAnotherLanguageWords

looksLikeActualEnglishWords = findingWordsLookLikeAnotherLanguage("russian", russianWords, cyrillicLetters, True, "english", englishWords)
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

print("\n\n-------------------------\n\n")

looksLikeActualRussianWords = findingWordsLookLikeAnotherLanguage("english", englishWords, latinLetters, False, "russian", russianWords)
for wordLine in looksLikeActualRussianWords[:50]:
    print(wordLine)

#Not much for good results for English to Cyrillic other than ТУРФ, which sounds like turf and means turf. Yeah this one's not very good.