def move_color(base_color, target_colors, play_for_minutes):
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

        while dx != 0 or dy != 0:
            if dx > 0:
                pyautogui.press('right')
                dx -= 1
            elif dx < 0:
                pyautogui.press('left')
                dx += 1
            if dy > 0:
                pyautogui.press('down')
                dy -= 1
            elif dy < 0:
                pyautogui.press('up')
                dy += 1

            pyautogui.hotkey('ctrl')

            if pyautogui.locateCenterOnScreen(Image.new("RGB", (1, 1), closest_target['color'])) is not None:
                break

            time.sleep(0.1)
            if keyboard.is_pressed('s'):
                messagebox.showinfo("Info", "Stopping the program.")
                return

            pyautogui.hotkey('ctrl', release=True)

    messagebox.showinfo("Info", "Movement completed.")