import numpy as np
import copy


def affine_forward(x, w, b):
  """
  Computes the forward pass for an affine (fully-connected) layer.

  The input x has shape (N, d_1, ..., d_k) and contains a minibatch of N
  examples, where each example x[i] has shape (d_1, ..., d_k). We will
  reshape each input into a vector of dimension D = d_1 * ... * d_k, and
  then transform it to an output vector of dimension M.

  Inputs:
  - x: A numpy array containing input data, of shape (N, d_1, ..., d_k)
  - w: A numpy array of weights, of shape (D, M)
  - b: A numpy array of biases, of shape (M,)
  
  Returns a tuple of:
  - out: output, of shape (N, M)
  - cache: (x, w, b)
  """
  out = None
  #############################################################################
  # TODO: Implement the affine forward pass. Store the result in out. You     #
  # will need to reshape the input into rows.                                 #
  #############################################################################
  N = x.shape[0]
  D = np.prod(x.shape[1:])
  out = np.dot(x.reshape(N,D), w)+b
  #############################################################################
  #                             END OF YOUR CODE                              #
  #############################################################################
  cache = (x, w, b)
  return out, cache


def affine_backward(dout, cache):
  """
  Computes the backward pass for an affine layer.

  Inputs:
  - dout: Upstream derivative, of shape (N, M)
  - cache: Tuple of:
    - x: Input data, of shape (N, d_1, ... d_k)
    - w: Weights, of shape (D, M)

  Returns a tuple of:
  - dx: Gradient with respect to x, of shape (N, d1, ..., d_k)
  - dw: Gradient with respect to w, of shape (D, M)
  - db: Gradient with respect to b, of shape (M,)
  """
  x, w, b = cache
  dx, dw, db = None, None, None
  #############################################################################
  # TODO: Implement the affine backward pass.                                 #
  #############################################################################
  db = np.sum(dout, axis=0)
  N = x.shape[0]
  D = np.prod(x.shape[1:])
  dw = np.dot(x.reshape(N,D).T, dout)
  dx = np.dot(dout, w.T).reshape(x.shape)
  #############################################################################
  #                             END OF YOUR CODE                              #
  #############################################################################
  return dx, dw, db


def relu_forward(x):
  """
  Computes the forward pass for a layer of rectified linear units (ReLUs).

  Input:
  - x: Inputs, of any shape

  Returns a tuple of:
  - out: Output, of the same shape as x
  - cache: x
  """
  out = None
  #############################################################################
  # TODO: Implement the ReLU forward pass.                                    #
  #############################################################################
  out = np.maximum(x,0)
  #############################################################################
  #                             END OF YOUR CODE                              #
  #############################################################################
  cache = x
  return out, cache


def relu_backward(dout, cache):
  """
  Computes the backward pass for a layer of rectified linear units (ReLUs).

  Input:
  - dout: Upstream derivatives, of any shape
  - cache: Input x, of same shape as dout

  Returns:
  - dx: Gradient with respect to x
  """
  dx, x = None, cache
  #############################################################################
  # TODO: Implement the ReLU backward pass.                                   #
  #############################################################################
  dx = copy.deepcopy(dout)
  dx[x<0] = 0
  #############################################################################
  #                             END OF YOUR CODE                              #
  #############################################################################
  return dx


