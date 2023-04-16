import omni.ui as ui
import omni.usd
from .style import ImageAndTextButton, common_style
import os
from pathlib import Path
from PIL import ImageGrab
from omni.kit.viewport.utility import get_active_viewport, get_active_viewport_window

from .model import ExtensionModel
from .treeview import KeyframeItem, KeyframeModel, KeyframeDelegate

filepath = os.path.dirname(os.path.abspath(__file__))

class CamItem(ui.AbstractItem):
    """Single item of the model"""

    def __init__(self, name, prim, keynum, empty):
        super().__init__()
        self.name_model = ui.SimpleStringModel(name)
        self.prim_model = ui.SimpleStringModel(prim)
        self.keynum_model = ui.SimpleIntModel(keynum)
        self.empty_model = ui.SimpleStringModel(empty)
    
    def __repr__(self):
        return f'"{self.name_model.as_string} {self.prim_model.as_string} {self.keynum_model.as_string} {self.empty_model.as_string}"'

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
        return 4

    def get_item_value_model(self, item, column_id):
        if column_id == 0:
            return item.name_model
        elif column_id ==1:
            return item.prim_model
        elif column_id == 2:
            return item.keynum_model
        elif column_id == 3:
            return item.empty_model
            
    def on_changed(self, args):
        regrouped = zip(*(iter(args),) * 4)
        self._children = [CamItem(*t) for t in regrouped]
        self._item_changed(None)

class CamDelegate(ui.AbstractItemDelegate):
    
    def build_widget(self, model, item, column_id, level, expanded):
        # TreeView Widget
        if isinstance(item, CamItem):
            if column_id == 0:
                value_model = model.get_item_value_model(item, column_id)
                text = value_model.get_value_as_string()
                with ui.VStack(style=common_style, height=35, width=ui.Percent(100)):
                    with ui.HStack(height=20, name='treeviewItem'):
                        ui.Spacer(width=ui.Pixel(20))
                        ui.Image(os.path.join(Path(filepath).parent.parent.parent, 'data') + "/video.svg", width=20)
                        ui.Label(text, name="BlockName")
                        ui.Spacer()
                    ui.Line(height=3, width=ui.Percent(100))
            if column_id == 3:
                with ui.VStack(style=common_style, height=35, width=ui.Percent(100)):
                    with ui.HStack(style=common_style, height=30, width=ui.Percent(100)):
                        ui.Button(
                            "",
                            width=30,
                            height=30,
                            image_url = os.path.join(Path(filepath).parent.parent.parent, 'data') + "/Add_Key.svg",
                            tooltip='Add Keyframes',
                            mouse_pressed_fn=ExtensionUI.on_click_add_keyframe,
                        )
                        ui.Button(
                            "",
                            width=30,
                            height=30,
                            image_url = os.path.join(Path(filepath).parent.parent.parent, 'data') + "/play_.svg",
                            tooltip='Play',
                        )
                        ui.Button(
                            "",
                            width=30,
                            height=30,
                            image_url = os.path.join(Path(filepath).parent.parent.parent, 'data') + "/Delete.svg",
                            tooltip='DELETE All Keyframes',
                        )
            if column_id == 2:
                value_model = model.get_item_value_model(item, column_id)
                text = value_model.get_value_as_string()
                with ui.VStack(style=common_style, height=35, width=ui.Percent(100)):
                    with ui.HStack(height=20, name='treeviewItem'):
                        ui.Spacer()
                        ui.Label(text, name="BlockNum")
                        ui.Spacer()
                    ui.Line(height=3, width=ui.Percent(100))

