import math


class Executor:
    def __init__(self, w_value, t_value, cp_value, cx_value, cd_value, cy_value, dt_value):
        self.w_value = w_value
        self.t_value = t_value
        self.cp_value = cp_value
        self.cx_value = cx_value
        self.cd_value = cd_value
        self.cy_value = cy_value
        self.dt_value = dt_value
        self.w_ontime_value = self.w_value / self.t_value
        self.p_value = math.sqrt(self.cy_value / (self.cx_value + self.cy_value))
        self.q_st_value = math.sqrt(2 * self.w_ontime_value * self.cd_value/self.cx_value)

    def calculate_parameters(self, sale_lower=None, sale_higher=None, sale_percent=None):
        if sale_lower is not None and sale_higher is not None and sale_lower > sale_higher:
            raise Exception('Lower value must be lower than higher')
        if sale_percent is None:
            sale_percent = 0
        product_price = self.cp_value * (1 - sale_percent)
        standard_opt_order = opt_order = self.q_st_value / self.p_value

        if sale_lower is not None and opt_order < sale_lower:
            opt_order = sale_lower
        if sale_higher is not None and opt_order > sale_higher:
            opt_order = sale_higher

        corrected_q_st_value = self.q_st_value
        if standard_opt_order != opt_order:
            corrected_q_st_value = opt_order * self.p_value

        opt_stock = corrected_q_st_value * self.p_value
        orders_count = math.floor(self.w_value / opt_order)
        opt_time = (opt_order * self.t_value) / self.w_value
        loss_density = self.p_value ** 2
        d_order_point = self.w_ontime_value * self.dt_value - (opt_order - opt_stock)
        order_point = self.w_ontime_value * self.dt_value

        store_sum_price = 0.5 * math.pow(opt_stock, 2) * self.t_value * self.cx_value / opt_order
        delivery_sum_price = self.w_value * self.cd_value / opt_order
        product_sum_price = self.w_value * product_price
        missing_sum_price = 0.5 * math.pow(opt_order - opt_stock, 2) * self.t_value * self.cy_value / opt_order

        return {
            'q_opt': opt_order,
            'k': sale_percent,
            'm_opt': opt_stock,
            't_opt': opt_time,
            'ord_opt': order_point,
            'd_ord_opt': d_order_point,
            'orders': orders_count,
            's_x': store_sum_price,
            's_d': delivery_sum_price,
            's_p': product_sum_price,
            's_y': missing_sum_price,
            'lossd': loss_density,
            's_sum': store_sum_price + product_sum_price + delivery_sum_price + missing_sum_price
        }