def batchnorm_forward(x, gamma, beta, bn_param):
  """
  Forward pass for batch normalization.
  
  During training the sample mean and (uncorrected) sample variance are
  computed from minibatch statistics and used to normalize the incoming data.
  During training we also keep an exponentially decaying running mean of the mean
  and variance of each feature, and these averages are used to normalize data
  at test-time.

  At each timestep we update the running averages for mean and variance using
  an exponential decay based on the momentum parameter:

  running_mean = momentum * running_mean + (1 - momentum) * sample_mean
  running_var = momentum * running_var + (1 - momentum) * sample_var

  Note that the batch normalization paper suggests a different test-time
  behavior: they compute sample mean and variance for each feature using a
  large number of training images rather than using a running average. For
  this implementation we have chosen to use running averages instead since
  they do not require an additional estimation step; the torch7 implementation
  of batch normalization also uses running averages.

  Input:
  - x: Data of shape (N, D)
  - gamma: Scale parameter of shape (D,)
  - beta: Shift paremeter of shape (D,)
  - bn_param: Dictionary with the following keys:
    - mode: 'train' or 'test'; required
    - eps: Constant for numeric stability
    - momentum: Constant for running mean / variance.
    - running_mean: Array of shape (D,) giving running mean of features
    - running_var Array of shape (D,) giving running variance of features

  Returns a tuple of:
  - out: of shape (N, D)
  - cache: A tuple of values needed in the backward pass
  """
  mode = bn_param['mode']
  eps = bn_param.get('eps', 1e-5)
  momentum = bn_param.get('momentum', 0.9)

  N, D = x.shape
  running_mean = bn_param.get('running_mean', np.zeros(D, dtype=x.dtype))
  running_var = bn_param.get('running_var', np.zeros(D, dtype=x.dtype))

  out, cache = None, None
  if mode == 'train':
    #############################################################################
    # TODO: Implement the training-time forward pass for batch normalization.   #
    # Use minibatch statistics to compute the mean and variance, use these      #
    # statistics to normalize the incoming data, and scale and shift the        #
    # normalized data using gamma and beta.                                     #
    #                                                                           #
    # You should store the output in the variable out. Any intermediates that   #
    # you need for the backward pass should be stored in the cache variable.    #
    #                                                                           #
    # You should also use your computed sample mean and variance together with  #
    # the momentum variable to update the running mean and running variance,    #
    # storing your result in the running_mean and running_var variables.        #
    #############################################################################
    x_mean = np.mean(x, axis=0)
    x__mean = x-x_mean
    x__mean2 = x__mean**2
    x_var = np.mean(x__mean2, axis=0)
    x_var_sqrt = np.sqrt(x_var+eps)
    inv_x_var_sqrt = 1.0 / x_var_sqrt
    x_hat = x__mean * inv_x_var_sqrt
    out_ = gamma*x_hat
    out = out_ + beta
    cache = (x, x__mean, inv_x_var_sqrt, x_hat, gamma)
  
    running_mean = momentum*running_mean + (1-momentum)*x_mean
    running_var = momentum*running_var + (1-momentum)*x_var
    #############################################################################
    #                             END OF YOUR CODE                              #
    #############################################################################
  elif mode == 'test':
    #############################################################################
    # TODO: Implement the test-time forward pass for batch normalization. Use   #
    # the running mean and variance to normalize the incoming data, then scale  #
    # and shift the normalized data using gamma and beta. Store the result in   #
    # the out variable.                                                         #
    #############################################################################
    out = gamma*((x-running_mean) / np.sqrt(running_var+eps)) + beta
    #############################################################################
    #                             END OF YOUR CODE                              #
    #############################################################################
  else:
    raise ValueError('Invalid forward batchnorm mode "%s"' % mode)

  # Store the updated running means back into bn_param
  bn_param['running_mean'] = running_mean
  bn_param['running_var'] = running_var

  return out, cache


'''def batchnorm_backward(dout, cache):
  """
  Backward pass for batch normalization.
  
  For this implementation, you should write out a computation graph for
  batch normalization on paper and propagate gradients backward through
  intermediate nodes.
  
  Inputs:
  - dout: Upstream derivatives, of shape (N, D)
  - cache: Variable of intermediates from batchnorm_forward.
  
  Returns a tuple of:
  - dx: Gradient with respect to inputs x, of shape (N, D)
  - dgamma: Gradient with respect to scale parameter gamma, of shape (D,)
  - dbeta: Gradient with respect to shift parameter beta, of shape (D,)
  """
  dx, dgamma, dbeta = None, None, None
  #############################################################################
  # TODO: Implement the backward pass for batch normalization. Store the      #
  # results in the dx, dgamma, and dbeta variables.                           #
  #############################################################################
  x_mean, x__mean, x__mean2, x_var, x_var_sqrt, inv_x_var_sqrt, x_hat, out_, gamma, beta, bn_param = cache
  N = dout.shape[0]
  dbeta = np.sum(dout, axis=0)
  dgamma = np.sum(x_hat*dout, axis= 0)
  dgammax = dout
  dout_ = gamma*dgammax
  dinv_x_var_sqrt = np.sum(x__mean * dout_, axis=0)
  dx_var_sqrt = -1.0/(x_var_sqrt**2) * dinv_x_var_sqrt
  dx_var = 0.5/x_var_sqrt * dx_var
  #dx__mean2 = 1.0/N * np.ones((x__mean2.shape)) * dx_var
  dx__mean2 = np.ones((x__mean2.shape)) * dx_var / float(N)
  dx__mean = inv_x_var_sqrt*dout_ + 2 * x__mean * dx__mean2
  dx = dx__mean
  dx_mean = - np.sum(dx_mean, axis=0)
  #dx += 1 / float(N) * np.ones((dx_mean.shape)) * dx_mean
  dx +=  ((np.ones((dx_mean.shape)) * dx_mean)/float(N))
  #############################################################################
  #                             END OF YOUR CODE                              #
  #############################################################################

  return dx, dgamma, dbeta'''


