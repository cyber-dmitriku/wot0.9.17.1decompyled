# Source Generated with Decompyle++
# File: __init__.pyc (Python 2.6)

from gui import GUI_SETTINGS
from gui.Scaleform.customization.CamouflageInterface import CamouflageInterface
from gui.Scaleform.customization.EmblemInterface import EmblemLeftInterface, EmblemRightInterface
from gui.Scaleform.customization.HornInterface import HornInterface
from gui.Scaleform.customization.InscriptionInterface import InscriptionLeftInterface, InscriptionRightInterface
_VEHICLE_CUSTOMIZATIONS = []
if GUI_SETTINGS.customizationCamouflages:
    _VEHICLE_CUSTOMIZATIONS.append({
        'sectionName': 'camouflage',
        'sectionUserString': '#menu:customization/labels/camouflage/section',
        'priceUserString': '#menu:customization/labels/camouflage/price',
        'interface': CamouflageInterface,
        'position': -1 })

if GUI_SETTINGS.customizationEmblems:
    _VEHICLE_CUSTOMIZATIONS.append({
        'sectionName': 'emblemLeft',
        'sectionUserString': '#menu:customization/labels/emblemLeft/section',
        'priceUserString': '#menu:customization/labels/emblemLeft/price',
        'interface': EmblemLeftInterface,
        'position': 0 })

if GUI_SETTINGS.customizationEmblems:
    _VEHICLE_CUSTOMIZATIONS.append({
        'sectionName': 'emblemRight',
        'sectionUserString': '#menu:customization/labels/emblemRight/section',
        'priceUserString': '#menu:customization/labels/emblemRight/price',
        'interface': EmblemRightInterface,
        'position': 1 })

if GUI_SETTINGS.customizationInscriptions:
    _VEHICLE_CUSTOMIZATIONS.append({
        'sectionName': 'inscriptionLeft',
        'sectionUserString': '#menu:customization/labels/inscriptionLeft/section',
        'priceUserString': '#menu:customization/labels/inscriptionLeft/price',
        'interface': InscriptionLeftInterface,
        'position': 0 })

if GUI_SETTINGS.customizationInscriptions:
    _VEHICLE_CUSTOMIZATIONS.append({
        'sectionName': 'inscriptionRight',
        'sectionUserString': '#menu:customization/labels/inscriptionRight/section',
        'priceUserString': '#menu:customization/labels/inscriptionRight/price',
        'interface': InscriptionRightInterface,
        'position': 1 })

if GUI_SETTINGS.customizationHorns:
    _VEHICLE_CUSTOMIZATIONS.append({
        'sectionName': 'horn',
        'sectionUserString': '#menu:customization/labels/horn/section',
        'priceUserString': '#menu:customization/labels/horn/price',
        'interface': HornInterface,
        'position': -1 })


