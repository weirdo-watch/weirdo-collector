# Weirdo-collector
Have a favorite internet weirdo? Keeping tabs on them through a series of disparate, quirky tools is difficult. Weirdo-collector aims to simplify collection and storage of social media posts and other internet miscellany.

Currently supported collectors:
* Twitter

**Weirdo-tracker is currently pre-release software.** Use beyond simple trial is not recommended. APIs, as well as command structure, will likely change.

## Installation
 You’ll need Python 3.8 to use weirdo-watcher. It’s developed against 3.8 and hasn’t been tested against earlier, but will probably work with 3.6+. Matrix testing will come at some point.

### Install from git with pip
```
pip install git+https://github.com/weirdo-watch/weirdo-collector.git
```

## Usage

### Configuration
Configuration is stored using YAML. There are two levels of configuration— appplication and user (weirdo). By default, weirdo-collector looks for application-specific configuration in `./weirdo-collector.yaml`. User configuration is stored at `<base directory>/<user>/config.yaml`.

### Storage
Weirdo-collector stores output in a standardized directory structure by default.

```
weirdos
└── <weirdo>
    ├── README.md
    ├── config.yaml
    ├── data
    │   └── <service>.<storage method>
    └── doc
```
