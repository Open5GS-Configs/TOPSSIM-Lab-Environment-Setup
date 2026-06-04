from abc import ABC, abstractmethod

class InfrastructureManager(ABC):

    @abstractmethod
    def callInfManager(self, config):
        pass


    @abstractmethod
    def destroy(self):
        pass