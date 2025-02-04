import copy
import opsc
import oobb
import oobb_base
import yaml
import os
import scad_help

def main(**kwargs):
    make_scad(**kwargs)

def make_scad(**kwargs):
    parts = []

    typ = kwargs.get("typ", "")

    if typ == "":
        #setup    
        #typ = "all"
        typ = "fast"
        #typ = "manual"

    oomp_mode = "project"
    #oomp_mode = "oobb"

    if typ == "all":
        filter = ""; save_type = "all"; navigation = True; overwrite = True; modes = ["3dpr"]; oomp_run = True
        #filter = ""; save_type = "all"; navigation = True; overwrite = True; modes = ["3dpr", "laser", "true"]
    elif typ == "fast":
        filter = ""; save_type = "none"; navigation = False; overwrite = True; modes = ["3dpr"]; oomp_run = False
    elif typ == "manual":
    #filter
        filter = ""
        #filter = "test"

    #save_type
        save_type = "none"
        #save_type = "all"
        
    #navigation        
        #navigation = False
        navigation = True    

    #overwrite
        overwrite = True
                
    #modes
        #modes = ["3dpr", "laser", "true"]
        modes = ["3dpr"]
        #modes = ["laser"]    

    #oomp_run
        oomp_run = True
        #oomp_run = False    

    #adding to kwargs
    kwargs["filter"] = filter
    kwargs["save_type"] = save_type
    kwargs["navigation"] = navigation
    kwargs["overwrite"] = overwrite
    kwargs["modes"] = modes
    kwargs["oomp_mode"] = oomp_mode
    kwargs["oomp_run"] = oomp_run
    
       
    # project_variables
    if True:
        pass
    
    # declare parts
    if True:

        directory_name = os.path.dirname(__file__) 
        directory_name = directory_name.replace("/", "\\")
        project_name = directory_name.split("\\")[-1]
        #max 60 characters
        length_max = 40
        if len(project_name) > length_max:
            project_name = project_name[:length_max]
            #if ends with a _ remove it 
            if project_name[-1] == "_":
                project_name = project_name[:-1]
                
        #defaults
        kwargs["size"] = "oobb"
        kwargs["width"] = 1
        kwargs["height"] = 1
        kwargs["thickness"] = 3
        #oomp_bits
        if oomp_mode == "project":
            kwargs["oomp_classification"] = "project"
            kwargs["oomp_type"] = "github"
            kwargs["oomp_size"] = "oomlout"
            kwargs["oomp_color"] = project_name
            kwargs["oomp_description_main"] = ""
            kwargs["oomp_description_extra"] = ""
            kwargs["oomp_manufacturer"] = ""
            kwargs["oomp_part_number"] = ""
        elif oomp_mode == "oobb":
            kwargs["oomp_classification"] = "oobb"
            kwargs["oomp_type"] = "part"
            kwargs["oomp_size"] = ""
            kwargs["oomp_color"] = ""
            kwargs["oomp_description_main"] = ""
            kwargs["oomp_description_extra"] = ""
            kwargs["oomp_manufacturer"] = ""
            kwargs["oomp_part_number"] = ""

        part_default = {} 
       
        part_default["project_name"] = project_name
        part_default["full_shift"] = [0, 0, 0]
        part_default["full_rotations"] = [0, 0, 0]
        
        part = copy.deepcopy(part_default)
        p3 = copy.deepcopy(kwargs)
        p3["width"] = 2
        p3["height"] = 2
        p3["thickness"] = 9
        #p3["extra"] = ""
        part["kwargs"] = p3
        nam = "base"
        part["name"] = nam
        if oomp_mode == "oobb":
            p3["oomp_size"] = nam
        parts.append(part)


    kwargs["parts"] = parts

    scad_help.make_parts(**kwargs)

    #generate navigation
    if navigation:
        sort = []
        #sort.append("extra")
        sort.append("name")
        sort.append("width")
        sort.append("height")
        sort.append("thickness")
        
        scad_help.generate_navigation(sort = sort)


