import random
from kivy.config import Config
Config.set('graphics','resizable', False)
Config.write()
from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.gridlayout import GridLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.core.text import LabelBase
from kivy.uix.screenmanager import *
from kivy.lang import Builder
from kivy.core.window import Window
import pickle

Window.size = (400, 700)
LabelBase.register(name = 'Mono', fn_regular='free-mono-gras.otf')

with open('diff_1.pickle', 'rb') as file:
    diff_1_questions = pickle.load(file)
    file.close()

with open('diff_2.pickle', 'rb') as file:
    diff_2_questions = pickle.load(file)
    file.close()

with open('diff_3.pickle', 'rb') as file:
    diff_3_questions = pickle.load(file)
    file.close()

correct = 0

def find_list(dictionary):
    q = []
    for i in dictionary.keys():
        q.append(i)
    return q


def generate_question(q):
    res = []
    for i in range(0, 10):
        a = random.choice(q)
        res.append(a)
        q.remove(a)
    return res


def generate_anwers(questions, dictionary):
    all_answers = []
    for i in range(0, 10):
        current_answers = dictionary[questions[i]]['incorrect']
        current_answers.append(dictionary[questions[i]]['correct'])
        current_answers = sorted(current_answers, key=lambda x:random.random())
        all_answers.append(current_answers)
    return all_answers

def results_easy(count):
    main_text =  f'Ты ответил правильно на {count} вопросов из 10'
    if 0 <= count <= 3:
        main_text += '\nНе расстраивайся, в следующий раз у тебя всё получится. \nПопробуй ещё раз'
    if 3 < count <= 6:
        main_text += '\nТы показал достойный результат, но пора покорять новые галактики!'
    if 6 < count <= 10:
        main_text += '\nПоздравляю! Первый уровень пройден. \nДвигайся к новым знаниям!'
    return main_text

def results_medium(count):
    main_text = f'Ты ответил правильно на {count} вопросов из 10'
    if 0 <= count <= 3:
        main_text += '\nНе расстраивайся, в следующий раз у тебя всё получится. \nПопробуй ещё раз'
    if 3 < count <= 6:
        main_text += '\nТы показал достойный результат, но пора покорять новые галактики!'
    if 6 < count <= 10:
        main_text += '\nПоздравляю! Твои знания о космосе впечетляют, но ты можешь больше - стать "Космическим Гением"'
    return main_text

def results_hard(count):
    main_text = f'Ты ответил правильно на {count} вопросов из 10'
    if 0 <= count <= 3:
        main_text += '\nНе расстраивайся, в следующий раз у тебя всё получится. \nПопробуй ещё раз'
    if 3 < count <= 6:
        main_text += '\nТы показал достойный результат, но пора покорять новые галактики!'
    if 6 < count <= 10:
        main_text += '\nПоздравляю! Теперь ты - "Космический Гений"\nТвои знания в области астрономии превосходны. \nТеперь тебе не страшны никакие Вселенские испытания'
    return main_text


questions_1 = find_list(diff_1_questions)
questions_1 = generate_question(questions_1)
answers_1 = generate_anwers(questions_1, diff_1_questions)
questions_2 = find_list(diff_2_questions)
questions_2 = generate_question(questions_2)
answers_2 = generate_anwers(questions_2, diff_2_questions)
questions_3 = find_list(diff_3_questions)
questions_3 = generate_question(questions_3)
answers_3 = generate_anwers(questions_3, diff_3_questions)

class Quiz(App):
    def build(self):
        sm = ScreenManager(transition = NoTransition())
        sm.add_widget(MainScreen(name = 'MainScreen'))
        sm.add_widget(ChooseDifficulty(name ='ChooseDifficulty'))
        sm.add_widget(Diff1Screen(name='Diff1Screen'))
        sm.add_widget(diff_2_screen(name='diff_2_screen'))
        sm.add_widget(diff_3_screen(name='diff_3_screen'))
        return sm

class ChooseDifficulty(Screen):
    def diff_1(self):
        self.manager.current = 'Diff1Screen'

    def diff_2(self):
        self.manager.current = 'diff_2_screen'

    def diff_3(self):
        self.manager.current = 'diff_3_screen'


class MainScreen(Screen):
    pass
