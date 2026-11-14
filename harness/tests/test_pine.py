"""Round-trip parity of the genome compilers (SPEC 10.1 item 5, 18.3): five hand-written genomes are
exported to Pine, the Pine signal layer is executed from text by the independent replay interpreter,
and every order input and the resulting trade list must equal the research engine's."""
import os
import sys

import pytest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from audit import pine_replay, static_audit  # noqa: E402
from genome import compile_pine  # noqa: E402
from genome.genome import A, new_genome  # noqa: E402

GENOMES = {
    "trail_pullback_limit": new_genome([A("tr_pullback_depth")], regime=[A("st_trail_regime"), A("st_htf_ema")],
                                       entry={"type": "limit", "offset_atr": 0.25, "valid_minutes": 15}, stop=A("r_stop_swing"),
                                       exits=[A("x_target_prior_extreme"), A("x_breakeven")], tf=5),
    "sweep_vwap": new_genome([A("tr_sweep_prior_day")], regime=[A("st_htf_bar_dir")], location=[A("loc_vwap_band")], stop=A("r_stop_level"),
                             exits=[A("x_target_vwap"), A("x_time_stop", m=120), A("x_invalidate_ema")], tf=5),
    "squeeze_supertrend": new_genome([A("tr_squeeze_release"), A("tr_cci_breakout")], regime=[A("st_supertrend")], filters=[A("f_atr_rank_low"), A("f_weekday_block")],
                                     combine="OR", stop=A("r_stop_atr"), exits=[A("x_target_r"), A("x_trail_r")], tf=10),
    "intermarket_round": new_genome([A("tr_divergence_at_session_extreme"), A("tr_round_number_reject")], combine="OR",
                                    regime=[A("st_other_instrument_trend")], filters=[A("f_adx_low")], stop=A("r_stop_signal_bar"),
                                    exits=[A("x_target_session_mid"), A("x_invalidate_supertrend")], tf=5),
    "orb_seq_stop_entry": new_genome([A("tr_opening_range_break"), A("tr_hma_turn")], combine="SEQ", within=5, location=[A("loc_confirmed_swing", k=2.0)],
                                     filters=[A("f_session_segment", seg=1), A("f_relative_volume_high", k=1.0)],
                                     entry={"type": "stop", "offset_atr": 0.1, "valid_minutes": 10}, stop=A("r_stop_session_extreme"),
                                     exits=[A("x_target_atr", k=1.5), A("x_partial"), A("x_invalidate_rsi_mid")], tf=5),
}


@pytest.mark.parametrize("name", list(GENOMES))
def test_pine_round_trip_parity(name):
    g = GENOMES[name]
    src = compile_pine.export(g)
    assert not static_audit.scan_pine(src)
    r = pine_replay.parity(g, src, sessions=25, warm=25, seed=1)
    assert r["match"], r["details"]
    assert r["vanished"] == 0 and r["late"] == 0
    assert all(d["trade_lists_equal"] for d in r["details"]) and len(r["details"]) == 4


def test_replay_detects_a_changed_pine_file():
    g = GENOMES["sweep_vwap"]
    src = compile_pine.export(g).replace("ta.ema(", "ta.sma(")          # a silently wrong translation
    r = pine_replay.parity(g, src, sessions=25, warm=25, seed=1)
    assert not r["match"]


def test_export_keeps_the_owner_webhook_layer_and_paper_defaults():
    src = compile_pine.export(GENOMES["sweep_vwap"])
    for needle in ('"06 Webhook / Live Gates"', 'input.string("Sim/Paper", "Execution mode"', 'input.string("internal_paper", "Webhook mode"',
                   'input.bool(false, "I accept full live-trading risk"', "process_orders_on_close = false", "calc_on_every_tick = false",
                   "margin_long = 0", "pyramiding = 0", 'executionMode == "Live" and webhookMode == "live" and acceptLiveRisk',
                   '\\"action\\":\\"', '\\"broker_root\\":\\"', '\\"live\\":"', "CLOSE_LONG", "CLOSE_SHORT", "SELL_SHORT", '"BUY"',
                   'comment = "L"', 'comment = "S"', "barstate.isconfirmed"):
        assert needle in src, needle
    assert "http" not in src.lower() and "SMART_TREND_V1" not in src
    order = [src.index(k) for k in ('\\"action\\"', '\\"side\\"', '\\"qty\\"', '\\"symbol\\"', '\\"broker_root\\"', '\\"price\\"', '\\"key\\"', '\\"tag\\"', '\\"live\\"')]
    assert order == sorted(order)                                        # payload field order as in the owner's script
