from flet import *
from flet_route import path, Routing
from admin_home import AdminPage
from admin_event_list import EventListPage
from admin_class_list import ClassListPage
from user_home import UserPage
from user_event_list import UserEventListPage

from index import IndexPage

def main(app_page: Page):

    theme = Theme()
    theme.page_transitions.macos = PageTransitionTheme.FADE_UPWARDS
    theme.page_transitions.ios = PageTransitionTheme.FADE_UPWARDS
    app_page.theme = theme

    app_routes = [
        path(url = "/", clear=True, view=IndexPage().view),
        path(url = "/home", clear = True, view = UserPage().view),
        path(url = "/home-admin", clear = True, view = AdminPage().view),
        path(url = "/event-list", clear = True, view = EventListPage().view),
        path(url = "/class-list", clear=True, view=ClassListPage().view),
        path(url="/user-event-list", clear=True, view=UserEventListPage().view)
    ]

    Routing(page = app_page, app_routes = app_routes)
    app_page.go(app_page.route)


app(target=main, view = WEB_BROWSER, assets_dir = "assets")