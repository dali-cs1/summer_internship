import sys 
import xml.etree.ElementTree as ET
import random as rd
import os 
os.chdir('C:/DART/user_data/simulations/Simulation_monastir5_2parc')
numberofsimulations= int(sys.argv[1]) if (len(sys.argv)-1) else 100
scale=[0.7301768635720954,0.5880751480363158,0.6464369978453722,0.4949389884767317,0.6002016846252726,0.7592017515543708,0.550093930407065,0.550093930407065,0.5630390881277901,0.6790506900449919,0.4949389884767317,0.6464369978453722,0.550093930407065,0.6237478875356424,0.550093930407065,0.5756932318942564,0.5880751480363158,0.5630390881277901,0.6464369978453722,0.550093930407065,0.6351937576001964,0.5368367068128,0.5092880175337438,0.6237478875356424,0.5368367068128,0.6120880203991055,0.6120880203991055,0.4328115899072573,0.4158319250237616,0.6002016846252726,0.3796008757771854,0.6351937576001964,0.48016134770021807,0.48016134770021807,0.5092880175337438,0.4158319250237616,0.6464369978453722,0.449149813366463,0.48016134770021807,0.6002016846252726,0.5368367068128,0.550093930407065,0.550093930407065,0.6120880203991055,0.4328115899072573,0.33952534502249593,0.4649142257838635,0.5232436978048867,0.6574880034437269,0.5092880175337438,0.6574880034437269,0.699949430051015,0.4949389884767317,0.48016134770021807,0.6002016846252726,0.6351937576001964,0.6002016846252726,0.6002016846252726,0.4649142257838635,0.6683563100334274]
def sequencemaker(i):
    cab=list()
    cw=list()
    scaledeviation=list()
    for j in range(numberofsimulations)  : 
        cab.append(str(rd.random()*70 + 20))
        cw.append(str(rd.random()*0.04+0.01))
        scaledeviation.append(str(scale[i-2]*(0.8+0.4*rd.random())))
    return f"""    <DartSequencerDescriptorEntry args="{';'.join(cab)}"
                    propertyName="Coeff_diff.Surfaces.LambertianMultiFunctions.LambertianMulti[{i}].Lambertian.ProspectExternalModule.ProspectExternParameters.Cab" type="enumerate"/>
                <DartSequencerDescriptorEntry args="{';'.join(cw)}"
                    propertyName="Coeff_diff.Surfaces.LambertianMultiFunctions.LambertianMulti[{i}].Lambertian.ProspectExternalModule.ProspectExternParameters.Cw" type="enumerate"/>
                <DartSequencerDescriptorEntry args="{';'.join(scaledeviation)}"
                    propertyName="object_3d.ObjectList.Object[{i-2}].GeometricProperties.ScaleProperties.xscale" type="enumerate"/>
                <DartSequencerDescriptorEntry args="{';'.join(scaledeviation)}"
                    propertyName="object_3d.ObjectList.Object[{i-2}].GeometricProperties.ScaleProperties.yscale" type="enumerate"/>
                <DartSequencerDescriptorEntry args="{';'.join(scaledeviation)}"
                    propertyName="object_3d.ObjectList.Object[{i-2}].GeometricProperties.ScaleProperties.zscale" type="enumerate"/>
                
            """
sequencecore=""
for i in range ( 2,62 ) :
    sequencecore += sequencemaker(i)
sequence="""<?xml version="1.0" encoding="UTF-8"?>
<DartFile version="5.10.2">
    <DartSequencerDescriptor sequenceName="sequence;;allproperty">
        <DartSequencerDescriptorEntries>
        <DartSequencerDescriptorGroup currentDisplayedPage="1" groupName="tree">
        
""" +"          "+ sequencecore +"""
        </DartSequencerDescriptorGroup>
        </DartSequencerDescriptorEntries>
                <DartSequencerPreferences atmosphereMaketLaunched="false"
            dartLaunched="true" deleteAll="false"
            deleteAtmosphere="false" deleteAtmosphereMaket="false"
            deleteBandFolder="false" deleteDartLut="false"
            deleteDartSequenceur="false" deleteDartTxt="false"
            deleteDirection="false" deleteInputs="false"
            deleteLibPhase="false" deleteMaket="false"
            deleteMaketTreeResults="false" deletePlyFolder="false"
            deleteScnFiles="false" deleteTreePosition="false"
            deleteTriangles="false" demGeneratorLaunched="false"
            directionLaunched="false" displayEnabled="true"
            genMode="XML" hapkeLaunched="true"
            individualDisplayEnabled="false" maketLaunched="true"
            numberOfEnumerateValuesDisplayed="1000"
            numberParallelThreads="4" phaseLaunched="true"
            prospectLaunched="false"
            triangleFileProcessorLaunched="true" useBroadBand="true"
            useSceneSpectra="true" vegetationLaunched="false" zippedResults="false"/>
        <DartLutPreferences addedDirection="false" atmosToa="false"
            atmosToaOrdre="false" coupl="true" fluorescence="true"
            generateLUT="true" iterx="true" luminance="true"
            maketCoverage="false" ordre="true" otherIter="true"
            phiMax="" phiMin="" productsPerType="false"
            reflectance="true" sensor="true" storeIndirect="false"
            thetaMax="" thetaMin="" toa="true"/>
    </DartSequencerDescriptor>
</DartFile>"""
tree = ET.XML(sequence)
with open("allproperty.xml", "wb") as f:
    f.write(ET.tostring(tree))
print("finished running for",numberofsimulations,"sequences")
