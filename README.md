# DeepSignal2


## A deep-learning method for detecting DNA methylation state from Oxford Nanopore sequencing reads.
DeepSignal2 BiLSTM+Inception structure to detect DNA methylation state from Nanopore reads. It is
built with **Python3** and **Pytorch**.

## Contents
- [Installation](#Installation)
- [Quick start](#Quick-start)

## Installation
deepsignal2 is built on Python3. [tombo](https://github.com/nanoporetech/tombo) is required to re-squiggle the raw signals from nanopore reads before running deepsignal.
   - Prerequisites:\
       [Python3.*](https://www.python.org/)\
       [PyTorch](https://pytorch.org/) (version not tested)\
       [tombo](https://github.com/nanoporetech/tombo) (version 1.5.1)
   - Dependencies:\
       [numpy](http://www.numpy.org/)\
       [h5py](https://github.com/h5py/h5py)\
       [statsmodels](https://github.com/statsmodels/statsmodels/)\
       [scikit-learn](https://scikit-learn.org/stable/)

#### 1. Create an environment
We highly recommend to use a virtual environment for the installation of deepsignal2 and its dependencies. A virtual environment can be created and (de)activated as follows by using [conda](https://conda.io/docs/):
```bash
# create
conda create -n deepsignal2env python=3.6
# activate
conda activate deepsignal2env
# deactivate
conda deactivate
```
The virtual environment can also be created by using [virtualenv](https://github.com/pypa/virtualenv/).

#### 2. Install deepsignal2
- After creating and activating the environment, download deepsignal2 (**lastest version**) from github:
```bash
git clone https://github.com/PengNi/deepsignal2.git
```

- [tombo](https://github.com/nanoporetech/tombo) is required to be installed in the same environment:
```bash
# install using conda
conda install -c bioconda ont-tombo
# or install using pip
pip install ont-tombo
```

- install [PyTorch](https://pytorch.org/) (version not tested) in the same environment:

```bash
# install using conda
conda install pytorch==1.4.0 torchvision==0.5.0 cudatoolkit=10.1 -c pytorch
# or install using pip
pip install torch==1.4.0 torchvision==0.5.0
```


## Quick start
To call modifications, the raw fast5 files should be basecalled ([Guppy>=3.6.1](https://nanoporetech.com/community)) and then be re-squiggled by [tombo (version 1.5.1)](https://github.com/nanoporetech/tombo). At last, modifications of specified motifs can be called by deepsignal. The following are commands to call 5mC in CG, CHG, and CHH contexts as follows:
```bash
# 1. guppy basecall
guppy_basecaller -i fast5s/ -r -s fast5s_guppy --config dna_r9.4.1_450bps_hac_prom.cfg
cat fast5s_guppy/*.fastq > fast5s_guppy.fastq
# 2. tombo resquiggle
tombo preprocess annotate_raw_with_fastqs --fast5-basedir fast5s/ --fastq-filenames fast5s_guppy.fastq --basecall-group Basecall_1D_000 --basecall-subgroup BaseCalled_template --overwrite --processes 10
tombo resquiggle fast5s/ /path/to/reference/genome.fa --processes 10 --corrected-group RawGenomeCorrected_000 --basecall-group Basecall_1D_000 --overwrite
# 3. deepsignal call_mods
# we call CG, CHG, CHH methylation separately
# CG
CUDA_VISIBLE_DEVICES=0 python /path/to/deepsignal2/deepsignal2/call_modifications.py --input_path fast5s/ --model_path /path/to/CG_model/.ckpt --result_file fast5s.CG.call_mods.tsv --corrected_group RawGenomeCorrected_000 --reference_path /path/to/reference/genome.fa --motifs CG --nproc 30 --nproc_gpu 6
python /path/to/deepsignal2/scripts/call_modification_frequency.py --input_path fast5s.CG.call_mods.tsv --result_file fast5s.CG.call_mods.frequency.tsv --prob_cf 0.8
# CHG
CUDA_VISIBLE_DEVICES=0 python /path/to/deepsignal2/deepsignal2/call_modifications.py --input_path fast5s/ --model_path /path/to/CHG_model/.ckpt --result_file fast5s.CHG.call_mods.tsv --corrected_group RawGenomeCorrected_000 --reference_path /path/to/reference/genome.fa --motifs CHG --nproc 30 --nproc_gpu 6
python /path/to/deepsignal2/scripts/call_modification_frequency.py --input_path fast5s.CHG.call_mods.tsv --result_file fast5s.CHG.call_mods.frequency.tsv --prob_cf 0.8
# CHH
CUDA_VISIBLE_DEVICES=0 python /path/to/deepsignal2/deepsignal2/call_modifications.py --input_path fast5s/ --model_path /path/to/CHH_model/.ckpt --result_file fast5s.CHH.call_mods.tsv --corrected_group RawGenomeCorrected_000 --reference_path /path/to/reference/genome.fa --motifs CHH --nproc 30 --nproc_gpu 6
python /path/to/deepsignal2/scripts/call_modification_frequency.py --input_path fast5s.CHH.call_mods.tsv --result_file fast5s.CHH.call_mods.frequency.tsv --prob_cf 0.8
```
Note:
- If the fast5 files are in multi-read FAST5 format, please use _multi_to_single_fast5_ command from the [ont_fast5_api package](https://github.com/nanoporetech/ont_fast5_api) to convert the fast5 files before using tombo (Ref to [issue #173](https://github.com/nanoporetech/tombo/issues/173) in [tombo](https://github.com/nanoporetech/tombo)).
```bash
multi_to_single_fast5 -i $multi_read_fast5_dir -s $single_read_fast5_dir -t 30 --recursive
```


## Usage


License
=========
Copyright (C) 2020 [Jianxin Wang](mailto:jxwang@mail.csu.edu.cn), [Feng Luo](mailto:luofeng@clemson.edu), [Peng Ni](mailto:nipeng@csu.edu.cn)

This program is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.

This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.

You should have received a copy of the GNU General Public License along with this program. If not, see <https://www.gnu.org/licenses/>.

[Jianxin Wang](mailto:jxwang@mail.csu.edu.cn), [Peng Ni](mailto:nipeng@csu.edu.cn),
School of Computer Science and Engineering, Central South University, Changsha 410083, China

[Feng Luo](mailto:luofeng@clemson.edu), School of Computing, Clemson University, Clemson, SC 29634, USA
