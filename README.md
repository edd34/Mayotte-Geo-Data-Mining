# Mayotte Geo Data Mining

This project implement Open Street Map package, binding and API in order to find point of interest near a geographical point in Mayotte.

## Configure the virtual environment

### Create a new environment virtualenv

Create a virutal environment using [virtualenv](https://docs.python.org/fr/3/library/venv.html).

```bash
python3 -m venv venv
```

### Entering the environment

```bash
source venv/bin/activate
```

## Installation of package listed in requirement.txt

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install the dependencies.

```bash
pip3 install -r requirements.txt
```
## Steps when running the program for the first time.

In order to run the backend program, you should follow the steps described below. All commands are run from the root folder.

### refreshing the map

```bash
python download_geojson.py
```


### running the server app

```bash
python server
```

## Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.

## License

[MIT](https://choosealicense.com/licenses/mit/)
