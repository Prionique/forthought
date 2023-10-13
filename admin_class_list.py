from flet import *
from flet_route import Params, Basket
from sqlite3 import *
import threading
import flet as ft
from data import update_class, add_class

class ClassListPage:
    def __init__(self):
        pass

    def view(self, page: Page, params: Params, basket: Basket):

        green_con = Container(theme=Theme(color_scheme_seed=colors.GREEN_ACCENT_200),
                              theme_mode=ThemeMode.DARK)

        page.scroll = "auto"
        page.auto_scroll = True


        appBar = AppBar(title=Text("Список класів"),
                        leading=IconButton(icon=icons.ARROW_BACK_IOS_NEW, on_click=lambda _ : page.go("/home-admin")),
                        center_title=True)

        div = Divider()

        def new_class(_):

            div_ = Divider()

            def submit(s_):

                add_class(class_id.value, class_t.value, class_l.value, class_r.value, teacher_login.value, teacher_pwd.value)

                new_class_dialog.open = False
                page.update()
                page.go("/")
                page.go("/class-list")

            class_id = TextField(label = "Індекс")
            class_t = TextField(label = "Вчитель")
            class_l = TextField(label= "Лідер")
            class_r = TextField(label = "Кабінет")
            teacher_login = TextField(label ="Teacher's Username")
            teacher_pwd = TextField(label = "Teacher's Password")


            teacher_form = ft.Row([teacher_login, teacher_pwd])

            add_button = ft.Row(
                controls=[ElevatedButton(text="+ Додати клас", on_click= lambda _ : submit(_))],
                alignment=MainAxisAlignment.CENTER
            )

            body_ = Container(Column(controls=[class_id, class_t, class_l, class_r, teacher_form, add_button], scroll = ScrollMode.ALWAYS), padding=15)


            new_class_dialog = BottomSheet(content=body_)

            page.dialog = new_class_dialog
            new_class_dialog.open = True
            page.update()


        new_class_card = Card(
            content=Container(
                content=Column(
                    [
                        ListTile(
                            title=TextButton(icon=icons.ADD,
                                             text="Новий класс",
                                             on_click=lambda _: new_class(_))
                        ),
                    ]
                ),
                width=2000,
                padding=10,
            ))


        body = Column(scroll=ScrollMode.ALWAYS, controls=[div],
                      )

        cl = Column(
            spacing=10,
            height = page.height - 105,
            scroll=ScrollMode.ALWAYS,

        )

        con = connect("data.db")
        cur = con.cursor()

        a = []

        for c in cur.execute("select * from classes"):
            a.append(c)

        a.sort()



        class Class(UserControl):

            def __init__(self, id, teacher, leader, room, username, pwd):
                super().__init__()

                self.card = None
                self.id = id
                self.teacher = teacher
                self.leader = leader
                self.room = room
                self.username = username
                self.pwd = pwd


            def build(self, dlg=None):

                def extend(l):

                    def _delete(e):

                        cur.execute("delete from classes where id==:i and teacher==:t",
                                    {"i" : f"{self.id}", "t" : f"{self.teacher}"})
                        con.commit()

                        page.update()

                        action_dlg.open = False
                        page.go("/")
                        page.go("/class-list")


                    def edit(_):

                        def save_(_):

                            update_class(str(self.id), str(self.teacher), str(id_field.value), str(t_field.value),
                                         str(l_field.value), str(r_field.value), str(teacher_login.value), str(teacker_pwd.value))

                            edit_dialog.open = False

                            page.go("/")
                            page.go("/class-list")
                            page.update()

                        id_field = TextField(label = "Індекс", value = self.id)
                        t_field = TextField(label = "Вчитель", value = self.teacher)
                        l_field = TextField(label="Лідер", value=self.leader)
                        r_field = TextField(label = "Кабінет", value=self.room, keyboard_type = KeyboardType.NUMBER)
                        teacher_login = TextField(label ="Логін вчителя", value = self.username)
                        teacker_pwd = TextField(label ="Пароль вчителя", value = self.pwd)
                        sub_button = ft.Row([ElevatedButton("Зберегти", on_click = lambda _ : save_(_))],
                                            alignment = MainAxisAlignment.CENTER)

                        edit_dialog = BottomSheet(Container(content =
                            Column(
                                [
                                    id_field,
                                    t_field,
                                    l_field,
                                    r_field,
                                    Divider(),
                                    teacher_login,
                                    teacker_pwd,
                                    sub_button
                                ], scroll = ScrollMode.ALWAYS),
                            padding = 15, height=600
                        ), on_dismiss = lambda _ : page.go("/class-list")
                        )
                        action_dlg.open = False
                        page.update()

                        page.dialog = edit_dialog
                        edit_dialog.open = True
                        page.update()



                    action_dlg = BottomSheet(Container(ResponsiveRow(controls = [
                        TextButton("Змінити", icon = icons.EDIT, on_click = lambda _ : edit(_)),
                        TextButton("Видалити", icon=icons.DELETE, on_click = lambda _ : _delete(_)),
                        Container(height=10)],
                                                                     ), padding = 15)
                    )

                    page.dialog = action_dlg
                    action_dlg.open = True
                    page.update()


                self.card = Card(
                    content = Container(
                        content=Column(
                            controls = [ListTile(
                                    leading = Text(f"{self.id}", size=20),
                                    title=Text(f"{self.teacher}\n"
                                               , weight = "bold"),
                                    subtitle = Text(f"Лідер        •  {self.leader}\n"
                                                    f"Кабінет     •  {self.room}")
                                )]
                        ), padding = 10, on_click = extend
                    ),
                    width=2000
                )


                return self.card

        for i in a:

            cl.controls.append(Class(i[0], i[1], i[2], i[3], i[4], i[5]))
            page.update()


        body.controls.append(cl)

        green_con.content = new_class_card

        view = View("/class-list",
                    controls=[div, green_con, body, appBar])

        return view