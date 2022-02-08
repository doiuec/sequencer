#-*- coding: utf-8 -*-

from kivy.app import App
from kivy.uix.widget import Widget
from kivy.core.window import Window
from kivy.vector import Vector
from kivy.properties import NumericProperty, ReferenceListProperty
from kivy.properties import StringProperty, ObjectProperty, BooleanProperty
from kivy.clock import Clock
from kivy.core.audio import SoundLoader
import subprocess as sp
import time
import threading
import pygame

Window.size = (1200, 800)


class sequencer(Widget):
    appquit = 0
    ball = ObjectProperty(None)
    play_state = -1
    loop_state = -1
    bpm_value = 120
    bpm_value_ = 120
    insts = [[ -1 for i in range(16)] for j in range(5)]
    play_500 = 1
    kick_sound = SoundLoader.load('./sound_effects/kick.wav')
    snare_sound = SoundLoader.load('./sound_effects/snare.wav')
    crash_sound = SoundLoader.load('./sound_effects/crash.wav')
    hihat_sound = SoundLoader.load('./sound_effects/hihat.wav')
    counter = 0
    pygame.mixer.init(frequency = 44100)
    pygame.mixer.music.load("./sound_effects/kick.mp3")


    

    def change_bpm(self, *args):
        sequencer.bpm_value_ = int(args[1])
        sequencer.bpm_value = (sequencer.bpm_value_ ) / 50
        self.ball.velocity = Vector(sequencer.bpm_value, 0)

    def change_vol(self, *args):
        vol = int(args[1]) / 100
        pygame.mixer.music.set_volume(vol)

    def change_inst(self, text):
        file = "./sound_effects/" + text + ".mp3"
        pygame.mixer.music.load( file )


    def serve_ball(self):
        self.ball.center = self.center
        self.ball.velocity = Vector(sequencer.bpm_value, 0)

    def update(self, play_state):
        if sequencer.play_state == 1:
            self.ball.move()
            # playsound("./sound_effects/kick.mp3")
            # print(sequencer.insts[0][0])
            # bounce off left and right

            if (self.ball.x < 230) or (self.ball.right > 1200):
                self.ball.pos = (230, 160)
                if sequencer.loop_state == 1:
                    self.ball.velocity_x *= -1
                else:
                    sequencer.play_state = -1
                    self.ball.pos = (230, 160)
        else:
            pass

    def kick(self):
        sequencer.kick_sound.play()

    def snare(self):
        sequencer.snare_sound.play()

    def hihat(self):
        sequencer.hihat_sound.play()

    def crash(self):
        sequencer.crash_sound.play()

    def music(self):
        #exec('{} = {}'.format(name, x))
        while(True):
            for i in range(16):
                if sequencer.play_state == 1:
                    if sequencer.insts[0][i] == 1:
                        pygame.mixer.music.play(1) 
                        print(1-60 /sequencer.bpm_value_ + 0.55)
                        time.sleep(1 - 60 /sequencer.bpm_value_ + 0.75)
                        pygame.mixer.music.stop()

                time.sleep(100/1000)
                    # print(sequencer.insts[0])
                    # snare_list = sequencer.insts[1]
                    # hihat_list = sequencer.insts[2]

                    # print("loop_after")
                    # print(sequencer.insts[0][0])
                    #if i == 0:
                    #    print(sequencer.insts[0][i])
                    # kick_thread = threading.Thread(target = sequencer.kick, args = kick_list)
                    # snare_thread = threading.Thread(target = sequencer.snare, args = snare_list)
                    # hihat_thread = threading.Thread(target = sequencer.hihat, args = hihat_list)
                    # if 'kick_thread' in locals():
                    #     print("90")
                    #     kick_thread.start()
                    #     print("91")
                    # if 'snare_thread' in locals():
                    #     snare_thread.start()
                    # if 'hihat_thread' in locals():
                    #     hihat_thread.start()
                    # thread_list = threading.enumerate()
                    # thread_list.remove(threading.main_thread())
                    # for thread in thread_list[2:]:
                    #     print(thread_list[2:])
                    #     thread.join
                    #     print(thread_list[2:])
                    # time.sleep(0.5)
                    # print(threading.enumerate())

    def button_play(self):
        sequencer.play_state = 1
    
    def button_stop(self):
        sequencer.play_state = -1
        self.ball.pos = (230, 160)

    def button_loop(self):
        sequencer.play_state = -1
        sequencer.loop_state *= -1

    def button_quit(self):
        sequencer.appquit = 1

    def sound_trigger_kick(self, *args):
        #print(args[0])
        sequencer.insts[0][args[0]-1] *= -1
        #print(sequencer.insts[0][args[0]-1])

    def sound_trigger_snare(self, *args):
        #print(args[0])
        sequencer.insts[1][args[0]-1] *= -1
        #print(sequencer.insts[0][args[0]-1])

    def sound_trigger_hihat(self, *args):
        #print(args[0])
        sequencer.insts[2][args[0]-1] *= -1
        #print(sequencer.insts[0][args[0]-1])

    def sound_trigger_crash(self, *args):
        #print(args[0])
        sequencer.insts[3][args[0]-1] *= -1
        #print(sequencer.insts[0][args[0]-1])

        

class PongBall(Widget):
    velocity_x = NumericProperty(0)
    velocity_y = NumericProperty(0)
    velocity = ReferenceListProperty(velocity_x, velocity_y)

    def move(self):
        self.pos = Vector(*self.velocity) + self.pos



class TestApp(App):

    def build(self):
        game = sequencer()
        game.serve_ball()
        #thread1 = threading.Thread(target = Clock.schedule_interval(game.update, 1.0 / 60.0))
        Clock.schedule_interval(game.update, 1.0 / 60.0)
        thread2 = threading.Thread(target = game.music)
        #thread_list = threading.enumerate()
        #thread_list.remove(threading.main_thread())
        #thread1.start()
        thread2.start()
        return game

if __name__ == '__main__':
    TestApp().run()
