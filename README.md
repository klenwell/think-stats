# Think Stats
This repository is effectively my workbook for the online Think Stats textbook available here:

- https://greenteapress.com/wp/think-stats-2e/

The course comes with its own Github repository:

- https://github.com/AllenDowney/ThinkStats2


## Installation
### Anaconda
This guide follows instructions provided by [this Digital Ocean article](https://www.digitalocean.com/community/tutorials/how-to-install-anaconda-on-ubuntu-18-04-quickstart).

1. Download latest version from https://repo.anaconda.com/archive:

        $ cd /tmp
        $ curl -O https://repo.anaconda.com/archive/Anaconda3-2020.07-Linux-x86_64.sh
        $ md5sum Anaconda3-2020.07-Linux-x86_64.sh
        1046c40a314ab2531e4c099741530ada  Anaconda3-2020.07-Linux-x86_64.sh

1. Compare with MD5 value (`1046c40a314ab2531e4c099741530ada`) listed here:

    - https://repo.anaconda.com/archive/

1. Run install script:

       $ bash Anaconda3-2020.07-Linux-x86_64.sh
       # Review and agree to license
       # Use default install path (e.g. /home/klenwell/anaconda3)
       # Run conda init
       ...
       modified      /home/klenwell/.bashrc

### Create New Conda Environment
1. Clone repository:

        $ git clone git@github.com:klenwell/think-stats.git

1. Create conda environment:

        $ cd think-stats
        $ conda env create --name think-stats --file=think-stats.yml
        $ conda activate think-stats

1. Check conda installation:

        $ conda info

            active environment : think-stats
           active env location : /home/klenwell/anaconda3/envs/think-stats
                   shell level : 2
              user config file : /home/klenwell/.condarc
        populated config files :
                 conda version : 4.8.3

### Test Application
I prefer the command line to iPython. So this project is set up to use the [Cement framework](https://github.com/datafolklabs/cement) for command line interactions. To test Think Stats is ready for you, run the following commands:

    $ cd tests/preface/
    $ python nsfg.py
    (13593, 244)
    All tests passed.

To drop into the Python debugger (from project root directory):

    $ python app.py interactive

To use the iPython local web application, first run (from project root):

    $ ipython notebook

Then open the URL listed in your browser if not automatically redirected to your browser.


## Development
The app comes packaged with [flake8](http://flake8.pycqa.org/en/latest/) for style guide enforcement. Before commiting any code, please run `flake8` and correct any reported issues:

```
# Bad: needs to be fixed
$ cd think-stats
$ flake8
./tests/preface/nsfg.py:10:1: F401 'sys' imported but unused

# Good: no output
$ flake8
```

Please feel free to submit pull requests and file bugs on the issue tracker. This is a hobby project of mine so I cannot guarantee a prompt response.
