import pygame


def init():
    pygame.init()
    # pygame needs a window to detect the inputs
    window = pygame.display.set_mode((1280, 540))


def getkey(keyname):
    answer = False
    for event in pygame.event.get(): pass
    keyInput = pygame.key.get_pressed()
    myKey = getattr(pygame, 'K_{}'.format(keyname))
    if keyInput[myKey]:
        answer = True
    pygame.display.update()
    return answer


def main():
    if getkey("LEFT"):
        print("Go left")
    if getkey("RIGHT"):
        print("Go right")


# if runned as the main file
if __name__ == '__main__':
    init()
    while True:
        main()
