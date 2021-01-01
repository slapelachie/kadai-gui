import gi

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk
from kadai.themer import Themer
from kadai.config_handler import ConfigHandler

configHandler = ConfigHandler()
configHandler.save()
kadai_config = configHandler.get()


class MainWindow(Gtk.Window):
    def __init__(self):
        self.image_path = None

        Gtk.Window.__init__(self)

        padding = 15

        notebook = Gtk.Notebook()
        self.add(notebook)

        update_page = Gtk.Grid()
        update_page.set_border_width(padding)
        update_page.set_column_spacing(padding)
        update_page.set_row_spacing(padding)

        notebook.append_page(update_page, Gtk.Label("Update"))

        browse_button = Gtk.Button(label="Browse")
        browse_button.connect("clicked", self.on_browse_clicked)

        self.image_path_label = Gtk.Label("")

        label = Gtk.Label("Light Mode")

        switch = Gtk.Switch()
        switch.set_active(False)

        update_button = Gtk.Button(label="Update")
        update_button.connect("clicked", self.on_update_clicked)

        update_page.attach(browse_button, 0, 0, 1, 1)
        update_page.attach(self.image_path_label, 1, 0, 4, 1)
        update_page.attach(update_button, 0, 2, 1, 1)
        # update_page.attach(label, 1, 1, 1, 1)
        # update_page.attach(switch, 0, 1, 1, 1)

        self.set_border_width(padding)

        self.set_title("kadai-gtk")
        self.set_size_request(700, 500)

        self.connect("destroy", Gtk.main_quit)

    def on_changed(self, widget):
        # do shit on change
        pass

    def on_browse_clicked(self, widget):
        dialog = Gtk.FileChooserDialog(
            title="Choose a picture", parent=self, action=Gtk.FileChooserAction.OPEN
        )
        dialog.add_buttons(
            Gtk.STOCK_CANCEL,
            Gtk.ResponseType.CANCEL,
            Gtk.STOCK_OPEN,
            Gtk.ResponseType.OK,
        )

        self.browse_filters(dialog)
        response = dialog.run()

        if response == Gtk.ResponseType.OK:
            self.image_path = dialog.get_filename()
            self.image_path_label.set_text(dialog.get_filename())

        dialog.destroy()

    def on_update_clicked(self, widget):
        themer = Themer(
            self.image_path, kadai_config["data_directory"], config=kadai_config
        )
        themer.update()

    def browse_filters(self, dialog):
        filter_image = Gtk.FileFilter()
        filter_image.set_name("Image files")
        filter_image.add_mime_type("image/jpeg")
        filter_image.add_mime_type("image/png")
        filter_image.add_mime_type("image/webp")
        dialog.add_filter(filter_image)