def get_base(thing, **kwargs):

    prepare_print = kwargs.get("prepare_print", False)
    width = kwargs.get("width", 1)
    height = kwargs.get("height", 1)
    depth = kwargs.get("thickness", 3)                    
    rot = kwargs.get("rot", [0, 0, 0])
    pos = kwargs.get("pos", [0, 0, 0])
    extra = kwargs.get("extra", "")
    

    depth_latch = 4
    shift_nut = depth_latch / 2
    thickness_material = 3
    width_piece = 20
    tolerance = 0.5
    #add middle plate
    if True:
        #top
        p3 = copy.deepcopy(kwargs)
        p3["type"] = "positive"
        p3["shape"] = f"rounded_rectangle"  
        p3["radius"]  = 0.625
        
        wid = 10 - tolerance
        hei = 10 - tolerance - depth_latch
        dep = depth#thickness_material + 1 + tolerance
        size = [wid, hei, dep]
        p3["size"] = size
        pos1 = copy.deepcopy(pos)         
        pos1[1] += depth_latch / 2
        pos1[2] += depth - dep
        p3["pos"] = pos1
        oobb_base.append_full(thing,**p3)
        
        
    #add cross plate
    if True:
        #top
        p3 = copy.deepcopy(kwargs)
        p3["type"] = "positive"
        p3["shape"] = f"rounded_rectangle"
        p3["radius"]  = 1
        tolerance = 0.3
        wid = width_piece - tolerance
        hei = 6 - tolerance - depth_latch
        dep = 3 + tolerance
        size = [wid, hei, dep]
        p3["size"] = size
        p3["holes"] = True
        pos1 = copy.deepcopy(pos)
        pos1[0] += 0
        pos1[1] += depth_latch / 2
        pos1[2] += depth - dep
        p3["pos"] = pos1
        oobb_base.append_full(thing,**p3)

        #inside
        p3 = copy.deepcopy(kwargs)
        p3["type"] = "positive"
        p3["shape"] = f"rounded_rectangle"
        p3["radius"]  = 1        
        wid = wid
        hei = hei + depth_latch
        dep = depth - thickness_material - tolerance
        size = [wid, hei, dep]
        p3["size"] = size
        p3["holes"] = True
        pos1 = copy.deepcopy(pos)
        pos1[0] += 0
        pos1[1] += 0
        pos1[2] += 0
        p3["pos"] = pos1
        oobb_base.append_full(thing,**p3)

    #add up and down plate
        hei_middle_piece = 15
    if True:
        #top
        p3 = copy.deepcopy(kwargs)
        p3["type"] = "positive"
        p3["shape"] = f"rounded_rectangle"
        p3["radius"]  = 1
        tolerance = 0.5
        wid = 6 - tolerance
        hei = hei_middle_piece - tolerance
        dep = 3
        size = [wid, hei, dep]
        p3["size"] = size
        p3["holes"] = True
        pos1 = copy.deepcopy(pos)
        pos1[0] += 0
        pos1[1] += 0
        pos1[2] += depth - dep
        p3["pos"] = pos1
        oobb_base.append_full(thing,**p3)

        #inside
        p3 = copy.deepcopy(kwargs)
        p3["type"] = "positive"
        p3["shape"] = f"rounded_rectangle"
        p3["radius"]  = 1        
        wid = wid
        hei = hei
        dep = depth - 3
        size = [wid, hei, dep]
        p3["size"] = size
        p3["holes"] = True
        pos1 = copy.deepcopy(pos)
        pos1[0] += 0
        pos1[1] += 0
        pos1[2] += 0
        p3["pos"] = pos1
        oobb_base.append_full(thing,**p3)


    #add holes seperate
    p3 = copy.deepcopy(kwargs)
    p3["type"] = "p"
    p3["shape"] = f"oobb_holes"
    p3["both_holes"] = True  
    p3["depth"] = depth
    p3["holes"] = "perimeter"
    #p3["m"] = "#"
    pos1 = copy.deepcopy(pos)         
    p3["pos"] = pos1
    #oobb_base.append_full(thing,**p3)

    
    #add mounting nut
    p3 = copy.deepcopy(kwargs)
    p3["type"] = "n"
    p3["shape"] = f"oobb_nut"
    p3["depth"] = 5
    p3["hole"] = True
    p3["radius_name"] =  "m3"
    p3["m"] = "#"
    p3["overhang"] = True
    pos1 = copy.deepcopy(pos)
    pos1[0] += 0
    pos1[1] += shift_nut
    p3["pos"] = pos1
    oobb_base.append_full(thing,**p3)

    if prepare_print:
        #put into a rotation object
        components_second = copy.deepcopy(thing["components"])
        return_value_2 = {}
        return_value_2["type"]  = "rotation"
        return_value_2["typetype"]  = "p"
        pos1 = copy.deepcopy(pos)
        pos1[0] += 50
        return_value_2["pos"] = pos1
        return_value_2["rot"] = [180,0,0]
        return_value_2["objects"] = components_second
        
        thing["components"].append(return_value_2)

    
        #add slice # top
        p3 = copy.deepcopy(kwargs)
        p3["type"] = "n"
        p3["shape"] = f"oobb_slice"
        pos1 = copy.deepcopy(pos)
        pos1[0] += -500/2
        pos1[1] += 0
        pos1[2] += -500/2        
        p3["pos"] = pos1
        #p3["m"] = "#"
        oobb_base.append_full(thing,**p3)
    
if __name__ == '__main__':
    kwargs = {}
    main(**kwargs)