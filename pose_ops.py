import bpy

def create_first_person(do_gun_pose):
    ob = bpy.context.object
    bones = ob.pose.bones

    if(do_gun_pose):
        bones['CON_WeaponController'].location = (19.9882, 61.4135, 1.9112)
        bones['CON_WeaponController'].rotation_euler =(1.624226342755719e-06,9.97385427581321e-07,-8.940695579440217e-07)
        bones['CON_HandPole_R'].location = (0.1248, -23.4333, -37.7582)
        bones['CON_HandPole_L'].location = (-34.2684, -71.1743, -47.5947)

    bones['Bip01'].location =  (-8.4542, 0.0000, 0.0000)
    bones['Bip01'].rotation_quaternion = (0.976144015789032,-0.2052910327911377,0.00044966558925807476,0.07069850713014603)
    bones['CON_Neck'].location =  (0.0000, 0.0000, -0.0001)
    bones['CON_Neck'].rotation_quaternion = (1.0,-3.1739468795422e-06,-9.10833477973938e-07,-3.6880368270431063e-07)
    bones['CON_Head'].location =  (0.0000, -0.0000, 0.0000)
    bones['CON_Head'].rotation_quaternion = (0.9329584836959839,-0.0948825478553772,0.3390125036239624,-0.07520870119333267)
    bones['CON_Clavicle_R'].location =  (-0.0001, -0.0000, 0.0001)
    bones['CON_Clavicle_R'].rotation_quaternion = (0.9952892065048218,-0.06359859555959702,-0.009631948545575142,0.07253902405500412)
    bones['CON_Clavicle_L'].location =  (0.0000, -0.0000, 0.0000)
    bones['CON_Clavicle_L'].rotation_quaternion = (0.996451735496521,-0.0016799337463453412,0.00023602257715538144,-0.08415041863918304)
    bones['Bip01_IK_Hand_Root'].location =  (89.2364, 0.0000, -0.0000)
    bones['Bip01_IK_Hand_Root'].rotation_quaternion = (0.8354006409645081,-0.545075535774231,-0.05030930042266846,-0.04967343062162399)
    bones['IK_Feet_Root'].location =  (0.0000, 0.0000, 0.0000)
    bones['IK_Feet_Root'].rotation_quaternion = (0.7071068286895752,-0.7071067094802856,0.0,0.0)
    bones['CON_FootController_R'].location =  (9.9848, -0.5111, -12.9437)
    bones['CON_FootController_R'].rotation_quaternion = (0.9820308685302734,-0.023410126566886902,0.18659980595111847,-0.01575024239718914)
    bones['CON_FootController_L'].location =  (18.7356, 0.6325, 28.9663)
    bones['CON_FootController_L'].rotation_quaternion = (0.9336397051811218,0.007280784659087658,0.3580193817615509,0.009276616387069225)
    bones['CON_HandPole_R'].location =  (0.1249, -23.4333, -37.7583)
    bones['CON_HandPole_wire_R'].location =  (0.0000, 0.0000, 0.0000)
    bones['CON_HandPole_L'].location =  (-34.2684, -71.1743, -47.5947)
    bones['CON_HandPole_wire_L'].location =  (0.0000, 0.0000, 0.0000)
    bones['CON_FootPole_L'].location =  (27.5849, -8.7865, 24.9113)
    bones['CON_FootPole_L'].rotation_quaternion = (0.7149566411972046,-0.6426025629043579,0.22436945140361786,-0.15986721217632294)
    bones['CON_FootPole_wire_L'].location =  (0.0000, 0.0000, 0.0000)
    bones['CON_FootPole_wire_L'].rotation_quaternion = (1.0,0.0,0.0,0.0)
    bones['CON_FootPole_R'].location =  (23.1308, -25.4642, 5.3653)
    bones['CON_FootPole_R'].rotation_quaternion = (0.5194221138954163,-0.8096367716789246,0.1836218535900116,-0.2024158090353012)
    bones['CON_FootPole_wire_R'].location =  (0.0000, 0.0000, 0.0000)
    bones['CON_FootPole_wire_R'].rotation_quaternion = (1.0,0.0,0.0,0.0)
    bones['CON_SpineRoot'].location =  (-0.0925, -8.4500, -0.2496)
    bones['CON_SpineRoot'].rotation_quaternion = (0.9511289596557617,0.09634412080049515,-0.2927543818950653,-0.01914340630173683)
    bones['CON_PelvisController'].location =  (0.0000, 0.0000, 0.0000)
    bones['CON_PelvisController'].rotation_quaternion = (1.0,0.0,0.0,0.0)
    bones['CON_SpineController'].location =  (-0.5469, -0.6123, 5.3028)
    bones['CON_SpineController'].rotation_quaternion = (0.9835909008979797,0.15902507305145264,-0.08464404195547104,-0.00976839940994978)
    bones['CON_Camera'].location =  (18.5670, 35.4196, 12.8286)
    bones['CON_Camera'].rotation_euler = (1.7210838905157289e-06,6.397578431460715e-07,-1.1920930091946502e-06)
    
