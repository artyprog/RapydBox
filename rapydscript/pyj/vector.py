/* This module use paperjs 
 *
 * Paper.js v0.9.15 - The Swiss Army Knife of Vector Graphics Scripting.
 * http://paperjs.org/
 *
 * Copyright (c) 2011 - 2013, Juerg Lehni & Jonathan Puckey
 * http://lehni.org/ & http://jonathanpuckey.com/
 */


Vector = (def ():
    def create(x=0, y=0):
        return new paper.Point(x, y)
    return {create : create }
)()