def batchnorm_backward_alt(dout, cache):
  """
  Alternative backward pass for batch normalization.
  
  For this implementation you should work out the derivatives for the batch
  normalizaton backward pass on paper and simplify as much as possible. You
  should be able to derive a simple expression for the backward pass.
  
  Note: This implementation should expect to receive the same cache variable
  as batchnorm_backward, but might not use all of the values in the cache.
  
  Inputs / outputs: Same as batchnorm_backward
  """
  dx, dgamma, dbeta = None, None, None
  #############################################################################
  # TODO: Implement the backward pass for batch normalization. Store the      #
  # results in the dx, dgamma, and dbeta variables.                           #
  #                                                                           #
  # After computing the gradient with respect to the centered inputs, you     #
  # should be able to compute gradients with respect to the inputs in a       #
  # single statement; our implementation fits on a single 80-character line.  #
  #############################################################################
  x, x__mean, inv_x_var_sqrt, x_hat, gamma = cache
  dbeta = np.sum(dout, axis=0)
  dgamma = np.sum(x_hat*dout, axis= 0)
  N=x.shape[0]
  dx = (1. / N) * gamma * inv_x_var_sqrt * (N * dout - np.sum(dout, axis=0) - x__mean * inv_x_var_sqrt**2 * np.sum(dout * (x__mean), axis=0))
  #dx = (1. / N) * gamma * (x_var + eps)**(-0.5) * (N * dout - np.sum(dout, axis=0) - (x - x_mean) * (x_var + eps)**(-1.0) * np.sum(dout * (x - x_mean), axis=0))
  #############################################################################
  #                             END OF YOUR CODE                              #
  #############################################################################
  
  return dx, dgamma, dbeta


def dropout_forward(x, dropout_param):
  """
  Performs the forward pass for (inverted) dropout.

  Inputs:
  - x: Input data, of any shape
  - dropout_param: A dictionary with the following keys:
    - p: Dropout parameter. We drop each neuron output with probability p.
    - mode: 'test' or 'train'. If the mode is train, then perform dropout;
      if the mode is test, then just return the input.
    - seed: Seed for the random number generator. Passing seed makes this
      function deterministic, which is needed for gradient checking but not in
      real networks.

  Outputs:
  - out: Array of the same shape as x.
  - cache: A tuple (dropout_param, mask). In training mode, mask is the dropout
    mask that was used to multiply the input; in test mode, mask is None.
  """
  p, mode = dropout_param['p'], dropout_param['mode']
  if 'seed' in dropout_param:
    np.random.seed(dropout_param['seed'])

  mask = None
  out = None

  if mode == 'train':
    ###########################################################################
    # TODO: Implement the training phase forward pass for inverted dropout.   #
    # Store the dropout mask in the mask variable.                            #
    ###########################################################################
    mask = np.random.rand(*x.shape) < p
    out = x*mask
    ###########################################################################
    #                            END OF YOUR CODE                             #
    ###########################################################################
  elif mode == 'test':
    ###########################################################################
    # TODO: Implement the test phase forward pass for inverted dropout.       #
    ###########################################################################
    out = x
    ###########################################################################
    #                            END OF YOUR CODE                             #
    ###########################################################################

  cache = (dropout_param, mask)
  out = out.astype(x.dtype, copy=False)

  return out, cache


