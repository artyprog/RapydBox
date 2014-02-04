mod = ["rapydscript/pyj/modone.py",
       "rapydscript/pyj/main.py"]


def loadModules() :  
    lstreq = []
    counter = [0]
    dictSrc  = {}

    for i in range(len(mod)):
        lstreq.push([i,jQuery.get(mod[i])]) 
       
    for [i,j] in lstreq:
        (def (index):
            lstreq[index][1].done(def (r):                
                dictSrc[index] = r
                counter[0] = counter[0] + 1
                allLoaded = (counter[0] == len(mod))
                if (allLoaded):
                    for i in range(len(mod)):
                        evaluate(dictSrc[i])
                    window.Application.start()
            )     
        )(i)
         
loadModules()