class Diff1Screen(Screen):
    def __init__(self, **kwargs):
        super(Diff1Screen, self).__init__(**kwargs)
        global questions_1
        global answers_1
        global diff_1_questions

        self.cur_number = 0
        self.ans_1 = answers_1[self.cur_number][0]
        self.ans_2 = answers_1[self.cur_number][1]
        self.ans_3 = answers_1[self.cur_number][2]
        self.ans_4 = answers_1[self.cur_number][3]
        self.label_text = diff_1_questions[questions_1[self.cur_number]]['question']

        self.layout = BoxLayout(orientation="vertical", padding=(0, 0, 0, 100), spacing=20)
        self.buttons = GridLayout(spacing=30, size_hint=(0.9, 1), pos_hint={'center_x': 0.5}, cols=1)
        self.add_widget(self.layout)
        self.question = Label(text = self.label_text, font_name = 'Mono', text_size = (self.width * 3, None), halign = 'center', font_size = 25, pos_hint = {'center_x': 0.5})

        self.ans_1_b = Button(text=self.ans_1, font_name = 'Mono', font_size = 20, background_color = (134/255, 180/255, 230/255, 1), on_press=lambda instance: self.check_and_next(self.ans_1))
        self.ans_2_b = Button(text=self.ans_2, font_name = 'Mono',font_size = 20,background_color = (134/255, 180/255, 230/255, 1),on_press=lambda instance: self.check_and_next(self.ans_2))
        self.ans_3_b = Button(text=self.ans_3, font_name = 'Mono',font_size = 20, background_color = (134/255, 180/255, 230/255, 1),on_press=lambda instance: self.check_and_next(self.ans_3))
        self.ans_4_b = Button(text=self.ans_4, font_name = 'Mono',font_size = 20,background_color = (134/255, 180/255, 230/255, 1),on_press=lambda instance: self.check_and_next(self.ans_4))

        self.layout.add_widget(self.question)
        self.buttons.add_widget(self.ans_1_b)
        self.buttons.add_widget(self.ans_2_b)
        self.buttons.add_widget(self.ans_3_b)
        self.buttons.add_widget(self.ans_4_b)
        self.layout.add_widget(self.buttons)


    def check_and_next(self, button_text):
        global correct
        if button_text == diff_1_questions[questions_1[self.cur_number]]['correct']:
            correct += 1
        self.cur_number += 1
        if self.cur_number <= 9:
            self.label_text = diff_1_questions[questions_1[self.cur_number]]['question']
            self.question.text = self.label_text
            self.ans_1 = answers_1[self.cur_number][0]
            self.ans_2 = answers_1[self.cur_number][1]
            self.ans_3 = answers_1[self.cur_number][2]
            self.ans_4 = answers_1[self.cur_number][3]
            self.ans_1_b.text = self.ans_1
            self.ans_2_b.text = self.ans_2
            self.ans_3_b.text = self.ans_3
            self.ans_4_b.text = self.ans_4
        else:
            self.question.text = results_easy(correct)
            self.buttons.remove_widget(self.ans_1_b)
            self.buttons.remove_widget(self.ans_2_b)
            self.buttons.remove_widget(self.ans_3_b)
            self.buttons.remove_widget(self.ans_4_b)
            self.back_button = Button(text = 'Назад',font_name = 'Mono',font_size = 20, background_color = (134/255, 180/255, 230/255, 1), on_press = lambda x: self.back())
            self.buttons.add_widget(self.back_button)
            self.buttons.size_hint = (None, 0.15)
    def back(self):
        global correct
        global questions_1
        global answers_1
        correct = 0
        questions_1 = find_list(diff_1_questions)
        questions_1 = generate_question(questions_1)
        answers_1 = generate_anwers(questions_1, diff_1_questions)
        self.manager.current = 'MainScreen'
        self.remove_widget(self.layout)
        self.layout.remove_widget(self.question)
        self.layout.remove_widget(self.buttons)
        self.cur_number = 0
        self.ans_1 = answers_1[self.cur_number][0]
        self.ans_2 = answers_1[self.cur_number][1]
        self.ans_3 = answers_1[self.cur_number][2]
        self.ans_4 = answers_1[self.cur_number][3]
        self.label_text = diff_1_questions[questions_1[self.cur_number]]['question']

        self.layout = BoxLayout(orientation="vertical", padding=(0, 0, 0, 100), spacing=20)
        self.buttons = GridLayout(spacing=30, size_hint=(0.9, 1), pos_hint={'center_x': 0.5}, cols=1)
        self.add_widget(self.layout)
        self.question = Label(text=self.label_text, font_name = 'Mono', text_size=(self.width * 0.8, None), halign='center', font_size=25, pos_hint={'center_x': 0.5})

        self.ans_1_b = Button(text=self.ans_1, font_name = 'Mono',font_size = 20,background_color = (134/255, 180/255, 230/255, 1), on_press=lambda instance: self.check_and_next(self.ans_1))
        self.ans_2_b = Button(text=self.ans_2,font_name = 'Mono',font_size = 20,background_color = (134/255, 180/255, 230/255, 1), on_press=lambda instance: self.check_and_next(self.ans_2))
        self.ans_3_b = Button(text=self.ans_3,font_name = 'Mono',font_size = 20,background_color = (134/255, 180/255, 230/255, 1), on_press=lambda instance: self.check_and_next(self.ans_3))
        self.ans_4_b = Button(text=self.ans_4,font_name = 'Mono',font_size = 20,background_color = (134/255, 180/255, 230/255, 1), on_press=lambda instance: self.check_and_next(self.ans_4))

        self.layout.add_widget(self.question)
        self.buttons.add_widget(self.ans_1_b)
        self.buttons.add_widget(self.ans_2_b)
        self.buttons.add_widget(self.ans_3_b)
        self.buttons.add_widget(self.ans_4_b)
        self.layout.add_widget(self.buttons)


    """self.manager.current = 'Q2'"""

