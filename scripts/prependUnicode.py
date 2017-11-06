fileLines = []
with open('../emojiList.txt', 'r') as file:
    for line in file:
        fileLines.append(line.strip())

with open('../emojiList.txt', 'w+') as file:
    for line in fileLines:
        file.write('U+1F' + line + '\n')