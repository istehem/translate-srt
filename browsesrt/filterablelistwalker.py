import urwid

class FilterableListWalker(urwid.SimpleFocusListWalker):

    def get_focus(self):
        return super().get_focus()
