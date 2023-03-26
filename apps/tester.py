output = """
Happy: 0 Sad: 4 Fear: 5 Angry: 3 Surprise: 2  {     "Happy": 0,     "Sad": 4,   
  "Fear": 5,     "Angry": 3,     "Surprise": 2 }
"""

import json
import subprocess


json_str = output[output.index("{") : output.index("}") + 1]
print(json_str)
json_obj = json.loads(json_str)
print(json_obj["Happy"])
