window.ximport = def (m, name="X"):
    jQuery.ajaxSetup({async : False})    
    jQuery.get(m, def (r):
                    evaluate(r,True,name)
    )
    jQuery.ajaxSetup({async : True})  


#################################################### Dom manipulations ##################################################
Dom = (def ():
    def getId(id):
        return  document.getElementById(id)

    return {getId : getId}
)()


################################################### Application ###########################################################
Application  = (def ($,D):

    editor_setted = False
    editor_value = None
    editor_width = "100%"
    editor_height = "100%"

    fs = require('fs')	

    def setEditor(id):
        nonlocal cm,  editor_setted   
        if editor_setted: return 
        elt = D.getId(id)
        cm = CodeMirror.fromTextArea(elt)       
        cm.setOption("mode","python")
        cm.setOption("theme","monokai")
        cm.setOption("indentUnit",4)
        cm.setOption("lineNumbers",True)
        cm.setSize(editor_width, editor_height)
        editor_setted  = True

    # Menu
    def loadSample():
        select =  D.getId("select")
        index = select.selectedIndex
        if (index > 0):
            option = select.selectedOptions[0].innerHTML
            $.get("sketches/" + option, def(r):
                setEditorValue(r)            
            )

    # Script manage
    def loadScript():
        loadf = $("#loadFile") 
        loadf.trigger("click")
        loadf.change(def (evt):
                         path = $(this).val()
                         #setEditorValue(path) 
                         fs.readFile(path,'utf8', def (err,c):
                             setEditorValue(c)
                         )
        )

    def saveImage():
        data = canvas.save()
        saveas = $("#saveas") 
        saveas.trigger("click")
        saveas.change(def (evt) :
            path = $(this).val()                		       
            require("fs").writeFile( path , 
                data[22:], 'base64', 
                def ():
                    alert("Image successfully saved")
            )
        )

    def saveScript():
        data = getEditorValue()
        saveas = $("#saveas") 
        saveas.trigger("click")
        saveas.change(def (evt) :
            path = $(this).val()                		       
            require("fs").writeFile( path , data,
                def ():
                    alert("Script successfully saved")
            )
        )

    def stopAnim():
        window.canvas.stop()        

    def getEditorValue():
        nonlocal editor_value
        editor_value  = cm.getValue()
        return editor_value
    
    def setEditorValue(src):
        cm.setValue(src)
        editor_value = src
      
    def run():
        try:
            window.canvas.stop()
            delete(window.canvas)            
            window.canvas = new Canvas(Dom.getId('canvas'))  
            evaluate(getEditorValue())	
        except:
            alert("error when evaluating");	    

    def setupCanvas():
        window.canvas = new Canvas(Dom.getId('canvas'))            
        $.get("sketches/first.pyj", def(r):
                setEditorValue(r)            
                evaluate(getEditorValue())	
        )
           
    def main():       
        setEditor("editor")
        setupCanvas()

    return { start: main, 
             run : run, 
             loadScript : loadScript,
             saveScript : saveScript,
             saveImage : saveImage,
             stopAnim : stopAnim,
             loadSample : loadSample,
           }

)(jQuery,Dom)


