import abc


class GroupsArgumentMapper(abc.ABC):

    @abc.abstractmethod
    def map(self, group_argument: str) -> str:
        pass
