"""
UwU~!s your flow. Might be useful if you had an extra bad day.'   
"""

import random
import re
import requests

from mitmproxy import http

flamingo = 'rgb(242, 205, 205)'
mauve = 'rgb(203, 166, 247)'
peach = 'rgb(250, 179, 135)'
green = 'rgb(166, 227, 161)'
colors = [flamingo, mauve, peach, green]
bg_color_re = re.compile(r'background-color:\s*rgb\(\d{1,3}, \d{1,3}, \d{1,3}\)')

def response(flow: http.HTTPFlow) -> None:
    if flow.response and flow.response.content and flow.response.headers:
        try:
            type = flow.response.headers['Content-Type']
        finally:
            is_image = 'image' in type
        if is_image:
            kitten_image_url = requests.get('https://cataas.com/cat')
            flow.response.content = kitten_image_url.content
            flow.response.headers['Content-Type'] = 'image/jpeg'
            flow.response.headers['Content-Length'] = len(flow.response.content)
        else:
            content_str = flow.response.content.decode()
            content_str = bg_color_re.sub(f'background-color: {random.choice(colors)}', content_str)
            flow.response.content = content_str.encode()
            flow.response.headers['Content-Length'] = str(len(flow.response.content))