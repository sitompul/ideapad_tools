#!/usr/bin/env python3

import gi
import os
from pathlib import Path

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk


modules = [
    {
        "label": "Battery Threshold",
        "path": "/sys/bus/platform/drivers/ideapad_acpi/VPC2004:00/conservation_mode"
    },
    {
        "label": "Fn Lock",
        "path": "/sys/bus/platform/drivers/ideapad_acpi/VPC2004:00/fn_lock"
    },
    {
        "label": "Camera Power",
        "path": "/sys/bus/platform/drivers/ideapad_acpi/VPC2004:00/camera_power"
    }
]

class ListBoxWindow(Gtk.Window):
    def __init__(self):
        # Read file input

        self.status = [None] * len(modules)
        for i in range(len(modules)):
          module = modules[i]
          self.status[i] = Path(module["path"]).read_text().strip()

        Gtk.Window.__init__(self, title="Ideapad Tools")
        self.set_border_width(10)

        box_outer = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=6)
        self.add(box_outer)

        listbox = Gtk.ListBox()
        listbox.set_selection_mode(Gtk.SelectionMode.NONE)
        box_outer.pack_start(listbox, True, True, 0)

        for index in range (len(modules)):
          module = modules[index]
          
          row = Gtk.ListBoxRow()
          hbox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=50)
          row.add(hbox)
          vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
          hbox.pack_start(vbox, True, True, 0)

          label = Gtk.Label()
          label.set_text(module["label"])
          label.set_xalign(0)
          vbox.pack_start(label, True, True, 0)

          switch = Gtk.Switch()
          switch.props.valign = Gtk.Align.CENTER
          switch.connect("notify::active", self.on_toggle_switch, index)
          switch.set_active(self.status[index] == "1")
          hbox.pack_start(switch, False, True, 0)

          listbox.add(row)
    def on_toggle_switch (self, switch, gparam, i):
      module = modules[i]
      if switch.get_active():
        Path(module["path"]).write_text("1")
      else:
        Path(module["path"]).write_text("0")


win = ListBoxWindow()
win.connect("destroy", Gtk.main_quit)
win.show_all()
Gtk.main()