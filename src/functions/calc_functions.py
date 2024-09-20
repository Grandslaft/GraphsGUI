import math
import numpy as np
import pyfftw
import matplotlib.pyplot as plt
from .precipitates import calcPrecipitate2d
import os

R = 8.3144598
a0Al = 4.05E-10
a0Cr = 2.91E-10
a0Fe = 2.86E-10
ERROR = 1.0E-5
dt = 1.0E-2


def parameters(Cr0, Al0, T, N, K, r0, ell):
    pars = []
    pars.append(Cr0)
    pars.append(Al0)
    pars.append(T)
    pars.append(N)
    pars.append(K)
    pars.append(r0)
    GFe = 1225.7 + 124.134*T - 23.5143*T*math.log(T) - 0.439752E-2*T*T - 0.589269E-7*T*T*T + 77358.5/T
    pars.append(GFe)
    GCr = - 8856.94 + 157.48*T - 26.908*T*math.log(T) + 0.189435E-2*T*T - 0.147721E-5*T*T*T + 139250.0/T
    pars.append(GCr)
    GAl = - 1193.24 + 218.235446*T - 38.5844296*T*math.log(T) + 0.18531982E-1*T*T - 0.576227E-5*T*T*T + 74092.0/T
    pars.append(GAl)
    L0FeCr = 20500 - 9.68*T
    pars.append(L0FeCr)
    L0CrAl = - 54900 + 10.0*T
    pars.append(L0CrAl)
    L0FeAl = -122452.9 + 31.6455*T
    pars.append(L0FeAl)
    DFe = 0.28E-3*math.exp(-251000/(R*T))
    pars.append(DFe)
    DCr = 0.37E-2*math.exp(-267000/(R*T))
    pars.append(DCr)
    DAl = 0.52E-3*math.exp(-246000/(R*T))
    pars.append(DAl)
    kappa = L0FeCr / (6.0 * R * T)
    pars.append(kappa)
    scaling = ell * ell / DAl
    pars.append(scaling)
    dose = K*scaling
    pars.append(dose)
    Gamma = N*dose
    pars.append(Gamma)
    return pars


