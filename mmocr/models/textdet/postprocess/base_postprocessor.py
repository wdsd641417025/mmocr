# Copyright (c) OpenMMLab. All rights reserved.
from functools import partial

import numpy as np
import torch.nn as nn

# from mmocr.utils import check_argument


class BasePostprocessor:

    def __init__(self, text_repr_type='poly'):
        assert text_repr_type in ['poly', 'quad'
                                  ], f'Invalid text repr type {text_repr_type}'

        self.text_repr_type = text_repr_type

    def is_valid_instance(self, area, confidence, area_thresh,
                          confidence_thresh):

        return bool(area >= area_thresh and confidence > confidence_thresh)


class BaseTextDetPostProcessor(nn.Module):
    """the results must has the same format as.

    #polygon'size is batch_size * poly_num_per_img * point_num
    [dict(
         filename=filename,
         polygon=list[list[list[float]]],
         polygon_score=list[list[float]])]
    """

    def __init__(self,
                 text_repr_type='poly',
                 train_cfg=None,
                 test_cfg=None,
                 **kwargs):
        assert text_repr_type in ['poly', 'quad']
        self.train_cfg = train_cfg
        self.test_cfg = test_cfg

    def forward(self, pred_results, img_metas=None, **kwargs):

        cfg = self.train_cfg if self.training else self.test_cfg
        cfg.update(kwargs)
        if len(img_metas) == 1:
            img_metas = [img_metas]
        pred_results = self.split_results(pred_results, img_metas)
        forward_single = partial(self._forward_single, **cfg)
        results = list(map(forward_single, pred_results, img_metas))

        return results

    def _forward_single(self,
                        pred_result,
                        img_meta=None,
                        rescale=False,
                        property=None,
                        filter_and_location=True,
                        reconstruct=True,
                        extra_property=None,
                        rescale_extra_property=False,
                        **kwargs):

        if filter_and_location:
            results = self.filter_and_location(pred_result, img_meta, **kwargs)

        if reconstruct:
            results = self.reconstruct_text_instance(results, **kwargs)

        if rescale and property is not None:
            for key in property:
                assert key in results
            results = self.rescale_results(results,
                                           img_meta[0]['scale_factor'],
                                           property)

        if rescale_extra_property and extra_property is not None:
            for key in extra_property:
                assert key in results
            results = self.rescale_results(results,
                                           img_meta[0]['scale_factor'],
                                           extra_property)
        return results

    def rescale_results(self, results, scale_factor, property=None):
        """Rescale results via scale_factor."""
        assert isinstance(scale_factor, np.ndarray)
        assert scale_factor.shape[0] == 4
        for key in property:
            _rescale_single_result = partial(
                self._rescale_single_result, scale_factor=scale_factor)
            results[key] = list(map(_rescale_single_result, results[key]))
        return results

    def _rescale_single_result(self, polygon, scale_factor):
        polygon = np.array(polygon)
        poly_shape = polygon.shape
        reshape_polygon = polygon.reshape(1, -1)
        single_instance_point_num = reshape_polygon.shape[-1] / 2
        scale_factor = np.repeat(scale_factor[:2], single_instance_point_num)
        polygon = (reshape_polygon * scale_factor).reshape(poly_shape).tolist()
        return polygon

    def filter_and_location(self, results, img_meta, **kwargs):
        return results

    def reconstruct_text_instance(self, results, **kwargs):
        return results

    def split_results(self, pred_results, img_metas, **kwargs):
        """convert pred_results to the follow format:

        list(dict()) the list' size is batch size dict contain single image
        pred result
        """
        return pred_results
