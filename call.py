from multiprocessing import Pool


def run(idx):
  import torch

  import fusion_cuda
  import sys
  import math
  from torch import nn
  from torch.autograd import Function
  from torch.nn.parameter import Parameter
  from torch.nn import functional as f
  from torch.nn.modules.utils import _pair
  torch.backends.cudnn.enabled = False

  torch.manual_seed(42)

  device = torch.device("cuda")
  dtype = torch.float32

  kwargs = {'dtype': dtype,
            'device': device,
            'requires_grad': True}


  def check(kernels):
    half = len(kernels) // 2
    for i in range(half):
      print(torch.all(torch.eq(kernels[i], kernels[i+half])))
  for _ in range(1):
    if idx == 1:
      print(fusion_cuda.histc(torch.randn(0), 1)[0][0])
    if idx == 2:
      print(fusion_cuda.histc_maxpool()[0][0])
    if idx == 3:
      print(fusion_cuda.hist_norm()[0][0])
    if idx == 4:
      print(fusion_cuda.histc_upsample()[0][0])
    if idx == 5:
      print(fusion_cuda.im2col_batchnorm()[0][0])
    if idx == 6:
      print(fusion_cuda.im2col_maxpool()[0][0])
    if idx == 7:
      check(fusion_cuda.max_pool_batch_norm())
    if idx == 8:
      print(fusion_cuda.im2col_upsample()[0][0])
    if idx == 9:
      print(fusion_cuda.call_max_pool_upsample_fused()[0][0])
    if idx == 0:
      check(fusion_cuda.upsample_batchnorm())
    torch.cuda.empty_cache()
    torch.cuda.synchronize(device=None)

if len(sys.argv) == 2:
    run(int(sys.argv[1]))
else:
    with Pool(1) as p:
      p.map(run, range(10))



