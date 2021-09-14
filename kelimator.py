# kelimator main kod dosyasi
#git comment
import pygame
import random as rd
from pygame import transform
from pygame import key
from pygame.constants import *
from pygame.locals import *
import pandas as pd
import time as ti
import tkinter as tk
root = tk.Tk()


# pygame.mixer.pre_init(44100, 16, 2, 4096)
pygame.mixer.init()
pygame.init()


# defining constants
SCREEN_SIZE = WIDTH, HEIGHT = (
    root.winfo_screenwidth(), root.winfo_screenheight())
FPS = 30
NUMBER_OF_LETTERS = 8
COUNTDOWN_TIME = 60
MISSED_WORDS_COUNTDOWN = 10
VOWEL_LIST1 = ["a", "e", "ı", "i", "o"]
VOWEL_LIST2 = ["u", "ü", "ö"]
SURD_LIST1 = [
    "r",
    "t",
    "y",
    "p",
    "s",
    "d",
    "h",
    "k",
    "c",
    "b",
    "n",
    "m",
]
SURD_LIST2 = [
    "ğ",
    "ş",
    "ç",
    "z",
    "f",
    "g",
    "l",
    "v",
    "j",
]

# defining events
CORRECT_GUESS = pygame.USEREVENT + 1
UNCORRECT_GUESS = pygame.USEREVENT + 2
USED_GUESS = pygame.USEREVENT + 3
pygame.event.set_allowed(
    [QUIT, KEYDOWN, CORRECT_GUESS, UNCORRECT_GUESS, USED_GUESS])


# file operations - from txt to pandas dataframe
letters = VOWEL_LIST1 + VOWEL_LIST2 + SURD_LIST1 + SURD_LIST2

letterIdxDict = {}

for letter in letters:
    letterIdxDict[letter] = letters.index(letter)

zeros = [0 for i in range(29)]

t1 = ti.time()
dic = {}


for letter in letters:
    file_name = "./words/" + str(letter).upper() + ".txt"
    with open(file_name, "r") as t:
        for word in t:
            data = word.strip()
            if " " in data or len(data) < 3:
                continue
            dic[data] = zeros.copy()
            check = True

            for letter in data:
                if letter in letterIdxDict:
                    idx = letterIdxDict[str(letter)]
                    if dic[data][idx] == 0:
                        dic[data][idx] = 1
                    else:
                        del dic[data]
                        break
                else:
                    del dic[data]
                    break


df = pd.DataFrame.from_dict(dic, orient="index")

df.columns = letters
t5 = ti.time()
print(t5 - t1)
print(df.shape[0])


# defining colors
BLACK = (0, 0, 0)

RED = (255, 0, 0)
BLUE = (19, 147, 220)
PURPLE = (149, 35, 206)
SCORE_COLOR = (165, 41, 43)


# initializing pygame display variables
WIN = pygame.display.set_mode(SCREEN_SIZE, pygame.FULLSCREEN)
STARTING_BACKGROUND = pygame.transform.scale(
    pygame.image.load("./images/starting.jpeg").convert(), (WIDTH, HEIGHT)
)
GAME_BACKGROUND = pygame.transform.scale(
    pygame.image.load("./images/game.jpeg").convert(), (WIDTH, HEIGHT)
)
LETTERS_TABLE = pygame.transform.scale(
    pygame.image.load("./images/harfler.png").convert(), (800, 120)
)

MISSED_WORDS_BACKGROUND = pygame.transform.scale(
    pygame.image.load("./images/blue.jpeg").convert(), (WIDTH, HEIGHT)
)

AFTER_ROUND_BACKGROUND = pygame.transform.scale(
    pygame.image.load("./images/tutorialPage.jpeg").convert(), (WIDTH, HEIGHT)
)

TUTORIAL_PAGE_BACKGROUND = pygame.transform.scale(
    pygame.image.load("./images/manLandscape.jpeg").convert(), (WIDTH, HEIGHT)
)

GUESS_TABLE = pygame.transform.scale(
    pygame.image.load("./images/tahminler.png").convert(), (800, 512)
)

