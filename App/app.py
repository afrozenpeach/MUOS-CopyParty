import graphic as gr
import input
import sys
import time
import os
import subprocess
import threading
import multiprocessing
import queue

skip_input_check = False
menu_pressed = False

def start():
    gr.draw_clear()
    gr.draw_paint()
    p = multiprocessing.Process(target=run_script)
    p.start()

def update(process):
    global current_window, selected_position, skip_input_check, menu_pressed

    if skip_input_check:
        input.reset_input()
        skip_input_check = False
    else:
        input.check()

    if input.key("MENUF"):
        menu_pressed = True
        input.reset_input()
        return

    if menu_pressed and input.key("START"):
        gr.draw_end()
        process.terminate()
        sys.exit()

    if menu_pressed and input.key("SELECT"):
        sys.exit()

    if not input.key("START") and not input.key("MENUF"):
        menu_pressed = False

def run_script():
    gr.draw_clear()
    gr.draw_text((100, 200), f"Listening on 3923...")
    gr.draw_text((100, 220), f"To close hit menu + start")
    gr.draw_text((100, 240), f"To leave running until device is rebooted hit menu + select")
    gr.draw_paint()

    process = subprocess.Popen(
        ["python3", "/mnt/mmc/MUOS/application/CopyParty/App/copyparty-sfx.py", "-c", "/mnt/mmc/MUOS/application/CopyParty/App/copyparty.conf"] ,
        cwd=os.path.dirname("/mnt/mmc/MUOS/application/CopyParty/")
    )

    while True:
        update(process)

    base_dir = os.path.dirname("/mnt/mmc/MUOS/application/CopyParty/")
    logs_dir = os.path.join(base_dir, "logs")

    if not os.path.exists(logs_dir):
        os.makedirs(logs_dir)

    filename_no_ext = os.path.splitext(os.path.basename("/mnt/mmc/MUOS/application/CopyParty/"))[0]
    timestamp = time.strftime("%Y%m%d_%H%M%S")
    log_filename = os.path.join(logs_dir, f"{filename_no_ext}_log_{timestamp}.log")

    try:
        with open(log_filename, "w", encoding="utf-8") as log_file:
            log_file.write(f"--- Output ---\n")
            log_file.writelines(all_output)
            log_file.write("\n--- End of output ---\n")
    except Exception as e:
        gr.draw_log(f"Error writing log: {e}", fill="red", outline="red")
        gr.draw_paint()
        time.sleep(2)

    gr.button_circle((290, 460), "B", "Back")
    gr.draw_paint()
    
    while True:
        input.check()
        if input.key("B"):
            break
        time.sleep(0.1)
