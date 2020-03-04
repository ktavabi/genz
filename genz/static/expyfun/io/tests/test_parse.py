import warnings

import numpy as np
from nose.tools import assert_equal, assert_in, assert_raises, assert_true

from genz.static.expyfun import ExperimentController, __version__
from genz.static.expyfun import TrackerUD, TrackerBinom, TrackerDealer
from genz.static.expyfun import _TempDir, _hide_window
from genz.static.expyfun import (read_tab, reconstruct_tracker,
                                 reconstruct_dealer
                                 )

warnings.simplefilter('always')

temp_dir = _TempDir()
std_args = ['test']  # experiment name
std_kwargs = dict(output_dir=temp_dir, full_screen=False, window_size=(1, 1),
                  participant='foo', session='01', stim_db=0.0, noise_db=0.0,
                  verbose=True, version='dev')


@_hide_window
def test_parse():
    """Test .tab parsing."""
    with ExperimentController(*std_args, **std_kwargs) as ec:
        ec.identify_trial(ec_id='one', ttl_id=[0])
        ec.start_stimulus()
        ec.write_data_line('misc', 'trial one')
        ec.stop()
        ec.trial_ok()
        ec.write_data_line('misc', 'between trials')
        ec.identify_trial(ec_id='two', ttl_id=[1])
        ec.start_stimulus()
        ec.write_data_line('misc', 'trial two')
        ec.stop()
        ec.trial_ok()
        ec.write_data_line('misc', 'end of experiment')

    assert_raises(ValueError, read_tab, ec.data_fname, group_start='foo')
    assert_raises(ValueError, read_tab, ec.data_fname, group_end='foo')
    assert_raises(ValueError, read_tab, ec.data_fname, group_end='trial_id')
    assert_raises(RuntimeError, read_tab, ec.data_fname, group_end='misc')
    data = read_tab(ec.data_fname)
    keys = list(data[0].keys())
    assert_equal(len(keys), 6)
    for key in ['trial_id', 'flip', 'play', 'stop', 'misc', 'trial_ok']:
        assert_in(key, keys)
    assert_equal(len(data[0]['misc']), 1)
    assert_equal(len(data[1]['misc']), 1)
    data, params = read_tab(ec.data_fname, group_end=None, return_params=True)
    assert_equal(len(data[0]['misc']), 2)  # includes between-trials stuff
    assert_equal(len(data[1]['misc']), 2)
    assert_equal(params['version'], 'dev')
    assert_equal(params['version_used'], __version__)
    assert_true(params['file'].endswith('test_parse.py'))


@_hide_window
def test_reconstruct():
    """Test Tracker objects reconstruction"""

    # test with one TrackerUD
    with ExperimentController(*std_args, **std_kwargs) as ec:
        tr = TrackerUD(ec, 1, 1, 3, 1, 5, np.inf, 3)
        while not tr.stopped:
            tr.respond(np.random.rand() < tr.x_current)

    tracker = reconstruct_tracker(ec.data_fname)[0]
    assert_true(tracker.stopped)
    tracker.x_current

    # test with one TrackerBinom
    with ExperimentController(*std_args, **std_kwargs) as ec:
        tr = TrackerBinom(ec, .05, .5, 10)
        while not tr.stopped:
            tr.respond(True)

    tracker = reconstruct_tracker(ec.data_fname)[0]
    assert_true(tracker.stopped)
    tracker.x_current

    # tracker not stopped
    with ExperimentController(*std_args, **std_kwargs) as ec:
        tr = TrackerUD(ec, 1, 1, 3, 1, 5, np.inf, 3)
        tr.respond(np.random.rand() < tr.x_current)
        assert_true(not tr.stopped)
    assert_raises(ValueError, reconstruct_tracker, ec.data_fname)

    # test with dealer
    with ExperimentController(*std_args, **std_kwargs) as ec:
        tr = [TrackerUD(ec, 1, 1, 3, 1, 5, np.inf, 3) for _ in range(3)]
        td = TrackerDealer(ec, tr)

        for _, x_current in td:
            td.respond(np.random.rand() < x_current)

    dealer = reconstruct_dealer(ec.data_fname)[0]
    assert_true(all(td._x_history == dealer._x_history))
    assert_true(all(td._tracker_history == dealer._tracker_history))
    assert_true(all(td._response_history == dealer._response_history))
    assert_true(td.shape == dealer.shape)
    assert_true(td.trackers.shape == dealer.trackers.shape)

    # no tracker/dealer in file
    with ExperimentController(*std_args, **std_kwargs) as ec:
        ec.identify_trial(ec_id='one', ttl_id=[0])
        ec.start_stimulus()
        ec.write_data_line('misc', 'trial one')
        ec.stop()
        ec.trial_ok()
        ec.write_data_line('misc', 'end')

    assert_raises(ValueError, reconstruct_tracker, ec.data_fname)
    assert_raises(ValueError, reconstruct_dealer, ec.data_fname)
