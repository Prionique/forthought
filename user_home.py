from flet import *
from flet_route import Params, Basket

from index import user
import sqlite3
class UserPage:
    def __init__(self):
        pass

    def view(self, page: Page, params: Params, basket: Basket):

        white_con = Container(theme=Theme(color_scheme_seed=colors.LIGHT_BLUE_600),
                             theme_mode=ThemeMode.DARK)
        white_con2 = Container(theme=Theme(color_scheme_seed=colors.LIGHT_BLUE_600),
                              theme_mode=ThemeMode.DARK)


        con = Container(width=10)


        appBar = AppBar(title = Row([
            Text("Forethought", weight = FontWeight.BOLD),
            Text("Teacher")
        ],
        alignment = MainAxisAlignment.CENTER),
                        center_title=True,
                        leading= Row([IconButton(icon=icons.LOGOUT, on_click=lambda _ : page.go("/"))]))

        div = Divider()


        class Concert:
            def __init__(self):
                pass
            def build(self):
                pass

        def refresh(_):
            con = sqlite3.connect("data.db")
            cur = con.cursor()
            a = []
            for i in cur.execute("select * from concerts where public==:p", {"p": "True"}):
                a.append(i)

            if len(a) != 0:
                view.controls.append(Text(str(a)))
                page.update()

        b = IconButton(icon = icons.REFRESH, on_click = lambda _ : refresh(_))

        event_list_card = Card(
            content=Container(
                content=Column(
                    [
                        ListTile(
                            title=TextButton(icon=icons.FORMAT_LIST_NUMBERED,
                                             text="Список заходів",
                                             on_click=lambda _: page.go("/user-event-list"))
                        ),
                    ]
                ),
                width=2000,
                padding=10,
            )
        )

        requests_list_card = Card(
            content=Container(
                content=Column(
                    [
                        ListTile(
                            title=TextButton(icon=icons.SCHEDULE_SEND,
                                             text="Запити",
                                             on_click=lambda _: page.go("/user-requests"))
                        ),
                    ]
                ),
                width=2000,
                padding=10,
            )
        )

        view = View("/home", appbar=appBar, controls = [appBar, div, event_list_card, requests_list_card])


        return view