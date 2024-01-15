import ttkbootstrap as tb
from K import *
from views.helper import View
import requests as req
from json import dumps


class RegistrationView(View):
    def __init__(self, app):
        super().__init__(app)
        self.role = "Admin"
        self.name_var = tb.StringVar()
        self.nick_var = tb.StringVar()
        self.email_var = tb.StringVar()
        self.password_var1 = tb.StringVar()
        self.password_var2 = tb.StringVar()
        self.create_widgets()

    def create_widgets(self):
        bg1 = tb.Frame(self.frame)
        bg1.pack(expand=True, fill=BOTH)
        bg2 = tb.Frame(self.frame, bootstyle=DARK)
        bg2.pack(expand=True, fill=BOTH, side=BOTTOM)


        entry_width = 40
        label_padx, label_pady = 8, 8
        entry_padx, entry_pady = 8, 8

        tb.Label(bg1, text="First & Last Name: ", bootstyle="dark", font=(FONT_FAMILY, 21)).pack(padx=label_padx,
                                                                                               pady=label_pady)
        tb.Entry(bg1, textvariable=self.name_var, width=entry_width).pack(padx=entry_padx, pady=entry_pady)
        tb.Label(bg1, text="Username: ", bootstyle="dark", font=(FONT_FAMILY, 21)).pack(padx=label_padx,
                                                                                             pady=label_pady)
        tb.Entry(bg1, textvariable=self.nick_var, width=entry_width).pack(padx=entry_padx, pady=entry_pady)
        tb.Label(bg1, text="Email: ", bootstyle="dark", font=(FONT_FAMILY, 21)).pack(padx=label_padx,
                                                                                          pady=label_pady)
        tb.Entry(bg1, textvariable=self.email_var, width=entry_width).pack(padx=entry_padx, pady=entry_pady)
        tb.Label(bg1, text="Password: ", bootstyle="dark", font=(FONT_FAMILY, 21)).pack(padx=label_padx,
                                                                                             pady=label_pady)
        tb.Entry(bg1, textvariable=self.password_var1, show="*", width=entry_width).pack(padx=entry_padx,
                                                                                         pady=entry_pady)
        tb.Label(bg1, text="Confirm ur Password: ", bootstyle="dark", font=(FONT_FAMILY, 21)).pack(
            padx=label_padx, pady=label_pady)
        tb.Entry(bg1, textvariable=self.password_var2, show="*", width=entry_width).pack(padx=entry_padx,
                                                                                         pady=entry_pady)

        label_bottom = tb.Label(bg2, text="New Teacher Please Create An Account", bootstyle="inverse dark",
                                font=(FONT_FAMILY, 35))
        label_bottom.pack(pady=30)

        tb.Button(bg2, text="Submit", bootstyle=SUCCESS, command=self.register).pack(side=RIGHT, padx=15, pady=5)
        tb.Button(bg2, text="Back", command=self.app.show_home_view, bootstyle=DANGER).pack(side=RIGHT, padx=3, pady=5)

    def register(self):
        if self.password_var1.get() == self.password_var2.get():
            id_loop = True
            id = 0
            while id_loop:
                try:
                    auth = req.post(f"{self.app.url}users", data=dumps({"alt_name": self.nick_var.get(),
                                                                        "id": id,
                                                                      "email": self.email_var.get(),
                                                                      "name": self.name_var.get(),
                                                                      "password": self.password_var1.get(),
                                                                      "role": "Admin"})).json()
                    id_loop = False
                except:
                    id += 1
            if auth is None:
                self.create_toast("Success", "U Got An Account")
                auth = req.post(f"{self.app.url}token", data={"username": self.email_var.get(),
                                                                  "password": self.password_var1.get()}).json()
                self.app.token = {"access_token": auth["access_token"], "token_type": "bearer"}
                self.app.authenticated = TRUE
                self.app.email = self.email_var.get()
                self.password_var1.set("")
                self.app.show_tasks_view()
            else:
                self.create_toast("401 Error", "You are not our teacher")
        else:
            self.create_toast("401 Error", "Wrong Password")
