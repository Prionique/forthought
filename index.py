from flet import *
from flet_route import Params, Basket
import sqlite3


class IndexPage:

    user = []

    def __init__(self):
        pass
    def view(self, page: Page, params: Params, basket: Basket):


        page.title = "Forethought"

        app_view = View("/")

        div = Divider()
        page.vertical_alignment = "center"
        page.horizontal_alignment = "center"

        bar = AppBar(title = Text("     "))
        app_view.controls.append(bar)

        text = Row(controls=[Text("Forethought", size=30, weight="w500")],
                   alignment=MainAxisAlignment.CENTER)
        text_under = Row(controls=[
            Text("Система школи №173 \nдля організації шкільних заходів", text_align="center", color=colors.GREY)],
                         alignment=MainAxisAlignment.CENTER)

        but = Row([TextButton("Login", width=180)], alignment=MainAxisAlignment.CENTER)
        bar = AppBar(title=Text("   "))

        con = Container(height = 10)

        def _login(w):
            if login.value == "":
                login.focus()
            elif pwd.value == '':
                pwd.focus()
            else:

                con_ = sqlite3.connect("data.db")
                cur = con_.cursor()

                for q in cur.execute("select * from admin_"):

                    if login.value == q[0]:
                        if pwd.value == q[1]:
                            page.go("/home-admin")
                    else:
                        for i in cur.execute("select * from classes"):

                            if i[4] == login.value:
                                if i[5] == pwd.value:
                                    user.append(f"{login.value}")
                                    page.go("/home")
                                else:
                                    pass





        login = TextField(label="Username", border=InputBorder.UNDERLINE)
        pwd = TextField(label="Password", password=True, can_reveal_password=True, border=InputBorder.UNDERLINE)
        login_button = Row([FilledTonalButton("Увійти в систему", on_click = lambda _ : _login(_))], alignment = MainAxisAlignment.CENTER)


        form = Container(Column([text, text_under, div, login, pwd, con, login_button]),
                         padding = 50)


        app_view.controls.append(form)

        return app_view

user = IndexPage().user