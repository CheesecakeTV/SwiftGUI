from abc import abstractmethod

all_themes: dict[str: type] = dict()

class _BaseTheme_meta(type):

    def __new__(mcs, name, bases, namespace):
        returning: type | "BaseTheme" = super().__new__(mcs, name, bases, namespace)

        if not name.startswith("Base"):
            all_themes[returning.suffix + name] = returning

        return returning

class BaseTheme(metaclass= _BaseTheme_meta):
    """
    Inherit this to create your own theme
    """
    suffix: str = ""    # Will be added before the name in all_themes

    def __init__(self):
        self.apply()

    def __call__(self, *args, **kwargs):
        self.apply()

    @abstractmethod
    def apply(self) -> None:
        """
        Configurations belong in here
        :return:
        """
        raise NotImplementedError("You tried to apply BaseTheme. BaseTheme should not be applied, it is only to create more themes from.")
