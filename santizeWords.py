russianLetters = ['А', 'а', 'Б', 'б', 'В', 'в', 'Г', 'г', 'Д', 'д', 'Е', 'е', 'Ё', 'ё', 'Ж', 'ж', 'З', 'з', 'И', 'и', 'Й', 'й', 'К', 'к', 'Л', 'л', 'М', 'м', 'Н', 'н', 'О', 'о', 'П', 'п', 'Р', 'р', 'С', 'с', 'Т', 'т', 'У', 'у', 'Ф', 'ф', 'Х', 'х', 'Ц', 'ц', 'Ч', 'ч', 'Ш', 'ш', 'Щ', 'щ', 'Ъ', 'ъ', 'Ы', 'ы', 'Ь', 'ь', 'Э', 'э', 'Ю', 'ю', 'Я', 'я']

englishLetters = ['A', 'a', 'B', 'b', 'C', 'c', 'D', 'd', 'E', 'e', 'F', 'f', 'G', 'g', 'H', 'h', 'I', 'i', 'J', 'j', 'K', 'k', 'L', 'l', 'M', 'm', 'N', 'n', 'O', 'o', 'P', 'p', 'Q', 'q', 'R', 'r', 'S', 's', 'T', 't', 'U', 'u', 'V', 'v', 'W', 'w', 'X', 'x', 'Y', 'y', 'Z', 'z']

def santizeWords(fileName, sanitizedWordList, validCharacters, charactersNotInLanguage):
    f = open(fileName, "r", encoding='utf8')
    for word in f:  # Investigatory gathering of letters we might either exclude words that include or to remove from word
        word = word.strip()
        dontAdd = False
        for letter in word:
            if letter not in validCharacters:
                if letter not in charactersNotInLanguage:
                    charactersNotInLanguage.append(letter)
                dontAdd = True
        if not dontAdd:      #Don't add if there are invalid characters
            sanitizedWordList.append(word)
    f.close()

charactersNotInRussian = []     #To Investigate
charactersNotInEnglish = []     #To Investigate

sanitizedEnglishWordList = []
santizeWords("english.txt", sanitizedEnglishWordList, englishLetters, charactersNotInEnglish)
print(charactersNotInEnglish)

with open("english-sanitized.txt", "w", encoding='utf8') as f:
    f.write('\n'.join(sanitizedEnglishWordList))

sanitizedRussianWordList = []

santizeWords("russian.txt", sanitizedRussianWordList, russianLetters, charactersNotInRussian)
print(charactersNotInRussian)

with open("russian-sanitized.txt", "w", encoding='utf8') as f:
    f.write('\n'.join(sanitizedRussianWordList))


