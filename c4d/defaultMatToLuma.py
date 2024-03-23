import c4d
from c4d import gui

def main():
    mat = doc.GetActiveMaterials() if doc.GetActiveMaterials() else doc.GetMaterials()
    if len(mat) == 0: return

    for i, m in enumerate(mat):
        try:
            colortex = m[c4d.MATERIAL_COLOR_SHADER][c4d.BITMAPSHADER_FILENAME]
            m[c4d.MATERIAL_USE_LUMINANCE]     = True
            m[c4d.MATERIAL_USE_ALPHA]     = True

            lumatex = c4d.BaseList2D(c4d.Xbitmap)
            lumatex[c4d.BITMAPSHADER_FILENAME] = colortex
            m.InsertShader(lumatex)
            m[c4d.MATERIAL_LUMINANCE_SHADER]  = lumatex

            alphatex = c4d.BaseList2D(c4d.Xbitmap)
            alphatex[c4d.BITMAPSHADER_FILENAME] = colortex
            m.InsertShader(alphatex)
            m[c4d.MATERIAL_ALPHA_SHADER]  = alphatex


            m[c4d.MATERIAL_USE_COLOR] = False
            m[c4d.MATERIAL_USE_REFLECTION] = False

            m[c4d.ID_BASELIST_NAME] = m[c4d.MATERIAL_LUMINANCE_SHADER][c4d.BITMAPSHADER_FILENAME]

            m.Message(c4d.MSG_UPDATE)

        except:
            pass


    c4d.EventAdd()

if __name__=='__main__':
    main()