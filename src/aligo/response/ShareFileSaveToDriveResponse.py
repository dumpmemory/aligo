"""..."""
from dataclasses import dataclass

from datclass import DatClass


@dataclass
class ShareFileSaveToDriveResponse(DatClass):
    """..."""
    file_id: str = None
    drive_id: str = None
    domain_id: str = None
    async_task_id: str = None
