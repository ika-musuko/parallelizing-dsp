import pygame
import pyaudio

class SeqSynth():
    keymap = {
          pygame.K_q              :    "c4"
        , pygame.K_w              :   "c+4"
        , pygame.K_e              :    "d4"
        , pygame.K_r              :   "d+4"
        , pygame.K_t              :    "e4"
        , pygame.K_y              :    "f4"
        , pygame.K_u              :   "f+4"
        , pygame.K_i              :    "g4"
        , pygame.K_o              :   "g+4"
        , pygame.K_p              :    "a4"
        , pygame.K_LEFTBRACKET    :   "a+4"
        , pygame.K_RIGHTBRACKET   :    "b4"
        , pygame.K_a              :    "c5"
        , pygame.K_s              :   "c+5"
        , pygame.K_d              :    "d5"
        , pygame.K_f              :   "d+5"
        , pygame.K_g              :    "e5"
        , pygame.K_h              :    "f5" 
        , pygame.K_j              :   "f+5"
        , pygame.K_k              :    "g5"
        , pygame.K_l              :   "g+5"
        , pygame.K_SEMICOLON      :    "a5"
        , pygame.K_QUOTE          :   "a+5"
        , pygame.K_BACKSLASH      :    "b5"
        , pygame.K_z              :    "c6"
        , pygame.K_x              :   "c+6"
        , pygame.K_c              :    "d6"
        , pygame.K_v              :   "d+6"
        , pygame.K_b              :    "e6"
        , pygame.K_n              :    "f6"
        , pygame.K_m              :   "f+6"
        , pygame.K_COMMA          :    "g6"
        , pygame.K_PERIOD         :   "g+6"
        , pygame.K_SLASH          :    "a6"
    }
    def __init__(self):
        pygame.init()
        self.init_key_handler()
    
    def init_key_handler(self):
        

def main():
    SeqSynth()

if __name__ == "__main__":
    main()