import tkinter as tk
import threading

class Auto:
    def __init__(self, name, maxTank, maxSpeed, speed, tankinhalt, positionX, verbrauch):
        self.name = name
        self.maxTank = maxTank
        self.maxSpeed = maxSpeed
        self.speed = speed
        self.tankinhalt = tankinhalt
        self.positionX = positionX
        self.verbrauch = verbrauch

    def __str__(self):
        return f"Ich bin {self.name}, mein Tank enthält gerade noch {self.tankinhalt} Liter Sprit und meine Geschwindigkeit beträgt {self.speed} und meine Position ist: {self.positionX}"

    def fahren(self, time):
        if self.tankinhalt > 0:
            self.positionX += self.speed * time
            if (self.tankinhalt - self.verbrauch) < 0:
                self.tankinhalt = 0
            else:
                self.tankinhalt -= self.verbrauch

    def tanken(self, liter):
        if (self.tankinhalt + liter) > self.maxTank:
            self.tankinhalt = self.maxTank
        else:
            self.tankinhalt += liter

class AutoGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Autorennen")

        self.carlist = []
        self.race_thread = None
        self.car_entries = []

        self.main_frame = tk.Frame(root)
        self.create_main_view()

    def create_main_view(self):
        self.main_frame.pack()

        car_count_label = tk.Label(self.main_frame, text="Wie viele Autos sollen erstellt werden?")
        car_count_label.pack()

        self.car_count_entry = tk.Entry(self.main_frame)
        self.car_count_entry.pack()

        create_cars_button = tk.Button(self.main_frame, fg="white", bg="grey",text="Autos erstellen", command=self.show_create_cars_view)
        create_cars_button.pack()

    def show_create_cars_view(self):
        car_count = int(self.car_count_entry.get())
        self.main_frame.pack_forget()

        self.create_cars_frame = tk.Frame(self.root)
        self.create_cars_frame.pack()

        self.car_entries = []

        def create_car(i):
            name_entry, maxTank_entry, maxSpeed_entry, speed_entry, tankinhalt_entry, verbrauch_entry = self.car_entries[i]
            name = name_entry.get()
            maxTank = int(maxTank_entry.get()) if maxTank_entry.get() else 0
            maxSpeed = int(maxSpeed_entry.get()) if maxSpeed_entry.get() else 0
            speed = int(speed_entry.get()) if speed_entry.get() else 0
            tankinhalt = int(tankinhalt_entry.get()) if tankinhalt_entry.get() else 0
            verbrauch = float(verbrauch_entry.get()) if verbrauch_entry.get() else 0

            auto = Auto(name, maxTank, maxSpeed, speed, tankinhalt, 0, verbrauch)
            self.carlist.append(auto)
            name_entry.config(state='disabled')

        for i in range(car_count):
            name_label = tk.Label(self.create_cars_frame, fg="blue", bg="grey", text=f"Name für das Fahrzeug {i + 1}:")
            name_label.pack()

            name_entry = tk.Entry(self.create_cars_frame)
            name_entry.pack()

            maxTank_label = tk.Label(self.create_cars_frame, text=f"Maximaler Tankinhalt für Fahrzeug {i + 1}:")
            maxTank_label.pack()

            maxTank_entry = tk.Entry(self.create_cars_frame)
            maxTank_entry.pack()

            maxSpeed_label = tk.Label(self.create_cars_frame, text=f"Maximale Geschwindigkeit für Fahrzeug {i + 1}:")
            maxSpeed_label.pack()

            maxSpeed_entry = tk.Entry(self.create_cars_frame)
            maxSpeed_entry.pack()

            speed_label = tk.Label(self.create_cars_frame, text=f"Geschwindigkeit für Fahrzeug {i + 1} im Rennen:")
            speed_label.pack()

            speed_entry = tk.Entry(self.create_cars_frame)
            speed_entry.pack()

            tankinhalt_label = tk.Label(self.create_cars_frame, text=f"Tankinhalt für Fahrzeug {i + 1} zum Start:")
            tankinhalt_label.pack()

            tankinhalt_entry = tk.Entry(self.create_cars_frame)
            tankinhalt_entry.pack()

            verbrauch_label = tk.Label(self.create_cars_frame, text=f"Verbrauch für Fahrzeug {i + 1}:")
            verbrauch_label.pack()

            verbrauch_entry = tk.Entry(self.create_cars_frame)
            verbrauch_entry.pack()

            self.car_entries.append((name_entry, maxTank_entry, maxSpeed_entry, speed_entry, tankinhalt_entry, verbrauch_entry))

            create_button = tk.Button(self.create_cars_frame, text="Auto erstellen", bg="grey", fg="white", command=lambda i=i: create_car(i))
            create_button.pack()

        race_time_label = tk.Label(self.create_cars_frame, text="Wie lange soll das Rennen dauern (in Sekunden)?")
        race_time_label.pack()

        self.race_time_entry = tk.Entry(self.create_cars_frame)
        self.race_time_entry.pack()

        self.race_button = tk.Button(self.create_cars_frame, text="Autorennen starten", fg="red", command=self.start_race)
        self.race_button.pack()

    def start_race(self):
        rennzeit = int(self.race_time_entry.get())
        self.race_thread = threading.Thread(target=self.run_race, args=(rennzeit,))
        self.race_thread.start()

    def run_race(self, rennzeit):
        for x in range(rennzeit):
            for car in self.carlist:
                if not self.race_thread.is_alive():
                    return

                car.fahren(1)

                if x % 5 == 0 and car.tankinhalt <= 0:
                    car.tanken(20)

        if self.race_button:
            self.race_button["state"] = tk.NORMAL

        self.show_winners()

    def show_winners(self):
        if not self.carlist:
            return

        max_distance = max(car.positionX for car in self.carlist)
        winners = [car for car in self.carlist if car.positionX == max_distance]

        winner_names = ", ".join([car.name for car in winners])
        winner_text = f"Das Rennen ist vorbei. Gewinner: {winner_names}"
        self.create_cars_frame.pack_forget()
        self.winner_label = tk.Label(self.root, text=winner_text, bg="red", fg="white")
        self.winner_label.pack()

if __name__ == '__main__':
    root = tk.Tk()
    app = AutoGUI(root)
    root.geometry()
    root.configure(bg='grey')  # Hintergrundfarbe des Hauptfensters in Grau setzen
    root.mainloop()