def dropout_backward(dout, cache):
  """
  Perform the backward pass for (inverted) dropout.

  Inputs:
  - dout: Upstream derivatives, of any shape
  - cache: (dropout_param, mask) from dropout_forward.
  """
  dropout_param, mask = cache
  mode = dropout_param['mode']
  
  dx = None
  if mode == 'train':
    ###########################################################################
    # TODO: Implement the training phase backward pass for inverted dropout.  #
    ###########################################################################
    dx = dout*mask*dropout_param['p']
    ###########################################################################
    #                            END OF YOUR CODE                             #
    ###########################################################################
  elif mode == 'test':
    dx = dout
  return dx


def conv_forward_naive(x, w, b, conv_param):
  """
  A naive implementation of the forward pass for a convolutional layer.

  The input consists of N data points, each with C channels, height H and width
  W. We convolve each input with F different filters, where each filter spans
  all C channels and has height HH and width HH.

  Input:
  - x: Input data of shape (N, C, H, W)
  - w: Filter weights of shape (F, C, HH, WW)
  - b: Biases, of shape (F,)
  - conv_param: A dictionary with the following keys:
    - 'stride': The number of pixels between adjacent receptive fields in the
      horizontal and vertical directions.
    - 'pad': The number of pixels that will be used to zero-pad the input.

  Returns a tuple of:
  - out: Output data, of shape (N, F, H', W') where H' and W' are given by
    H' = 1 + (H + 2 * pad - HH) / stride
    W' = 1 + (W + 2 * pad - WW) / stride
  - cache: (x, w, b, conv_param)
  """
  out = None
  #############################################################################
  # TODO: Implement the convolutional forward pass.                           #
  # Hint: you can use the function np.pad for padding.                        #
  #############################################################################
  N, C, H, W = x.shape
  F = w.shape[0]
  HH, WW = w.shape[:2]
  stride = conv_param['stride']
  pad = conv_param['pad']
  H_ = (H+2*pad-HH)/stride + 1
  W_ = (W+2*pad-WW)/stride + 1
  x_padded = np.lib.pad(x, ((0,) (0,), (pad,), (pad,)), 'constant')
  out = np.zeros((N,F,H_,W_))
  for n in range(N):
    for f in range(F):
      for h_ in range(H_):
        for w_ in range(W_):
          out[n,f,h_,w_] = np.sum(x_padded[n,:,h_*stride:h_*stride+HH,w_*stride:w_stride+WW] * w[f,]) + b[f]
  #############################################################################
  #                             END OF YOUR CODE                              #
  #############################################################################
  cache = (x, w, b, conv_param)
  return out, cache


def conv_backward_naive(dout, cache):
  """
  A naive implementation of the backward pass for a convolutional layer.

  Inputs:
  - dout: Upstream derivatives.
  - cache: A tuple of (x, w, b, conv_param) as in conv_forward_naive

  Returns a tuple of:
  - dx: Gradient with respect to x
  - dw: Gradient with respect to w
  - db: Gradient with respect to b
  """
  dx, dw, db = None, None, None
  #############################################################################
  # TODO: Implement the convolutional backward pass.                          #
  #############################################################################
  x, w, b, conv_param = cache
  N, C, H, W = x.shape
  F = w.shape[0]
  HH, WW = w.shape[:2]
  stride = conv_param['stride']
  pad = conv_param['pad']
  H_, W_ = dout.shape[2:]
  x_padded = np.lib.pad(x, ((0,) (0,), (pad,), (pad,)), 'constant')
  dx = np.zeros(x.shape)
  for n in range(N):
    for h in range(H):
      for w_i in range(W):
        for f in range(F):
          for h_ in range(H_):
            for w_ in range(W_):
              mask_1 = np.zeros_like(w[f, :, :, :])
              mask_2 = np.zeros_like(w[f, :, :, :])
              if (h + pad - hh * S) < HH and (h + pad - hh * S) >= 0:
                mask_1[:, h + pad - hh * S, :] = 1.0
              if (w_ + pad - hw * S) < WW and (w_ + pad - hw * S) >= 0:
                mask_2[:, :, w_ + pad - hw * S] = 1.0
              dx[n,:,h,w_i] += dout[n,f,h_,w_]*np.sum( w[f,:,:,:] * mask_1 * mask_2, axis=(1, 2))

  dw = np.zeros(w.shape)
  for f in range(F):
    for c in range(C):
      for hh in range(HH):
        for ww in range(WW):
            dw[f,c,hh,ww]=np.sum(dout[:,f,:,:]*x_padded[:,c,hh:hh+Hh*stride:stride, ww:ww+Hw*stride:stride])

  db = np.zeros(b.shape)
  for f in range(F):
      db[f] = np.sum(dout[:,f,:,:])
  #############################################################################
  #                             END OF YOUR CODE                              #
  #############################################################################
  return dx, dw, db