class ExtensionUI():

    def __init__(self, controller):
        self.controller = controller
        self._model = ExtensionModel(self)
        self.datafilepath =  os.path.join(Path(filepath).parent.parent.parent, 'data')
        self.thumbFolderPath = self.datafilepath + '/thumbnails'
        self.selected_cam = None
        self.build_controll_window()
        
    def build_controll_window(self):
        self.window = ui.Window("Camera Controller")
        self.window.deferred_dock_in("Property")
        self.window.frame.set_style({
            "Window":{
                "background_color": 0xFFD1D1D1,
                "padding":5
            }
        })
        with self.window.frame:
            with ui.VStack(style=common_style):
                ui.Label("Camera Navigation System", name="Title", height=40)  
                self.camera_header = ui.VStack(height=550)
                with self.camera_header:
                    self.build_camera_treeview()
                    self.add_block()
                    self.build_page_keyframes()
                    self.keyframe_view.visible = False

    def build_camera_treeview(self):
        self.camStack = self._model.get_camera_data()
        self.camModel = CamModel(self.camStack)
        self.camDel = CamDelegate()
        self.camera_frame = ui.ScrollingFrame(
            horizontal_scrollbar_policy=ui.ScrollBarPolicy.SCROLLBAR_ALWAYS_OFF,
            vertical_scrollbar_policy=ui.ScrollBarPolicy.SCROLLBAR_AS_NEEDED,
        )
        with self.camera_frame:
            with ui.VStack(width=ui.Percent(100)):
                treeview = ui.TreeView(
                    self.camModel, 
                    root_visible=False,
                    header_visible=False,
                    delegate=self.camDel,
                    selection_changed_fn=self.on_treeview_selection_changed,
                )
                treeview.column_widths = [ui.Fraction(1), ui.Pixel(0), ui.Pixel(100), ui.Pixel(100)]
                treeview.set_mouse_double_clicked_fn(self.on_treeview_double_clicked)
    
    def add_block(self):
        self.add_cam = ui.ScrollingFrame(
            style= common_style, height=70, width=ui.Percent(100), name="add",
            horizontal_scrollbar_policy=ui.ScrollBarPolicy.SCROLLBAR_ALWAYS_OFF,
            vertical_scrollbar_policy=ui.ScrollBarPolicy.SCROLLBAR_ALWAYS_OFF,
            mouse_pressed_fn=self.on_click_add_camera
            )
        with self.add_cam:
            with ui.HStack(width=ui.Percent(100)):
                ui.Spacer(width=ui.Pixel(20))
                ui.Image(self.datafilepath + "/add.svg", width=18)
                ui.Label("New Camera", name="AddLabel")
                ui.Spacer()
    
    def build_page_keyframes(self):
        self.keyframe_view = ui.VStack(height=ui.Percent(100))
        with self.keyframe_view:
            with ui.HStack(height=30, width=ui.Percent(100)):
                with ui.HStack(style={"margin_width":5}, alignment=ui.Alignment.RIGHT_CENTER):
                    ui.Button(
                        "",
                        width=30,
                        height=30,
                        mouse_pressed_fn=self._model.delete_animationData,
                        image_url = self.datafilepath + "/Delete.svg",
                        tooltip='DELETE All Keyframes',
                    )
                ui.Spacer(width=5)
            ui.Spacer(height=5)
            
            self.build_keyframe_block()
            
    def build_keyframe_block(self):      
        self.keyframeModel = KeyframeModel(self._model.get_keyframe_data())
        self.keyDel = KeyframeDelegate()
        self.keyframeBlock = ui.ScrollingFrame(
            height=ui.Percent(100), name='keyframe', visible = True,
            horizontal_scrollbar_policy=ui.ScrollBarPolicy.SCROLLBAR_ALWAYS_OFF,
            vertical_scrollbar_policy=ui.ScrollBarPolicy.SCROLLBAR_AS_NEEDED,
        )
        with self.keyframeBlock:
            with ui.VStack(height=ui.Percent(100)):    
                treeview = ui.TreeView(
                    self.keyframeModel, 
                    root_visible=False,
                    header_visible=False,
                    delegate=self.keyDel
                )
                treeview.column_widths = [ui.Pixel(0), ui.Fraction(1)]        
                    
    def on_treeview_selection_changed(self, selected_items):
        # Change Selected Camera and active
        for item in selected_items:
            path = item.prim_model.as_string
            self.selected_cam = path
            
            ctx = omni.usd.get_context()
            selection = ctx.get_selection().set_selected_prim_paths([path], True)
            viewport = get_active_viewport()
            viewport.camera_path = path

    def on_treeview_double_clicked(self, x, y, btn, m):
        if btn == 0:
            self.camera_frame.visible = False
            self.add_cam.visible = False
            self.keyframe_view.visible = True
                
    def on_click_add_camera(self, x, y, btn, m):
        # Click To Add Camera
        if btn == 0:
            camPath, camPrim = self._model.create_camera()
            self.camStack.insert(0, camPrim.GetName())
            self.camStack.insert(1, camPath)
            self.camStack.insert(2, 0)
            
            self.camModel.on_changed(self.camStack)
    
    def on_click_add_keyframe(self, a, b, c):
        # Keyframe Timeline
        print(a, b, c)
        timelineInterface = omni.timeline.get_timeline_interface()
        current_time = int(timelineInterface.get_current_time() * timelineInterface.get_time_codes_per_seconds())
        '''
        fPath = self.thumbFolderPath + '/' + self.selected_cam.split('/')[-1]
        if not self._model.scope_is_exist(fPath):
            os.mkdir(fPath)
        savePath =  fPath + '/'+ str(current_time) + '.png'
        # Screenshot & Save
        minPos = min([get_active_viewport_window().width, get_active_viewport_window().height])
        region = (100, 100, minPos-100, minPos-100)
        img = ImageGrab.grab(region)
        img.save(savePath)
        '''
        # Add keyframe
        print(self, current_time)
        omni.kit.commands.execute("SetAnimCurveKeys", paths=[self.selected_cam], time=current_time)
        
        # Refresh
        #self.keyframeModel.on_changed(self._model.get_keyframe_data())
    
    def shutdown(self):
        self.controller = None
        self.datafilepath =  None
        self.window = None