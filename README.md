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
        $ conda env create --name think-stats --file=environment.yml
        $ conda activate think-stats

1. Test Repo:

        $ cd tests/preface
        $ python nsfg.py
        (13593, 244)
        All tests passed.
