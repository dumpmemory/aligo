"""FaceThumbnail"""
from dataclasses import dataclass

from datclass import DatClass


@dataclass
class FaceThumbnail(DatClass):
    """FaceThumbnail"""
    face_id: str = None
    face_group_id: str = None
    face_thumbnail: str = None
