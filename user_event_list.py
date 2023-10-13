from flet import *
from flet_route import Params, Basket
from sqlite3 import *
import threading
import flet as ft
from datetime import *
from index import user

class UserEventListPage:
    def __init__(self):
        pass

    def view(self, page: Page, params: Params, basket: Basket):

        view = View("/user-event-list")

        appBar = AppBar(title=Text("Список Заходів"),
                        leading=IconButton(icon=icons.ARROW_BACK_IOS_NEW, on_click=lambda _: page.go("/home")),
                        center_title=True)
        view.controls.append(appBar)



        # Container for green button
        green_con = Container(theme=Theme(color_scheme_seed=colors.GREEN_ACCENT_200),
                              theme_mode=ThemeMode.DARK)


        view.controls.append(green_con)

        # Command which creates new event in database and app overlay
        def new_event(_):

            div = Divider()



        # Creating scrollable column
        class State :
            i = 0

        s = State()
        sem = threading.Semaphore()

        page.scroll = "auto"
        page.auto_scroll = True

        # Creating an App Bar

        div = Divider()

        # Body content
        body = Column(scroll=ScrollMode.ALWAYS, controls=[div],
                      )
        view.controls.append(body)
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
            width = page.width,
            scroll=ScrollMode.ALWAYS,
            on_scroll_interval=0,
            on_scroll=on_scroll,
        )

        # Connecting to the database
        con = connect("data.db")
        cur = con.cursor()

        a = []

        for c in cur.execute("select * from concerts where public==:p", {"p": "True"}):
            a.append(c)

        a.reverse()
        if len(a) == 0:

            body.controls.append(

                    ft.Row([Text("Немає доступних заходів")], alignment = MainAxisAlignment.CENTER)

                )
        else:
            pass

        # Creating event objects
        class Concert(UserControl):

            def __init__(self, concert_title, concert_date, concert_time, public):
                super().__init__()

                self.card = None
                self.title = concert_title
                self.date = concert_date
                self.time = concert_time
                self.public = public


            def build(self, dlg=None):

                today = str(datetime.today())

                day = int(self.date[:2])
                month = int(self.date[3:])
                year = datetime.today().year


                date = datetime(day= day, month = month, year = year)

                dedline = str(date-timedelta(days = 3))

                dedline = f"{dedline[8:10]}.{dedline[5:7]}"

                def close_dlg(e):
                    dlg_modal.open = False
                    page.update()

                body = Column()

                txt = Text("Додайте посилання на папку Google Drive з сценарієм та матеріалами виступу")

                body.controls.append(txt)

                link = TextField(prefix_icon = icons.LINK, label = "Посилання", keyboard_type=KeyboardType.URL)
                body.controls.append(link)

                sub_button = ft.Row([TextButton("Надіслати запит")], alignment = MainAxisAlignment.CENTER)
                body.controls.append(sub_button)


                dialog_body = Column(
                                [ft.Row([ft.Text(f"{self.title}", size = 20, weight = FontWeight.BOLD)], alignment = MainAxisAlignment.CENTER),
                                ft.Row([ft.Text("Заявка на участь у концерті")], alignment = MainAxisAlignment.CENTER),
                                ft.Row([Text(f"Дедлайн : {dedline}")], alignment = MainAxisAlignment.CENTER),

                                 Divider(),
                                 body]
                            )

                dlg_modal = ft.BottomSheet(
                    content = Container(dialog_body,
                        width=page.width,
                        height=1000,
                        padding=10
                        )
                    )

                def open_dlg_modal(e):
                    page.dialog = dlg_modal
                    dlg_modal.open = True
                    page.update()


                self.card = Card(
                    content = Container(
                        content=Column(
                            controls = [ListTile(
                                    leading = Icon(icons.EVENT_ROUNDED),
                                    title=Text(
                                        "", size = 20, spans = [TextSpan(
                                            f"{self.title}", style=TextStyle(italic=True)
                                        )]
                                    ),
                                    subtitle = Column(
                                        [
                                            Text(f"\nДата   : {self.date}\nЧас     : {self.time}\n\nДедлайн для заявок : {dedline}"),
                                            TextButton("Подати заявку на номер", on_click = open_dlg_modal)


                                         ])
                                )]
                        ), padding = 10
                    ),
                    width=2000
                )

                return self.card

        for i in a:

            cl.controls.append(Concert(concert_title = i[0], concert_date = i[1], concert_time = i[2], public = i[3]))
            page.update()
            s.i += 1


        body.controls.append(cl)

        return view