__author__ = 'song'
from shutil import copyfile
import os
import numpy as np
from scipy import interpolate


def copy_file(filename_in, filename_out, workingdir):
    #test if filename_out has no pathname, if s
    #print

    #print(filename_out)
    if(workingdir):
        filename_out = os.path.basename(filename_out)

    copyfile(filename_in, filename_out)
    #print(filename_in)
    #print(filename_out)

initialPoints=[0.029999999329447746, 0.0, 0.0, 0.029999999329447746, 0.05999999865889549, 0.0, 0.029999999329447746, 0.0, 0.18823499977588654, 0.029999999329447746, 0.0, 0.17647099494934082, 0.029999999329447746, 0.0, 0.1647060066461563, 0.029999999329447746, 0.0, 0.1529410034418106, 0.029999999329447746, 0.0, 0.1411760002374649, 0.029999999329447746, 0.0, 0.1294119954109192, 0.029999999329447746, 0.0, 0.11764699965715408, 0.029999999329447746, 0.0, 0.10588199645280838, 0.029999999329447746, 0.0, 0.09411759674549103, 0.029999999329447746, 0.0, 0.0823528990149498, 0.029999999329447746, 0.0, 0.07058820128440857, 0.029999999329447746, 0.0, 0.05882349982857704, 0.029999999329447746, 0.0, 0.047058798372745514, 0.029999999329447746, 0.0, 0.035294100642204285, 0.029999999329447746, 0.0, 0.023529399186372757, 0.029999999329447746, 0.0, 0.011764699593186378, 0.029999999329447746, 0.012000000104308128, 0.0, 0.029999999329447746, 0.024000000208616257, 0.0, 0.029999999329447746, 0.035999998450279236, 0.0, 0.029999999329447746, 0.04800000041723251, 0.0, 0.029999999329447746, 0.05999999865889549, 0.011764699593186378, 0.029999999329447746, 0.05999999865889549, 0.023529399186372757, 0.029999999329447746, 0.05999999865889549, 0.035294100642204285, 0.029999999329447746, 0.05999999865889549, 0.047058798372745514, 0.029999999329447746, 0.05999999865889549, 0.05882349982857704, 0.029999999329447746, 0.05999999865889549, 0.07058820128440857, 0.029999999329447746, 0.05999999865889549, 0.0823528990149498, 0.029999999329447746, 0.05999999865889549, 0.09411759674549103, 0.029999999329447746, 0.05999999865889549, 0.10588199645280838, 0.029999999329447746, 0.05999999865889549, 0.11764699965715408, 0.029999999329447746, 0.05999999865889549, 0.1294119954109192, 0.029999999329447746, 0.05999999865889549, 0.1411760002374649, 0.029999999329447746, 0.05999999865889549, 0.1529410034418106, 0.029999999329447746, 0.05999999865889549, 0.1647060066461563, 0.029999999329447746, 0.05999999865889549, 0.17647099494934082, 0.029999999329447746, 0.05999999865889549, 0.18823499977588654, 0.029999999329447746, 0.010083899833261967, 0.12352900207042694, 0.029999999329447746, 0.010076900012791157, 0.05293489992618561, 0.029999999329447746, 0.010733000002801418, 0.016103100031614304, 0.029999999329447746, 0.010579599998891354, 0.02891560085117817, 0.029999999329447746, 0.049044299870729446, 0.028733599931001663, 0.029999999329447746, 0.010118099860846996, 0.041088998317718506, 0.029999999329447746, 0.04955330118536949, 0.04095439985394478, 0.029999999329447746, 0.04978429898619652, 0.052883099764585495, 0.029999999329447746, 0.010188600048422813, 0.07647059857845306, 0.029999999329447746, 0.0499580018222332, 0.08823519945144653, 0.029999999329447746, 0.010066299699246883, 0.11176499724388123, 0.029999999329447746, 0.04984290152788162, 0.12352900207042694, 0.029999999329447746, 0.010126800276339054, 0.06470470130443573, 0.029999999329447746, 0.04990730062127113, 0.06469280272722244, 0.029999999329447746, 0.04999839887022972, 0.07646829634904861, 0.029999999329447746, 0.01018850039690733, 0.0882352963089943, 0.029999999329447746, 0.010126300156116486, 0.10000000149011612, 0.029999999329447746, 0.049940600991249084, 0.10000000149011612, 0.029999999329447746, 0.049880098551511765, 0.11176499724388123, 0.029999999329447746, 0.04989289864897728, 0.14706000685691833, 0.029999999329447746, 0.010149899870157242, 0.14710700511932373, 0.029999999329447746, 0.010902700014412403, 0.17138800024986267, 0.029999999329447746, 0.011040300130844116, 0.1841839998960495, 0.029999999329447746, 0.010084499605000019, 0.13530200719833374, 0.029999999329447746, 0.04990470036864281, 0.13529400527477264, 0.029999999329447746, 0.010360900312662125, 0.15910199284553528, 0.029999999329447746, 0.049862898886203766, 0.15889300405979156, 0.029999999329447746, 0.04946810007095337, 0.17104199528694153, 0.029999999329447746, 0.04921820014715195, 0.18397800624370575, 0.029999999329447746, 0.029798099771142006, 0.010646999813616276, 0.029999999329447746, 0.03019680082798004, 0.18952099978923798, 0.029999999329447746, 0.039873600006103516, 0.009673969820141792, 0.029999999329447746, 0.04893919825553894, 0.015936799347400665, 0.029999999329447746, 0.020058000460267067, 0.11764699965715408, 0.029999999329447746, 0.020177900791168213, 0.07058720290660858, 0.029999999329447746, 0.04005439952015877, 0.09411759674549103, 0.029999999329447746, 0.0202076006680727, 0.09411759674549103, 0.029999999329447746, 0.040022898465394974, 0.07058169692754745, 0.029999999329447746, 0.03989249840378761, 0.11764699965715408, 0.029999999329447746, 0.020401200279593468, 0.03521990031003952, 0.029999999329447746, 0.03901999816298485, 0.035113800317049026, 0.029999999329447746, 0.020041299983859062, 0.04701169952750206, 0.029999999329447746, 0.03962339833378792, 0.04695989936590195, 0.029999999329447746, 0.03986850008368492, 0.058789800852537155, 0.029999999329447746, 0.02004930004477501, 0.058809999376535416, 0.029999999329447746, 0.0395394004881382, 0.16481299698352814, 0.029999999329447746, 0.020106300711631775, 0.10588199645280838, 0.029999999329447746, 0.039889201521873474, 0.1294119954109192, 0.029999999329447746, 0.020882999524474144, 0.1649859994649887, 0.029999999329447746, 0.04008369892835617, 0.08235129714012146, 0.029999999329447746, 0.020205099135637283, 0.08235269784927368, 0.029999999329447746, 0.03999119997024536, 0.10588199645280838, 0.029999999329447746, 0.03990820050239563, 0.1529950052499771, 0.029999999329447746, 0.02003129944205284, 0.12941299378871918, 0.029999999329447746, 0.020085399970412254, 0.14121200144290924, 0.029999999329447746, 0.039931099861860275, 0.14118899405002594, 0.029999999329447746, 0.020292000845074654, 0.1530729979276657, 0.029999999329447746, 0.02010129950940609, 0.1904049962759018, 0.029999999329447746, 0.036958999931812286, 0.02189759910106659, 0.029999999329447746, 0.023000599816441536, 0.1782190054655075, 0.029999999329447746, 0.029962800443172455, 0.12353000044822693, 0.029999999329447746, 0.030022600665688515, 0.0646928995847702, 0.029999999329447746, 0.03002849966287613, 0.11176499724388123, 0.029999999329447746, 0.03010929934680462, 0.10000000149011612, 0.029999999329447746, 0.03014340065419674, 0.08823490142822266, 0.029999999329447746, 0.03010929934680462, 0.07646679878234863, 0.029999999329447746, 0.030000800266861916, 0.1353060007095337, 0.029999999329447746, 0.02988710068166256, 0.052891600877046585, 0.029999999329447746, 0.030064299702644348, 0.14712099730968475, 0.029999999329447746, 0.029760999605059624, 0.04137219861149788, 0.029999999329447746, 0.03017139993607998, 0.15867699682712555, 0.029999999329447746, 0.037438198924064636, 0.17811299860477448, 0.029999999329447746, 0.022540399804711342, 0.021966999396681786, 0.029999999329447746, 0.030206499621272087, 0.1689620018005371, 0.029999999329447746, 0.02973630093038082, 0.03111409954726696, 0.029999999329447746, 0.04017059877514839, 0.19032199680805206, 0.029999999329447746, 0.019814299419522285, 0.009743420407176018]
#weniger Angriffpunkte z bis 0.121:initialPoints=[0.029999999329447746, 0.0, 0.0, 0.029999999329447746, 0.05999999865889549, 0.0, 0.029999999329447746, 0.0, 0.11764699965715408, 0.029999999329447746, 0.0, 0.10588199645280838, 0.029999999329447746, 0.0, 0.09411759674549103, 0.029999999329447746, 0.0, 0.0823528990149498, 0.029999999329447746, 0.0, 0.07058820128440857, 0.029999999329447746, 0.0, 0.05882349982857704, 0.029999999329447746, 0.0, 0.047058798372745514, 0.029999999329447746, 0.0, 0.035294100642204285, 0.029999999329447746, 0.0, 0.023529399186372757, 0.029999999329447746, 0.0, 0.011764699593186378, 0.029999999329447746, 0.012000000104308128, 0.0, 0.029999999329447746, 0.024000000208616257, 0.0, 0.029999999329447746, 0.035999998450279236, 0.0, 0.029999999329447746, 0.04800000041723251, 0.0, 0.029999999329447746, 0.05999999865889549, 0.011764699593186378, 0.029999999329447746, 0.05999999865889549, 0.023529399186372757, 0.029999999329447746, 0.05999999865889549, 0.035294100642204285, 0.029999999329447746, 0.05999999865889549, 0.047058798372745514, 0.029999999329447746, 0.05999999865889549, 0.05882349982857704, 0.029999999329447746, 0.05999999865889549, 0.07058820128440857, 0.029999999329447746, 0.05999999865889549, 0.0823528990149498, 0.029999999329447746, 0.05999999865889549, 0.09411759674549103, 0.029999999329447746, 0.05999999865889549, 0.10588199645280838, 0.029999999329447746, 0.05999999865889549, 0.11764699965715408, 0.029999999329447746, 0.010076900012791157, 0.05293489992618561, 0.029999999329447746, 0.010733000002801418, 0.016103100031614304, 0.029999999329447746, 0.010579599998891354, 0.02891560085117817, 0.029999999329447746, 0.049044299870729446, 0.028733599931001663, 0.029999999329447746, 0.010118099860846996, 0.041088998317718506, 0.029999999329447746, 0.04955330118536949, 0.04095439985394478, 0.029999999329447746, 0.04978429898619652, 0.052883099764585495, 0.029999999329447746, 0.010188600048422813, 0.07647059857845306, 0.029999999329447746, 0.0499580018222332, 0.08823519945144653, 0.029999999329447746, 0.010066299699246883, 0.11176499724388123, 0.029999999329447746, 0.010126800276339054, 0.06470470130443573, 0.029999999329447746, 0.04990730062127113, 0.06469280272722244, 0.029999999329447746, 0.04999839887022972, 0.07646829634904861, 0.029999999329447746, 0.01018850039690733, 0.0882352963089943, 0.029999999329447746, 0.010126300156116486, 0.10000000149011612, 0.029999999329447746, 0.049940600991249084, 0.10000000149011612, 0.029999999329447746, 0.049880098551511765, 0.11176499724388123, 0.029999999329447746, 0.029798099771142006, 0.010646999813616276, 0.029999999329447746, 0.039873600006103516, 0.009673969820141792, 0.029999999329447746, 0.04893919825553894, 0.015936799347400665, 0.029999999329447746, 0.020058000460267067, 0.11764699965715408, 0.029999999329447746, 0.020177900791168213, 0.07058720290660858, 0.029999999329447746, 0.04005439952015877, 0.09411759674549103, 0.029999999329447746, 0.0202076006680727, 0.09411759674549103, 0.029999999329447746, 0.040022898465394974, 0.07058169692754745, 0.029999999329447746, 0.03989249840378761, 0.11764699965715408, 0.029999999329447746, 0.020401200279593468, 0.03521990031003952, 0.029999999329447746, 0.03901999816298485, 0.035113800317049026, 0.029999999329447746, 0.020041299983859062, 0.04701169952750206, 0.029999999329447746, 0.03962339833378792, 0.04695989936590195, 0.029999999329447746, 0.03986850008368492, 0.058789800852537155, 0.029999999329447746, 0.02004930004477501, 0.058809999376535416, 0.029999999329447746, 0.020106300711631775, 0.10588199645280838, 0.029999999329447746, 0.04008369892835617, 0.08235129714012146, 0.029999999329447746, 0.020205099135637283, 0.08235269784927368, 0.029999999329447746, 0.03999119997024536, 0.10588199645280838, 0.029999999329447746, 0.036958999931812286, 0.02189759910106659, 0.029999999329447746, 0.030022600665688515, 0.0646928995847702, 0.029999999329447746, 0.03002849966287613, 0.11176499724388123, 0.029999999329447746, 0.03010929934680462, 0.10000000149011612, 0.029999999329447746, 0.03014340065419674, 0.08823490142822266, 0.029999999329447746, 0.03010929934680462, 0.07646679878234863, 0.029999999329447746, 0.02988710068166256, 0.052891600877046585, 0.029999999329447746, 0.029760999605059624, 0.04137219861149788, 0.029999999329447746, 0.022540399804711342, 0.021966999396681786, 0.029999999329447746, 0.02973630093038082, 0.03111409954726696, 0.029999999329447746, 0.019814299419522285, 0.009743420407176018]

