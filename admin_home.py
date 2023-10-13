from flet import *
from flet_route import Params, Basket

class AdminPage:
    def __init__(self):
        pass

    def view(self, page: Page, params: Params, basket: Basket):
        page.title = "Admin"

        white_con = Container(theme=Theme(color_scheme_seed=colors.LIGHT_BLUE_600),
                             theme_mode=ThemeMode.DARK)
        white_con2 = Container(theme=Theme(color_scheme_seed=colors.LIGHT_BLUE_600),
                              theme_mode=ThemeMode.DARK)


        con = Container(width=10)


        appBar = AppBar(title = Row([
            Text("Forethought", weight="bold"),
            Text("Admin")
        ],
        alignment = MainAxisAlignment.CENTER),
                        center_title=True,
                        leading=IconButton(icon=icons.LOGOUT, on_click=lambda _ : page.go("/")))

        div = Divider()

        event_list_card = Card(
            content=Container(
                content=Column(
                    [
                        ListTile(
                            title=TextButton(icon=icons.FORMAT_LIST_NUMBERED,
                                             text="Список заходів",
                                             on_click=lambda _ : page.go("/event-list"))
                        ),
                    ]
                ),
                width=2000,
                padding=10,
            )
        )

        class_list_card = Card(
            content=Container(
                content=Column(
                    [
                        ListTile(
                            title=TextButton(icon=icons.FORMAT_LIST_BULLETED,
                                             text="Список класів",
                                             on_click=lambda _ : page.go("/class-list"))
                        ),
                    ]
                ),
                width=2000,
                padding=10,
            )
        )

        white_con.content = event_list_card

        white_con2.content = class_list_card

        view = View("/home-admin", appbar=appBar, controls = [appBar, div, white_con, white_con2])

        return view