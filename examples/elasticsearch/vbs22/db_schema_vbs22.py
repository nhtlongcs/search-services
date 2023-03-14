from typing import List, Optional
from pydantic import BaseModel

class Video(BaseModel):
    v3cId: str
    vimeoId: str
    title: str
    description: str
    duration: int
    uploadDate: str
    channel: str
    license: str
    width: int
    height: int
    tags: List[str]
    categories: List[str]


# {'categories': ['/categories/sports'],
#  'channel': 'valentinxflad',
#  'description': '<p class="first">On Sunday, May 25th, many riders from Paris '
#                 'and from Argentina came to the infamous &quot;Opera '
#                 'Spot&quot; in the middle of Paris to ride together.</p>\n'
#                 '<p>It was a great time: we rode as hard as we could, we spoke '
#                 'together, we chilled a lot...</p>\n'
#                 '<p>Valentin FLAD - May 2014</p>',
#  'duration': 273,
#  'height': 720,
#  'license': 'by-nc-sa',
#  'tags': ['fish eye',
#           'edit',
#           'flad',
#           'vid?o',
#           'acrobatique',
#           'Flatland',
#           'riding',
#           'BMX',
#           'canon',
#           'v?lo',
#           'paris',
#           'jam',
#           'Flat',
#           'france',
#           'sport',
#           'Opera',
#           'Bike',
#           'extreme'],
#  'title': 'PARISIANA JAM',
#  'uploadDate': '2014-05-31 10:32:38',
#  'v3cId': '00001',
#  'vimeoId': '96990666',
#  'width': 1280}
