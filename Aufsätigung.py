##################################################################
# GUI für Erstellung Struktur 'HK AUFS PTV*' ######################
# und automatisch: 'Continue' Optimierung 1x #######################
# mit MIN DOSE für HK AUFS #########################################
# HR 28 NOV 2019 ##################################################
#################################################################

import wpf
from System.Windows import *
from System.Windows.Controls import *
class MyWindow(Window):
    def __init__(self, plan, beam_set):
        ### DATEI fuer GUI-FORMATIERUNG liegt auf sr00016080 und 79 ###
        pathtofile=r"C:\script_files\HR_gui_example.xaml"
        wpf.LoadComponent(self, pathtofile)

        ### ALLE STRUKTUREN DIE MIT 'PT' BEGINNEN IN LISTE ZUR AUSWAHL ###
        roi_list = [r.OfRoi.Name for r in plan.GetStructureSet().RoiGeometries if r.PrimaryShape != None]
        ptv_roi_list=[]
        for dummy in range(len(roi_list)):
            if roi_list[dummy][:2]=="PT": ptv_roi_list.append(roi_list[dummy])
        self.SelectROI.ItemsSource = ptv_roi_list

        ### AUSWAHL OB AUCH LUNGE ABGEZOGEN WERDEN SOLL ###
        self.SelectLung.ItemsSource = ['ja','nein']

        ### AUSWAHL OB OPTIMIERUNG GLEICH STARTEN SOLL ###
        self.SelectOpt.ItemsSource = ['ja','nein']

        ### AUSWAHL welches Beamset im Plan ###
        self.SelectBeamset.ItemsSource = bslist
        beamsetcounter=len(bslist)-1
        if len(bslist)>1: 
            self.BeamSetPanel.Visibility=Visibility.Visible

        fraction_dose=beam_set.Prescription.DosePrescriptions[0].DoseValue

        ### OUTPUT USER KONTROLLE IN GUI FUER VERSCHREIBUNG ###
        fd_gui='(HK AUFS mit Min Dose = '+str(fraction_dose/100)+'Gy, weight=300)'
        self.PrescrDose.Text=fd_gui
        self.PrescrDosePanel.Visibility=Visibility.Visible

    def ComputeClicked(self, sender, event):
        roi_name = self.SelectROI.SelectedItem
        lungyes  = self.SelectLung.SelectedItem
        optyes   = self.SelectOpt.SelectedItem
        beamset_sel = self.SelectBeamset.SelectedItem
        fraction_dose=beam_set.Prescription.DosePrescriptions[0].DoseValue
  
        # wenn nichts ausgewaehlt, schließt GUI einfach:
        try:
            print roi_name[1]
            print lungyes[1]
            print optyes[1]
        except:
            print 'Bitte alles anklickern :)'
            sys.exit()

        hkaufsname="HK AUFS " + roi_name

        if lungyes=="ja":
            hkaufsnametmp="TMP HK AUFS " + roi_name

            with CompositeAction('ROI Algebra (' + hkaufsnametmp + ')'):
                retval_0 = case.PatientModel.CreateRoi(Name=hkaufsnametmp, Color="Cyan", Type="Control", TissueName=None, RbeCellTypeName=None, RoiMaterial=None)
                retval_0.SetAlgebraExpression(ExpressionA={ 'Operation': "Union", 'SourceRoiNames': [roi_name], 'MarginSettings': { 'Type': "Expand", 'Superior': 0, 'Inferior': 0, 'Anterior': 0, 'Posterior': 0, 'Right': 0, 'Left': 0 } }, ExpressionB={ 'Operation': "Union", 'SourceRoiNames': ["hk isoroi"], 'MarginSettings': { 'Type': "Expand", 'Superior': 0, 'Inferior': 0, 'Anterior': 0, 'Posterior': 0, 'Right': 0, 'Left': 0 } }, ResultOperation="Subtraction", ResultMarginSettings={ 'Type': "Expand", 'Superior': 0, 'Inferior': 0, 'Anterior': 0, 'Posterior': 0, 'Right': 0, 'Left': 0 })
                retval_0.UpdateDerivedGeometry(Examination=examination, Algorithm="Auto")

            with CompositeAction('ROI Algebra (hkaufsname)'):
                retval_0 = case.PatientModel.CreateRoi(Name=hkaufsname, Color="Blue", Type="Control", TissueName=None, RbeCellTypeName=None, RoiMaterial=None)
                retval_0.SetAlgebraExpression(ExpressionA={ 'Operation': "Union", 'SourceRoiNames': [hkaufsnametmp], 'MarginSettings': { 'Type': "Expand", 'Superior': 0, 'Inferior': 0, 'Anterior': 0, 'Posterior': 0, 'Right': 0, 'Left': 0 } }, ExpressionB={ 'Operation': "Union", 'SourceRoiNames': ["Lunge re.", "Lunge li."], 'MarginSettings': { 'Type': "Expand", 'Superior': 0.5, 'Inferior': 0.5, 'Anterior': 0.5, 'Posterior': 0.5, 'Right': 0.5, 'Left': 0.5 } }, ResultOperation="Subtraction", ResultMarginSettings={ 'Type': "Expand", 'Superior': 0, 'Inferior': 0, 'Anterior': 0, 'Posterior': 0, 'Right': 0, 'Left': 0 })
                retval_0.UpdateDerivedGeometry(Examination=examination, Algorithm="Auto")

            self.DialogResult = True
            case.PatientModel.RegionsOfInterest[hkaufsnametmp].DeleteRoi()

        else:
            with CompositeAction('ROI Algebra (' + hkaufsname + ')'):
                retval_0 = case.PatientModel.CreateRoi(Name=hkaufsname, Color="Cyan", Type="Control", TissueName=None, RbeCellTypeName=None, RoiMaterial=None)
                retval_0.SetAlgebraExpression(ExpressionA={ 'Operation': "Union", 'SourceRoiNames': [roi_name], 'MarginSettings': { 'Type': "Expand", 'Superior': 0, 'Inferior': 0, 'Anterior': 0, 'Posterior': 0, 'Right': 0, 'Left': 0 } }, ExpressionB={ 'Operation': "Union", 'SourceRoiNames': ["hk isoroi"], 'MarginSettings': { 'Type': "Expand", 'Superior': 0, 'Inferior': 0, 'Anterior': 0, 'Posterior': 0, 'Right': 0, 'Left': 0 } }, ResultOperation="Subtraction", ResultMarginSettings={ 'Type': "Expand", 'Superior': 0, 'Inferior': 0, 'Anterior': 0, 'Posterior': 0, 'Right': 0, 'Left': 0 })
                retval_0.UpdateDerivedGeometry(Examination=examination, Algorithm="Auto")


        case.PatientModel.RegionsOfInterest['hk isoroi'].Name = "HK ISOROI " + roi_name
        #self.DialogResult = True

        if optyes=="ja":
            beamsetcounter=0
            if len(bslist)>1:
                for dummy in range(len(bslist)):
                    if bslist[dummy]==beamset_sel:
                        beamsetcounter=dummy
            with CompositeAction('Add Optimization Function'):
                retval_0 = plan.PlanOptimizations[beamsetcounter].AddOptimizationFunction(FunctionType="MinDose", RoiName=hkaufsname, IsConstraint=False, RestrictAllBeamsIndividually=False, RestrictToBeam=None, IsRobust=False, RestrictToBeamSet=None, UseRbeDose=False)
                nroffunct=np.shape(plan.PlanOptimizations[beamsetcounter].Objective.ConstituentFunctions)[0]
                plan.PlanOptimizations[beamsetcounter].Objective.ConstituentFunctions[nroffunct-1].DoseFunctionParameters.DoseLevel = fraction_dose
                plan.PlanOptimizations[beamsetcounter].Objective.ConstituentFunctions[nroffunct-1].DoseFunctionParameters.Weight = 300
            plan.PlanOptimizations[0].RunOptimization()

    def CloseClicked(self, sender, event):
        self.DialogResult = True

##################################################
#################### MAIN ########################

from connect import *
import sys
import numpy as np

case = get_current("Case")
examination = get_current("Examination")
plan = get_current("Plan")
beam_set = get_current("BeamSet")

#Namen der einzelnen beamsets im aktuellen Plan
#falls wenn z.b. Boost schon fertig, noch der PTV Plan
#nachträglich geaendert werden muss (sonst wird min-dose
#immer im zuletzt angelegten beamset angelegt)
bslist=plan.BeamSets._
bslist=bslist.split(',')

window = MyWindow(plan, beam_set)
window.ShowDialog()

##################################################
##################################################
