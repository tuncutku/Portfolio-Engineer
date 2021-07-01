"""Sample analytics results"""

from pandas import Timestamp

periodic_return_cum_raw = {
    "AAPL": {
        Timestamp("2020-05-04 00:00:00"): 1.0,
        Timestamp("2020-05-05 00:00:00"): 1.0150089132104245,
        Timestamp("2020-05-06 00:00:00"): 1.0254809371628122,
        Timestamp("2020-05-07 00:00:00"): 1.036089465009817,
        Timestamp("2020-05-08 00:00:00"): 1.0607502228828025,
        Timestamp("2020-05-11 00:00:00"): 1.0774414231208804,
        Timestamp("2020-05-12 00:00:00"): 1.065128225390523,
        Timestamp("2020-05-13 00:00:00"): 1.0522676459919136,
        Timestamp("2020-05-14 00:00:00"): 1.0587321930196596,
        Timestamp("2020-05-15 00:00:00"): 1.052472874711072,
        Timestamp("2020-05-18 00:00:00"): 1.0772704517301632,
        Timestamp("2020-05-19 00:00:00"): 1.071045390750017,
        Timestamp("2020-05-20 00:00:00"): 1.091875317615875,
    },
    "RY.TO": {
        Timestamp("2020-05-04 00:00:00"): 1.0,
        Timestamp("2020-05-05 00:00:00"): 0.996946141421931,
        Timestamp("2020-05-06 00:00:00"): 0.9938923762969063,
        Timestamp("2020-05-07 00:00:00"): 0.9887244229531517,
        Timestamp("2020-05-08 00:00:00"): 1.0023489422657372,
        Timestamp("2020-05-11 00:00:00"): 1.0171481663438018,
        Timestamp("2020-05-12 00:00:00"): 0.9970635184454345,
        Timestamp("2020-05-13 00:00:00"): 0.968992186484428,
        Timestamp("2020-05-14 00:00:00"): 0.9765092690000081,
        Timestamp("2020-05-15 00:00:00"): 0.9706364927969661,
        Timestamp("2020-05-18 00:00:00"): 0.9706364927969661,
        Timestamp("2020-05-19 00:00:00"): 0.9834389991328489,
        Timestamp("2020-05-20 00:00:00"): 1.010218436210961,
    },
}

periodic_return_raw = {
    "AAPL": {
        Timestamp("2020-05-05 00:00:00"): 0.015008913210424524,
        Timestamp("2020-05-06 00:00:00"): 0.010317174377577842,
        Timestamp("2020-05-07 00:00:00"): 0.010344929352226861,
        Timestamp("2020-05-08 00:00:00"): 0.023801764911056233,
        Timestamp("2020-05-11 00:00:00"): 0.015735278558524524,
        Timestamp("2020-05-12 00:00:00"): -0.011428182976937595,
        Timestamp("2020-05-13 00:00:00"): -0.012074207679450222,
        Timestamp("2020-05-14 00:00:00"): 0.0061434436878957666,
        Timestamp("2020-05-15 00:00:00"): -0.005912088391999304,
        Timestamp("2020-05-18 00:00:00"): 0.02356125047488633,
        Timestamp("2020-05-19 00:00:00"): -0.0057785498248359435,
        Timestamp("2020-05-20 00:00:00"): 0.019448220444953757,
    },
    "RY.TO": {
        Timestamp("2020-05-05 00:00:00"): -0.0030538585780689464,
        Timestamp("2020-05-06 00:00:00"): -0.0030631194586592247,
        Timestamp("2020-05-07 00:00:00"): -0.0051997112232711196,
        Timestamp("2020-05-08 00:00:00"): 0.013779895586974122,
        Timestamp("2020-05-11 00:00:00"): 0.014764543018933152,
        Timestamp("2020-05-12 00:00:00"): -0.01974603952791132,
        Timestamp("2020-05-13 00:00:00"): -0.028154005679371097,
        Timestamp("2020-05-14 00:00:00"): 0.007757629649061126,
        Timestamp("2020-05-15 00:00:00"): -0.006014050649059466,
        Timestamp("2020-05-18 00:00:00"): 0.0,
        Timestamp("2020-05-19 00:00:00"): 0.013189805278175148,
        Timestamp("2020-05-20 00:00:00"): 0.02723039975201802,
    },
}

weighted_return_raw = {
    Timestamp("2020-05-05 00:00:00"): 0.0025751179419302417,
    Timestamp("2020-05-06 00:00:00"): 0.0011450002718261989,
    Timestamp("2020-05-07 00:00:00"): -0.00025879111192143606,
    Timestamp("2020-05-08 00:00:00"): 0.016986796836035826,
    Timestamp("2020-05-11 00:00:00"): 0.01507537100431188,
    Timestamp("2020-05-12 00:00:00"): -0.017067353298721718,
    Timestamp("2020-05-13 00:00:00"): -0.022917881371074193,
    Timestamp("2020-05-14 00:00:00"): 0.007232564354207712,
    Timestamp("2020-05-15 00:00:00"): -0.005980881888380351,
    Timestamp("2020-05-18 00:00:00"): 0.007785490609402548,
    Timestamp("2020-05-19 00:00:00"): 0.007001031175416956,
    Timestamp("2020-05-20 00:00:00"): 0.02470431273518519,
}

weighted_cum_return_raw = {
    Timestamp("2020-05-04 00:00:00"): 1.0,
    Timestamp("2020-05-05 00:00:00"): 1.0025751179419302,
    Timestamp("2020-05-06 00:00:00"): 1.0037230667245,
    Timestamp("2020-05-07 00:00:00"): 1.0034633121160013,
    Timestamp("2020-05-08 00:00:00"): 1.0205089395313314,
    Timestamp("2020-05-11 00:00:00"): 1.035893490407983,
    Timestamp("2020-05-12 00:00:00"): 1.018213530227344,
    Timestamp("2020-05-13 00:00:00"): 0.9948782333311711,
    Timestamp("2020-05-14 00:00:00"): 1.0020737541783393,
    Timestamp("2020-05-15 00:00:00"): 0.9960804694111528,
    Timestamp("2020-05-18 00:00:00"): 1.0038354445519626,
    Timestamp("2020-05-19 00:00:00"): 1.0108633277942594,
    Timestamp("2020-05-20 00:00:00"): 1.0358360115766188,
}