WRITING_TABLE = pygame.transform.scale(
    pygame.image.load("./images/yazi.png").convert(), (800, 70)
)


tutorialWidth = int(WIDTH * 0.5)
tutorialHeight = int(0.625 * tutorialWidth)
TUTORIAL_GENERAL = pygame.transform.scale(
    pygame.image.load("./images/tutorial.png").convert(),
    (tutorialWidth, tutorialHeight),
)


# initializing font
pygame.font.init()
pygame.display.set_caption("Kelimatör")
welcome_font = pygame.font.SysFont("georgia", 60)
message_font = pygame.font.SysFont("georgia", 30)
title_font = pygame.font.SysFont("georgia", 80)
letter_font = pygame.font.SysFont("georgia", 40)

# initializing sound
goodGuess = pygame.mixer.Sound("./sounds/goodGuess.mp3")
badGuess = pygame.mixer.Sound("./sounds/badGuess.mp3")
background = pygame.mixer.Sound("./sounds/background.mp3")

# helper functions will be defined from there
def displayStartingScreen():
    WIN.blit(STARTING_BACKGROUND, (0, 0))
    welcome_message = welcome_font.render("Kelimatöre Hoşgeldiniz", 1, BLACK)
    WIN.blit(welcome_message, (WIDTH / 6, 2 * HEIGHT / 3))

    space_message = message_font.render("(SPACE'e basın)", 2, BLACK)
    WIN.blit(space_message, (WIDTH / 5, HEIGHT * 3 / 4))

    pygame.display.update()


