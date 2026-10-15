# Source Generated with Decompyle++
# File: main_interfaces.pyc (Python 2.6)

import constants
from debug_utils import LOG_ERROR, LOG_CURRENT_EXCEPTION
from gui.Scaleform.Barracks import Barracks
from gui.Scaleform.BattleLoading import BattleLoading
from gui.Scaleform.Inventory import Inventory
from gui.Scaleform.Hangar import Hangar
from gui.Scaleform.Login import Login
from gui.Scaleform.Prebattle import Prebattle
from gui.Scaleform.Profile import Profile
from gui.Scaleform.Shop import Shop
from gui.Scaleform.StartGameVideo import StartGameVideo
from gui.Scaleform.Training import Training
from gui.Scaleform.VehicleCustomization import VehicleCustomization
from gui.Scaleform.techtree.techtree_page import TechTreePage
from gui.Scaleform.techtree.research_page import ResearchPage
import exceptions
idict = {
    'login': Login,
    'hangar': Hangar,
    'inventory': Inventory,
    'shop': Shop,
    'profile': Profile,
    'prebattle': Prebattle,
    'battleloading': BattleLoading,
    'training': Training,
    'startgamevideo': StartGameVideo,
    'barracks': Barracks,
    'customization': VehicleCustomization,
    'techtree': TechTreePage,
    'research': ResearchPage }
if constants.IS_DEVELOPMENT:
    
    try:
        from gui.Scaleform.development.ManagementBattles import ManagementBattles
        idict.update({
            'development/management_battles': ManagementBattles })
    except exceptions.ImportError:
        
        class ManagementBattles:
            pass

        LOG_CURRENT_EXCEPTION()
        LOG_ERROR('Package gui.Scaleform.development not found.')
    


