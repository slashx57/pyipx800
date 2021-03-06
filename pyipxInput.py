# -*- coding: utf-8 -*-

import collections
import time
from threading import Lock

from pyipx800 import pyipxBase

class Input(pyipxBase.pyipxBase):
  """Representing an IPX800 Digital Input."""
  _mutex = Lock()
  _updatets = time.time()

  def __init__(self, ipx, id: int):
    super().__init__(ipx, id)

  def update(self):
    with Input._mutex:
      if (self._content==None or (time.time() - Input._updatets >= pyipxBase.pyipxBase.scan_interval)):
        self._content = self._ipx.request({"Get": "D"})
        Input._updatets = time.time()
    return self._content

  @staticmethod
  def len(ipx):
    return len(ipx.request({"Get": "D"}))

  @property
  def state(self) -> bool:
    """Return the current Input status."""
    self.update()
    return self._content[f"D{self.id}"] == 1
