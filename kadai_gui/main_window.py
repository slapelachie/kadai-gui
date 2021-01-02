import gi
import os
import kadai

from kadai.themer import Themer
from kadai.config_handler import ConfigHandler

from .utils import utils

gi.require_version("Gtk", "3.0")
from gi.repository import GLib, Gtk, GdkPixbuf

configHandler = ConfigHandler()
configHandler.save()
kadai_config = configHandler.get()


class MainWindow(Gtk.Window):
    def __init__(self):
        Gtk.Window.__init__(self)

        self.image_path = os.readlink(
            os.path.join(kadai_config["data_directory"], "image")
        )
        self.padding = 15
        self.width, self.height = 700, 500

        notebook = Gtk.Notebook()
        self.add(notebook)

        update_page = Gtk.Grid()
        update_page = setPagePadding(update_page, self.padding)

        options_page = Gtk.Grid()
        options_page = setPagePadding(options_page, self.padding)

        notebook.append_page(update_page, Gtk.Label("Update"))
        notebook.append_page(options_page, Gtk.Label("Options"))

        ### Update Page ###

        browse_button = Gtk.Button(label="Browse")
        browse_button.connect("clicked", self.onBrowseClicked)

        self.image_path_label = Gtk.Label(self.image_path)

        self.current_image_pixbuf = scalePixbufImage(
            GdkPixbuf.Pixbuf.new_from_file(self.image_path),
            self.width - (self.padding * 4),
        )
        self.current_image = Gtk.Image()
        self.current_image.set_from_pixbuf(self.current_image_pixbuf)

        pallete_image = utils.generatePalleteImage(self.image_path)
        self.pallete_image_pixbuf = scalePixbufImage(
            image2pixbuf(pallete_image), self.width - (self.padding * 4)
        )
        self.pallete_image = Gtk.Image()
        self.pallete_image.set_from_pixbuf(self.pallete_image_pixbuf)

        update_button = Gtk.Button(label="Update")
        update_button.connect("clicked", self.onUpdateClicked)

        update_page.attach(self.current_image, 0, 0, 4, 1)
        update_page.attach(self.pallete_image, 0, 1, 4, 1)
        update_page.attach(self.image_path_label, 0, 2, 4, 1)
        update_page.attach(browse_button, 0, 3, 2, 1)
        update_page.attach(update_button, 2, 3, 2, 1)

        ### Options Page ###

        label = Gtk.Label("Light Mode")

        self.light_mode_switch = Gtk.Switch()
        self.light_mode_switch.set_active(False)

        options_page.attach(label, 0, 1, 1, 1)
        options_page.attach(self.light_mode_switch, 1, 1, 1, 1)

        self.set_border_width(self.padding)
        self.set_title("kadai-gtk")
        self.set_size_request(self.width, self.height)
        self.set_resizable(False)

        self.connect("destroy", Gtk.main_quit)

    def onChanged(self, widget):
        # do shit on change
        pass

    def onBrowseClicked(self, widget):
        dialog = Gtk.FileChooserDialog(
            title="Choose a picture", parent=self, action=Gtk.FileChooserAction.OPEN
        )
        dialog.add_buttons(
            Gtk.STOCK_CANCEL,
            Gtk.ResponseType.CANCEL,
            Gtk.STOCK_OPEN,
            Gtk.ResponseType.OK,
        )

        self.browseFilters(dialog)
        response = dialog.run()

        if response == Gtk.ResponseType.OK:
            self.image_path = dialog.get_filename()
            self.image_path_label.set_text(
                utils.resizeString(dialog.get_filename(), 80)
            )

        self.current_image_pixbuf = scalePixbufImage(
            GdkPixbuf.Pixbuf.new_from_file(dialog.get_filename()),
            self.width - (self.padding * 4),
        )
        self.current_image.set_from_pixbuf(self.current_image_pixbuf)

        pallete_image = utils.generatePalleteImage(self.image_path)
        self.pallete_image_pixbuf = scalePixbufImage(
            image2pixbuf(pallete_image), self.width - (self.padding * 4)
        )
        self.pallete_image.set_from_pixbuf(self.pallete_image_pixbuf)

        dialog.destroy()

    def onUpdateClicked(self, widget):
        themer = Themer(
            self.image_path, kadai_config["data_directory"], config=kadai_config
        )

        if self.light_mode_switch.get_active():
            themer.enableLightTheme()

        themer.update()

    def browseFilters(self, dialog):
        filter_image = Gtk.FileFilter()
        filter_image.set_name("Image files")
        filter_image.add_mime_type("image/jpeg")
        filter_image.add_mime_type("image/png")
        filter_image.add_mime_type("image/webp")
        dialog.add_filter(filter_image)


def image2pixbuf(image):
    data = image.tobytes()
    w, h = image.size
    data = GLib.Bytes.new(data)
    pix = GdkPixbuf.Pixbuf.new_from_bytes(
        data, GdkPixbuf.Colorspace.RGB, False, 8, w, h, w * 3
    )
    return pix


def setPagePadding(page, padding):
    page.set_border_width(padding)
    page.set_column_spacing(padding)
    page.set_row_spacing(padding)

    return page


def scalePixbufImage(pixbuf_image, new_width):
    scaled_width, scaled_height = utils.getScaledDimensions(
        (
            pixbuf_image.get_width(),
            pixbuf_image.get_height(),
        ),
        new_width,
    )

    return pixbuf_image.scale_simple(
        scaled_width, scaled_height, GdkPixbuf.InterpType.BILINEAR
    )
