from pydantic import BaseModel
from typing import Optional, Dict, Any
import json

class BRDP(BaseModel):
    """BRDP of YoLink API."""
    code: str
    desc: str
    method: str
    data: Dict[str, Any]
    event: Optional[str]  # 'event' field is marked as optional


# Sample JSON data missing the 'event' field
json_string = '''
{
    "code": "000000",
    "time": 1701414599470,
    "msgid": 1701414599470,
    "method": "Home.getGeneralInfo",
    "desc": "Success",
    "data": {"id": "53c5283d408d4e6aba799330fbeeeaa9"}
}
'''

# Attempt to create a BRDP object using the provided JSON data
try:
    brdp = BRDP()
    brdp.parse_raw(json_string)
    brdp = BRDP.model_construct(**json.loads(json_string))
    print(brdp)
except Exception as e:
    print(f"Validation error occurred: {e}")