def create_third_person_stand(do_gun_pose):
    ob = bpy.context.object
    bones = ob.pose.bones

    if(do_gun_pose):
        bones['CON_WeaponController'].location = (9.4287, 72.4890, 2.0239)
        bones['CON_WeaponController'].rotation_euler =(-8.34464913168631e-07,3.1193224003800424e-07,-7.152556236178498e-07)
        bones['CON_HandPole_R'].location = (25.6588, -35.9514, -43.0548)
        bones['CON_HandPole_L'].location = (-37.2178, -57.6102, -46.6358)

    bones['Bip01'].location =  (-3.4650, -0.0100, -0.0051)
    bones['Bip01'].rotation_quaternion = (0.9916289448738098,-0.06308760493993759,-0.002713423455134034,0.11262597143650055)
    bones['CON_Neck'].location =  (-0.0010, 0.0016, 0.0002)
    bones['CON_Neck'].rotation_quaternion = (0.9852550029754639,0.13948704302310944,0.09150270372629166,-0.03799065575003624)
    bones['CON_Head'].location =  (-0.0000, -0.0000, 0.0000)
    bones['CON_Head'].rotation_quaternion = (0.959834635257721,-0.2422582507133484,0.12962639331817627,-0.05679267272353172)
    bones['CON_Clavicle_R'].location =  (-0.0001, -0.0000, 0.0001)
    bones['CON_Clavicle_R'].rotation_quaternion = (0.966080367565155,-0.2333001047372818,-0.026287222281098366,0.10755854099988937)
    bones['CON_Clavicle_L'].location =  (0.0000, -0.0000, -0.0000)
    bones['CON_Clavicle_L'].rotation_quaternion = (0.9123682975769043,-0.20112408697605133,-0.030032891780138016,-0.35529038310050964)
    bones['Bip01_IK_Hand_Root'].location =  (89.2364, -0.0000, 0.0000)
    bones['Bip01_IK_Hand_Root'].rotation_quaternion = (0.8354002237319946,-0.5450761318206787,-0.05030933395028114,-0.04967339709401131)
    bones['IK_Feet_Root'].location =  (0.0000, 0.0000, 0.0000)
    bones['IK_Feet_Root'].rotation_quaternion = (0.7071068286895752,-0.7071067094802856,0.0,0.0)
    bones['CON_FootController_R'].location =  (5.7195, -0.7990, 10.3623)
    bones['CON_FootController_R'].rotation_quaternion = (0.9908437728881836,-0.014000384137034416,-0.1340940147638321,-0.0071747624315321445)
    bones['CON_FootController_L'].location =  (1.2108, -0.5099, 16.2243)
    bones['CON_FootController_L'].rotation_quaternion = (0.9963873028755188,0.015410716645419598,0.08332504332065582,0.005641312338411808)
    bones['CON_HandPole_R'].location =  (25.6588, -35.9514, -43.0548)
    bones['CON_HandPole_wire_R'].location =  (0.0000, 0.0000, 0.0000)
    bones['CON_HandPole_L'].location =  (-37.2178, -57.6102, -46.6358)
    bones['CON_HandPole_wire_L'].location =  (0.0000, 0.0000, 0.0000)
    bones['CON_FootPole_L'].location =  (1.5693, -11.9946, 21.1613)
    bones['CON_FootPole_L'].rotation_quaternion = (0.695519745349884,-0.7180079221725464,0.026627404615283012,0.0028169171418994665)
    bones['CON_FootPole_wire_L'].location =  (0.0000, 0.0000, 0.0000)
    bones['CON_FootPole_wire_L'].rotation_quaternion = (1.0,0.0,0.0,0.0)
    bones['CON_FootPole_R'].location =  (-0.1987, -16.2270, 18.6221)
    bones['CON_FootPole_R'].rotation_quaternion = (0.6770884990692139,-0.7333962917327881,-0.05617412179708481,-0.022923598065972328)
    bones['CON_FootPole_wire_R'].location =  (0.0000, 0.0000, 0.0000)
    bones['CON_FootPole_wire_R'].rotation_quaternion = (1.0,0.0,0.0,0.0)
    bones['CON_SpineRoot'].location =  (-0.0430, -3.4629, -0.1123)
    bones['CON_SpineRoot'].rotation_quaternion = (0.9896544218063354,0.1268962025642395,-0.06636292487382889,-0.00880327820777893)
    bones['CON_PelvisController'].location =  (0.0000, 0.0000, 0.0000)
    bones['CON_PelvisController'].rotation_quaternion = (1.0,0.0,0.0,0.0)
    bones['CON_SpineController'].location =  (0.6972, -1.5757, 8.9202)
    bones['CON_SpineController'].rotation_quaternion = (0.9709132313728333,0.17857076227664948,-0.15600892901420593,-0.033183854073286057)
    bones['CON_Camera'].location =  (12.3846, 46.6454, 7.3332)
    bones['CON_Camera'].rotation_euler = (0.8527955412864685,-3.0810420513153076,0.39767563343048096)
    
