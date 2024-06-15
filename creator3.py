from solver import outside_score
import random

def holisticScore(puzzle):
    achievements = outside_score(puzzle)
    totalScore = achievements[0]
    totalMult = 1
    for i in range(1, len(achievements)):
        award = achievements[i]
        if award in {"200M"}:
            totalMult += 0.05
        if award in {"4C"}:
            totalMult += 0.05
        if award in {"PA"}:
            totalMult += 0.05
        if award in {"M8"}:
            totalMult += 0.5
    return totalScore*totalMult

alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
initPuzzle = "INAKGNISDSOARILTHNOAMEUWC"
initPuzzle = "balyedvnstaniauerolckwegf".upper()
rawPuzzle = "AINOSERTLHMCDWKGUYVPFXBJZ"
initPuzzle = "Q Q Q Q Q Q S I Q Q Q A N Q Q Q R O E Q Q Q Q Q Q".replace(" ", "")
initPuzzle = "QQQQQQQIQQQANQQQQQQQQQQQQQ"
initPuzzle = ''.join(random.sample(rawPuzzle, 25))
states = open("states.txt", "r")
two_letter_freq = {}
for state in states:
    state = state.replace("\n", "")
    if not state == "CALIFORNIA":
        for i in range(len(state)-1):
            twoLetter = state[i:i+2]
            if twoLetter in two_letter_freq:
                two_letter_freq[twoLetter] += 1
            else:
                two_letter_freq[twoLetter] = 1
sorted_tlfreq = {k: v for k, v in sorted(two_letter_freq.items(), key=lambda item: item[1], reverse=True)}


initScore = holisticScore(initPuzzle)
finalPuzzle = ""
finalScore = -1
prevInd = -1
prevScore = -1
for loop in range(100):
    maxScore = -1
    maxPuzzle = ""
    newPrevInd = -1
    for i in range(25):
        if not i == prevInd:
            for letter in alphabet:
                if not initPuzzle[i] == letter:
                    tempScore = holisticScore(initPuzzle[:i]+letter+initPuzzle[i+1:])
                    if tempScore > maxScore:
                        maxScore = tempScore
                        maxPuzzle = initPuzzle[:i]+letter+initPuzzle[i+1:]
                        newPrevInd = i
    prevInd = newPrevInd
    if maxScore > finalScore:
        finalScore = maxScore
        finalPuzzle = maxPuzzle
    if maxScore > prevScore:
        initPuzzle = maxPuzzle
        initScore = maxScore
        prevScore = initScore
    else:
        initPuzzle = ""
        initScore = -1
        for i in range(10000):
            puzzle = ''.join(random.sample(maxPuzzle,len(maxPuzzle)))
            score = holisticScore(puzzle)
            if score > initScore:
                initScore = score
                initPuzzle = puzzle
        if initScore > finalScore:
            finalScore = initScore
            finalPuzzle = initPuzzle
        prevScore = initScore

    print(loop)
    print(maxPuzzle)
    print(maxScore)

print("FINAL:")
print(finalPuzzle)
print(finalScore)
# MALSODISGNCARILTHNOAAEISC (219,823,417, 20S, 200M)
# LSATUMICNENOGWARAORDKCLIE (213,224,182, 20S, 400M)
# KGDAUARINDMSOAMWELIHTNNOC (187,029,017, 20S, 4C, NOCAL)
# GDIVTOAIGENLRNWDAOKACHMIS (229,096,877, 20S, 200M)