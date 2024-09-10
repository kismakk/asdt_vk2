import random
import time
import threading
import tkinter as tk
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# Globaalit muuttujat
MAIN_DIMENSIONS = "600x600"
MAIN_XY = "700+200"
GRAPH_DIMENSIONS = "600x500"
GRAPH_XY = "50+200"
UPDATE_INTERVAL = 0.1
RUNNING = False
CHECK_RUNNING = False

# Ikkunat juoksukilpailulle ja maailmanennätyksille
main_window = tk.Tk()
main_window.title("Ernestin ja Kernestin juoksuharjoitukset")
main_window.geometry(f"{MAIN_DIMENSIONS}+{MAIN_XY}")

graph_window = tk.Toplevel(main_window)
graph_window.title("Maailmanennätykset")
graph_window.geometry(f"{GRAPH_DIMENSIONS}+{GRAPH_XY}")

runtimes_by_year = {
    1968: (9.95, "Jim Hines"),
    1983: (9.93, "Calvin Smith"),
    1988: (9.92, "Carl Lewis"),
    1991: (9.90, "Leroy Burrell"),
    1994: (9.85, "Leroy Burrell"),
    1999: (9.79, "Maurice Greene"),
    2007: (9.74, "Asafa Powell"),
    2009: (9.58, "Usain Bolt"),
}

runtimes_by_lions = {
    "lion_speed": 4.86,
    "lions": {
        1: (5.11, "Mauri"),
        2: (4.95, "Lauri"),
        3: (4.83, "Sauli"),
        4: (4.91, "Matti"),
        5: (4.78, "Teppo"),
        6: (4.56, "Seppo"),
        7: (4.66, "Ville"),
        8: (5.22, "Kalle"),
        9: (5.01, "Jere"),
        10: (4.99, "Kari"),
    }
}

years = list(runtimes_by_year.keys())
runtimes = [value[0] for value in runtimes_by_year.values()]

# Yhdistetään sanakirjat keskenään
runtimes_by_year_with_lions = dict(runtimes_by_year, **runtimes_by_lions)

fig = Figure(figsize=(6, 6), dpi=100)
ax = fig.add_subplot(111)
ax.plot(years, runtimes, "bo-")
ax.set_xlabel("Year")
ax.set_ylabel("Time (s)")

canvas = FigureCanvasTkAgg(fig, master=graph_window)
canvas.draw()
canvas.get_tk_widget().pack()

# Canvas juoksuradan piirtämiseen
running_field = tk.Canvas(main_window, width=400, height=200)
running_field.pack(side="bottom", padx=10, pady=50)

# Lähtö- ja maaliviivat
start_line = running_field.create_line(50, 60, 50, 160, fill="green", width=3)
end_line = running_field.create_line(350, 60, 350, 160, fill="red", width=3)

# Label viestejä varten
message_label = tk.Label(main_window, text="", font=("Ubuntu Mono", 12))
message_label.pack(side="bottom", padx=10, pady=10)

# Juoksijat
ernesti = {
    "shape": running_field.create_oval(45, 95, 55, 105, fill="blue"),
    "name": "Ernesti",
    "finished": False,
    "race_time": 0.0
}
kernesti = {
    "shape": running_field.create_oval(45, 115, 55, 125, fill="yellow"),
    "name": "Kernesti",
    "finished": False,
    "race_time": 0.0
}


def disable_buttons():
    """
    Poistaa kaikki painikkeet käytöstä juoksun ajaksi.
    """
    send_ernesti_button.config(state=tk.DISABLED)
    send_kernesti_button.config(state=tk.DISABLED)
    sendboth_button.config(state=tk.DISABLED)


def enable_buttons():
    """
    Aktivoi kaikki painikkeet juoksun päätyttyä.
    """
    send_ernesti_button.config(state=tk.NORMAL)
    send_kernesti_button.config(state=tk.NORMAL)
    sendboth_button.config(state=tk.NORMAL)


def update_message(message):
    """
    Päivittää viestin näytölle.

    :param message: Viesti
    """
    message_label.config(text=message)


