import re
from pathlib import Path
from typing import Any, Dict

from weirdo_collector.logging import get_logger


class Collector(object):
    """Base Collector, all Collectors originate here"""

    def __init__(self, username: str, **kwargs) -> None:
        self._config: Dict[str, Any] = kwargs.pop("config", {})
        self.username: str = self._config["username"] or username
        self.interval: str = kwargs.pop("interval", "1d")

        self.logger = get_logger()

        if len(kwargs) > 0:
            self.logger.debug("Unused kwargs: {}".format(kwargs))

    def collect(self) -> bool:
        """
        Primary method/action for the class, collects data for a given service
        """
        raise NotImplementedError("Method must be defined in derrived class")

    @property
    def output_file(self) -> Path:
        """
        Return a path to the desired output file
        """
        raise NotImplementedError("Method must be defined in derrived class")

    def __getattr__(self, key):
        try:
            return self._config[key]
        except KeyError as e:
            raise AttributeError(e)


class TwitterCollector(Collector):
    """docstring for TwitterCollector"""

    service: str = "twitter"

    def __init__(self, username: str, **kwargs) -> None:
        # self.include_retweets: bool = kwargs.pop("include_retweets", True)
        # self.include_replies: bool = kwargs.pop("include_replies", True)
        super().__init__(username, **kwargs)

    @property
    def output_file(self) -> Path:
        if "output_file" in self._config:
            return Path(
                str(self._config.get("output_file"))
            )  # set sting here to satisfy mypy
        return Path("weirdos", self.username, "data", self.service + ".sqlite")

    def collect(self) -> bool:
        if not self.output_file.is_file():
            self.logger.warning(
                "output_file: {} does not exist,".format(self.output_file)
                + " ignoring interval: {} for baseline run".format(self.interval),
            )

        import twint

        # Venting for a second... I looked at the twint code and <gasp>
        twint_config = twint.Config()
        twint_config.All = self.username
        twint_config.Since = "2020-8-25 00:00:00"
        twint_config.Database = self.output_file
        twint_config.Debug = False

        twint.run.Search(twint_config)

        self.logger.debug(
            "collect: {} {} {}".format(self.service, self.output_file, self.interval)
        )

        return True


def get_collectors() -> Dict[str, str]:
    """
    Returns a dict of service slug -> CollectorClass

    A little introspection is good for the soul
    """
    services: Dict[str, str] = {}
    for collector in filter(re.compile(r"^\w+Collector$").search, globals().keys()):
        services[eval(collector).service] = collector
    return services
