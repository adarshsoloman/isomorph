from abc import ABC, abstractmethod
from typing import List, Dict, Any

class BasePrimitive(ABC):
    @property
    @abstractmethod
    def name(self) -> str:
        """Display name of the primitive."""
        pass

    @property
    @abstractmethod
    def description(self) -> str:
        """One line description of what it does."""
        pass

    @property
    @abstractmethod
    def input_schema(self) -> Dict[str, Any]:
        """JSON-compatible dict of input requirements."""
        pass

    @property
    @abstractmethod
    def output_schema(self) -> Dict[str, Any]:
        """JSON-compatible dict of output format."""
        pass

    @property
    @abstractmethod
    def assumptions(self) -> List[str]:
        """What must be true for this to work correctly."""
        pass

    @property
    @abstractmethod
    def example_input(self) -> Dict[str, Any]:
        """A concrete working example input."""
        pass

    @property
    @abstractmethod
    def expected_output(self) -> Dict[str, Any]:
        """What the example input should produce."""
        pass

    @abstractmethod
    def run(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """Execute the primitive on the provided data."""
        pass
