import numpy as np
import gc
import pandas as pd


class BonePrior:
    """
    Assumed that everyone is strict symmetrical object, including bones,
    """
    def __init__(self, binary_arr=None):
        """
        :param binary_arr: input only binary arr
        """
        self.binary_arr = binary_arr

        # decrepated
        # self.binary_arr[self.binary_arr < hu_threshold] = 0
        # self.binary_arr[self.binary_arr >= hu_threshold] = 1

        # calc zoy-axis center line.
        self.zoy_symmetric_y_axis_line = None
        self.zoy_symmetric_y_axis_line_df = None
        self.set_zoy_center_y_axis_line()

        self.arr_shape = self.binary_arr.shape

        self.spine_y_width = 0.0

        # will not use
        del self.binary_arr
        gc.collect()

    def set_zoy_center_y_axis_line(self):
        zoy_count_distribution = self.binary_arr.sum(axis=1)
        y_shape = zoy_count_distribution.shape[1]
        zoy_count_distribution[:, :(y_shape//3)] = 0
        zoy_count_distribution[:, (y_shape * 2 // 3):] = 0
        zoy_acc_distribution = np.add.accumulate(zoy_count_distribution, axis=1)

        def numpy_arr_binary_search(arr):
            center_line_arr = np.zeros((arr.shape[0], 2))
            for i in range(arr.shape[0]):
                left_idx = np.searchsorted(arr[i], arr[i, -1] / 2.0, side='left')
                right_idx = np.searchsorted(arr[i], arr[i, -1] / 2.0, side='right')
                center_line_arr[i] = i, (left_idx + right_idx) // 2
            return center_line_arr

        zoy_symmetric_y_axis_line = numpy_arr_binary_search(zoy_acc_distribution)
        zoy_symmetric_y_axis_line_df = pd.DataFrame({'z': zoy_symmetric_y_axis_line[:, 0],
                                                     'y.center': zoy_symmetric_y_axis_line[:, 1]})

        zoy_symmetric_y_axis_line_df['filter_mean'] = zoy_symmetric_y_axis_line_df['y.center'].rolling(100,
                                                                                                       min_periods=50,
                                                                                                       win_type='parzen',
                                                                                                       axis=0).mean()
        zoy_symmetric_y_axis_line_df['filter_mean'] = zoy_symmetric_y_axis_line_df['filter_mean'].fillna(method='bfill', axis=0).fillna(method='ffill', axis=0)

        def f(row):
            if abs(row['y.center'] - row['filter_mean']) > 70:
                return None
            return row['y.center']
        zoy_symmetric_y_axis_line_df['y.center'] = zoy_symmetric_y_axis_line_df.apply(lambda row: f(row), axis=1)
        zoy_symmetric_y_axis_line_df['y.center'] = zoy_symmetric_y_axis_line_df['y.center'].interpolate()
        self.zoy_symmetric_y_axis_line_df = zoy_symmetric_y_axis_line_df

    def get_zoy_symmetric_y_axis_line_df(self):
        return self.zoy_symmetric_y_axis_line_df

    def get_prior_shape(self):
        return self.arr_shape

    def set_zoy_width(self):
        pass

    def get_zoy_width(self):
        pass





