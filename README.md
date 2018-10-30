# ulogAnalysis
Simple scripts to analyse ulog data using pandas python package

## Installation
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

### installation setup

The build-system in use is [flit](https://flit.readthedocs.io/en/latest/)
```bash
pip install flit
```

Now we can build the projct:
```
flit install -s
```
The `-s` stands for symlink which gives the option to test changes without reinstalling the package.


The projcet uses [black](https://github.com/ambv/black) for code-formatting and [flake8](https://pypi.org/project/flake8/) for style-guide enforcement. [pre-commit-framework](https://github.com/pre-commit/pre-commit) is used to ensure that each commit first gets adjusted through `blake` and then checked by `flake8`. First, we need to add `pre-commit` to our
system:
```bash
pre-commit install
```

To test if everything is setup correctly, you can run the `px4_attitude`-script, which creates a pdf with a few plots in it. Make sure that the path to the ulg-file exists. 
```bash
px4_attitude logs/cd6d8090-8c7f-41e5-bf62-3c95cc09fba1.ulg
```