def move_character(runner, distance_per_update, elapsed_time, race_time):
    """
    Rekurssiivinen funktio, joka liikuttaa juoksijaa radalla. Juoksun päätyttyä tulostetaan juoksijan nimi ja aika.

    :param runner: Juoksijan tiedot
    :param distance_per_update: Askeleen pituus
    :param elapsed_time: Kulunut aika
    :param race_time: Suoritukseen menevä aika
    """
    global RUNNING
    shape = runner["shape"]
    name = runner["name"]
    if elapsed_time < race_time and RUNNING:
        running_field.move(shape, distance_per_update, 0)
        main_window.update()
        time.sleep(0.1)
        move_character(runner, distance_per_update, elapsed_time + 0.1, race_time)
    else:
        if RUNNING:
            print(f"{name}n juoksu kesti {race_time:.2f} sekuntia.")
            runner["finished"] = True
            runner["race_time"] = race_time


def send_ernesti_running():
    """
    Lähettää Ernestin juoksemaan radalle.
    """
    global RUNNING
    RUNNING = True

    ernesti["finished"] = False

    disable_buttons()

    race_time = random.uniform(10, 18)
    distance_per_update = (300 / (race_time / UPDATE_INTERVAL))

    move_character(ernesti, distance_per_update, 0, race_time)

    if RUNNING and not CHECK_RUNNING:
        update_message(f"Ernestin aika: {race_time:.2f} sekuntia.")


def send_kernesti_running():
    """
    Lähettää Kernestin juoksemaan radalle.
    """
    global RUNNING
    RUNNING = True

    kernesti["finished"] = False

    disable_buttons()

    race_time = random.uniform(10, 18)
    distance_per_update = (300 / (race_time / UPDATE_INTERVAL))

    move_character(kernesti, distance_per_update, 0, race_time)

    if RUNNING and not CHECK_RUNNING:
        update_message(f"Kernestin aika: {race_time:.2f} sekuntia.")


def print_winner():
    """
    Tulostaa voittajan.
    """
    ernesti_time, kernesti_time = ernesti["race_time"], kernesti["race_time"]

    times_string = f"Ernestin aika: {ernesti_time:.2f} sekuntia, Kernestin aika: {kernesti_time:.2f} sekuntia"

    if ernesti_time < kernesti_time:
        update_message(f"Voittaja on Ernesti! {times_string}")
    else:
        update_message(f"Voittaja on Kernesti! {times_string}")


def check_if_finished():
    """
    Tarkistaa, ovatko molemmat juoksijat päässeet maaliin.
    """
    if not CHECK_RUNNING:
        return

    if ernesti["finished"] and kernesti["finished"]:
        print_winner()
    else:
        main_window.after(100, check_if_finished)


def send_both_running():
    """
    Lähettää Ernestin ja Kernestin juoksemaan radalle käyttäen säikeitä.
    """
    global RUNNING, CHECK_RUNNING
    RUNNING = True
    CHECK_RUNNING = True

    ernesti["finished"] = False
    kernesti["finished"] = False

    disable_buttons()

    t1 = threading.Thread(target=send_ernesti_running)
    t2 = threading.Thread(target=send_kernesti_running)

    t1.start()
    t2.start()

    check_if_finished()


def reset():
    """
    Lopettaa juoksun, palauttaa juoksijat lähtöviivalle, resetoi arvot ja aktivoi painikkeet.
    """
    global RUNNING, CHECK_RUNNING
    RUNNING = False
    CHECK_RUNNING = False

    running_field.delete(ernesti["shape"])
    running_field.delete(kernesti["shape"])

    ernesti["shape"] = running_field.create_oval(45, 95, 55, 105, fill="blue")
    kernesti["shape"] = running_field.create_oval(45, 115, 55, 125, fill="yellow")

    ernesti["race_time"] = 0.0
    kernesti["race_time"] = 0.0
    ernesti["finished"] = False
    kernesti["finished"] = False

    update_message("")
    enable_buttons()


# Painikkeet
send_ernesti_button = tk.Button(main_window, text="Lähetä Ernesti", command=send_ernesti_running)
send_ernesti_button.pack(side="top", padx=10, pady=10)

send_kernesti_button = tk.Button(main_window, text="Lähetä Kernesti", command=send_kernesti_running)
send_kernesti_button.pack(side="top", padx=10, pady=10)

sendboth_button = tk.Button(main_window, text="Yhteislähtö", command=send_both_running)
sendboth_button.pack(side="top", padx=10, pady=10)

reset_button = tk.Button(main_window, text="Reset", command=reset)
reset_button.pack(side="top", padx=10, pady=10)

main_window.mainloop()