class diff_2_screen(Screen):
    def __init__(self, **kwargs):
        super(diff_2_screen, self).__init__(**kwargs)
        global questions
        global answers_2
        global diff_2_questions

        self.cur_number = 0
        self.ans_1 = answers_2[self.cur_number][0]
        self.ans_2 = answers_2[self.cur_number][1]
        self.ans_3 = answers_2[self.cur_number][2]
        self.ans_4 = answers_2[self.cur_number][3]
        self.label_text = diff_2_questions[questions_2[self.cur_number]]['question']

        self.layout = BoxLayout(orientation="vertical", padding=(0, 0, 0, 100), spacing=20)
        self.buttons = GridLayout(spacing=30, size_hint=(0.9, 1), pos_hint={'center_x': 0.5}, cols=1)
        self.add_widget(self.layout)
        self.question = Label(text=self.label_text, font_name = 'Mono',text_size=(Window.width / 2, None), halign='center', font_size=25, pos_hint={'center_x': 0.5})

        self.ans_1_b = Button(text=self.ans_1,font_name = 'Mono',font_size = 20,background_color = (134/255, 180/255, 230/255, 1), on_press=lambda instance: self.check_and_next(self.ans_1))
        self.ans_2_b = Button(text=self.ans_2,font_name = 'Mono',font_size = 20,background_color = (134/255, 180/255, 230/255, 1), on_press=lambda instance: self.check_and_next(self.ans_2))
        self.ans_3_b = Button(text=self.ans_3,font_name = 'Mono',font_size = 20,background_color = (134/255, 180/255, 230/255, 1), on_press=lambda instance: self.check_and_next(self.ans_3))
        self.ans_4_b = Button(text=self.ans_4,font_name = 'Mono',font_size = 20,background_color = (134/255, 180/255, 230/255, 1), on_press=lambda instance: self.check_and_next(self.ans_4))

        self.layout.add_widget(self.question)
        self.buttons.add_widget(self.ans_1_b)
        self.buttons.add_widget(self.ans_2_b)
        self.buttons.add_widget(self.ans_3_b)
        self.buttons.add_widget(self.ans_4_b)
        self.layout.add_widget(self.buttons)

    def check_and_next(self, button_text):
        global correct
        if button_text == diff_2_questions[questions_2[self.cur_number]]['correct']:
            correct += 1
        self.cur_number += 1
        if self.cur_number <= 9:
            self.label_text = diff_2_questions[questions_2[self.cur_number]]['question']
            self.question.text = self.label_text
            self.ans_1 = answers_2[self.cur_number][0]
            self.ans_2 = answers_2[self.cur_number][1]
            self.ans_3 = answers_2[self.cur_number][2]
            self.ans_4 = answers_2[self.cur_number][3]
            self.ans_1_b.text = self.ans_1
            self.ans_2_b.text = self.ans_2
            self.ans_3_b.text = self.ans_3
            self.ans_4_b.text = self.ans_4
        else:
            self.question.text = results_medium(correct)
            self.buttons.remove_widget(self.ans_1_b)
            self.buttons.remove_widget(self.ans_2_b)
            self.buttons.remove_widget(self.ans_3_b)
            self.buttons.remove_widget(self.ans_4_b)
            self.back_button = Button(text='Назад',font_name = 'Mono',font_size = 20,background_color = (134/255, 180/255, 230/255, 1), on_press=lambda x: self.back())
            self.buttons.add_widget(self.back_button)
            self.buttons.size_hint = (None, 0.15)

    def back(self):
        global correct
        global questions_2
        global answers_2
        questions_2 = find_list(diff_2_questions)
        questions_2 = generate_question(questions_2)
        answers_2 = generate_anwers(questions_2, diff_2_questions)
        correct = 0
        self.manager.current = 'MainScreen'
        self.remove_widget(self.layout)
        self.layout.remove_widget(self.question)
        self.layout.remove_widget(self.buttons)
        self.cur_number = 0
        self.ans_1 = answers_2[self.cur_number][0]
        self.ans_2 = answers_2[self.cur_number][1]
        self.ans_3 = answers_2[self.cur_number][2]
        self.ans_4 = answers_2[self.cur_number][3]
        self.label_text = diff_2_questions[questions_2[self.cur_number]]['question']

        self.layout = BoxLayout(orientation="vertical", padding=(0, 0, 0, 100), spacing=20)
        self.buttons = GridLayout(spacing=30, size_hint=(0.9, 1), pos_hint={'center_x': 0.5}, cols=1)
        self.add_widget(self.layout)
        self.question = Label(text=self.label_text, font_name = 'Mono', text_size=(self.width * 0.8, None), halign='center', font_size=25,pos_hint={'center_x': 0.5})

        self.ans_1_b = Button(text=self.ans_1,font_name = 'Mono',font_size = 20,background_color = (134/255, 180/255, 230/255, 1), on_press=lambda instance: self.check_and_next(self.ans_1))
        self.ans_2_b = Button(text=self.ans_2,font_name = 'Mono',font_size = 20,background_color = (134/255, 180/255, 230/255, 1), on_press=lambda instance: self.check_and_next(self.ans_2))
        self.ans_3_b = Button(text=self.ans_3,font_name = 'Mono',font_size = 20,background_color = (134/255, 180/255, 230/255, 1), on_press=lambda instance: self.check_and_next(self.ans_3))
        self.ans_4_b = Button(text=self.ans_4,font_name = 'Mono',font_size = 20,background_color = (134/255, 180/255, 230/255, 1), on_press=lambda instance: self.check_and_next(self.ans_4))

        self.layout.add_widget(self.question)
        self.buttons.add_widget(self.ans_1_b)
        self.buttons.add_widget(self.ans_2_b)
        self.buttons.add_widget(self.ans_3_b)
        self.buttons.add_widget(self.ans_4_b)
        self.layout.add_widget(self.buttons)

