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

    def setEditor(id):
        nonlocal cm,  editor_setted   
        if editor_setted: return 
        elt = D.getId(id)
        cm = CodeMirror.fromTextArea(elt)
        cm.setValue("alert('Hello from RapydScript')")
        cm.setOption("mode","python")
        cm.setOption("theme","monokai")
        cm.setOption("indentUnit",4)
        cm.setOption("lineNumbers",True)
        cm.setSize(620, 650)
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
                         alert(path)
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
        alert("Stop Animation")

    def pauseAnim():
        alert("pauseAnimation")

    def getEditorValue():
        nonlocal editor_value
        editor_value  = cm.getValue()
        return editor_value
    
    def setEditorValue(src):
        cm.setValue(src)
        editor_value = src
    
    def run():
        try:
            delete(window.canvas)
            window.canvas = new Canvas(Dom.getId('canvas'))    
            evaluate(getEditorValue())	
        except:
            alert("error when evaluating");	    

    def setupCanvas():
        window.canvas = new Canvas(Dom.getId('canvas'))    
        setEditorValue(defaultScript)

    def hello():
        alert("HELLO")

    def main():
        setEditor("editor")
        setupCanvas()
 
    return { start: main, 
             run : run, 
             loadScript : loadScript,
             saveScript : saveScript,
             saveImage : saveImage,
             stopAnim : stopAnim,
             pauseAnim : pauseAnim,
             loadSample : loadSample,
             hello : App.hello
           }

)(jQuery,Dom)

##################################################### Miscellanous ##############################


defaultScript = """# Basic script0
# Click 'Run' to launch it


WIDTH, HEIGHT = 625, 640

canvas.size(WIDTH,HEIGHT)
fill(1,0.98,0.89)
rect(0,0,WIDTH,HEIGHT)
stroke(1,0,0)
line(0,0,WIDTH,HEIGHT)
"""


