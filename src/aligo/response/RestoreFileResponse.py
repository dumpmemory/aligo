"""..."""
from dataclasses import dataclass

from datclass import DatClass


@dataclass
class RestoreFileResponse(DatClass):
    """..."""
    drive_id: str = None
    file_id: str = None
    domain_id: str = None
    async_task_id: str = None