def create_third_person_crouch(do_gun_pose):
    ob = bpy.context.object
    bones = ob.pose.bones
    if(do_gun_pose):
        bones['CON_WeaponController'].location = (12.4487, 47.8192, -49.7752)
        bones['CON_WeaponController'].rotation_euler =(-8.940698137394065e-08,-6.119395834502939e-07,-1.8775458556774538e-06)
        bones['CON_HandPole_R'].location = (43.8243, 13.6052, -63.8940)
        bones['CON_HandPole_L'].location = (-52.0431, -10.3860, -57.6961)

    bones['Bip01'].location =  (-52.1679, -22.2340, 0.0723)
    bones['Bip01'].rotation_quaternion = (0.9935274124145508,-0.10970040410757065,0.014158840291202068,-0.025859685614705086)
    bones['CON_Neck'].location =  (-0.0012, 0.0006, 0.0001)
    bones['CON_Neck'].rotation_quaternion = (0.987941563129425,0.04638040438294411,0.11141380667686462,-0.09699112176895142)
    bones['CON_Head'].location =  (-0.0000, -0.0000, -0.0000)
    bones['CON_Head'].rotation_quaternion = (0.9597418308258057,-0.2780558168888092,0.023711970075964928,-0.031914666295051575)
    bones['CON_Clavicle_R'].location =  (-0.0001, -0.0000, 0.0001)
    bones['CON_Clavicle_R'].rotation_quaternion = (0.9646276831626892,-0.16354796290397644,-0.0019530835561454296,0.2067406177520752)
    bones['CON_Clavicle_L'].location =  (0.0000, -0.0000, 0.0000)
    bones['CON_Clavicle_L'].rotation_quaternion = (0.8970201015472412,-0.13497571647167206,0.009823624044656754,-0.4207612872123718)
    bones['Bip01_IK_Hand_Root'].location =  (89.2364, 0.0000, -0.0000)
    bones['Bip01_IK_Hand_Root'].rotation_quaternion = (0.7071073651313782,-0.7071062922477722,2.1238010461388512e-08,6.305565847242178e-08)
    bones['IK_Feet_Root'].location =  (0.0000, 0.0000, 0.0000)
    bones['IK_Feet_Root'].rotation_quaternion = (0.7071068286895752,-0.7071067094802856,0.0,0.0)
    bones['CON_FootController_R'].location =  (6.9236, -10.7355, -34.5170)
    bones['CON_FootController_R'].rotation_quaternion = (0.7141512036323547,-0.6871949434280396,-0.05630305036902428,-0.12075189501047134)
    bones['CON_FootController_L'].location =  (14.5272, -0.5012, 16.9340)
    bones['CON_FootController_L'].rotation_quaternion = (0.9836386442184448,0.012044780887663364,0.17939713597297668,0.011250818148255348)
    bones['CON_HandPole_R'].location =  (43.8243, 13.6052, -63.8940)
    bones['CON_HandPole_wire_R'].location =  (0.0000, 0.0000, 0.0000)
    bones['CON_HandPole_L'].location =  (-52.0431, -10.3860, -57.6961)
    bones['CON_HandPole_wire_L'].location =  (0.0000, 0.0000, 0.0000)
    bones['CON_FootPole_L'].location =  (10.1404, -16.2917, 25.0694)
    bones['CON_FootPole_L'].rotation_quaternion = (0.7320947647094727,-0.6689984798431396,0.05391542986035347,-0.1164965033531189)
    bones['CON_FootPole_wire_L'].location =  (0.0000, 0.0000, 0.0000)
    bones['CON_FootPole_wire_L'].rotation_quaternion = (1.0,0.0,0.0,0.0)
    bones['CON_FootPole_R'].location =  (1.0611, -37.1959, -72.8030)
    bones['CON_FootPole_R'].rotation_quaternion = (0.1784999966621399,0.9836193323135376,0.01771377958357334,0.017805738374590874)
    bones['CON_FootPole_wire_R'].location =  (0.0000, 0.0000, 0.0000)
    bones['CON_FootPole_wire_R'].rotation_quaternion = (1.0,0.0,0.0,0.0)
    bones['CON_SpineRoot'].location =  (-0.3739, -51.4878, -23.7637)
    bones['CON_SpineRoot'].rotation_quaternion = (0.9935610890388489,-0.011846788227558136,-0.11245976388454437,0.0069911596365273)
    bones['CON_PelvisController'].location =  (0.0000, 0.0000, 0.0000)
    bones['CON_PelvisController'].rotation_quaternion = (1.0,0.0,0.0,0.0)
    bones['CON_SpineController'].location =  (1.4233, -4.8646, 15.0013)
    bones['CON_SpineController'].rotation_quaternion = (0.9027373790740967,0.421050101518631,-0.07113732397556305,-0.05217078700661659)
    bones['CON_Camera'].location =  (22.3022, 52.6204, -30.2414)
    bones['CON_Camera'].rotation_euler = (1.751046061515808,-0.5115243196487427,0.35704338550567627)

