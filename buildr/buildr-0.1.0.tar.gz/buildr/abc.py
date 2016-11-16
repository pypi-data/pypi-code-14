import abc
import typing


class AbstractStage(abc.ABC):
    """Stage definition"""

    @abc.abstractproperty
    def image(self) -> typing.Optional[str]:
        """Image to use for the stage, if any"""

    @abc.abstractproperty
    def pre(self) -> typing.List[str]:
        """Pre-run work - errors that happen
        during this group count as an error"""

    @abc.abstractproperty
    def run(self) -> typing.List[str]:
        """Main build run, errors that happen
        during this group count as a failure"""

    @abc.abstractproperty
    def post(self) -> typing.List[str]:
        """Post-run work, error that happen
        during this group count as an error"""

    @abc.abstractproperty
    def skip(self) -> bool:
        """Defines if the stage should be skipped
        for some reason."""


class AbstractManifest(abc.ABC):
    """Manifest definition"""

    @abc.abstractproperty
    def stages(self) -> typing.Optional[AbstractStage]:
        """List of stages to run, in order."""

    @abc.abstractproperty
    def image(self) -> str:
        """Image to use for the full run, if any."""

    @abc.abstractproperty
    def env(self) -> typing.Optional[str]:
        """Environment for the image."""