def variables(Size, TotSize):
    vars = []
    k2 = Init_k_space_2d(Size, TotSize)
    vars.append(k2)
    Cr_r = np.zeros(TotSize, dtype=complex)
    Cr_k = np.zeros(TotSize, dtype=complex)
    fft_plan_Cr = pyfftw.FFTW(Cr_r, Cr_k, direction='FFTW_FORWARD', flags=('FFTW_MEASURE',))
    vars.append(Cr_r)
    vars.append(Cr_k)
    vars.append(fft_plan_Cr)
    Al_r = np.zeros(TotSize, dtype=complex)
    Al_k = np.zeros(TotSize, dtype=complex)
    fft_plan_Al = pyfftw.FFTW(Al_r, Al_k, direction='FFTW_FORWARD', flags=('FFTW_MEASURE',))
    vars.append(Al_r)
    vars.append(Al_k)
    vars.append(fft_plan_Al)
    dGdCr_r = np.zeros(TotSize, dtype=complex)
    dGdCr_k = np.zeros(TotSize, dtype=complex)
    fft_plan_dGdCr = pyfftw.FFTW(dGdCr_r, dGdCr_k, direction='FFTW_FORWARD', flags=('FFTW_MEASURE',))
    vars.append(dGdCr_r)
    vars.append(dGdCr_k)
    vars.append(fft_plan_dGdCr)
    dGdAl_r = np.zeros(TotSize, dtype=complex)
    dGdAl_k = np.zeros(TotSize, dtype=complex)
    fft_plan_dGdAl = pyfftw.FFTW(dGdAl_r, dGdAl_k, direction='FFTW_FORWARD', flags=('FFTW_MEASURE',))
    vars.append(dGdAl_r)
    vars.append(dGdAl_k)
    vars.append(fft_plan_dGdAl)
    f11Cr_r = np.zeros(TotSize, dtype=complex)
    f11Cr_k = np.zeros(TotSize, dtype=complex)
    fft_plan_f11Cr = pyfftw.FFTW(f11Cr_k, f11Cr_r, direction='FFTW_BACKWARD', flags=('FFTW_MEASURE',))
    vars.append(f11Cr_r)
    vars.append(f11Cr_k)
    vars.append(fft_plan_f11Cr)
    f12Cr_r = np.zeros(TotSize, dtype=complex)
    f12Cr_k = np.zeros(TotSize, dtype=complex)
    fft_plan_f12Cr = pyfftw.FFTW(f12Cr_k, f12Cr_r, direction='FFTW_BACKWARD', flags=('FFTW_MEASURE',))
    vars.append(f12Cr_r)
    vars.append(f12Cr_k)
    vars.append(fft_plan_f12Cr)
    f11Al_r = np.zeros(TotSize, dtype=complex)
    f11Al_k = np.zeros(TotSize, dtype=complex)
    fft_plan_f11Al = pyfftw.FFTW(f11Al_k, f11Al_r, direction='FFTW_BACKWARD', flags=('FFTW_MEASURE',))
    vars.append(f11Al_r)
    vars.append(f11Al_k)
    vars.append(fft_plan_f11Al)
    f12Al_r = np.zeros(TotSize, dtype=complex)
    f12Al_k = np.zeros(TotSize, dtype=complex)
    fft_plan_f12Al = pyfftw.FFTW(f12Al_k, f12Al_r, direction='FFTW_BACKWARD', flags=('FFTW_MEASURE',))
    vars.append(f12Al_r)
    vars.append(f12Al_k)
    vars.append(fft_plan_f12Al)
    f2Cr_r = np.zeros(TotSize, dtype=complex)
    f2Cr_k = np.zeros(TotSize, dtype=complex)
    fft_plan_f2Cr = pyfftw.FFTW(f2Cr_r, f2Cr_k, direction='FFTW_FORWARD', flags=('FFTW_MEASURE',))
    vars.append(f2Cr_r)
    vars.append(f2Cr_k)
    vars.append(fft_plan_f2Cr)
    f2Al_r = np.zeros(TotSize, dtype=complex)
    f2Al_k = np.zeros(TotSize, dtype=complex)
    fft_plan_f2Al = pyfftw.FFTW(f2Al_r, f2Al_k, direction='FFTW_FORWARD', flags=('FFTW_MEASURE',))
    vars.append(f2Al_r)
    vars.append(f2Al_k)
    vars.append(fft_plan_f2Al)
    out_fCr_r = np.zeros(TotSize, dtype=complex)
    out_fCr_k = np.zeros(TotSize, dtype=complex)
    fft_plan_outCr = pyfftw.FFTW(out_fCr_k, out_fCr_r, direction='FFTW_BACKWARD', flags=('FFTW_MEASURE',))
    vars.append(out_fCr_r)
    vars.append(out_fCr_k)
    vars.append(fft_plan_outCr)
    out_fAl_r = np.zeros(TotSize, dtype=complex)
    out_fAl_k = np.zeros(TotSize, dtype=complex)
    fft_plan_outAl = pyfftw.FFTW(out_fAl_k, out_fAl_r, direction='FFTW_BACKWARD', flags=('FFTW_MEASURE',))
    vars.append(out_fAl_r)
    vars.append(out_fAl_k)
    vars.append(fft_plan_outAl)
    return vars


def M_CrCr(xFe, xCr, xAl, DFe, DCr, DAl):
    M_xx = xCr*((1.0 - xCr)*(1.0 - xCr)*DCr + xCr*xFe*DFe + xAl*xCr*DAl)/DAl
    return M_xx


def M_AlAl(xFe, xCr, xAl, DFe, DCr, DAl):
    M_yy = xAl*((1.0 - xAl)*(1.0 - xAl)*DAl + xAl*xFe*DFe + xAl*xCr*DCr)/DAl
    return M_yy


def M_CrAl(xFe, xCr, xAl, DFe, DCr, DAl):
    M_xy = xCr*xAl*(xFe*DFe - (1.0 - xCr)*DCr - (1.0 - xAl)*DAl)/DAl
    return M_xy


def dG0FeCrAl_dCr(xFe, xCr, xAl, GFe, GCr, GAl, L0FeCr, L0FeAl, L0CrAl, T):
    dG0 = GCr - GFe + xFe*L0FeCr - xCr*L0FeCr + xAl*L0CrAl - xAl*L0FeAl + R*T*(np.log(xCr) - np.log(xFe))
    return dG0


