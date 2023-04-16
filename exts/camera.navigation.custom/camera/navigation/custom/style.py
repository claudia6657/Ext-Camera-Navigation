import omni.ui as ui
from functools import partial

def show_tooltip(label):
    """Show a tooltip.

    Use this callback to avoid issues with the tooltip inheriting style
    (in particular margin/padding) from parent widgets.
    """
    ui.Label(
        label,
        style={
            "color": 0xFF585A51,
            "background_color": 0xFFCAF5FB,
            "margin": 2,
            "padding": 4,
        },
    )
    return

class ImageAndTextButton(ui.ZStack):
    """Hack class to allow centering an icon and text in a Button."""

    def __init__(self, label, width, height, image_path, image_width, image_height, mouse_pressed_fn, tooltip):

        super().__init__(width=width, height=height, style={"margin": 1, "padding": 1})

        with self:

            # Add a button with a blank space for the label - this ensures it respects the
            # height
            ui.Button(
                " ",
                width=ui.Percent(100),
                height=height,
                mouse_pressed_fn=mouse_pressed_fn,
                tooltip_fn=partial(show_tooltip, tooltip),
            )

            # HStack with an image and label
            with ui.HStack(width=ui.Percent(100)):
                ui.Spacer()
                im = ui.Image(image_path, width=image_width)
                ui.Spacer(width=ui.Pixel(4))
                ui.Label(label, width=0)
                ui.Spacer()
                          
Margin = 5

class Colors:
    Text = ui.color.shade(0xFF171717, light=0xFFE0E0E0)
    LightText = ui.color.shade(0xFF919191, light=0xFFE0E0E0)
    SpecificText = ui.color.shade(0xFF7F6600, light=0xFFE0E0E0)
    BlockBackground = ui.color.shade(0xFFDCDCDC, light=0xFFE0E0E0)
    HoverBackground = ui.color.shade(0xFF9F9F9F, light=0xFFE0E0E0)
    Border = ui.color.shade(0x10525252, light=0xFFE0E0E0)

common_style={
    "Label::Title":{"font_size": 20, "margin_width":Margin, "color":Colors.Text},
    "Label::BlockName":{"font_size": 20, "margin_width":Margin*2, "color":Colors.Text},
    "Label::BlockNum":{"font_size": 20, "margin_width":Margin*2, "color":Colors.SpecificText},
    "Label::AddLabel":{"font_size": 18, "margin_width":Margin*2, "color":Colors.LightText},
    "ScrollingFrame":{
        "background_color":Colors.BlockBackground,
        "border_radius":5,
        "border_color": Colors.Border,
        "margin_width": Margin,
        "margin_height": Margin *2
    },
    "ScrollingFrame::add:hovered":{
        "background_color":Colors.HoverBackground,
        "border_radius":5,
        "border_color": Colors.Border,
        "margin_width": Margin,
        "margin_height": Margin *2
    },
    "ScrollingFrame::keyframe":{
        "background_color": 0x00,
        "border_radius":5,
        "border_color": Colors.Border,
        "margin_width": Margin,
        "margin_height": Margin *2
    },
    "HStack::treeviewItem":{"margin_height": 10},
    "HStack::ScreenshotBlock":{"background_color":Colors.BlockBackground},
    "Line":{"color":Colors.LightText},
}

