import omni.ui as ui
import omni.usd
import os
from pathlib import Path

from .style import ImageAndTextButton, common_style
# ============================================================
# Camera Item Data
# ============================================================
filepath = os.path.dirname(os.path.abspath(__file__))

class CamItem(ui.AbstractItem):
    """Single item of the model"""

    def __init__(self, name, prim, keynum):
        super().__init__()
        self.name_model = ui.SimpleStringModel(name)
        self.prim_model = ui.SimpleStringModel(prim)
        self.keynum_model = ui.SimpleIntModel(keynum)
    
    def __repr__(self):
        return f'"{self.name_model.as_string} {self.prim_model.as_string} {self.keynum_model.as_string}"'

class CamModel(ui.AbstractItemModel):  
    def __init__(self, args):
        super().__init__()
        self.on_changed(args)

    def get_item_children(self, item):
        """Returns all the children when the widget asks it."""
        if item is not None:
            # Since we are doing a flat list, we return the children of root only.
            # If it's not root we return.
            return []

        return self._children

    def get_item_value_model_count(self, item):
        """The number of columns"""
        return 3

    def get_item_value_model(self, item, column_id):
        if column_id == 0:
            return item.name_model
        elif column_id ==1:
            return item.prim_model
        elif column_id == 2:
            return item.keynum_model
    
    def on_changed(self, args):
        regrouped = zip(*(iter(args),) * 3)
        self._children = [CamItem(*t) for t in regrouped]
        self._item_changed(None)

class CamDelegate(ui.AbstractItemDelegate):
    
    def build_widget(self, model, item, column_id, level, expanded):
        # TreeView Widget
        if isinstance(item, CamItem):
            if column_id == 0:
                value_model = model.get_item_value_model(item, column_id)
                text = value_model.get_value_as_string()
                with ui.VStack(style=common_style, height=25, width=ui.Percent(100)):
                    with ui.HStack(height=20, name='treeviewItem'):
                        ui.Spacer(width=ui.Pixel(20))
                        ui.Image(os.path.join(Path(filepath).parent.parent.parent, 'data') + "/video.svg", width=20)
                        ui.Label(text, name="BlockName")
                        ui.Spacer()
                    ui.Line(height=3, width=ui.Percent(100))
            
            if column_id == 2:
                value_model = model.get_item_value_model(item, column_id)
                text = value_model.get_value_as_string()
                with ui.VStack(style=common_style, height=25, width=ui.Percent(100)):
                    with ui.HStack(height=20, name='treeviewItem'):
                        ui.Spacer()
                        ui.Label(text, name="BlockNum")
                        ui.Spacer()
                    ui.Line(height=3, width=ui.Percent(100))

# ============================================================
# Keyframe Data
# ============================================================

class KeyframeItem(ui.AbstractItem):
    """Single item of the model"""

    def __init__(self, camName, imagePath):
        super().__init__()
        self.camName_model = ui.SimpleStringModel(camName)
        self.imagePath_model = ui.SimpleStringModel(imagePath)
    
    def __repr__(self):
        return f'"{self.camName_model.as_string} {self.imagePath_model.as_string}"'

class KeyframeModel(ui.AbstractItemModel):
    def __init__(self, args):
        super().__init__()
        self.on_changed(args)

    def get_item_children(self, item):
        """Returns all the children when the widget asks it."""
        if item is not None:
            # Since we are doing a flat list, we return the children of root only.
            # If it's not root we return.
            return []

        return self._children

    def get_item_value_model_count(self, item):
        """The number of columns"""
        return 2

    def get_item_value_model(self, item, column_id):
        if column_id == 0:
            return item.camName_model
        elif column_id ==1:
            return item.imagePath_model
    
    def on_changed(self, args):
        regrouped = zip(*(iter(args),) * 2)
        self._children = [KeyframeItem(*t) for t in regrouped]
        self._item_changed(None)
        
        return self._children

class KeyframeDelegate(ui.AbstractItemDelegate):
            
    def build_widget(self, model, item, column_id, level, expanded):
        # TreeView Widget
        selection  = omni.usd.get_context().get_selection().get_selected_prim_paths()
        self.selected_cam = selection
        
        if isinstance(item, KeyframeItem):
            if column_id == 1:
                relative_model = model.get_item_value_model(item, 0).get_value_as_string()
                if str(relative_model) in str(selection):
                    value_model = model.get_item_value_model(item, column_id)
                    text = value_model.get_value_as_string()
                    imagePath = text.split('/')
                    
                    self.keyGrid = ui.VGrid(column_width = 100,height=ui.Percent(100))
                    
                    with self.keyGrid:
                        
                        for ip in imagePath:
                            if ip == "":
                                pass
                            else:
                                imagepath = os.path.join(Path(filepath).parent.parent.parent, 'data') + '/thumbnails/' + relative_model + '/' + ip
                                with ui.HStack():
                                    ui.Button(
                                        "",
                                        width=100,
                                        height=100,
                                        image_url = imagepath,
                                        tooltip=str(ip),
                                    )
                                print(imagepath)
