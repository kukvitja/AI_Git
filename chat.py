import random
import json
import sys
from random import randint
import os
import webbrowser
# from RecognizingСommands import *
import keyboard
# import pyautogui
# from pywinauto.application import Application

import torch

from model import NeuralNet
from nltk_fanc import bag_of_words, tokenize

from Include import Sound
from Include.Wikipendia import wiki_search
from funk import *
#
# level_truth = 1
pach_file_train_dataset = "data/traindataset.json"
#
# pach_file_remember = "data/memory.json"



device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

with open('data/talkdata.json', 'r', encoding='utf-8') as json_data:
    dataset = json.load(json_data)

FILE = "data.pt"
data = torch.load(FILE)

input_size = data["input_size"]
hidden_size = data["hidden_size"]
output_size = data["output_size"]
all_words = data['all_words']
names = data['names']
model_state = data["model_state"]

model = NeuralNet(input_size, hidden_size, output_size).to(device)
model.load_state_dict(model_state)
model.eval()

def define_phrase(task):

    sentence = tokenize(task)
    X = bag_of_words(sentence, all_words)
    X = X.reshape(1, X.shape[0])
    X = torch.from_numpy(X).to(device)


    output = model(X)
    _, predicted = torch.max(output, dim=1)
    name = names[predicted.item()]

    probs = torch.softmax(output, dim=1)
    prob = probs[0][predicted.item()]
    print(prob.item())
    if prob.item() > 0.80:
        for intent in dataset['dataset']:
            if name == intent["name"]:
                if intent['action'] != "None":
                    try:
                        task = eval(intent["action"])(arr_text_input=task.split(), question_text=intent['requests'])
                    except:
                        pass
                    if task != None:
                        Sound.talk(task)
                if len(intent['response']) > 0:
                    Sound.talk(random.choice(intent['response']))
                return True

    else:
        print("Записать в тренеровочний файл")
        remember_data(task,task,pach_file_train_dataset)
        with open('data/newdataset.txt', 'w', encoding='utf-8') as f:
            f.write(task)
            f.close()
        return False

def print_pressed_keys(e):

    if e.name == '`' or e.name == '\'' or e.name == 'ё':
        # start_new_thread()
        Sound.talk('я слушаю')
        tasks = Sound.write()
        # Команди роботи
        if 'напомни' in tasks:
            Sound.talk(get_remember(pach_file_remember = pach_file_remember, arr_text_input=tasks.split()))
        # Розговор на осносе датасет
        elif define_phrase(tasks):
            pass
        # elif 'напомни' in tasks or 'когда' in tasks:
        #     Sound.talk(get_remember(pach_file_remember = pach_file_remember, arr_text_input=tasks.split()))
        # Розговор на основі даних питання відповідь


        # Отговорки коли не знає що відповісти
        else:
            Sound.talk(random.choice(dataset['answers_know']))
    elif e.name == 'esc':
        print('You Pressed A Key!')



if __name__ == '__main__':
    # keyboard.on_release(print_pressed_keys)
    # keyboard.wait()
    while True:
        Sound.talk('я слушаю')
        tasks = Sound.write()

        if 'напомни' in tasks:
            Sound.talk(get_remember(pach_file_remember=pach_file_remember, arr_text_input=tasks.split()))

        elif "интересное" in tasks:
            driver = init_driver()
            stories = talk_storis(driver)
            Sound.talk(stories)
        elif "приготовься к работе" in tasks:
            Sound.talk("Выполняю. Можеш пока по курить. Я всё сделаю")
            start_main_work()
        elif "сканировать" in tasks or "сканируй" in tasks:
            Sound.talk("Сканирую")
            scanner()
        elif "открой браузер" in tasks:
            Sound.talk("Открываю")
            os.startfile(r'C:\Program Files (x86)\Google\Chrome\Application\chrome.exe')
        elif "открой документы" in tasks:
            Sound.talk("Открываю")
            os.startfile(r"C:\Users\Viktor\Documents\Doky")
        elif "открой рабочую папку" in tasks:
            Sound.talk("Открываю")
            os.startfile(r"C:\Users\Viktor\Documents\Work")
        elif "обнови declaration" in tasks:
            Sound.talk("Обновляю Подождите")
            os.system(r'D:\MasterD\MDUPDATE.exe a')
        elif "открой declaration" in tasks:
            Sound.talk("Открываю програму")
            os.startfile(r'D:\MasterD\MD-Declaration\DeclPlus.exe')
        elif "открой мой сайт" in tasks:
            Sound.talk("Открываю Брокер кх")
            webbrowser.open_new('https://www.brokerkh.net.ua/')
        elif "закрой declaration" in tasks:
            Sound.talk("Закрываю")
            os.system('TASKKILL /IM DeclPlus.exe')
        elif "закрой браузер" in tasks:
            Sound.talk("Закрываю")
            os.system('TASKKILL /IM chrome.exe')
        elif "сверни всё" in tasks or "сверни все окна" in tasks:
            Sound.talk("Свертаю все окна")
            pyautogui.hotkey('winleft', 'd')
        elif "найди" in tasks or "найти" in tasks:
            search(tasks)
            Sound.talk("Вот что я нашла")
        # elif "пока" in tasks:
        #     Sound.talk("Пока мой повелитель")
        #     sys.exit()
        elif "выключить комп" in tasks or "выключи комп" in tasks:
            Sound.talk("Выключаю")
            os.system('shutdown -s')

        elif define_phrase(tasks):
            pass

        else:
            Sound.talk(random.choice(dataset['answers_know']))