def create_third_person_prone(do_gun_pose):
    ob = bpy.context.object
    bones = ob.pose.bones

    if(do_gun_pose):
        bones['CON_WeaponController'].location = (23.2769, 100.0214, -112.4146)
        bones['CON_WeaponController'].rotation_euler =(5.453825451695593e-06,-8.056546789703134e-07,8.974222510005347e-06)
        bones['CON_HandPole_R'].location = (47.5108, -1.3577, -146.4869)
        bones['CON_HandPole_L'].location = (-89.4034, -22.6787, -134.5078)


    bones['Bip01'].location =  (-74.9586, -0.4686, -0.0233)
    bones['Bip01'].rotation_quaternion = (0.7211042642593384,-0.08645390719175339,0.0735553428530693,0.6834647059440613)
    bones['CON_Neck'].location =  (-0.0000, -0.0030, 0.0009)
    bones['CON_Neck'].rotation_quaternion = (0.9567407369613647,-0.2905648946762085,-0.001940679969266057,-0.014679187908768654)
    bones['CON_Head'].location =  (-0.0000, -0.0001, -0.0000)
    bones['CON_Head'].rotation_quaternion = (0.9801562428474426,-0.1781926453113556,0.08591271936893463,-0.012656325474381447)
    bones['CON_Clavicle_R'].location =  (-0.0001, -0.0000, 0.0001)
    bones['CON_Clavicle_R'].rotation_quaternion = (0.9660462141036987,0.09017010033130646,-0.0020247672218829393,0.24211566150188446)
    bones['CON_Clavicle_L'].location =  (0.0000, -0.0000, 0.0000)
    bones['CON_Clavicle_L'].rotation_quaternion = (0.9690423607826233,-0.03614269196987152,-0.0008557341643609107,-0.2442333847284317)
    bones['Bip01_IK_Hand_Root'].location =  (89.2364, 0.0000, -0.0000)
    bones['Bip01_IK_Hand_Root'].rotation_quaternion = (0.835400402545929,-0.5450760722160339,-0.05030928924679756,-0.049673378467559814)
    bones['IK_Feet_Root'].location =  (0.0000, 0.0000, 0.0000)
    bones['IK_Feet_Root'].rotation_quaternion = (0.7071068286895752,-0.7071067094802856,0.0,0.0)
    bones['CON_FootController_R'].location =  (34.6562, 1.1180, -67.6743)
    bones['CON_FootController_R'].rotation_quaternion = (0.6366413831710815,-0.4121864438056946,0.4224715232849121,-0.496294230222702)
    bones['CON_FootController_L'].location =  (-52.6684, 2.2779, -46.4116)
    bones['CON_FootController_L'].rotation_quaternion = (0.6937732696533203,-0.27796322107315063,-0.2758646309375763,0.6044120788574219)
    bones['CON_HandPole_R'].location =  (47.5109, -1.3573, -146.4871)
    bones['CON_HandPole_wire_R'].location =  (0.0000, 0.0000, 0.0000)
    bones['CON_HandPole_L'].location =  (-89.4035, -22.6785, -134.5079)
    bones['CON_HandPole_wire_L'].location =  (0.0000, 0.0000, 0.0000)
    bones['CON_FootPole_L'].location =  (-16.1541, -47.0037, -56.2108)
    bones['CON_FootPole_L'].rotation_quaternion = (0.2019272744655609,-0.8783064484596252,0.27364909648895264,0.33603498339653015)
    bones['CON_FootPole_wire_L'].location =  (0.0000, 0.0000, 0.0000)
    bones['CON_FootPole_wire_L'].rotation_quaternion = (1.0,0.0,0.0,0.0)
    bones['CON_FootPole_R'].location =  (14.4940, -59.8346, -59.4216)
    bones['CON_FootPole_R'].rotation_quaternion = (0.10937076807022095,-0.9343153238296509,-0.13181957602500916,-0.31259676814079285)
    bones['CON_FootPole_wire_R'].location =  (0.0000, 0.0000, 0.0000)
    bones['CON_FootPole_wire_R'].rotation_quaternion = (1.0,0.0,0.0,0.0)
    bones['CON_SpineRoot'].location =  (-0.8411, -74.9075, -2.6814)
    bones['CON_SpineRoot'].rotation_quaternion = (0.7111020088195801,0.6933353543281555,-0.0932612270116806,0.07015965133905411)
    bones['CON_PelvisController'].location =  (0.0000, 0.0000, 0.0000)
    bones['CON_PelvisController'].rotation_quaternion = (1.0,0.0,0.0,0.0)
    bones['CON_SpineController'].location =  (-1.0583, -0.0521, -0.2891)
    bones['CON_SpineController'].rotation_quaternion = (0.9886091351509094,-0.14915844798088074,0.011272492818534374,0.016636276617646217)
    bones['CON_Camera'].location =  (29.9971, 110.0772, -112.7282)
    bones['CON_Camera'].rotation_euler = (1.5255683660507202,-0.15121279656887054,0.4953800141811371)
    
    
