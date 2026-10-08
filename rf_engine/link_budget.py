def noise_floor_dbm(bandwidth_hz: float, noise_figure_db: float = 5.0) -> float:
    if bandwidth_hz <= 0:
        raise ValueError("Bandwidth must be > 0.")
    return -174.0 + 10*__import__("math").log10(bandwidth_hz) + noise_figure_db

def mapl_db(tx_power_dbm, tx_gain_dbi, rx_gain_dbi, cable_loss_db,
            body_loss_db, penetration_loss_db, shadow_margin_db,
            interference_margin_db, rx_sensitivity_dbm):
    # MAPL = total available link budget before propagation loss.
    return (tx_power_dbm + tx_gain_dbi + rx_gain_dbi
            - cable_loss_db - body_loss_db - penetration_loss_db
            - shadow_margin_db - interference_margin_db
            - rx_sensitivity_dbm)

def received_power_dbm(tx_power_dbm, tx_gain_dbi, rx_gain_dbi,
                       path_loss_db, other_losses_db=0.0):
    return tx_power_dbm + tx_gain_dbi + rx_gain_dbi - path_loss_db - other_losses_db

def rsrp_dbm(tx_power_dbm, tx_gain_dbi, rx_gain_dbi,
             path_loss_db, other_losses_db=0.0):
    return received_power_dbm(tx_power_dbm, tx_gain_dbi, rx_gain_dbi,
                               path_loss_db, other_losses_db)
