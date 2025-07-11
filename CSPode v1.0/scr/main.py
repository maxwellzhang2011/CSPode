import pygame
import json
import pyclip
from pyclip.win_clip import ClipboardNotTextFormatException
import os

pygame.init()
scr = pygame.display.set_mode((800, 600), 16)
logo = pygame.image.load("C:/Program Files/CSPode v1.0/datas/logo.png")
pygame.display.set_icon(logo)
pygame.display.set_caption("CSPode v1.0")

default_stament = {
    "theme": (0, 0, 0),
    "size": 30,
    "txt color": (0, 255, 0),
    "spacing": 10,
    "blinker color": (255, 255, 255),
    "blinker weith": 4,
    "cmd color": (60, 60, 60),
    "blinker speed": 60,
    "error time": 120
}

def main():
    wrong = False
    try:
        with open("C:/Program Files/CSPode v1.0/datas/last_stament.json", "r") as f:
            a = f.read()
            stament = json.loads(a)
    except FileNotFoundError:
        with open("datas/last_stament.json", "w") as f:
            f.write(json.dumps(default_stament, indent=2))
        wrong = True
        stament = None
    codes = [""]
    #first loop timing
    first_loop_timing = True
    running = True
    x, y = 0, 1
    showy = 0
    clock = pygame.time.Clock()
    counter = 0
    toggle_on = True
    command_line = False
    command = ""
    finish_typing_command = False
    no_time = False
    no_time_counter = 0
    while running and not wrong:
        take_out_y = y
        digits = 0
        while take_out_y > 0:
            take_out_y //= 10
            digits += 1
        scr.fill(stament["theme"])
        if first_loop_timing:
            font = pygame.font.Font("C:/Program Files/CSPode v1.0/datas/font.ttf", stament["size"])
            first_loop_timing = False
        for ev in pygame.event.get():
            if ev.type == pygame.QUIT:
                running = False
            if ev.type == pygame.KEYDOWN:
                key = pygame.key.get_pressed()
                if key[pygame.K_BACKSPACE]:
                    if not command_line:
                        if x > 0 and y != 0:
                            codes[y - 1] = codes[y - 1][:x - 1] + codes[y - 1][x:]
                            x -= 1
                        elif y > 1:
                            if len(codes) > 1:
                                codes.pop(y - 1)
                                y -= 1
                                x = len(codes[y - 1])
                    else:
                        if len(command) != 0:
                            command = command[:-1]
                elif key[pygame.K_RETURN]:
                    if not command_line:
                        codes.insert(y, "")
                        y += 1
                        x = 0
                    else:
                        finish_typing_command = True
                elif key[pygame.K_TAB]:
                    codes[y - 1] = codes[y - 1][:x] + "  " + codes[y - 1][x:]
                    x += 2
                elif key[pygame.K_LEFT]:
                    if x > 0:
                        x -= 1
                    else:
                        if y > 1:
                            y -= 1
                elif key[pygame.K_RIGHT]:
                    if x < len(codes[y - 1]):
                        x += 1
                    else:
                        if y < len(codes):
                            y += 1
                elif key[pygame.K_DOWN]:
                    if y < len(codes):
                        y += 1
                        if x > len(codes[y - 1]):
                            x = len(codes[y - 1])
                elif key[pygame.K_UP]:
                    if y > 1:
                        y -= 1
                        if x > len(codes[y - 1]):
                            x = len(codes[y - 1])
                elif key[pygame.K_LCTRL] and key[pygame.K_v]:
                    try:
                        if not command_line:
                            codes[y - 1] = codes[y - 1][:x] + pyclip.paste(text=True) + codes[y - 1][x:]
                            x += len(pyclip.paste(text=True))
                        else:
                            command += pyclip.paste(text=True)
                    except ClipboardNotTextFormatException:
                        pass
                #un used key
                elif key[pygame.K_CAPSLOCK] or key[pygame.K_F1] or key[pygame.K_F2] or key[pygame.K_F3] or key[pygame.K_F4] or key[pygame.K_F5] or key[pygame.K_F6] or key[pygame.K_F7] or key[pygame.K_F8] or key[pygame.K_F9] or key[pygame.K_F10] or key[pygame.K_F11] or key[pygame.K_F12] or key[pygame.K_F13] or key[pygame.K_F14] or key[pygame.K_F15] or key[pygame.K_RALT] or key[pygame.K_RCTRL]:
                    pass
                elif ev.key == pygame.K_LSHIFT:
                    pass
                #un used key end
                elif key[pygame.K_LALT]:
                    command_line = not command_line
                elif key[pygame.K_RSHIFT]:
                    if command_line:
                        command = ""
                    else:
                        if len(codes) > 1:
                            y -= 1
                            x = len(codes[y - 1]) - 1
                            codes.pop(y)
                        else:
                            codes = [""]
                else:
                    letter = ev.unicode
                    if command_line:
                        command += letter
                    else:
                        codes[y - 1] = codes[y - 1][:x] + letter + codes[y - 1][x:]
                        x += 1
            elif ev.type == pygame.MOUSEWHEEL:
                if ev.y == 1:
                    if showy < len(codes) - 1:
                        showy += 1
                elif ev.y == -1:
                    if showy > 0:
                        showy -= 1
        if finish_typing_command:
            commands = command.split()
            finish_typing_command = False
            command = ""
            yes = False
            try:
                if commands[0] == "newfile":
                    codes = [""]
                    yes = True
                elif commands[0] == "setting":
                    if commands[1] == "theme":
                        yes = True
                        stament["theme"] = (int(commands[2]), int(commands[3]), int(commands[4]))
                    elif commands[1] == "txtcolor":
                        yes = True
                        stament["txt color"] = (int(commands[2]), int(commands[3]), int(commands[4]))
                    elif commands[1] == "txtsize":
                        yes = True
                        stament["size"] = int(commands[2])
                    elif commands[1] == "yspacing":
                        yes = True
                        stament["spacing"] = int(command[2])
                    elif commands[1] == "blkcolor":
                        yes = True
                        stament["blinker color"] = (int(commands[2]), int(commands[3]), int(commands[4]))
                    elif commands[1] == "blksize":
                        yes = True
                        stament["spacing"] = int(command[2])
                    elif commands[1] == "cmdcolor":
                        yes = True
                        stament["cmd color"] = (int(commands[2]), int(commands[3]), int(commands[4]))
                    elif commands[1] == "defalt":
                        yes = True
                        stament = default_stament
                    elif commands[1] == "blkspeed":
                        yes = True
                        stament["blinker speed"] = int(command[2])
                    elif commands[1] == "errortime":
                        yes = True
                        stament["error time"] = int(command[2])
                elif commands[0] == "exit":
                    running = False
                elif commands[0] == "savefile":
                    yes = True
                    lenth = len(commands)
                    place = ""
                    for i in range(1, lenth):
                        place += commands[i] + " "
                    print(place)
                    with open(place, "w") as f:
                        for i in range(len(codes)):
                            f.writelines(codes[i] + "\n")
                elif commands[0] == "openfile":
                    yes = True
                    path = ""
                    for i in range(1, len(commands)):
                        path += commands[i] + " "
                    if yes:
                        with open(path, "r") as f:
                            lines = sum(1 for _ in f)
                            f.seek(0)
                            codes = []
                            for i in range(lines):
                                codes.append(f.readline().replace("\n", ""))
                elif commands[0] == "remem":
                    if commands[1] == "read":
                        yes = True
                        name = ""
                        for i in range(2, len(commands)):
                            name += commands[i] + " "
                        try:
                            with open("datas/mems/" + name + ".txt", "r") as f:
                                lines = sum(1 for _ in f)
                                f.seek(0)
                                codes = []
                                for i in range(lines):
                                    codes.append(f.readline().replace("\n", ""))
                            if len(codes) < y:
                                y = len(codes)
                        except FileNotFoundError:
                            yes = False
                    elif commands[1] == "write":
                        yes = True
                        name = ""
                        for i in range(2, len(commands)):
                            name += commands[i] + " "
                        with open("datas/mems/" + name + ".txt", "w") as f:
                            lines = len(codes)
                            for i in range(lines):
                                f.writelines(codes[i] + "\n")
            except IndexError:
                yes = False
            if not yes:
                mem1 = stament["blinker color"]
                stament["blinker color"] = (255, 0, 0)
                no_time = True
        if not command_line:
            command = ""
        #points
        y_point = 0
        for i in range(showy, len(codes)):
            display_txt = font.render(str(i + 1), False, stament["txt color"])
            scr.blit(display_txt, (0, y_point * (stament["size"]) + y_point * stament["spacing"]))
            display_txt = font.render(codes[i], False, stament["txt color"])
            scr.blit(display_txt, (stament["size"] * digits, y_point * stament["size"] + y_point * stament["spacing"]))
            y_point += 1

        # updates
        if no_time:
            no_time_counter += 1

        if no_time_counter > stament["error time"]:
            no_time = False
            no_time_counter = 0
            stament["blinker color"] = mem1

        if counter == stament["blinker speed"]:
            toggle_on = not toggle_on
            counter = 0
        if toggle_on:
            blinker_x = stament["size"] * digits + font.size(codes[y - 1][:x])[0]
            blinker_y = (y - 1) * stament["size"] + (y - 1) * stament["spacing"]
            pygame.draw.line(scr, stament["blinker color"], (blinker_x, blinker_y), (blinker_x, blinker_y + font.get_height()), stament["blinker weith"])

        if command_line:
            command_rect = pygame.Rect(0, scr.get_height() - (stament["size"] * 2 + stament["spacing"]), scr.get_width(), stament["size"] * 2 + stament["spacing"])
            pygame.draw.rect(scr, stament["cmd color"], command_rect)
            fps = font.render("fps: " + str(int(clock.get_fps())), False, stament["txt color"])
            scr.blit(fps, (0, scr.get_height() - (stament["size"] * 2 + stament["spacing"])))

            command_render = font.render("command: " + command, False, stament["txt color"])
            scr.blit(command_render, (0, scr.get_height() - font.get_height()))

        if y == 0:
            codes = [""]
        clock.tick(60)
        counter += 1
        pygame.display.flip()
    return wrong, stament
if __name__ == "__main__":
    wrong, stament = main()
    pygame.quit()
    folder = "datas/mems"
    for i in os.scandir(folder):
        if i.is_file():
            os.remove(i.path)
    if wrong == True:
        print("we fount a error not something big please restart you app.")
        print("press control(on windows or linux), command(on mac) + c to exit")
        try:
            while True:
                pass
        except KeyboardInterrupt:
            pass
    else:
        with open("datas/last_stament.json", "w") as f:
            f.write(json.dumps(stament, indent=2))