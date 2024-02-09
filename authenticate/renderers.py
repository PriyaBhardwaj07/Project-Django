from rest_framework import renderers
import json

# The renderers module is used to define and customize how the response 
# content should be formatted.
# it is used so that at the front end they can see what error it is rather than blanks

class UserRenderer(renderers.JSONRenderer):
    charset='utf-8'
    def render(self,data,accepted_media_type=None,renderer_context=None):
        response =''
        if 'ErrorDetail' in str(data):
            response = json.dumps({'errors':data})
        else:
            response= json.dumps(data)
            
        return response
