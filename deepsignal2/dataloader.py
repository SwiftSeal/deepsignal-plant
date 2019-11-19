from torch.utils.data import Dataset
import linecache
import os
import numpy as np

base2code_dna = {'A': 0, 'C': 1, 'G': 2, 'T': 3, 'N': 4}
code2base_dna = {0: 'A', 1: 'C', 2: 'G', 3: 'T', 4: 'N'}


def parse_a_line(line):
    words = line.strip().split("\t")

    sampleinfo = "\t".join(words[0:6])

    kmer = np.array([base2code_dna[x] for x in words[6]])
    base_means = np.array([float(x) for x in words[7].split(",")])
    base_stds = np.array([float(x) for x in words[8].split(",")])
    base_signal_lens = np.array([int(x) for x in words[9].split(",")])
    cent_signals = np.array([float(x) for x in words[10].split(",")])
    label = int(words[11])

    return sampleinfo, kmer, base_means, base_stds, base_signal_lens, cent_signals, label


class SignalFeaData(Dataset):
    def __init__(self, filename, transform=None):
        self._filename = os.path.abspath(filename)
        self._total_data = 0
        self._transform = transform
        with open(filename, "r") as f:
            self._total_data = len(f.readlines())

    def __getitem__(self, idx):
        line = linecache.getline(self._filename, idx + 1)
        if line == "":
            return None
        else:
            output = parse_a_line(line)
            if self._transform is not None:
                output = self._transform(output)
            return output

    def __len__(self):
        return self._total_data