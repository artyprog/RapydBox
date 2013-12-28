// Code from Charles Law
function evaluate(data, create, name) {
    
    if (create == undefined) {
        create = false;
    }

    // Added by  me
    function createScript(src, name) {
        var head = document.getElementsByTagName('head')[0];
        var script = document.createElement('script');
        script.type = 'text/javascript';
        script.id = name;
        script.innerHTML = "\n" + src;               
        head.appendChild(script);
    }

    var rsOptions = {
        "filename": "demo",
        "toplevel": null,
        "basedir": null,
        "libdir": null
    };

    var outputOpts = {
        "beautify": true,
        "private_scope": false,
        "omit_baselib": true
    };

    var rapydscriptString = data;
    var output = OutputStream(outputOpts);
    rapydscriptString += '\n'; //just to be safe   
    try {
        var toplevel = parse(rapydscriptString, rsOptions);
        toplevel.print(output);
        if (create) {
            createScript(String(output), name);
        } else {
            eval(String(output));
        }

    } catch(err) {
        alert("ERROR: " + err.message + ". Line " + err.line + ", column " + err.col + ".");
    }

    return String(output);
}

/////////////////////////// Entry Point //////////////////

var mainScript = "rapydscript/pyj/moduleLoader.py";

jQuery.noConflict();
jQuery(document).ready(function () {
    jQuery.get(mainScript, function (r) {
        evaluate(r, true);
    });
});