def max_pool_forward_naive(x, pool_param):
  """
  A naive implementation of the forward pass for a max pooling layer.

  Inputs:
  - x: Input data, of shape (N, C, H, W)
  - pool_param: dictionary with the following keys:
    - 'pool_height': The height of each pooling region
    - 'pool_width': The width of each pooling region
    - 'stride': The distance between adjacent pooling regions

  Returns a tuple of:
  - out: Output data
  - cache: (x, pool_param)
  """
  out = None
  #############################################################################
  # TODO: Implement the max pooling forward pass                              #
  #############################################################################
  N, C, H, W = x.shape
  ph = pool_param['pool_height']
  pw = pool_param['pool_width']
  ps = pool_param['stride']
  newH = (H-ph)/ps + 1
  newW = (W-pw)/ps + 1
  print newH
  print newW
  out = np.zeros((N,C,newH,newW))
  for n in range(N):
    for c in range(C):
      for nh in range(newH):
        for nw in range(newW):
          out[n,c,nh,nw] = np.max(x[n,c,nh*ps:nh*ps+ph,nw*ps:nw*ps+pw])
  #############################################################################
  #                             END OF YOUR CODE                              #
  #############################################################################
  cache = (x, pool_param)
  return out, cache


def max_pool_backward_naive(dout, cache):
  """
  A naive implementation of the backward pass for a max pooling layer.

  Inputs:
  - dout: Upstream derivatives
  - cache: A tuple of (x, pool_param) as in the forward pass.

  Returns:
  - dx: Gradient with respect to x
  """
  dx = None
  #############################################################################
  # TODO: Implement the max pooling backward pass                             #
  #############################################################################
  x,pool_param = cache
  N, C, H, W = x.shape
  ph = pool_param['pool_height']
  pw = pool_param['pool_width']
  ps = pool_param['stride']
  newH = (H-ph)/ps + 1
  newW = (W-pw)/ps + 1
  dx = np.zeros((N,C,H,W))
  for n in range(N):
    for c in range(C):
      for nh in range(newH):
        for nw in range(newW):
          x_pooled = x[n,c,nh*ps:nh*ps+ph,nw*ps:nw*ps+pw]
          dx[n,c,nh*ps:nh*ps+ph,mw*ps:nw*ps+pw] += dout[n,c,nh,nw]*(x_pooled==np.max(x_pooled))
  #############################################################################
  #                             END OF YOUR CODE                              #
  #############################################################################
  return dx


