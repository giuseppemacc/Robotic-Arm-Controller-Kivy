from obj3D import Object3D
                       
all_Object = {}

def Dic_All_Obj(file_obj):
    with open (file_obj,"r") as file:
        lines = file.readlines()
        for line in lines:
            if line.startswith("o "):
                name = line[2:-10]
                all_Object.setdefault(name)
                with open(f"Object\\{name}.obj","w") as object:
                    object.write(f"o {name}\n")
                    for l in lines[lines.index(line)+1:]:
                        if(l.startswith("o ")):
                            break
                        else:
                            object.write(l)                   
    #più e alto più è chiaro
    color=[
        [.1,.1,.55,0], # S_Base
        [.1,.1,.60,0], # Nodo1
        [.1,.1,.65,0], # Braccio1
        [.1,.1,.70,0], # Nodo2
        [.1,.1,.75,0], # Braccio2
        [.1,.1,.80,0], # Nodo3
        [.1,.1,.85,0], # Pinza_Base
        [.1,.1,.90,0], # Pinza
        [.1,.1,.50,0], # Base
        [.1,.1,.95,0], # Pinza_1
        [.1,.1,.95,0]  # Pinza_2
    ]
    i = 0
    for key in all_Object.keys():
        print(key)
        obj = None
        obj = Object3D(f"Object\\{key}.obj",color[i])
        all_Object[key] = obj
        
        i+=1
        
        
    return all_Object