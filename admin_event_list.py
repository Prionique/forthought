from flet import *
import flet as ft
from flet_route import Params, Basket
from sqlite3 import *
import threading
from data import add_event
from data import update_event
class EventListPage:
    def __init__(self):
        pass

    def view(self, page: Page, params: Params, basket: Basket):

        # Container for green button
        green_con = Container(theme=Theme(color_scheme_seed=colors.GREEN_ACCENT_200),
                              theme_mode=ThemeMode.DARK)

        # Command which creates new event in database and app overlay
        def new_event(_):

            div = Divider()

            # Command which adds data to the database
            def submit(s):

                add_event(event_title.value, event_date.value, event_time.value, public.value)


                new_event_dialog.open = False
                page.go("/home-admin")
                page.go("/event-list")
                page.update()

            # Creating input fields
            event_title = TextField(label="Назва")
            event_date = TextField(label="Дата")
            event_time = TextField(label="Час")
            public = Switch(label = "Public")

            but = ft.Row([ElevatedButton("Додати захід", on_click = lambda _ : submit(_))],
                         alignment=MainAxisAlignment.CENTER)
            # Creating bottom dialog
            new_event_dialog = BottomSheet(Container(content=
            Column(
                [
                    event_title,
                    event_date,
                    event_time,
                    public,
                    but
                ]
            ), height=385,
                padding=15),
                on_dismiss=lambda _: page.go("/event-list"))

            page.update()

            page.dialog = new_event_dialog
            new_event_dialog.open = True
            page.update()

        # Creating button, which adds a new event
        new_event_card = Card(
            content=Container(
                content=Column(
                    [
                        ListTile(
                            title=TextButton(icon=icons.ADD,
                                             text="Новий захід",
                                             on_click=lambda _: new_event(_))
                        ),
                    ]
                ),
                width=2000,
                padding=10,
            )
        )

        # Adding button to the green container
        green_con.content = new_event_card

        # Creating scrollable column
        class State :
            i = 0

        s = State()
        sem = threading.Semaphore()

        page.scroll = "auto"
        page.auto_scroll = True

        # Creating an App Bar
        appBar = AppBar(title=Text("Список Заходів"),
                        leading=IconButton(icon=icons.ARROW_BACK_IOS_NEW, on_click=lambda _ : page.go("/home-admin")),
                        center_title=True)

        div = Divider()

        # Body content
        body = Column(scroll=ScrollMode.ALWAYS, controls=[div],
                      )
        # Column sroll event
        def on_scroll(e: OnScrollEvent) :
            if e.pixels >= e.max_scroll_extent - 100 :
                if sem.acquire(blocking=False) :
                    try :
                        for i in range(0, 10) :
                            pass
                            s.i += 1
                        cl.update()
                    finally :
                        sem.release()

        cl = Column(
            spacing=10,
            height = page.height - 200,
            scroll=ScrollMode.ALWAYS,
            on_scroll_interval=0,
            on_scroll=on_scroll,
        )

        # Connecting to the database
        con = connect("data.db")
        cur = con.cursor()

        a = []

        for c in cur.execute("select * from concerts"):
            a.append(c)

        a.reverse()

        # Creating event objects
        class Concert(UserControl):

            def __init__(self, concert_title, concert_date, concert_time, public):
                super().__init__()

                self.card = None
                self.title = concert_title
                self.date = concert_date
                self.time = concert_time
                self.public = public

                self.route = f"{concert_title}'{concert_date}'{concert_time}"


            def build(self, dlg=None):

                def extend(m):

                    def _delete(e):

                        cur.execute("delete from concerts where title==:t and date==:d",
                                    {"t" : f"{self.title}", "d" : f"{self.date}"})
                        con.commit()

                        page.update()

                        page.go("/home-admin")
                        page.go("/event-list")

                    def edit(_):

                        def update_event_(_):

                            update_event(self.title, self.date, title_field.value, d_field.value, t_field.value, public.value)
                            edit_dialog.open = False
                            action_dlg.open = False

                            page.update()

                            page.go("/home-admin")
                            page.go("/event-list")

                        title_field = TextField(label = "Назва", value=self.title)
                        d_field = TextField(label = "Дата", value = self.date)
                        t_field = TextField(label = "Час", value = self.time)

                        if self.public == "True":

                            public = Switch(label = "Public", value = True)

                        else:
                            public = Switch(label="Public", value=False)
                        but = ft.Row([ElevatedButton("Зберегти Зміни", on_click = update_event_)],
                                  alignment = MainAxisAlignment.CENTER)

                        edit_dialog = BottomSheet(Container(content =
                            Column(
                                [
                                    title_field,
                                    d_field,
                                    t_field,
                                    public,
                                    but
                                ]), height = 385,
                            padding = 15
                        ), on_dismiss = lambda _ : page.go("/event-list")
                        )
                        action_dlg.open = False
                        page.update()

                        page.dialog = edit_dialog
                        edit_dialog.open = True
                        page.update()

                    dlg = ft.AlertDialog(
                        title=ft.Text("Hello, you!"), on_dismiss=lambda e: print("Dialog dismissed!")
                    )

                    async def close_dlg(e):
                        dlg_modal.open = False
                        await e.control.page.update_async()

                    dlg_modal = ft.AlertDialog(
                        modal=True,
                        title=ft.Text("Please confirm"),
                        content=ft.Text("Do you really want to delete all those files?"),
                        actions=[
                            ft.TextButton("Yes", on_click=close_dlg),
                            ft.TextButton("No", on_click=close_dlg),
                        ],
                        actions_alignment=ft.MainAxisAlignment.END,
                        on_dismiss=lambda e: print("Modal dialog dismissed!"),
                    )

                    async def open_dlg(e):
                        e.control.page.dialog = dlg
                        dlg.open = True
                        await e.control.page.update_async()

                    async def open_dlg_modal(e):
                        e.control.page.dialog = dlg_modal
                        dlg_modal.open = True
                        await e.control.page.update_async()

                    action_dlg = BottomSheet(Container(

                            ResponsiveRow(controls = [
                                TextButton("Змінити", icon = icons.EDIT, on_click = lambda _ : edit(_)),
                                TextButton("Видалити", icon=icons.DELETE, on_click = lambda _ : _delete(_))
                                ], alignment = MainAxisAlignment.CENTER), padding = 15, height=190)
                    )

                    page.dialog = action_dlg
                    action_dlg.open = True
                    page.update()

                if self.public == "True":
                    ic = icons.REMOVE_RED_EYE
                else:
                    ic = icons.EVENT_ROUNDED

                self.card = Card(
                    content = Container(
                        content=Column(
                            controls = [ListTile(
                                    leading = Icon(ic),
                                    title=Text(
                                        f"{self.title}", size = 20, weight = FontWeight.BOLD
                                    ),
                                    subtitle = Text(f"\nДата   : {self.date}\nЧас     : {self.time}")
                                )]
                        ), padding = 10, on_click = lambda _ : extend(_)
                    ),
                    width=2000
                )

                return self.card

        for i in a:

            cl.controls.append(Concert(concert_title = i[0], concert_date = i[1], concert_time = i[2], public = i[3]))
            page.update()
            s.i += 1

        body.controls.append(cl)

        view = View("/event-list",
                    controls=[div, green_con, body, appBar])

        return view