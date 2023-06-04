from .base import InstructionBase


class DeductiveChain(InstructionBase):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._chain = []
    def execute(self, *args, **kwargs):
        raise NotImplementedError("DeductiveChain.execute() is not implemented.")