def dG0FeCrAl_dAl(xFe, xCr, xAl, GFe, GCr, GAl, L0FeCr, L0FeAl, L0CrAl, T):
    dG0 = GAl - GFe - xCr*L0FeCr + xCr*L0CrAl + xFe*L0FeAl - xAl*L0FeAl + R*T*(np.log(xAl) - np.log(xFe))
    return dG0


def omega(k2, G, r0):
    w = G*(1.0 - 1.0/(1.0 + k2*r0*r0))
    return w

def GenerateAll(Cr0, Al0, TotSize, fnameCr, fnameAl, flag):
    Cr = abs(np.random.normal(Cr0, ERROR, TotSize))
    Al = abs(np.random.normal(Al0, ERROR, TotSize))
    if flag == 1:
        xyz = read_data_from_xyz_file(fnameCr, TotSize)
        Cr = xyz[:, 2]
        if Al0 > ERROR:
            xyz = read_data_from_xyz_file(fnameAl, TotSize)
            Al = xyz[:, 2]
    Fe, Cr, Al = conservation(Cr0, Al0, Cr, Al)
    return Fe, Cr, Al


def Init_k_space_2d(Size, TotSize):
    k2 = np.zeros(TotSize)
    N21 = int(Size / 2 + 1)
    N2 = Size + 1
    kx = np.zeros(Size+2)
    ky = np.zeros(Size+2)
    delk = 2.0*math.pi/Size
    for i in range(N21):
        fk = i * delk
        kx[i] = fk
        ky[i] = fk
        kx[N2 - i] = -fk
        ky[N2 - i] = -fk
    for i in range(Size):
        for j in range(Size):
            k2[j+Size*i] = kx[i]*kx[i] + ky[j]*ky[j]
    return k2


def initPFT(Cr0, Al0, T, N, K, r0, ell, Size, TotSize, fnameCr, fnameAl, flag):
    pars = parameters(Cr0, Al0, T, N, K, r0, ell)
    Fe, Cr, Al = GenerateAll(Cr0, Al0, TotSize, fnameCr, fnameAl, flag)
    vars = variables(Size, TotSize)
    return Fe, Cr, Al, pars, vars


def conservation(Cr0, Al0, Cr, Al):
    Cr += Cr0 - Cr.mean()
    Cr = np.clip(Cr, ERROR, 1.0 - 2.0 * ERROR)
    Al += Al0 - Al.mean()
    Al = np.clip(Al, ERROR, 1.0 - 2.0 * ERROR)
    Fe = 1.0 - Cr - Al
    Fe = np.clip(Fe, 0.0, 1.0)
    return Fe, Cr, Al


