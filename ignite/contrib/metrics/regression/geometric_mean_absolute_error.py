from __future__ import division
import torch
from ignite.exceptions import NotComputableError
from ignite.contrib.metrics.regression._base import _BaseRegression


class GeometricMeanAbsoluteError(_BaseRegression):
    r"""
    Calculates the Geometric Mean Absolute Error.

    :math:`\text{GMAE} = exp(\frac{1}{n}\sum_{j=1}^n\ln(|A_j - P_j|)`)

    where, :math:`A_j` is the ground truth and :math:`P_j` is the predicted value.

    More details can be found in `Botchkarev 2018`__.

    - `update` must receive output of the form `(y_pred, y)`.
    - `y` and `y_pred` must be of same shape `(N, )` or `(N, 1)`.

    __ https://arxiv.org/abs/1809.03006
    """

    def reset(self):
        self._sum_of_errors = 0.0
        self._num_examples = 0

    def _update(self, output):
        y_pred, y = output
        errors = torch.log(torch.abs(y.view_as(y_pred) - y_pred))
        self._sum_of_errors += torch.sum(errors)
        self._num_examples += y.shape[0]

    def compute(self):
        if self._num_examples == 0:
            raise NotComputableError('GeometricMeanAbsoluteError must have at'
                                     'least one example before it can be computed.')
        return torch.exp(self._sum_of_errors / self._num_examples).item()