def create_rifle_hand_pose():
    ob = bpy.context.object
    bones = ob.pose.bones
    bones['CON_Finger0_R'].location =  (0.0001, -0.0001, -0.0001)
    bones['CON_Finger0_R'].rotation_quaternion = (0.9988075494766235,-1.920815748235327e-06,-7.974184882186819e-06,0.04882097616791725)   
    bones['CON_Finger01_R'].location =  (0.0000, -0.0001, 0.0000)
    bones['CON_Finger01_R'].rotation_quaternion = (0.9943140745162964,0.10387838631868362,0.0024427263997495174,-0.023299748077988625)    
    bones['CON_Finger02_R'].location =  (-0.0000, 0.0001, 0.0000)
    bones['CON_Finger02_R'].rotation_quaternion = (0.9607645273208618,0.27437663078308105,0.011148904450237751,-0.039050471037626266)     
    bones['CON_Finger1_R'].location =  (0.0001, -0.0001, -0.0000)
    bones['CON_Finger1_R'].rotation_quaternion = (0.9987584352493286,-0.04981576278805733,3.5359664707357297e-06,-3.0538735700247344e-06) 
    bones['CON_Finger11_R'].location =  (0.0000, 0.0000, -0.0000)
    bones['CON_Finger11_R'].rotation_quaternion = (0.9932568073272705,-0.1159355565905571,-2.857192885130644e-05,1.4399885913007893e-05)  
    bones['CON_Finger12_R'].location =  (-0.0000, -0.0000, 0.0000)
    bones['CON_Finger12_R'].rotation_quaternion = (0.9932616353034973,-0.11589383333921432,3.2944946724455804e-05,-1.2456558579287957e-05)
    bones['CON_Finger2_R'].location =  (0.0000, -0.0001, 0.0000)
    bones['CON_Finger2_R'].rotation_quaternion = (0.8428711295127869,0.5369787812232971,0.010221919976174831,-0.03343057632446289)        
    bones['CON_Finger21_R'].location =  (0.0000, -0.0000, -0.0000)
    bones['CON_Finger21_R'].rotation_quaternion = (0.8218982815742493,0.5696343183517456,-1.9104672901448794e-06,-3.6826920677413e-06)    
    bones['CON_Finger22_R'].location =  (0.0000, -0.0000, 0.0000)
    bones['CON_Finger22_R'].rotation_quaternion = (0.9786821603775024,0.20538075268268585,7.622385510330787e-06,-2.464023418724537e-05)   
    bones['CON_Finger3_R'].location =  (0.0001, -0.0001, 0.0000)
    bones['CON_Finger3_R'].rotation_quaternion = (0.8602012395858765,0.5027918219566345,0.03476713225245476,-0.07775257527828217)
    bones['CON_Finger31_R'].location =  (-0.0000, -0.0000, 0.0000)
    bones['CON_Finger31_R'].rotation_quaternion = (0.9199670553207397,0.39199569821357727,1.6986112314043567e-05,-4.0927530790213495e-05)
    bones['CON_Finger32_R'].location =  (0.0000, 0.0000, 0.0000)
    bones['CON_Finger32_R'].rotation_quaternion = (0.9789245128631592,0.2042228877544403,-2.9557273592217825e-05,1.5465044270968065e-05)
    bones['CON_Finger4_R'].location =  (0.0000, -0.0002, 0.0000)
    bones['CON_Finger4_R'].rotation_quaternion = (0.8537207245826721,0.5167063474655151,-0.0023268687073141336,-0.06457579135894775)
    bones['CON_Finger41_R'].location =  (0.0000, 0.0001, -0.0000)
    bones['CON_Finger41_R'].rotation_quaternion = (0.9785988330841064,0.20577789843082428,-2.28415010496974e-05,2.7235479137743823e-05)
    bones['CON_Finger42_R'].location =  (0.0000, -0.0001, 0.0000)
    bones['CON_Finger42_R'].rotation_quaternion = (0.9431618452072144,0.33233407139778137,2.437218245177064e-05,-2.5627236027503386e-05)
    bones['CON_Finger0_L'].location =  (0.0001, 0.0000, -0.0002)
    bones['CON_Finger0_L'].rotation_quaternion = (0.9874943494796753,-0.1289820522069931,0.05658946558833122,-0.07082559168338776)
    bones['CON_Finger01_L'].location =  (-0.0000, 0.0001, -0.0000)
    bones['CON_Finger01_L'].rotation_quaternion = (0.9829481244087219,-0.18315955996513367,0.0004588366427924484,-0.01629507541656494)
    bones['CON_Finger02_L'].location =  (0.0000, -0.0000, 0.0000)
    bones['CON_Finger02_L'].rotation_quaternion = (0.9260134100914001,0.37749069929122925,1.4985430425440427e-05,-6.134973318694392e-06)
    bones['CON_Finger1_L'].location =  (-0.0002, 0.0000, -0.0000)
    bones['CON_Finger1_L'].rotation_quaternion = (0.9986544251441956,0.011801162734627724,-0.03812752664089203,-0.03311185911297798)
    bones['CON_Finger11_L'].location =  (0.0000, 0.0000, -0.0000)
    bones['CON_Finger11_L'].rotation_quaternion = (0.8956955671310425,0.44466784596443176,1.5939765944494866e-05,-2.5254086722270586e-05)
    bones['CON_Finger12_L'].location =  (-0.0000, -0.0000, -0.0000)
    bones['CON_Finger12_L'].rotation_quaternion = (0.9999598264694214,-0.008965508081018925,-3.778248355956748e-05,2.1063638996565714e-05)
    bones['CON_Finger2_L'].location =  (-0.0003, -0.0000, -0.0000)
    bones['CON_Finger2_L'].rotation_quaternion = (0.9800550937652588,0.19525505602359772,0.02526845782995224,-0.02700064517557621)
    bones['CON_Finger21_L'].location =  (-0.0000, 0.0000, 0.0000)
    bones['CON_Finger21_L'].rotation_quaternion = (0.8153170347213745,0.579014778137207,1.2948915355082136e-05,-1.0417621524538845e-05)
    bones['CON_Finger22_L'].location =  (-0.0000, -0.0000, 0.0000)
    bones['CON_Finger22_L'].rotation_quaternion = (0.9859607219696045,-0.1669774204492569,-3.5025177567149512e-06,-7.375310815405101e-06)
    bones['CON_Finger3_L'].location =  (-0.0003, 0.0000, -0.0000)
    bones['CON_Finger3_L'].rotation_quaternion = (0.9515871405601501,0.30261483788490295,-0.05310327187180519,-0.00928877666592598)
    bones['CON_Finger31_L'].location =  (-0.0000, 0.0000, -0.0000)
    bones['CON_Finger31_L'].rotation_quaternion = (0.9451296329498291,0.32669559121131897,-7.272195148289029e-07,-1.2687895832641516e-05)
    bones['CON_Finger32_L'].location =  (0.0000, -0.0000, 0.0000)
    bones['CON_Finger32_L'].rotation_quaternion = (0.9952058792114258,-0.09780199080705643,-1.8361508409725502e-05,1.6226927982643247e-05)
    bones['CON_Finger4_L'].location =  (-0.0003, 0.0000, 0.0001)
    bones['CON_Finger4_L'].rotation_quaternion = (0.9786394834518433,0.19872352480888367,-0.05229100584983826,0.006292134523391724)
    bones['CON_Finger41_L'].location =  (0.0000, -0.0000, 0.0000)
    bones['CON_Finger41_L'].rotation_quaternion = (0.8737680315971375,0.4863429367542267,-2.800784568535164e-05,1.1570018614293076e-05)
    bones['CON_Finger42_L'].location =  (0.0000, -0.0000, 0.0000)
    bones['CON_Finger42_L'].rotation_quaternion = (0.9931303858757019,-0.11701320111751556,2.6803192668012343e-05,7.253609055624111e-06)
    bones['CON_Clavicle_R'].location =  (-0.0001, -0.0000, 0.0001)
    bones['CON_Clavicle_R'].rotation_quaternion = (0.9952892065048218,-0.06359859555959702,-0.009631948545575142,0.07253902405500412)
    bones['CON_Clavicle_L'].location =  (0.0000, -0.0000, 0.0000)
    bones['CON_Clavicle_L'].rotation_quaternion = (0.996451735496521,-0.0016799337463453412,0.00023602257715538144,-0.08415041863918304)
    bones['CON_HandPole_wire_L'].location =  (0.0000, 0.0000, 0.0000)
    bones['CON_WeaponRecoilBone'].location =  (0.0000, 0.0000, 0.0000)
    bones['CON_WeaponRecoilBone'].rotation_euler = (0.0,0.0,0.0)
    bones['CON_WeaponHandController_R'].location =  (-3.4473, -22.3963, 7.9781)
    bones['CON_WeaponHandController_R'].rotation_quaternion = (0.9754859209060669,-0.04719347879290581,-0.21259045600891113,-0.031707342714071274)
    bones['CON_WeaponHandController_L'].location =  (-1.2617, 2.1960, 3.9369)
    bones['CON_WeaponHandController_L'].rotation_quaternion = (0.8088748455047607,0.36685752868652344,-0.4161657392978668,-0.1947900652885437)
    bones['CON_WeaponSpin'].location =  (0.0000, 0.0000, 0.0000)
    bones['CON_WeaponSpin'].rotation_euler = (0.0,0.0,0.0)
    bones['CON_WeaponBone'].location =  (0.0000, 0.0000, 0.0000)
    bones['CON_WeaponBone'].rotation_euler = (0.0,0.0,0.0)


