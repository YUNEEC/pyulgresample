# pyulgresample
Package that processes ulog-data from [pyulog](https://github.com/PX4/pyulog). It converts ulog-data into pandas dataframe through resampling and provides convenient functions to add and extract additional information from the ulog-data.
To convert a `.ulg` file into `ulog`, please follow the [pyulog](https://github.com/PX4/pyulog) instruction.

## modules
### ulogdataframe
`ulogdataframe` contains the following classes:

- TopicMsgs
- DfUlg

#### TopicMsgs
This class is a convenient class to specify a specific topic with corresponding messages of interest.

#### DfUlg
This class contains a ulog-structure, pandas dataframe-structure and list of topics as class-members. It also contains a factory-method for converting a .ulg-file into class-members.

#### ulogconv
This module contains a few helper-functions for converting a .ulg-file into pandas-dataframe. It is mainly used by DfUlg.

#### mathpandas
Contains time-series functions.

#### loginfo
Functions that provide info about the ulg-file.


`dataframe` is a pandas dataframe with index equal to the merged timestamps. Each column represents a message-field.
For instance, the `thrust`-field of the message [vehicle_local_position_setpoint](https://github.com/PX4/Firmware/blob/master/msg/vehicle_local_position_setpoint.msg) message would be named as follow:

> T_vehicle_local_position_setpoint_0__F_thrust_x

if the field `x` of `vehicle_local_position_setpoint` is a scalar or

> T_vehicle_local_position_setpoint_0__F_x_0

if the field `x` is an array, where the 0 represents the index of the array.

The `T` stands for topic, which indicates the beginning of the topic. In this example, the topcic name is
`vehicle_local_position_setpoint`. The topic name is followed by a number, which indicates the topic instance. If there is only one instance of a specific topic, then this number will be `0`. The instance number is followed by two underlines and a capital letter `F`, which stands for field. In the example above, the field in question is `x`.

## installation
To prevent any conflict with the system python version, it is suggested to use a virtual enrionment with python version 3.6 and higher. Otherwise, python 3.6 and higher must be the python system version.
If you don't have 3.6 installed on your machinge, you can follow this [tutorial](http://ubuntuhandbook.org/index.php/2017/07/install-python-3-6-1-in-ubuntu-16-04-lts/).


### virtualenvwrapper

First install virtualenv:
```bash
sudo apt install virtualenv
```

Install virtualenvrapper: this will install `virtualenvwrapper.sh` in `~/.local/bin`
```bash
pip install virtualenvwrapper
```

Create a virtual environement directory
```bash
mkdir ~/.virtualenvs
```

Add virtual envrionment working-folder to bashrc and source virtualenvwrapper:
```bash
export WORKON_HOME=$HOME/.virtualenvs
source $HOME/.local/bin/virtualenvwrapper.sh
```

Open new terminal or source bashrc:
```bash
source ~/.bashrc
```

Create a virtual environment with python version 3 and no site packages included (python3 must be installed)
```bash
mkvirtualenv --python=python3 --no-site-packages [name-of-new-env]
```

You now created a new virtual environment with name [name-of-new-env].

To enter [name-of-new-env]:
```bash
workon [name-of-new-env]
```

To exit [name-of-new-env]:
```bash
deactivate
```

### build setup

The build-system in use is [flit](https://flit.readthedocs.io/en/latest/)
```bash
pip install flit
```

Now we can build the projct:
```
flit install -s
```
The `-s` stands for symlink which gives the option to test changes without reinstalling the package.


The projcet uses [black](https://github.com/ambv/black) for code-formatting and [flake8](https://pypi.org/project/flake8/) for style-guide enforcement. [pre-commit-framework](https://github.com/pre-commit/pre-commit) is used to ensure that each commit first gets adjusted through `blake` and then checked by `flake8`. [PEP257](https://github.com/FalconSocial/pre-commit-mirrors-pep257) docstring style checker is used as well. First, we need to add `pre-commit` to our
system:
```bash
pre-commit install
```

To test if everything is setup correctly, you can run the `px4_attitude`-script, which creates a pdf with a few plots in it. Make sure that the path to the ulg-file exists.
```bash
px4_attitude logs/cd6d8090-8c7f-41e5-bf62-3c95cc09fba1.ulg
```




