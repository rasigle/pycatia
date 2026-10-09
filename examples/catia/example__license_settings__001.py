"""

Example - License Settings - 001

Description:
    Determine if a license for DF1 has been requested.

Requirements:
    - CATIA running.

"""

##########################################################
# insert syspath to project folder so examples can be run.
# for development purposes.
import os
import sys

sys.path.insert(0, os.path.abspath("../../pyv5"))
##########################################################

from pyv5 import v5
from pyv5.interfaces.core.setting_controllers import SettingControllers
from pyv5.interfaces.system.license_setting_att import LicenseSettingAtt

cat_lic = "AL3.prd"

application = v5()
settings_controller = SettingControllers(application)
setting_controller = settings_controller.item("CATSysLicenseSettingCtrl")
license_settings = LicenseSettingAtt(setting_controller)

status = license_settings.get_license(cat_lic)

if status == "Requested":
    print(f'License "{cat_lic}" has been requested.')
elif status == "NotRequested":
    print(f'License "{cat_lic}" has not been requested.')