def drawMainGameWindow(
    letList, word, isUsed, wordList, score, guessReaction, time, noOfWords
):
    WIN.blit(GAME_BACKGROUND, (0, 0))
    title = title_font.render("Kelimatör", 1, BLACK)
    WIN.blit(title, (40, 40))
    WIN.blit(LETTERS_TABLE, (WIDTH * 7 / 10 -
             LETTERS_TABLE.get_width() / 2, 20))
    WIN.blit(
        GUESS_TABLE,
        (WIDTH * 7 / 10 - GUESS_TABLE.get_width() /
         2, 40 + LETTERS_TABLE.get_height()),
    )
    WIN.blit(
        WRITING_TABLE,
        (
            WIDTH * 7 / 10 - GUESS_TABLE.get_width() / 2,
            60 + LETTERS_TABLE.get_height() + GUESS_TABLE.get_height(),
        ),
    )
    userGuess = letter_font.render(word, 1, BLACK)
    WIN.blit(
        userGuess,
        (
            WIDTH * 7 / 10 - GUESS_TABLE.get_width() / 2 + 10,
            60 + LETTERS_TABLE.get_height() + GUESS_TABLE.get_height(),
        ),
    )
    score_title = letter_font.render("Puan", 1, SCORE_COLOR)
    WIN.blit(
        score_title,
        (WIDTH * 2 / 5 - score_title.get_width() / 2 - 60, HEIGHT * 7 / 10 + 5,),
    )
    score_count = letter_font.render(str(score), 1, SCORE_COLOR)
    WIN.blit(
        score_count,
        (WIDTH * 2 / 5 - score_count.get_width() / 2 - 60, HEIGHT * 7 / 10 + 35,),
    )

    reaction_message = message_font.render(guessReaction, 1, BLUE)

    WIN.blit(
        reaction_message,
        (
            WIDTH * 19 / 20 - reaction_message.get_width() + 15,
            60
            + LETTERS_TABLE.get_height()
            + GUESS_TABLE.get_height()
            + WRITING_TABLE.get_height() / 2
            - reaction_message.get_height() / 2,
        ),
    )
    countdown_title = letter_font.render("Zaman", 1, SCORE_COLOR)
    WIN.blit(
        countdown_title,
        (WIDTH * 2 / 5 - countdown_title.get_width() / 2 - 60, HEIGHT * 7 / 10 - 115,),
    )

    countdown = letter_font.render(
        str(int(COUNTDOWN_TIME - time)), 1, SCORE_COLOR)
    WIN.blit(
        countdown,
        (WIDTH * 2 / 5 - countdown.get_width() / 2 - 60, HEIGHT * 7 / 10 - 75,),
    )

    num_of_words_left_title = letter_font.render("Kalan", 1, SCORE_COLOR)
    num_of_words_left_title2 = letter_font.render("Kelime", 1, SCORE_COLOR)

    WIN.blit(
        num_of_words_left_title,
        (
            WIDTH * 2 / 5 - num_of_words_left_title.get_width() / 2 - 60,
            HEIGHT * 7 / 10 - 275,
        ),
    )

    WIN.blit(
        num_of_words_left_title2,
        (
            WIDTH * 2 / 5 - num_of_words_left_title2.get_width() / 2 - 60,
            HEIGHT * 7 / 10 - 235,
        ),
    )

    num_of_words_left_value = letter_font.render(
        str(noOfWords), 1, SCORE_COLOR)
    WIN.blit(
        num_of_words_left_value,
        (
            WIDTH * 2 / 5 - num_of_words_left_value.get_width() / 2 - 60,
            HEIGHT * 7 / 10 - 195,
        ),
    )

    for i in range(NUMBER_OF_LETTERS):
        if isUsed[letList[i]]:
            color = RED
        else:
            color = BLACK
        letter = letter_font.render(letList[i], 1, color)
        WIN.blit(
            letter,
            (
                WIDTH * 7 / 10
                - LETTERS_TABLE.get_width() / 2
                + (i + 1) * int(LETTERS_TABLE.get_width() / 9),
                20 + LETTERS_TABLE.get_height() / 2,
            ),
        )

    for x in range(len(wordList)):
        printWord = letter_font.render(wordList[x], 1, BLACK)

        WIN.blit(
            printWord,
            (
                WIDTH * 7 / 10 - GUESS_TABLE.get_width() / 2 + 10 + (200 * (x // 8)),
                100 + LETTERS_TABLE.get_height() + (50 * (x % 8)),
            ),
        )

    pygame.display.update()


def drawMissedWordsDisplay(df):
    WIN.blit(MISSED_WORDS_BACKGROUND, (0, 0))
    idx = 0
    for word in df.index:
        word_txt = letter_font.render(word, 1, BLACK)

        WIN.blit(
            word_txt,
            (WIDTH / 12 + (200 * (idx // 11)), HEIGHT / 10 + (50 * (idx % 11))),
        )

        idx += 1

        if idx == 88:
            break

    noOfWordsLeftStr = "Tahmin edilemeyen kelime sayısı: " + str(df.shape[0])
    noOfWordsLeft = letter_font.render(noOfWordsLeftStr, 1, SCORE_COLOR)
    WIN.blit(
        noOfWordsLeft,
        (
            WIDTH / 2 - noOfWordsLeft.get_width() / 2,
            HEIGHT / 15 - noOfWordsLeft.get_height() / 2,
        ),
    )

    start_game_message = message_font.render(
        "Devam etmek için SPACE'e basın", 1, BLACK)

    WIN.blit(
        start_game_message,
        (
            WIDTH * 19 / 20 - start_game_message.get_width(),
            HEIGHT * 19 / 20 - start_game_message.get_height(),
        ),
    )

    pygame.display.update()


def drawAfterRoundDisplay(score):
    WIN.blit(AFTER_ROUND_BACKGROUND, (0, 0))
    score_message = welcome_font.render("Skorunuz", 1, SCORE_COLOR)
    WIN.blit(
        score_message,
        (
            WIDTH / 5 - score_message.get_width() / 2,
            HEIGHT / 2 - score_message.get_height(),
        ),
    )

    score_value = welcome_font.render(str(score), 1, SCORE_COLOR)
    WIN.blit(
        score_value, (WIDTH / 5 - score_value.get_width() / 2, HEIGHT / 2,),
    )

    space_message = message_font.render(
        "Yeniden oynamak için SPACE'e", 1, BLACK)
    WIN.blit(
        space_message,
        (
            WIDTH * 4 / 5 - space_message.get_width() / 2,
            HEIGHT / 2 - space_message.get_height(),
        ),
    )

    quit_message = message_font.render("Çıkmak için C'ye basın.", 1, BLACK)
    WIN.blit(
        quit_message,
        (
            WIDTH * 4 / 5 - quit_message.get_width() / 2,
            HEIGHT / 2 + space_message.get_height() + 5,
        ),
    )

    pygame.display.update()


def drawTutorialDisplay():
    WIN.blit(TUTORIAL_PAGE_BACKGROUND, (0, 0))
    start_game_message = message_font.render(
        "Başlamak için SPACE'e basın", 1, BLACK)

    WIN.blit(
        start_game_message,
        (
            WIDTH * 19 / 20 - start_game_message.get_width(),
            HEIGHT * 19 / 20 - start_game_message.get_height(),
        ),
    )

    WIN.blit(
        TUTORIAL_GENERAL,
        (WIDTH / 12, HEIGHT * 2 / 5 - TUTORIAL_GENERAL.get_height() / 2,),
    )

    letter_message = message_font.render(
        "Haznendeki harfleri kullanarak", 1, BLACK)
    letter_message2 = message_font.render("kelimeler oluştur", 1, BLACK)
    guesses_message = message_font.render("ENTER'a bas ve doğru", 1, BLACK)
    guesses_message2 = message_font.render(
        "tahminlerini bu kısımdan gör", 1, BLACK)
    writing_message = message_font.render(
        "Kelimenin geçerli olup olmadığını", 1, BLACK)
    writing_message2 = message_font.render(
        "anlık olarak görebilirsin", 1, BLACK)

    messageWidth = int(WIDTH * 2 / 3 - 60)
    WIN.blit(letter_message, (messageWidth, HEIGHT / 6 - 30))

    WIN.blit(letter_message2, (messageWidth, HEIGHT / 6))

    WIN.blit(guesses_message, (messageWidth, HEIGHT / 3 + 30))

    WIN.blit(guesses_message2, (messageWidth, HEIGHT / 3 + 60))

    WIN.blit(writing_message, (messageWidth, HEIGHT * 3 / 5))

    WIN.blit(writing_message2, (messageWidth, HEIGHT * 3 / 5 + 30))

    pygame.display.update()


def isLetterProper(letter, letList, isUsed):
    if letter not in letList:
        return False

    if isUsed[letter]:
        return False

    isUsed[letter] = True
    return True


def userKeyboardInput(key, word, isUsed, letters, wordList, df):
    if key[K_e] and isLetterProper("e", letters, isUsed):
        word += "e"
    if key[K_r] and isLetterProper("r", letters, isUsed):
        word += "r"
    if key[K_t] and isLetterProper("t", letters, isUsed):
        word += "t"
    if key[K_y] and isLetterProper("y", letters, isUsed):
        word += "y"
    if key[K_u] and isLetterProper("u", letters, isUsed):
        word += "u"
    if key[K_i] and isLetterProper("ı", letters, isUsed):
        word += "ı"
    if key[K_o] and isLetterProper("o", letters, isUsed):
        word += "o"
    if key[K_p] and isLetterProper("p", letters, isUsed):
        word += "p"
    if key[K_LEFTBRACKET] and isLetterProper("ğ", letters, isUsed):
        word += "ğ"
    if key[K_RIGHTBRACKET] and isLetterProper("ü", letters, isUsed):
        word += "ü"
    if key[K_a] and isLetterProper("a", letters, isUsed):
        word += "a"
    if key[K_s] and isLetterProper("s", letters, isUsed):
        word += "s"
    if key[K_d] and isLetterProper("d", letters, isUsed):
        word += "d"
    if key[K_f] and isLetterProper("f", letters, isUsed):
        word += "f"
    if key[K_g] and isLetterProper("g", letters, isUsed):
        word += "g"
    if key[K_h] and isLetterProper("h", letters, isUsed):
        word += "h"
    if key[K_j] and isLetterProper("j", letters, isUsed):
        word += "j"
    if key[K_k] and isLetterProper("k", letters, isUsed):
        word += "k"
    if key[K_l] and isLetterProper("l", letters, isUsed):
        word += "l"
    if key[K_SEMICOLON] and isLetterProper("ş", letters, isUsed):
        word += "ş"
    if key[K_QUOTE] and isLetterProper("i", letters, isUsed):
        word += "i"
    if key[K_z] and isLetterProper("z", letters, isUsed):
        word += "z"
    if key[K_c] and isLetterProper("c", letters, isUsed):
        word += "c"
    if key[K_v] and isLetterProper("v", letters, isUsed):
        word += "v"
    if key[K_b] and isLetterProper("b", letters, isUsed):
        word += "b"
    if key[K_n] and isLetterProper("n", letters, isUsed):
        word += "n"
    if key[K_m] and isLetterProper("m", letters, isUsed):
        word += "m"
    if key[K_COMMA] and isLetterProper("ö", letters, isUsed):
        word += "ö"
    if key[K_PERIOD] and isLetterProper("ç", letters, isUsed):
        word += "ç"
    if key[K_RETURN] and len(word) >= 3:
        if word in wordList:
            pygame.event.post(pygame.event.Event(USED_GUESS))
        elif isWordValid(word, letters, df, wordList):
            wordList.insert(len(wordList), word)
            pygame.event.post(pygame.event.Event(CORRECT_GUESS))
        else:
            pygame.event.post(pygame.event.Event(UNCORRECT_GUESS))

        isUsed = resetDictToFalse(isUsed)
        word = ""

    return word, wordList, isUsed


def isWordValid(word, letList, df, wordList):
    letters = letList.copy()
    for letter in word:
        if letter not in letList:
            return False
        else:
            letters.remove(letter)

    if word not in df.index:
        return False

    return True


def resetDictToFalse(dic):
    for key in dic:
        dic[key] = False

    return dic


def isUsedDictCreation(letters):
    isUsed = {}
    for i in range(len(letters)):
        isUsed[str(letters[i])] = False

    return isUsed


def calculateCorrectGuessScore(word):
    score = 0
    for letter in word:
        if letter in VOWEL_LIST1:
            score += 5
        elif letter in VOWEL_LIST2:
            score += 10
        elif letter in SURD_LIST2:
            score += 20
        else:
            score += 40

    return score


def chooseWordsPerLetters(df, letsUserHave, letters):
    df2 = df.copy()
    dic = {}

    for letter in letsUserHave:
        dic[letter] = None

    for letter in letters:
        if letter not in dic:
            df2 = df2.loc[df2[letter] == 0]

    return df2


def createGuessReaction(word, df, wordList):
    if word == "":
        reaction = ""
    elif len(word) < 3:
        reaction = "Kısa kelime!"
    elif word in wordList:
        reaction = "Kullanılmış Kelime!"
    elif word not in df.index:
        reaction = "Geçersiz Kelime!"
    else:
        reaction = "Geçerli Kelime!"

    return reaction


def letterSelection():
    letterList = []
    idxList = []

    # select three from popular vowels
    for i in range(2):
        idx = rd.randint(0, 4)
        while idx in idxList:
            idx = rd.randint(0, 4)
        letterList.append(VOWEL_LIST1[idx])
        idxList.append(idx)

    # select one from unpopular vowels
    idx = rd.randint(0, 2)
    letterList.append(VOWEL_LIST2[idx])

    # empty the index list
    idxList = []

    # select four from popular surds
    for i in range(4):
        idx = rd.randint(0, 11)
        while idx in idxList:
            idx = rd.randint(0, 11)
        letterList.append(SURD_LIST1[idx])
        idxList.append(idx)

    idxList = []

    # select two from unpopular surds
    for i in range(1):
        idx = rd.randint(0, 8)
        while idx in idxList:
            idx = rd.randint(0, 8)
        letterList.append(SURD_LIST2[idx])
        idxList.append(idx)

    return letterList


# main function
def main():
    t2 = ti.time()
    print(t2 - t1)
    clock = pygame.time.Clock()
    firstScreen = True
    afterRoundDisplay = False
    tutorialScreen = True
    background.play(-1)

    while firstScreen:
        clock.tick(FPS)
        displayStartingScreen()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                firstScreen = False
                gameStarts = False

        keysPressed = pygame.key.get_pressed()

        if keysPressed[K_SPACE]:
            firstScreen = False
            run = True
            gameStarts = True

    while tutorialScreen:
        clock.tick(FPS)
        drawTutorialDisplay()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                tutorialScreen = False
                gameStarts = False
            if event.type == pygame.KEYDOWN:
                if event.key == K_SPACE:
                    tutorialScreen = False
                    pygame.display.update()

    while gameStarts:
        clock.tick(FPS)
        pygame.display.update()
        if run:
            # choosing letters and forming data structures for the new round
            letList = letterSelection()
            isUsed = isUsedDictCreation(letList)
            availableWordsDf = chooseWordsPerLetters(df, letList, letters)
            print(availableWordsDf)
            while availableWordsDf.shape[0] < 30 or availableWordsDf.shape[0] > 77:
                letList = letterSelection()
                isUsed = isUsedDictCreation(letList)
                availableWordsDf = chooseWordsPerLetters(df, letList, letters)
                print(availableWordsDf)
            numOfWords = availableWordsDf.shape[0]
            word = ""
            wordList = []
            score = 0
            guessReaction = ""
            running_time = 0

            background.stop()

            start_time = ti.time()

        # round loop
        while run:
            clock.tick(FPS)
            current_time = ti.time()
            running_time = current_time - start_time
            drawMainGameWindow(
                letList,
                word,
                isUsed,
                wordList,
                score,
                guessReaction,
                running_time,
                numOfWords,
            )

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                    gameStarts = False
                    missedWordsDisplay = False
                if event.type == CORRECT_GUESS:
                    pygame.mixer.Sound.play(goodGuess)
                    score += calculateCorrectGuessScore(wordList[-1])
                    numOfWords -= 1
                    availableWordsDf = availableWordsDf.drop(wordList[-1])
                if event.type == UNCORRECT_GUESS:
                    pygame.mixer.Sound.play(badGuess)
                    score -= 30
                if event.type == USED_GUESS:
                    pygame.mixer.Sound.play(badGuess)
                if event.type == pygame.KEYDOWN:
                    if event.key == K_BACKSPACE and len(word) > 0:
                        isUsed[word[-1]] = False
                        word = word[: len(word) - 1]
                    if event.key == K_TAB:
                        run = False
                        gameStarts = False
                        missedWordsDisplay = False

            keysPressed = pygame.key.get_pressed()

            word, wordList, isUsed = userKeyboardInput(
                keysPressed, word, isUsed, letList, wordList, availableWordsDf
            )

            guessReaction = createGuessReaction(
                word, availableWordsDf, wordList)

            if running_time >= COUNTDOWN_TIME:
                run = False
                missedWordsDisplay = True

        # updating the screen
        pygame.display.update()

        beforeMissedGuessTime = ti.time()
        print("no:" + str(numOfWords))

        while missedWordsDisplay:
            clock.tick(FPS)
            currentTimeInMissedGuess = ti.time()

            drawMissedWordsDisplay(availableWordsDf)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    missedWordsDisplay = False
                    afterRoundDisplay = False
                    gameStarts = False
                if event.type == pygame.KEYDOWN:
                    if event.key == K_SPACE:
                        missedWordsDisplay = False
                        afterRoundDisplay = True

        pygame.display.update()

        # out of the round loop, displaying round score and asking for another round
        while afterRoundDisplay:
            clock.tick(FPS)

            drawAfterRoundDisplay(score)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    afterRoundDisplay = False
                    gameStarts = False
                if event.type == pygame.KEYDOWN:
                    if event.key == K_SPACE:
                        run = True
                        afterRoundDisplay = False
                    if event.key == K_c:
                        gameStarts = False
                        afterRoundDisplay = False


# calling the main function
main()
