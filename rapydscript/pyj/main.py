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
        cm.setOption("theme","ambiance")
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

    # Signal user to run after loading script
    def changeRunButton(reset=False):
        r = Dom.getId("run")
        if reset:
            r.style.color = "rgb(230,250,255)"
        else:
            r.style.color = "red"

    # Script manage
    def loadScript():
        loadf = $("#loadFile") 
        loadf.trigger("click")
        loadf.change(def (evt):
                         path = $(this).val()
                         fs.readFile(path,'utf8', def (err,c):
                             setEditorValue(c)
                             changeRunButton()
                             loadf.val("")                      
                         )
        )

    def saveImage():
        data = canvas.save()
        saveas = $("#saveimage") 
        saveas.trigger("click")
        saveas.one("change", def (evt) :
            path = $(this).val() 
            $(this).val("")
            require("fs").writeFile( path + ".png", 
                data[22:], 'base64', 
                def ():
                    alert("Image successfully saved")
            )
        )

    def saveScript():
        data = getEditorValue()
        saveas = $("#savescript") 
        saveas.trigger("click")
        saveas.one("change", def (evt) :
            path = $(this).val()                		       
            require("fs").writeFile( path + ".pyj", data,
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
        changeRunButton(True)
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
           
    def clearCanvas():
        stopAnim()
        window.canvas.clear()
        delete(window.canvas)
        window.canvas = new Canvas(Dom.getId('canvas'))


    def clearScene():
        clearCanvas()
        cm.setValue("")


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
             clearCanvas : clearCanvas,
             clearScene : clearScene
           }

)(jQuery,Dom)


