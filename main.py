import pyautogui
import threading
import time
import keyboard
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from PIL import Image, ImageTk
import ttkthemes as th
import mouse
import sys

def pick_color(result):
    messagebox.showinfo("Info", "Move your mouse and press 'P' to pick the color.")
    while True:
        if keyboard.is_pressed('p'):
            position = mouse.get_position()
            color = pyautogui.screenshot().getpixel(position)
            result.append(color)
            messagebox.showinfo("Info", f"Color picked: {color}")
            break

def move_color(base_color, target_colors, play_for_minutes):
    screen_width, screen_height = pyautogui.size()

    def find_closest_target(base_position, target_colors):
        min_distance = float('inf')
        closest_target = None
        for target_color in target_colors:
            for x, y in target_color['positions']:
                distance = ((base_position[0] - x) ** 2 + (base_position[1] - y) ** 2) ** 0.5
                if distance < min_distance:
                    min_distance = distance
                    closest_target = target_color
        return closest_target

    start_time = time.time()
    while time.time() - start_time < play_for_minutes * 60:
        base_position = pyautogui.locateCenterOnScreen(Image.new("RGB", (1, 1), base_color))
        if base_position is None:
            messagebox.showerror("Error", "Base color not found.")
            break

        closest_target = find_closest_target(base_position, target_colors)
        if closest_target is None:
            messagebox.showerror("Error", "No target colors found.")
            break

        dx = closest_target['positions'][0][0] - base_position[0]
        dy = closest_target['positions'][0][1] - base_position[1]
        pyautogui.move(dx, dy, duration=1)

        if dx > 0:
            pyautogui.press('right')
        elif dx < 0:
            pyautogui.press('left')
        if dy > 0:
            pyautogui.press('down')
        elif dy < 0:
            pyautogui.press('up')

        pyautogui.hotkey('ctrl')

        while pyautogui.locateCenterOnScreen(Image.new("RGB", (1, 1), closest_target['color'])) is not None:
            time.sleep(0.1)
            if keyboard.is_pressed('s'):
                messagebox.showinfo("Info", "Stopping the program.")
                return
        pyautogui.hotkey('ctrl', release=True)

def on_pick_base_color():
    base_color = []
    pick_color(base_color)
    base_color_label.config(text="Base color picked: " + str(base_color[0]))

def on_pick_target_color():
    target_color = []
    pick_color(target_color)
    target_colors.append({'color': target_color[0], 'positions': [mouse.get_position()]})
    target_color_label.config(text="Target color picked: " + str(target_color[0]))

def on_start_click():
    base_color = base_color_label.cget("text").split(": ")[1]
    if base_color.startswith('#'):
        base_color = tuple(int(base_color[i:i+2], 16) for i in (1, 3, 5))
    else:
        base_color = eval(base_color)
    play_for_minutes = int(play_for_minutes_entry.get())

    move_color(base_color, target_colors, play_for_minutes)

    status_label.config(text="Movement completed.")

def on_stop_click():
    sys.exit()

# Create the main window
root = th.ThemedTk(theme="breeze")  # You can change the theme here
root.title("Color Mover")
root.geometry("300x250")

# Create frames
base_frame = ttk.Frame(root)
base_frame.pack(pady=10)

target_frame = ttk.Frame(root)
target_frame.pack(pady=10)

play_frame = ttk.Frame(root)
play_frame.pack(pady=10)

button_frame = ttk.Frame(root)
button_frame.pack(pady=10)

status_frame = ttk.Frame(root)
status_frame.pack(pady=10)

# Base color components
base_color_label = ttk.Label(base_frame, text="Base color:")
base_color_label.pack()

pick_base_color_button = ttk.Button(base_frame, text="Pick Base Color", command=on_pick_base_color)
pick_base_color_button.pack()

# Target color components
target_color_label = ttk.Label(target_frame, text="Target color:")
target_color_label.pack()

pick_target_color_button = ttk.Button(target_frame, text="Pick Target Color", command=on_pick_target_color)
pick_target_color_button.pack()

# Play for components
play_for_minutes_label = ttk.Label(play_frame, text="Play for (minutes):")
play_for_minutes_label.pack()

play_for_minutes_entry = ttk.Entry(play_frame)
play_for_minutes_entry.pack()

# Start button
start_button = ttk.Button(button_frame, text="Start", command=on_start_click)
start_button.pack()

# Stop button
stop_button = ttk.Button(button_frame, text="Stop", command=on_stop_click)
stop_button.pack()

# Status label
status_label = ttk.Label(status_frame, text="")
status_label.pack()

target_colors = []

root.mainloop()
