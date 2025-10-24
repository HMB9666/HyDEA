# HyDEA: Hybrid Deep lEarning line-search directions and iterative methods for Accelerated solutions

The source code and dataset for the paper: Bai H, Bian X. Hybrid deep learning and iterative methods for accelerated solutions of viscous incompressible flow. arXiv preprint arXiv:2506.03016, 2025.

<p align="center">
  <img width="1000" src="assets/HyDEA_workflow.png">
</p>

## Code

The code depends on PetIBM(https://github.com/barbagroup/PetIBM/tree/master?tab=readme-ov-file), python, pytorch, petsc4py.

PetIBM should be installed by following the procedure outlined in B.1 of official installation guide. Before compilation, ensure that the directories specified in both the CMakeLists.txt and the source files are correctly modified. 

#### Contents

1. [Requirements](#Requirements)
1. [Citation](#Citation)

## Requirements
> - Platforms: Ubuntu 20.04
> - Mamba
> - Python = 3.8
> - PetIBM
> - PyTorch = 2.1.0
> - Pybind 11
> - petsc4py 3.16.6
> - nlohmann

## Citation
@article{Bai_HyDEA,
  title={Hybrid deep learning and iterative methods for accelerated solutions of viscous incompressible flow},
  author={Heming Bai, and Xin Bian},
  journal={arXiv preprint arXiv:2506.03016},
  year={2025}
}