def calcPFT(Fe, Cr, Al, pars, vars, steps):
    Cr0 = pars[0]
    Al0 = pars[1]
    T = pars[2]
    N = pars[3]
    K = pars[4]
    r0 = pars[5]
    GFe = pars[6]
    GCr = pars[7]
    GAl = pars[8]
    L0FeCr = pars[9]
    L0CrAl = pars[10]
    L0FeAl = pars[11]
    DFe = pars[12]
    DCr = pars[13]
    DAl = pars[14]
    kappa = pars[15]
    scaling = pars[16]
    dose = pars[17]
    Gamma = pars[18]

    k2 = vars[0]
    Cr_r = vars[1]
    Cr_k = vars[2]
    fft_plan_Cr = vars[3]
    Al_r = vars[4]
    Al_k = vars[5]
    fft_plan_Al = vars[6]
    dGdCr_r = vars[7]
    dGdCr_k = vars[8]
    fft_plan_dGdCr = vars[9]
    dGdAl_r = vars[10]
    dGdAl_k = vars[11]
    fft_plan_dGdAl = vars[12]
    f11Cr_r = vars[13]
    f11Cr_k = vars[14]
    fft_plan_f11Cr = vars[15]
    f12Cr_r = vars[16]
    f12Cr_k = vars[17]
    fft_plan_f12Cr = vars[18]
    f11Al_r = vars[19]
    f11Al_k = vars[20]
    fft_plan_f11Al = vars[21]
    f12Al_r = vars[22]
    f12Al_k = vars[23]
    fft_plan_f12Al = vars[24]
    f2Cr_r = vars[25]
    f2Cr_k = vars[26]
    fft_plan_f2Cr = vars[27]
    f2Al_r = vars[28]
    f2Al_k = vars[29]
    fft_plan_f2Al = vars[30]
    out_fCr_r = vars[31]
    out_fCr_k = vars[32]
    fft_plan_outCr = vars[33]
    out_fAl_r = vars[34]
    out_fAl_k = vars[35]
    fft_plan_outAl = vars[36]

    for s in range(steps):
        Cr_r.real = Cr
        Cr_r.imag = 0.0
        Al_r.real = Al
        Al_r.imag = 0.0
        dGdCr_r.real = dG0FeCrAl_dCr(Fe, Cr, Al, GFe, GCr, GAl, L0FeCr, L0FeAl, L0CrAl, T)/(R*T)
        dGdCr_r.imag = 0.0
        dGdAl_r.real = dG0FeCrAl_dAl(Fe, Cr, Al, GFe, GCr, GAl, L0FeCr, L0FeAl, L0CrAl, T)/(R*T)
        dGdAl_r.imag = 0.0
        ballistic = omega(k2, Gamma, r0)
        fft_plan_Cr()
        fft_plan_Al()
        fft_plan_dGdCr()
        fft_plan_dGdAl()
        mCrCr = M_CrCr(Fe, Cr, Al, DFe, DCr, DAl)
        mAlAl = M_AlAl(Fe, Cr, Al, DFe, DCr, DAl)
        mCrAl = M_CrAl(Fe, Cr, Al, DFe, DCr, DAl)
        f11Cr_k.real = -np.sqrt(k2) * (dGdCr_k.imag + kappa * k2 * (2.0 * Cr_k.imag + Al_k.imag))
        f11Cr_k.imag = np.sqrt(k2) * (dGdCr_k.real + kappa * k2 * (2.0 * Cr_k.real + Al_k.real))
        f12Cr_k.real = -np.sqrt(k2) * (dGdAl_k.imag + kappa * k2 * (2.0 * Al_k.imag + Cr_k.imag))
        f12Cr_k.imag = np.sqrt(k2) * (dGdAl_k.real + kappa * k2 * (2.0 * Al_k.real + Cr_k.real))
        f11Al_k.real = -np.sqrt(k2) * (dGdAl_k.imag + kappa * k2 * (2.0 * Al_k.imag + Cr_k.imag))
        f11Al_k.imag = np.sqrt(k2) * (dGdAl_k.real + kappa * k2 * (2.0 * Al_k.real + Cr_k.real))
        f12Al_k.real = -np.sqrt(k2) * (dGdCr_k.imag + kappa * k2 * (2.0 * Cr_k.imag + Al_k.imag))
        f12Al_k.imag = np.sqrt(k2) * (dGdCr_k.real + kappa * k2 * (2.0 * Cr_k.real + Al_k.real))
        fft_plan_f11Cr()
        fft_plan_f12Cr()
        fft_plan_f11Al()
        fft_plan_f12Al()
        f2Cr_r.real = mCrCr * f11Cr_r.real + mCrAl * f12Cr_r.real
        f2Cr_r.imag = mCrCr * f11Cr_r.imag + mCrAl * f12Cr_r.imag
        f2Al_r.real = mAlAl * f11Al_r.real + mCrAl * f12Al_r.real
        f2Al_r.imag = mAlAl * f11Al_r.imag + mCrAl * f12Al_r.imag
        fft_plan_f2Cr()
        fft_plan_f2Al()
        out_fCr_k.real = -np.sqrt(k2) * f2Cr_k.imag - ballistic * Cr_k.real
        out_fCr_k.imag = np.sqrt(k2) * f2Cr_k.real - ballistic * Cr_k.imag
        out_fAl_k.real = -np.sqrt(k2) * f2Al_k.imag - ballistic * Al_k.real
        out_fAl_k.imag = np.sqrt(k2) * f2Al_k.real - ballistic * Al_k.imag
        fft_plan_outCr()
        fft_plan_outAl()
        if Cr0 > ERROR:
            Cr += dt * out_fCr_r.real
        if Al0 > ERROR:
            Al += dt * out_fAl_r.real
        Fe, Cr, Al = conservation(Cr0, Al0, Cr, Al)
    return Fe, Cr, Al

def read_data_from_xyz_file(fname, TotSize):
    with open(fname) as f:
        data = np.fromfile(f, dtype=float, count=TotSize * 3, sep=" ").reshape((TotSize, 3))
    return data