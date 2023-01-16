# observableprops

Just a simple utility for automatically creating class properties and adding observers to it.

## Example Usage

``` python
from observableprops import ObservablesMeta
from threading import Event


class ColorBox(metaclass=ObservablesMeta):
    observable_properties = {
        "color": "add_color_observer",
    }

def gui_update_color(new):
    """
    Updates the color of the label in the GUI.
    """
    print("Color updated", new)

colorbox = ColorBox()
colorbox.add_color_observer(gui_update_color)

colorbox.color = "Blue" # All the observers will be called
```