def keyframeall():
    ob = bpy.context.object
    bones = ob.pose.bones
    for bone in bones:
        bone.keyframe_insert("location",  frame=0, group= bone.name)
        bone.keyframe_insert("rotation_quaternion",  frame=0, group= bone.name)
        bone.keyframe_insert("rotation_euler",  frame=0, group= bone.name)

class SquadRig_OT_ApplyPose(bpy.types.Operator):
    bl_idname = "squadrig.apply_pose"
    bl_label = "Apply Pose"
    bl_options = {"REGISTER","UNDO"}
    
    new_pose_items = [
    ("FIRST_PERSON", "1p Basepose", "", 1),
    ("THIRD_PERSON_STAND", "3p Stand", "", 2),
    ("THIRD_PERSON_CROUCH", "3p Crouch", "", 3),
    ("THIRD_PERSON_PRONE", "3p Prone", "", 4),
    ]
    
    new_pose : bpy.props.EnumProperty(items=new_pose_items, name = "New Pose", description="Pose to apply.", default = "FIRST_PERSON")
    
    do_hands : bpy.props.BoolProperty(
        name="Do hand poses.",
        description="Also does sample hand and finger poses. Good for getting started.",
        default=False
    )
    
    do_gun_pose : bpy.props.BoolProperty(
        name="Do Gun Position",
        description="Does the gun position automatically.",
        default=True
    )

    do_keyframe : bpy.props.BoolProperty(
        name="Keyframe",
        description="Keyframe all the bones on the pose.",
        default=True
    )
    
    do_new_action : bpy.props.BoolProperty(
        name="Make New Action",
        description="Pose will be applied to a new action.",
        default=True
    )
    

    def execute(self, context):
        #create new action with name based on what action was made
        if self.do_new_action:
            if self.new_pose == "FIRST_PERSON":
                bpy.ops.squadrig.create_action(name="Animation_1p")
            elif self.new_pose == "THIRD_PERSON_STAND":
                bpy.ops.squadrig.create_action(name="Stand_3p")
            elif self.new_pose == "THIRD_PERSON_CROUCH":
                bpy.ops.squadrig.create_action(name="Crouch_3p")
            elif self.new_pose == "THIRD_PERSON_PRONE":
                bpy.ops.squadrig.create_action(name="Prone_3p")

        #do the actual posing
        if self.new_pose == "FIRST_PERSON":
            create_first_person(self.do_gun_pose)
        elif self.new_pose == "THIRD_PERSON_STAND":
            create_third_person_stand(self.do_gun_pose)
        elif self.new_pose == "THIRD_PERSON_CROUCH":
            create_third_person_crouch(self.do_gun_pose)
        elif self.new_pose == "THIRD_PERSON_PRONE":
            create_third_person_prone(self.do_gun_pose)
        
        #do sample hand poses
        if self.do_hands:
            create_rifle_hand_pose()
        
        #keyframe all the bones
        if self.do_keyframe:
            keyframeall()
        
        return {'FINISHED'}
