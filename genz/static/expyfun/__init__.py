"""Experiment control functions
"""

from . import analyze
from . import codeblocks
from . import io
from . import stimuli
from ._experiment_controller import (ExperimentController, wait_secs,
                                     get_keyboard_input
                                     )
from ._eyelink_controller import EyelinkController
from ._git import assert_version, download_version
from ._tdt_controller import TDTController
from ._trigger_controllers import decimals_to_binary, binary_to_decimals
# have to import verbose first since it's needed by many things
from ._utils import (set_log_level, set_log_file, set_config, check_units,
                     get_config, get_config_path, fetch_data_file,
                     run_subprocess
                     )
from ._utils import verbose_dec as verbose, building_doc
from ._version import __version__

# INIT LOGGING
set_log_level(None, False)
set_log_file()