class diff_3_screen(Screen):
    def __init__(self, **kwargs):
        super(diff_3_screen, self).__init__(**kwargs)
        global questions
        global answers_3
        global diff_3_questions

        self.cur_number = 0
        self.ans_1 = answers_3[self.cur_number][0]
        self.ans_2 = answers_3[self.cur_number][1]
        self.ans_3 = answers_3[self.cur_number][2]
        self.ans_4 = answers_3[self.cur_number][3]
        self.label_text = diff_3_questions[questions_3[self.cur_number]]['question']

        self.layout = BoxLayout(orientation="vertical", padding=(0, 0, 0, 100), spacing=20)
        self.buttons = GridLayout(spacing=30, size_hint=(0.9, 1), pos_hint={'center_x': 0.5}, cols=1)
        self.add_widget(self.layout)
        self.question = Label(text=self.label_text,font_name = 'Mono',text_size=(Window.width / 2, None), halign='center', font_size=25)

        self.ans_1_b = Button(text=self.ans_1, font_name = 'Mono', font_size = 20,background_color = (134/255, 180/255, 230/255, 1), on_press=lambda instance: self.check_and_next(self.ans_1))
        self.ans_2_b = Button(text=self.ans_2,font_name = 'Mono',font_size = 20,background_color = (134/255, 180/255, 230/255, 1), on_press=lambda instance: self.check_and_next(self.ans_2))
        self.ans_3_b = Button(text=self.ans_3,font_name = 'Mono',font_size = 20,background_color = (134/255, 180/255, 230/255, 1), on_press=lambda instance: self.check_and_next(self.ans_3))
        self.ans_4_b = Button(text=self.ans_4,font_name = 'Mono',font_size = 20,background_color = (134/255, 180/255, 230/255, 1), on_press=lambda instance: self.check_and_next(self.ans_4))

        self.layout.add_widget(self.question)
        self.buttons.add_widget(self.ans_1_b)
        self.buttons.add_widget(self.ans_2_b)
        self.buttons.add_widget(self.ans_3_b)
        self.buttons.add_widget(self.ans_4_b)
        self.layout.add_widget(self.buttons)

    def check_and_next(self, button_text):
        global correct
        if button_text == diff_3_questions[questions_3[self.cur_number]]['correct']:
            correct += 1
        self.cur_number += 1
        if self.cur_number <= 9:
            self.label_text = diff_3_questions[questions_3[self.cur_number]]['question']
            self.question.text = self.label_text
            self.ans_1 = answers_3[self.cur_number][0]
            self.ans_2 = answers_3[self.cur_number][1]
            self.ans_3 = answers_3[self.cur_number][2]
            self.ans_4 = answers_3[self.cur_number][3]
            self.ans_1_b.text = self.ans_1
            self.ans_2_b.text = self.ans_2
            self.ans_3_b.text = self.ans_3
            self.ans_4_b.text = self.ans_4
        else:
            self.question.text = results_hard(correct)
            self.buttons.remove_widget(self.ans_1_b)
            self.buttons.remove_widget(self.ans_2_b)
            self.buttons.remove_widget(self.ans_3_b)
            self.buttons.remove_widget(self.ans_4_b)
            self.back_button = Button(text='Назад',font_name = 'Mono',font_size = 20,background_color = (134/255, 180/255, 230/255, 1), on_press=lambda x: self.back())
            self.buttons.add_widget(self.back_button)
            self.buttons.size_hint = (None, 0.15)

    def back(self):
        global correct
        global answers_3
        global questions_3
        questions_3 = find_list(diff_3_questions)
        questions_3 = generate_question(questions_3)
        answers_3 = generate_anwers(questions_3, diff_3_questions)
        correct = 0
        self.manager.current = 'MainScreen'
        self.remove_widget(self.layout)
        self.layout.remove_widget(self.question)
        self.layout.remove_widget(self.buttons)
        self.cur_number = 0
        self.ans_1 = answers_3[self.cur_number][0]
        self.ans_2 = answers_3[self.cur_number][1]
        self.ans_3 = answers_3[self.cur_number][2]
        self.ans_4 = answers_3[self.cur_number][3]
        self.label_text = diff_3_questions[questions_3[self.cur_number]]['question']

        self.layout = BoxLayout(orientation="vertical", padding=(0, 0, 0, 100), spacing=20)
        self.buttons = GridLayout(spacing=30, size_hint=(0.9, 1), pos_hint={'center_x': 0.5}, cols=1)
        self.add_widget(self.layout)
        self.question = Label(text=self.label_text,font_name = 'Mono',text_size=(self.width * 0.8, None), halign='center',font_size=25,pos_hint={'center_x': 0.5})

        self.ans_1_b = Button(text=self.ans_1,font_name = 'Mono',font_size = 20,background_color = (134/255, 180/255, 230/255, 1), on_press=lambda instance: self.check_and_next(self.ans_1))
        self.ans_2_b = Button(text=self.ans_2,font_name = 'Mono',font_size = 20,background_color = (134/255, 180/255, 230/255, 1), on_press=lambda instance: self.check_and_next(self.ans_2))
        self.ans_3_b = Button(text=self.ans_3,font_name = 'Mono',font_size = 20,background_color = (134/255, 180/255, 230/255, 1), on_press=lambda instance: self.check_and_next(self.ans_3))
        self.ans_4_b = Button(text=self.ans_4,font_name = 'Mono',font_size = 20,background_color = (134/255, 180/255, 230/255, 1), on_press=lambda instance: self.check_and_next(self.ans_4))

        self.layout.add_widget(self.question)
        self.buttons.add_widget(self.ans_1_b)
        self.buttons.add_widget(self.ans_2_b)
        self.buttons.add_widget(self.ans_3_b)
        self.buttons.add_widget(self.ans_4_b)
        self.layout.add_widget(self.buttons)



Builder.load_file('main.kv')

if __name__ == '__main__':
    Quiz().run()