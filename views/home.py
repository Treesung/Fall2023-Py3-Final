import ttkbootstrap as tb
from K import *
from views.helper import View


class HomeView(View):
    def __init__(self, app):
        super().__init__(app)
        self.create_widgets()

    def create_widgets(self):
        bg1 = tb.Frame(self.frame)
        bg1.pack(expand=True, fill=BOTH)
        bg2 = tb.Frame(self.frame, bootstyle=DARK)
        bg2.pack(expand=True, fill=BOTH, side=BOTTOM)

        tb.Label(bg1, text="Get Your Salary", bootstyle="primary", font=(FONT_FAMILY, 40)).pack(side=TOP, pady=40)
        tb.Label(bg1, text="A way for teachers to check how much they earn", bootstyle="secondary",
                 font=(FONT_FAMILY, 20)).pack(side=TOP, pady=20)

        tb.Label(bg2, text="The most Pro teacher will get a 690 bonus!", bootstyle="inverse dark",
                 font=(FONT_FAMILY, 18)).pack(side=BOTTOM, pady=30)

        tb.Button(bg1, text="Register", command=self.app.show_registration_view, bootstyle=SUCCESS).pack(side=BOTTOM,
                                                                                                         ipadx=20,
                                                                                                         ipady=10,
                                                                                                         pady=30)
        tb.Button(bg2, text="Login", command=self.app.show_login_view, bootstyle=INFO).pack(side=BOTTOM, ipadx=25,
                                                                                            ipady=10, pady=30)