def generateBeamDisplacementsFromSplineCoeffs(coeffs,initialPoints):
    z= [0,0.1,0.2]
    y= [0,0.03,0.06]
    #9 Kontrollpunkte
    Z = np.array([z for i in y])
    Y = np.array([[i]*len(z) for i in y])
    X = np.array([[0.03,0.03,0.03],
              [0.03,0.03,0.03],
                 [0.03,0.03,0.03]])
    #print X
    #print Y
    #print Z

    tck = interpolate.bisplrep(Z,Y,X,kx=2,ky=2) # liefert (kx,ky,coe,tx,ty)
    #print tck
    #andere coeff z.B paraboloid : X-werte entsprechend aendern und tck[2] ausgeben lassen

    #Alle Punktkoodinaten gewinnen
    #z-koordinaten extraktieren
    _Z=np.zeros(len(initialPoints)/3)
    for i in range(len(initialPoints)/3):
      _Z[i]=initialPoints[3*i+2]

    _Y=np.zeros(len(initialPoints)/3)
    for i in range(len(initialPoints)/3):
          _Y[i]=initialPoints[3*i+1]

     #_X=np.zeros(len(_Z))
    #for i in range(len(_Z)):
    #    _X[i]=interpolate.bisplev(_Z[i],_Y[i],tck)
    ##print _X
    #oder
    _X=np.zeros(len(initialPoints)/3)
    for i in range(len(initialPoints)/3):
          _X[i]=initialPoints[3*i]


    _v=np.zeros((len(_X),3))
    for i in range(len(_X)):
        _v[i][0]=_X[i]
        _v[i][1]=_Y[i]
        _v[i][2]=_Z[i]

    #_v das gleiche wie A
    tck[2]= coeffs


    X_=np.zeros(len(_Z))
    for i in range(len(_Z)):
        X_[i]=interpolate.bisplev(_Z[i],_Y[i],tck)#x-werte mit coef=tck[2]
    ##print _X

    #v_ beschreiben die deformierten Punktkoordinaten der initialPoints mit tck[2]=coef

    v_=np.zeros((len(_X),3))

    for i in range(len(_X)):
        v_[i][0]=X_[i]
        v_[i][1]=_Y[i]
        v_[i][2]=_Z[i]-0.05





##print _v = print A
    Disp_v=v_-_v
    #print Disp_v
    n=np.zeros(3*len(Disp_v))
    k=0
    for i in range(len(Disp_v)):
        for j in range(3):
            n[k]=Disp_v[i][j]
            k=k+1
    Displist=n.tolist()
    return Displist

#print generateBeamDisplacementsFromSplineCoeffs([0.03,0.03,0.03,0.03,-0,13,0.03,0.03,0.03,0.03],initialPoints)
