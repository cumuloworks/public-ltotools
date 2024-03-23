import c4d
def main() -> None:
    copyfrom = op[c4d.ID_USERDATA,1]  
    copyto = op[c4d.ID_USERDATA,2]      
    copyfrom_morph_count = copyfrom.GetMorphCount()    
    copyto_morph_count = copyto.GetMorphCount()    
    for from_id in range(copyfrom_morph_count):
        from_morph = copyfrom.GetMorph(from_id)
        if from_morph is None:
            continue
        from_morph_name = from_morph.GetName()  
        from_morph_id = from_morph.GetID()          
        for to_id in range(copyto_morph_count):
            to_morph = copyto.GetMorph(to_id)
            if to_morph is None:
                continue
            to_morph_name = to_morph.GetName()              
            if from_morph_name == to_morph_name:
                to_morph_id = to_morph.GetID()  
                
                copyto[4000, (to_morph_id+10)*100+1] = copyfrom[4000, (from_morph_id+10)*100+1]
                break  
 