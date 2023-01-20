# -*- coding: utf-8 -*-

"""
Brython GUI for base type geographic 2D bounding box.

TODO :
    - add param 'name' for use it in HTML forms.
"""

__author__ = "thierry.herve@free.fr"
__copyright__ = "Thierry Hervé"
__license__ = "MIT"

from browser import html
import bbox

def BoundingBox_INPUT(id=''):
    input = html.INPUT('', id=id, type='text', size="45",
                    placeholder="latSW, longSW, latNE, longNE")
    return input

def BoundingBox_getvalue(input):
    V = input.value.split(',')
    if len(V) != 4:
        return None
    try:
        coords = bbox.BoundingBox([float(v) for v in V])
    except ValueError:
        return None
    
    return coords

def BoundingBox_setvalue(input, coords):
    input.value = ', '.join((f"{float(v):.5f}".rstrip('0') for v in coords))
        
