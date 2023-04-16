import omni.kit.commands
import omni.usd
import os
from pathlib import Path

scope = '/World/RecordCameras'
filepath = os.path.dirname(os.path.abspath(__file__))

class ExtensionModel():
    
    def __init__(self, controller):
        self.controller = controller
        self.datafilepath =  os.path.join(Path(filepath).parent.parent.parent, 'data')
        self.get_camera_data()
        self.get_keyframe_data()
        
    def create_camera(self):
        check = self.scope_is_exist(scope)
        if not check:
            omni.kit.commands.execute("CreatePrimCommand", prim_type='Scope', prim_path=scope)
        cam_path =  self.count_name(scope+'/Camera', 0)
        print(cam_path)
        omni.kit.commands.execute("CreatePrimCommand", prim_type='Camera', prim_path=cam_path)
        stage = omni.usd.get_context().get_stage()
        return cam_path, stage.GetPrimAtPath(cam_path)
    
    def scope_is_exist(self, path):
        stage = omni.usd.get_context().get_stage()
        scope_prim = stage.GetPrimAtPath(path)
        
        if scope_prim:
            return True
        else:
            return False
        
    def count_name(self, path, num):
        stage = omni.usd.get_context().get_stage()
        strnum = str(num)
        newpath = path + '_' + strnum
        scope_prim = stage.GetPrimAtPath(newpath)
        if scope_prim:
            return self.count_name(path, num+1)
        else:
            return newpath
    
    def delete_animationData(self, x, y, btn, m):
        del_camera = self.controller.selected_cam
        data = del_camera + '/animationData'
        stage = omni.usd.get_context().get_stage()
        prim = stage.GetPrimAtPath(data)
        if prim:
            omni.kit.commands.execute("DeletePrims", paths=[data])
        
        # Delete Thumbnails
        f = self.controller.thumbFolderPath + '/' + del_camera.split('/')[-1]
        tbs = os.listdir(f)
        for tb in tbs:
            os.remove(f + '/' + tb)
    #======================================================================================
    # Treeview Data
    #======================================================================================

    def get_camera_data(self):
        data = []
        
        stage = omni.usd.get_context().get_stage()
        scope_prim = stage.GetPrimAtPath(scope)
        if not scope_prim:
            return data
        
        cams = scope_prim.GetChildren()
        
        if len(cams) == 0:
            return data
        for cam in cams:
            data.append(cam.GetName())
            data.append(str(cam.GetPath()))
            animData = cam.GetChildren()
            if len(animData) == 0:
                data.append(0)
            elif 'animationData' not in str(animData[0]):
                data.append(0)
            else:
                l = len(animData[0].GetAttribute('visibility:x:inTangentTypes').Get())
                data.append(l)
            data.append("ep")
        
        return data
    
    def get_keyframe_data(self):
        data = []
        newData = []
        """(camName, imagePath, keyframe)"""
        
        Thumbnail_Folder = self.datafilepath + "/thumbnails"
        Cam_Thumbnails = os.listdir(Thumbnail_Folder)
        
        for tbs in Cam_Thumbnails:
            thumbsFolder = Thumbnail_Folder+'/'+tbs
            thumbs = os.listdir(thumbsFolder)
            newData.append(tbs)
            
            pathList = ''
            for tb in thumbs:
                pathList += tb +'/'                              
                data.append(tbs)
                keyframe = tb.split('.')[-2]
                imagepath = thumbsFolder +'/'+tb
                data.append(str(imagepath))
                data.append(keyframe)
            newData.append(pathList)
        # print(newData)
        return newData
                