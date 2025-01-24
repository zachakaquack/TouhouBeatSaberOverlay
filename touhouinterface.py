from tkinter.filedialog import askopenfilename
import serverside
import asyncio
import customtkinter as ctk
import threading



def create_obs_scene(text_variables, scene):
    # worst code ive ever written
    if text_variables[0].get():
        serverside.create_scene(scene)
    if text_variables[1].get():
        image_path = askopenfilename(filetypes=[("Image files", "*.png")], title='Open Background File')
        serverside.create_background(scene, image_path)
    if text_variables[2].get():
        serverside.create_text(scene, "mapper_name_text", 203.0, 2.0, "left")
    if text_variables[3].get():
        serverside.create_text(scene, "map_name_text", 305.0, 2.0, "right")
    if text_variables[4].get():
        serverside.create_text(scene, "author_name_text", 305.0, 32.0, "right")
    if text_variables[5].get():
        serverside.create_text(scene, "bpms_text", 305.0, 62.0, "right")
    if text_variables[6].get():
        serverside.create_text(scene, "diff_text", 727.0, 0.0, "center")  # holy shit wysi
    if text_variables[7].get():
        serverside.create_text(scene, "combos_text", 613.0, 187.0, "right")
    if text_variables[8].get():
        serverside.create_text(scene, "miss_text", 613.0, 230.0, "right")
    if text_variables[9].get():
        serverside.create_text(scene, "time_text", 613.0, 273.0, "right")
    if text_variables[10].get():
        serverside.create_text(scene, "ranks_text", 613.0, 147.0, "right")
    if text_variables[11].get():
        serverside.create_text(scene, "scores_text", 613.0, 62.0, "right")
    if text_variables[12].get():
        serverside.create_text(scene, "accuracy_text", 613.0, 105.0, "right")
    if text_variables[13].get():
        serverside.create_beat_saber_display(scene)



class App(ctk.CTk):
    def __init__(self):
        super().__init__()

        # setup
        # centers the window to the screen
        width = 1280
        height = 720

        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        x = int(((screen_width / 2) - (width / 2)))
        y = int(((screen_height / 2) - (height / 2)))

        self.geometry(f"{width}x{height}+{x}+{y}")

        # hit escape to quit
        self.bind("<Escape>", lambda z: self.quit())

        # no resizing windows
        self.resizable(False, False)

        # title of window
        self.title("touhou interface")

        self.rowconfigure(0, weight=1, uniform="a")
        self.rowconfigure((1, 2), weight=4, uniform="a")
        self.columnconfigure((0, 1), weight=1, uniform="a")

        button_font = ctk.CTkFont(family="Calibri", size=36, weight="bold")
        self.label_font = ctk.CTkFont(family="Calibri", size=24, weight="bold")

        # left side (launch and exit websocket)
        ctk.CTkLabel(self, text="Websocket Stuffs", font=self.label_font).grid(row=0, column=0, sticky="nsew")
        ctk.CTkButton(self, text="Launch Websocket (Start)", font=button_font, corner_radius=20,
                      command=
                      lambda: threading.Thread(target=lambda: asyncio.run(serverside.run()), daemon=True).start()
                      ).grid(row=1, column=0, sticky="nsew", padx=20, pady=20)
        ctk.CTkLabel(self, text="Close App to Close Websocket", font=button_font, corner_radius=20).grid(row=2,
                                                                                                         column=0,
                                                                                                         sticky="nsew",
                                                                                                         padx=20,
                                                                                                         pady=20)

        # right side (obs settings)
        right_side = ctk.CTkFrame(self, fg_color="#242424")
        right_side.grid(row=1, rowspan=2, column=1, sticky="nsew")
        right_side.columnconfigure((0, 1), weight=1, uniform='a')
        right_side.rowconfigure(0, weight=1, uniform="a")
        self.box_frame = ctk.CTkFrame(right_side, fg_color="#343434")
        self.box_frame.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)
        rows = []

        self.texts = ["Make Scene",
                      "Make Background",
                      "Make Mapper Name Text",
                      "Make Map Name Text",
                      "Make Song Author Text",
                      "Make BPM Text",
                      "Make Difficulty Text",
                      "Make Score Text",
                      "Make Accuracy Text",
                      "Make Rank Text",
                      "Make Combo Text",
                      "Make Miss Count Text",
                      "Make Progress Text",
                      "Make Beat Saber Display"]
        self.texts_variables = []

        for i in range(len(self.texts)):
            rows.append(i)
            self.texts_variables.append(ctk.BooleanVar(value=True))

        self.box_frame.rowconfigure(rows, weight=1, uniform="a")
        self.box_frame.columnconfigure(0, weight=1, uniform="a")

        self.obs_buttons = ctk.CTkFrame(right_side, fg_color="#343434")
        self.obs_buttons.grid(row=0, column=1, sticky="nsew", padx=5, pady=5)

        self.obs_buttons.rowconfigure(0, weight=8, uniform="a")
        self.obs_buttons.rowconfigure(3, weight=1, uniform="a")
        self.obs_buttons.rowconfigure((1, 2, 4), weight=2, uniform="a")
        self.obs_buttons.columnconfigure(0, weight=1, uniform="a")

        self.scene_name = ctk.StringVar(value="touhou_overlay")

        entry_font = ctk.CTkFont(family="Calibri", size=16)

        ctk.CTkLabel(self, text="OBS Stuffs", font=self.label_font).grid(row=0, column=1, sticky="nsew")
        ctk.CTkButton(self.obs_buttons, text="Set OBS", font=button_font, corner_radius=20,
                      command=lambda: create_obs_scene(self.texts_variables, self.scene_name.get())).grid(
            row=0, column=0, sticky="nsew", padx=20, pady=100)
        ctk.CTkButton(self.obs_buttons, text="Select All", font=button_font, corner_radius=20,
                      command=self.select_all).grid(row=1, column=0, sticky="nsew", padx=20, pady=20)
        ctk.CTkButton(self.obs_buttons, text="Deselect All", font=button_font, corner_radius=20,
                      command=self.deselect_all).grid(row=2, column=0, sticky="nsew", padx=20, pady=20)
        ctk.CTkLabel(self.obs_buttons, text="Scene Name", font=self.label_font).grid(row=3, column=0, sticky="nsew")
        ctk.CTkEntry(self.obs_buttons, font=entry_font, corner_radius=20, textvariable=self.scene_name).grid(row=4,
                                                                                                             column=0,
                                                                                                             sticky="nsew",
                                                                                                             padx=20,
                                                                                                             pady=20)

        for i in range(len(self.texts)):
            self.create_check(i)

    def create_check(self, i):
        ctk.CTkCheckBox(self.box_frame, text=self.texts[i], font=self.label_font, variable=self.texts_variables[i],
                        onvalue=True, offvalue=False).grid(row=i, column=0, sticky="nsew", padx=5, pady=5)

    def select_all(self):
        for item in self.texts_variables:
            item.set(True)

    def deselect_all(self):
        for item in self.texts_variables:
            item.set(False)


app = App()
app.mainloop()
