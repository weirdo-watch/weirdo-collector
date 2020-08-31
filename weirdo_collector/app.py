from pathlib import Path
from typing import Any, Dict, List

import yaml

import weirdo_collector.collector  # noqa: F401
from weirdo_collector.logging import get_logger


class App(object):
    """docstring for App"""

    def __init__(self, path: str = "", **kwargs) -> None:
        self.path: Path = Path(path or "weirdos")
        self.logger = get_logger(verbose=kwargs.get("verbose", False))

    @property
    # def users(self) -> List[Weirdo]:
    def users(self):
        return [
            Weirdo(x.parts[1], x)
            for x in self.path.glob("*/config.yaml")
            if x.is_file()
        ]

    def get_em(self) -> None:
        users = self.users

        if len(users) == 0:
            self.logger.warning(
                "Hey! We didn't find any weirdos in {}".format(self.path)
            )
        else:
            self.logger.info("Collecting weirdos!")
            for user in self.users:
                self.logger.info("Collecting user: {}".format(user.name.capitalize()))

                for service in user.services:
                    self.logger.info(
                        "{}: collecting service: {}".format(user.name, service)
                    )
                    user.collect(service)

    def main(self):
        self.get_em()


class Weirdo(object):
    """docstring for Weirdo"""

    def __init__(self, name: str, config_file: Path) -> None:
        self.name: str = name
        self.config_file: Path = config_file
        self.logger = get_logger()

    def collect(self, service: str) -> None:
        collectors: Dict[str, str] = weirdo_collector.collector.get_collectors()

        if service not in collectors:
            self.logger.warning(
                "Collector for {} not implemented, skipping".format(service)
            )
        else:
            service_collector: str = "weirdo_collector.collector." + collectors[service]

            svc = eval(service_collector)(
                self.name, config=self.service_config(service)
            )
            svc.collect()

        return

    def __str__(self) -> str:
        return self.name

    def service_config(self, service: str) -> Dict[str, Any]:
        return self.config["services"][service]

    @property
    def services(self) -> List[str]:
        return self.config["services"].keys()

    @property
    def config(self) -> Dict[str, Any]:
        if not hasattr(self, "_config"):
            with self.config_file.open() as config:
                self._config: Dict[str, Any] = yaml.full_load(config)
        return self._config
