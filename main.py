import os
import random
import pygame
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.clock import Clock

# Inicializando o pygame para tocar música
pygame.mixer.init()


def get_random_song(folder_path):
    # Lista todas as músicas na pasta
    songs = [song for song in os.listdir(folder_path) if song.endswith('.mp3')]
    return random.choice(songs)

def play_song_clip(song_path, start_time, duration):
    pygame.mixer.music.load(song_path)
    pygame.mixer.music.play(start=start_time)
    Clock.schedule_once(lambda dt: pygame.mixer.music.stop(), duration)


class MusicQuizApp(App):
    def build(self):
        layout = BoxLayout(orientation='vertical')
        self.label = Label(text="Adivinhe a música!")
        layout.add_widget(self.label)
        
        # Criando botões de resposta
        self.buttons = []
        for i in range(6):
            btn = Button(text=f"Alternativa {i+1}")
            btn.bind(on_press=self.check_answer)
            self.buttons.append(btn)
            layout.add_widget(btn)

        # Seleciona e toca a primeira música
        self.current_song = self.new_round()
        return layout

    def new_round(self):
        folder = 'assets/musics/'  # Caminho para as músicas
        song = get_random_song(folder)
        self.label.text = "Tocando..."
        start_time = random.randint(0, 30)  # Trecho aleatório da música
        play_song_clip(os.path.join(folder, song), start_time, 3)
        self.correct_answer = song
        self.set_alternatives(folder, song)
        return song

    def set_alternatives(self, folder, correct_song):
        # Gera alternativas
        all_songs = [song for song in os.listdir(folder) if song.endswith('.mp3')]
        random.shuffle(all_songs)
        alternatives = all_songs[:5]  # Pegando 5 alternativas erradas
        alternatives.append(correct_song)
        random.shuffle(alternatives)

        for i in range(6):
            self.buttons[i].text = alternatives[i]
    
    def check_answer(self, instance):
        if instance.text == self.correct_answer:
            self.label.text = "Correto!"
            self.show_feedback('green')
        else:
            self.label.text = "Errado!"
            self.show_feedback('red')
            play_song_clip(os.path.join('assets/musics/', self.correct_answer), random.randint(0, 30), 5)

        # Próxima música
        Clock.schedule_once(lambda dt: self.new_round(), 2)

    def show_feedback(self, color):
        # Simulação de luz piscando (somente para feedback visual)
        # Em um dispositivo real, você pode usar vibrações, LEDs, etc.
        self.label.color = color

# Iniciar o aplicativo
if __name__ == '__main__':
    MusicQuizApp().run()

