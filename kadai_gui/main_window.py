import gi
import os

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, GdkPixbuf
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

        # preview_page = Gtk.Grid()
        # preview_page.set_border_width(padding)
        # preview_page.set_column_spacing(padding)
        # preview_page.set_row_spacing(padding)

        notebook.append_page(update_page, Gtk.Label("Update"))
        # notebook.append_page(preview_page, Gtk.Label("Preview"))

        browse_button = Gtk.Button(label="Browse")
        browse_button.connect("clicked", self.on_browse_clicked)

        self.image_path_label = Gtk.Label("")

        label = Gtk.Label("Light Mode")

        switch = Gtk.Switch()
        switch.set_active(False)

        self.current_image_pixbuf = GdkPixbuf.Pixbuf.new_from_file(
            os.path.join(kadai_config["data_directory"], "image")
        )

        # get actual resized dimensions instead of hard coding
        self.current_image_pixbuf = self.current_image_pixbuf.scale_simple(
            480, 270, GdkPixbuf.InterpType.BILINEAR
        )

        self.current_image = Gtk.Image()
        self.current_image.set_from_pixbuf(self.current_image_pixbuf)

        update_button = Gtk.Button(label="Update")
        update_button.connect("clicked", self.on_update_clicked)

        update_page.attach(self.current_image, 0, 0, 5, 1)
        update_page.attach(browse_button, 0, 1, 1, 1)
        update_page.attach(self.image_path_label, 1, 1, 2, 1)
        update_page.attach(update_button, 0, 3, 1, 1)
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
            self.image_path_label.set_text(resize_string(dialog.get_filename(), 30))

        self.current_image_pixbuf = GdkPixbuf.Pixbuf.new_from_file(
            dialog.get_filename()
        )
        self.current_image_pixbuf = self.current_image_pixbuf.scale_simple(
            480, 270, GdkPixbuf.InterpType.BILINEAR
        )
        self.current_image.set_from_pixbuf(self.current_image_pixbuf)

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


def resize_string(string, length):
    if len(string) > length:
        pre_string = string[: int((length / 2))]
        post_string = string[-int((length / 2)) :]

        string = "{}...{}".format(pre_string, post_string)

    return string