def spatial_batchnorm_forward(x, gamma, beta, bn_param):
  """
  Computes the forward pass for spatial batch normalization.
  
  Inputs:
  - x: Input data of shape (N, C, H, W)
  - gamma: Scale parameter, of shape (C,)
  - beta: Shift parameter, of shape (C,)
  - bn_param: Dictionary with the following keys:
    - mode: 'train' or 'test'; required
    - eps: Constant for numeric stability
    - momentum: Constant for running mean / variance. momentum=0 means that
      old information is discarded completely at every time step, while
      momentum=1 means that new information is never incorporated. The
      default of momentum=0.9 should work well in most situations.
    - running_mean: Array of shape (D,) giving running mean of features
    - running_var Array of shape (D,) giving running variance of features
    
  Returns a tuple of:
  - out: Output data, of shape (N, C, H, W)
  - cache: Values needed for the backward pass
  """
  out, cache = None, None

  #############################################################################
  # TODO: Implement the forward pass for spatial batch normalization.         #
  #                                                                           #
  # HINT: You can implement spatial batch normalization using the vanilla     #
  # version of batch normalization defined above. Your implementation should  #
  # be very short; ours is less than five lines.                              #
  #############################################################################
  N,C,H,W = x.shape
  mode = bn_param['mode']
  eps = bn_param['eps']
  momentum = bn_param['momentum']
  running_mean = bn_param['running_mean']
  running_var = bn_param['running_var']
  if mode=='train':
    x_mean = (np.mean(x, axis=(0,2,3)).reshape(1,C,1,1))
    x_var = (np.mean((x-x_mean)**2, axis=(0,2,3)).reshape(1,C,1,1))
    running_mean = momentum * running_mean + (1-momentum)*np.squeeze(x_mean)
    running_var = momentum * running_var + (1-momentum)*np.squeeze(x_var)
  if mode=='test':
    x_mean = running_mean.reshape(1, C, 1, 1)
    x_var = running_var.reshape(1, C, 1, 1)

  x_hat = (x-x_mean)/np.sqrt(x_var+eps)
  out = gamma.reshape(1,C,1,1)*x_hat + beta.reshape(1,C,1,1)

  bn_param['running_mean'] = running_mean
  bn_param['running_var'] = running_var
  cache = (x_mean, x_var, x, x_hat, gamma, eps)
  #############################################################################
  #                             END OF YOUR CODE                              #
  #############################################################################

  return out, cache


def spatial_batchnorm_backward(dout, cache):
  """
  Computes the backward pass for spatial batch normalization.
  
  Inputs:
  - dout: Upstream derivatives, of shape (N, C, H, W)
  - cache: Values from the forward pass
  
  Returns a tuple of:
  - dx: Gradient with respect to inputs, of shape (N, C, H, W)
  - dgamma: Gradient with respect to scale parameter, of shape (C,)
  - dbeta: Gradient with respect to shift parameter, of shape (C,)
  """
  dx, dgamma, dbeta = None, None, None

  #############################################################################
  # TODO: Implement the backward pass for spatial batch normalization.        #
  #                                                                           #
  # HINT: You can implement spatial batch normalization using the vanilla     #
  # version of batch normalization defined above. Your implementation should  #
  # be very short; ours is less than five lines.                              #
  #############################################################################
  x_mean, x_var, x, x_hat, gamma, eps = cache
  N, C, H, W = x.shape
  gamma = gamma.reshape(1, C, 1, 1)
  dbeta = np.sum(dout, axis=(0, 2, 3))
  dgamma = np.sum(dout*x_hat, axis=(0, 2, 3))
  dx = (gamma/(N*H*W)) * (x_var+eps)**(-0.5) * ((N*W*H) * dout - np.sum(dout, axis=(0, 2, 3)).reshape(1, C, 1, 1) - (x-x_mean) * (x_var+eps)**(-1.0) * np.sum(dout * (x-x_mean), axis=(0, 2, 3)).reshape(1, C, 1, 1))
  #############################################################################
  #                             END OF YOUR CODE                              #
  #############################################################################

  return dx, dgamma, dbeta


def softmax_loss(x, y):
  """
  Computes the loss and gradient for softmax classification.

  Inputs:
  - x: Input data, of shape (N, C) where x[i, j] is the score for the jth class
    for the ith input.
  - y: Vector of labels, of shape (N,) where y[i] is the label for x[i] and
    0 <= y[i] < C

  Returns a tuple of:
  - loss: Scalar giving the loss
  - dx: Gradient of the loss with respect to x
  """
  probability = np.exp(x - np.max(x, axis=1, keepdims=True))
  probability /= np.sum(probability, axis=1, keepdims=True)
  N = x.shape[0]
  loss = -np.sum(np.log(probability[np.arange(N), y])) / N
  dx = probability.copy()
  dx[np.arange(N), y] -= 1
  dx /= N
  return loss, dx