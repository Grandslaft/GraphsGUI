import math
import numpy as np
import pyfftw

R = 8.3144598

ell = 2.86e-10
dk = math.pi / 1000

a0Al = 4.05e-10
a0Cr = 2.91e-10
a0Fe = 2.86e-10
ERROR = 1.0e-5
dt = 1.0e-2


class params:
    def __init__(self):
        pass

    def single_graph(self, T, xCr, xAl, N, K):
        self.T, self.xCr, self.xAl, self.N, self.K = T, xCr, xAl, N, K
        self.xFe = 1 - xCr - xAl
        self.L0_FeCr = 20500 - 9.68 * T
        self.L0_CrAl = -54900 + 10.0 * T
        self.L0_FeAl = -122452.9 + 31.6455 * T
        self.kappa = self.L0_FeCr / (6.0 * R * T)
        self.DFe = 0.28e-3 * math.exp(-251000 / (R * T))
        self.DCr = 0.37e-2 * math.exp(-267000 / (R * T))
        self.DAl = 0.52e-3 * math.exp(-246000 / (R * T))
        self.MFe = self.DFe / self.DAl
        self.MCr = self.DCr / self.DAl
        self.MAl = self.DAl / self.DAl
        self.MCrCr = xCr * (
            ((1.0 - xCr) * (1.0 - xCr)) * self.MCr
            + xCr * xAl * self.MAl
            + xCr * self.xFe * self.MFe
        )
        self.MAlAl = xAl * (
            ((1.0 - xAl) * (1.0 - xAl)) * self.MAl
            + xCr * xAl * self.MCr
            + xAl * self.xFe * self.MFe
        )
        self.MCrAl = (
            xCr
            * xAl
            * (self.xFe * self.MFe - (1.0 - xCr) * self.MCr - (1.0 - xAl) * self.MAl)
        )
        self.d2fdCr2 = (
            -2.0 * self.L0_FeCr + R * T * (1.0 / (1.0 - xCr - xAl) + 1.0 / xCr)
        ) / (R * T)
        self.d2fdCrdAl = (
            -self.L0_FeCr + self.L0_CrAl - self.L0_FeAl + R * T / (1.0 - xCr - xAl)
        ) / (R * T)
        self.d2fdAl2 = (
            -2.0 * self.L0_FeAl + R * T * (1.0 / (1.0 - xCr - xAl) + 1.0 / xAl)
        ) / (R * T)
        self.G = N * K * ell * ell / self.DAl

    def multi_graph(self, Cr0, Al0, T, N, K, r0, ell):
        self.Cr0, self.Al0, self.T, self.N, self.K, self.r0, self.ell = (
            Cr0,
            Al0,
            T,
            N,
            K,
            r0,
            ell,
        )
        self.GFe = (
            1225.7
            + 124.134 * T
            - 23.5143 * T * math.log(T)
            - 0.439752e-2 * T * T
            - 0.589269e-7 * T * T * T
            + 77358.5 / T
        )
        self.GCr = (
            -8856.94
            + 157.48 * T
            - 26.908 * T * math.log(T)
            + 0.189435e-2 * T * T
            - 0.147721e-5 * T * T * T
            + 139250.0 / T
        )
        self.GAl = (
            -1193.24
            + 218.235446 * T
            - 38.5844296 * T * math.log(T)
            + 0.18531982e-1 * T * T
            - 0.576227e-5 * T * T * T
            + 74092.0 / T
        )
        self.L0FeCr = 20500 - 9.68 * T
        self.L0CrAl = -54900 + 10.0 * T
        self.L0FeAl = -122452.9 + 31.6455 * T
        self.DFe = 0.28e-3 * math.exp(-251000 / (R * T))
        self.DCr = 0.37e-2 * math.exp(-267000 / (R * T))
        self.DAl = 0.52e-3 * math.exp(-246000 / (R * T))
        self.kappa = self.L0FeCr / (6.0 * R * T)
        self.scaling = ell * ell / self.DAl
        self.dose = K * self.scaling
        self.Gamma = N * self.dose

    def variables(self, Size, TotSize):
        self.k2 = Init_k_space_2d(Size, TotSize)
        self.Cr_r = np.zeros(TotSize, dtype=complex)
        self.Cr_k = np.zeros(TotSize, dtype=complex)
        self.fft_plan_Cr = pyfftw.FFTW(
            self.Cr_r, self.Cr_k, direction="FFTW_FORWARD", flags=("FFTW_MEASURE",)
        )
        self.Al_r = np.zeros(TotSize, dtype=complex)
        self.Al_k = np.zeros(TotSize, dtype=complex)
        self.fft_plan_Al = pyfftw.FFTW(
            self.Al_r, self.Al_k, direction="FFTW_FORWARD", flags=("FFTW_MEASURE",)
        )
        self.dGdCr_r = np.zeros(TotSize, dtype=complex)
        self.dGdCr_k = np.zeros(TotSize, dtype=complex)
        self.fft_plan_dGdCr = pyfftw.FFTW(
            self.dGdCr_r,
            self.dGdCr_k,
            direction="FFTW_FORWARD",
            flags=("FFTW_MEASURE",),
        )
        self.dGdAl_r = np.zeros(TotSize, dtype=complex)
        self.dGdAl_k = np.zeros(TotSize, dtype=complex)
        self.fft_plan_dGdAl = pyfftw.FFTW(
            self.dGdAl_r,
            self.dGdAl_k,
            direction="FFTW_FORWARD",
            flags=("FFTW_MEASURE",),
        )
        self.f11Cr_r = np.zeros(TotSize, dtype=complex)
        self.f11Cr_k = np.zeros(TotSize, dtype=complex)
        self.fft_plan_f11Cr = pyfftw.FFTW(
            self.f11Cr_k,
            self.f11Cr_r,
            direction="FFTW_BACKWARD",
            flags=("FFTW_MEASURE",),
        )
        self.f12Cr_r = np.zeros(TotSize, dtype=complex)
        self.f12Cr_k = np.zeros(TotSize, dtype=complex)
        self.fft_plan_f12Cr = pyfftw.FFTW(
            self.f12Cr_k,
            self.f12Cr_r,
            direction="FFTW_BACKWARD",
            flags=("FFTW_MEASURE",),
        )
        self.f11Al_r = np.zeros(TotSize, dtype=complex)
        self.f11Al_k = np.zeros(TotSize, dtype=complex)
        self.fft_plan_f11Al = pyfftw.FFTW(
            self.f11Al_k,
            self.f11Al_r,
            direction="FFTW_BACKWARD",
            flags=("FFTW_MEASURE",),
        )
        self.f12Al_r = np.zeros(TotSize, dtype=complex)
        self.f12Al_k = np.zeros(TotSize, dtype=complex)
        self.fft_plan_f12Al = pyfftw.FFTW(
            self.f12Al_k,
            self.f12Al_r,
            direction="FFTW_BACKWARD",
            flags=("FFTW_MEASURE",),
        )
        self.f2Cr_r = np.zeros(TotSize, dtype=complex)
        self.f2Cr_k = np.zeros(TotSize, dtype=complex)
        self.fft_plan_f2Cr = pyfftw.FFTW(
            self.f2Cr_r, self.f2Cr_k, direction="FFTW_FORWARD", flags=("FFTW_MEASURE",)
        )
        self.f2Al_r = np.zeros(TotSize, dtype=complex)
        self.f2Al_k = np.zeros(TotSize, dtype=complex)
        self.fft_plan_f2Al = pyfftw.FFTW(
            self.f2Al_r, self.f2Al_k, direction="FFTW_FORWARD", flags=("FFTW_MEASURE",)
        )
        self.out_fCr_r = np.zeros(TotSize, dtype=complex)
        self.out_fCr_k = np.zeros(TotSize, dtype=complex)
        self.fft_plan_outCr = pyfftw.FFTW(
            self.out_fCr_k,
            self.out_fCr_r,
            direction="FFTW_BACKWARD",
            flags=("FFTW_MEASURE",),
        )
        self.out_fAl_r = np.zeros(TotSize, dtype=complex)
        self.out_fAl_k = np.zeros(TotSize, dtype=complex)
        self.fft_plan_outAl = pyfftw.FFTW(
            self.out_fAl_k,
            self.out_fAl_r,
            direction="FFTW_BACKWARD",
            flags=("FFTW_MEASURE",),
        )


# single graph funcs
def A11(k, kappa, MCrCr, MAlAl, MCrAl, d2fdCr2, d2fdCrdAl, d2fdAl2, G, r0):
    a = -k * k * (
        MCrCr * (2.0 * k * k * kappa + d2fdCr2) + MCrAl * (k * k * kappa + d2fdCrdAl)
    ) - omega(k, G, r0)
    return a


def A12(k, kappa, MCrCr, MAlAl, MCrAl, d2fdCr2, d2fdCrdAl, d2fdAl2, G, r0):
    a = (
        -k
        * k
        * (
            MCrCr * (k * k * kappa + d2fdCrdAl)
            + MCrAl * (2.0 * k * k * kappa + d2fdAl2)
        )
    )
    return a


def A21(k, kappa, MCrCr, MAlAl, MCrAl, d2fdCr2, d2fdCrdAl, d2fdAl2, G, r0):
    a = (
        -k
        * k
        * (
            MAlAl * (k * k * kappa + d2fdCrdAl)
            + MCrAl * (2.0 * k * k * kappa + d2fdCr2)
        )
    )
    return a


def A22(k, kappa, MCrCr, MAlAl, MCrAl, d2fdCr2, d2fdCrdAl, d2fdAl2, G, r0):
    a = -k * k * (
        MAlAl * (2.0 * k * k * kappa + d2fdAl2) + MCrAl * (k * k * kappa + d2fdCrdAl)
    ) - omega(k, G, r0)
    return a


def spinodal(R):
    xcr = np.linspace(10, 90, 800)
    temp = []
    x = 0.0
    for i in range(len(xcr)):
        x = xcr[i] / 100
        y = -1.025000e6 * x * (-1.0 + x) / (-484.0 * x * x + 25.0 * R + 484.0 * x)
        temp.append(y)
    return xcr, temp


def lambda1(k, kappa, MCrCr, MAlAl, MCrAl, d2fdCr2, d2fdCrdAl, d2fdAl2, G, r0):
    a11 = A11(k, kappa, MCrCr, MAlAl, MCrAl, d2fdCr2, d2fdCrdAl, d2fdAl2, G, r0)
    a12 = A12(k, kappa, MCrCr, MAlAl, MCrAl, d2fdCr2, d2fdCrdAl, d2fdAl2, G, r0)
    a21 = A21(k, kappa, MCrCr, MAlAl, MCrAl, d2fdCr2, d2fdCrdAl, d2fdAl2, G, r0)
    a22 = A22(k, kappa, MCrCr, MAlAl, MCrAl, d2fdCr2, d2fdCrdAl, d2fdAl2, G, r0)
    A = 1.0
    B = -(a11 + a22)
    C = a11 * a22 - a12 * a21
    D = B * B - 4.0 * A * C
    if D >= 0.0:
        l = (-B + math.sqrt(D)) / (2.0 * A)
    else:
        l = 0.0
    return l


def lambda2(k, kappa, MCrCr, MAlAl, MCrAl, d2fdCr2, d2fdCrdAl, d2fdAl2, G, r0):
    a11 = A11(k, kappa, MCrCr, MAlAl, MCrAl, d2fdCr2, d2fdCrdAl, d2fdAl2, G, r0)
    a12 = A12(k, kappa, MCrCr, MAlAl, MCrAl, d2fdCr2, d2fdCrdAl, d2fdAl2, G, r0)
    a21 = A21(k, kappa, MCrCr, MAlAl, MCrAl, d2fdCr2, d2fdCrdAl, d2fdAl2, G, r0)
    a22 = A22(k, kappa, MCrCr, MAlAl, MCrAl, d2fdCr2, d2fdCrdAl, d2fdAl2, G, r0)
    A = 1.0
    B = -(a11 + a22)
    C = a11 * a22 - a12 * a21
    D = B * B - 4.0 * A * C
    if D >= 0.0:
        l = (-B - math.sqrt(D)) / (2.0 * A)
    else:
        l = 0.0
    return l


def compile_arrays(arrays):
    K_values_1 = arrays[0]
    T_values_1 = arrays[1]
    K_values_2 = arrays[2]
    T_values_2 = arrays[3]
    K_values_3 = arrays[4]
    T_values_3 = arrays[5]
    K_values_4 = arrays[6]
    T_values_4 = arrays[7]
    for i in range(len(K_values_2)):
        K_values_1.append(K_values_2[len(K_values_2) - 1 - i])
        T_values_1.append(T_values_2[len(T_values_2) - 1 - i])

    for i in range(len(K_values_4)):
        K_values_3.append(K_values_4[len(K_values_4) - 1 - i])
        T_values_3.append(T_values_4[len(T_values_4) - 1 - i])
    return T_values_1, K_values_1, T_values_3, K_values_3


# multigraph funcs
def M_CrCr(xFe, xCr, xAl, DFe, DCr, DAl):
    M_xx = (
        xCr
        * ((1.0 - xCr) * (1.0 - xCr) * DCr + xCr * xFe * DFe + xAl * xCr * DAl)
        / DAl
    )
    return M_xx


def M_AlAl(xFe, xCr, xAl, DFe, DCr, DAl):
    M_yy = (
        xAl
        * ((1.0 - xAl) * (1.0 - xAl) * DAl + xAl * xFe * DFe + xAl * xCr * DCr)
        / DAl
    )
    return M_yy


def M_CrAl(xFe, xCr, xAl, DFe, DCr, DAl):
    M_xy = xCr * xAl * (xFe * DFe - (1.0 - xCr) * DCr - (1.0 - xAl) * DAl) / DAl
    return M_xy


def dG0FeCrAl_dCr(xFe, xCr, xAl, GFe, GCr, GAl, L0FeCr, L0FeAl, L0CrAl, T):
    dG0 = (
        GCr
        - GFe
        + xFe * L0FeCr
        - xCr * L0FeCr
        + xAl * L0CrAl
        - xAl * L0FeAl
        + R * T * (np.log(xCr) - np.log(xFe))
    )
    return dG0


def dG0FeCrAl_dAl(xFe, xCr, xAl, GFe, GCr, GAl, L0FeCr, L0FeAl, L0CrAl, T):
    dG0 = (
        GAl
        - GFe
        - xCr * L0FeCr
        + xCr * L0CrAl
        + xFe * L0FeAl
        - xAl * L0FeAl
        + R * T * (np.log(xAl) - np.log(xFe))
    )
    return dG0


def omega(k2, G, r0):
    w = G * (1.0 - 1.0 / (1.0 + k2 * r0 * r0))
    return w


def read_data_from_xyz_file(fname, TotSize):
    with open(fname) as f:
        data = np.fromfile(f, dtype=float, count=TotSize * 3, sep=" ").reshape(
            (TotSize, 3)
        )
    return data


def read_data_from_vtk_file(fname, TotSize):
    X = np.zeros(TotSize)
    length = TotSize + 6 + 3
    with open(fname) as f:
        for i in range(length):
            f.readline()
        for i in range(TotSize):
            X[i] = f.readline()
    return X


def GenerateAll(
    Cr0: float, Al0: float, TotSize: int, to_import=False, vtk_path=[], xyz_path=[]
):
    Al = abs(np.random.normal(Al0, ERROR, TotSize))
    if to_import:
        if len(vtk_path) != 0:

            Cr = read_data_from_vtk_file(
                vtk_path[0] + "Cr" + vtk_path[1], TotSize
                )[:, 2]
            if Al0 > ERROR:
                Al = read_data_from_vtk_file(
                    vtk_path[0] + "Al" + vtk_path[1], TotSize
                    )[:, 2]
        if len(xyz_path) != 0:
            Cr = read_data_from_xyz_file(
                vtk_path[0] + "Cr" + vtk_path[1], TotSize
                )[:, 2]
            if Al0 > ERROR:
                Al = read_data_from_xyz_file(
                    vtk_path[0] + "Al" + vtk_path[1], TotSize
                    )[:, 2]
    else:
        Cr = abs(np.random.normal(Cr0, ERROR, TotSize))
        Al = abs(np.random.normal(Al0, ERROR, TotSize))

    Fe, Cr, Al = conservation(Cr0, Al0, Cr, Al)
    return Fe, Cr, Al


def Init_k_space_2d(Size, TotSize):
    k2 = np.zeros(TotSize)
    N21 = int(Size / 2 + 1)
    N2 = Size + 1
    kx = np.zeros(Size + 2)
    ky = np.zeros(Size + 2)
    delk = 2.0 * math.pi / Size
    for i in range(N21):
        fk = i * delk
        kx[i] = fk
        ky[i] = fk
        kx[N2 - i] = -fk
        ky[N2 - i] = -fk
    for i in range(Size):
        for j in range(Size):
            k2[j + Size * i] = kx[i] * kx[i] + ky[j] * ky[j]
    return k2


def initPFT(
    Cr0: float,
    Al0: float,
    T: float,
    N: float,
    K: float,
    r0: float,
    ell: float,
    Size: int,
    TotSize: int,
    to_import=False,
    vtk_path=[],
    xyz_path=[],
):
    pars = params()
    pars.multi_graph(Cr0, Al0, T, N, K, r0, ell)
    Fe, Cr, Al = GenerateAll(Cr0, Al0, TotSize, to_import, vtk_path, xyz_path)
    vars = params()
    vars.variables(Size, TotSize)
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
    for _ in range(steps):
        vars.Cr_r.real = Cr
        vars.Cr_r.imag = 0.0
        vars.Al_r.real = Al
        vars.Al_r.imag = 0.0
        vars.dGdCr_r.real = dG0FeCrAl_dCr(
            Fe,
            Cr,
            Al,
            pars.GFe,
            pars.GCr,
            pars.GAl,
            pars.L0FeCr,
            pars.L0FeAl,
            pars.L0CrAl,
            pars.T,
        ) / (R * pars.T)
        vars.dGdCr_r.imag = 0.0
        vars.dGdAl_r.real = dG0FeCrAl_dAl(
            Fe,
            Cr,
            Al,
            pars.GFe,
            pars.GCr,
            pars.GAl,
            pars.L0FeCr,
            pars.L0FeAl,
            pars.L0CrAl,
            pars.T,
        ) / (R * pars.T)
        vars.dGdAl_r.imag = 0.0
        ballistic = omega(vars.k2, pars.Gamma, pars.r0)
        vars.fft_plan_Cr()
        vars.fft_plan_Al()
        vars.fft_plan_dGdCr()
        vars.fft_plan_dGdAl()
        mCrCr = M_CrCr(Fe, Cr, Al, pars.DFe, pars.DCr, pars.DAl)
        mAlAl = M_AlAl(Fe, Cr, Al, pars.DFe, pars.DCr, pars.DAl)
        mCrAl = M_CrAl(Fe, Cr, Al, pars.DFe, pars.DCr, pars.DAl)
        vars.f11Cr_k.real = -np.sqrt(vars.k2) * (
            vars.dGdCr_k.imag
            + pars.kappa * vars.k2 * (2.0 * vars.Cr_k.imag + vars.Al_k.imag)
        )
        vars.f11Cr_k.imag = np.sqrt(vars.k2) * (
            vars.dGdCr_k.real
            + pars.kappa * vars.k2 * (2.0 * vars.Cr_k.real + vars.Al_k.real)
        )
        vars.f12Cr_k.real = -np.sqrt(vars.k2) * (
            vars.dGdAl_k.imag
            + pars.kappa * vars.k2 * (2.0 * vars.Al_k.imag + vars.Cr_k.imag)
        )
        vars.f12Cr_k.imag = np.sqrt(vars.k2) * (
            vars.dGdAl_k.real
            + pars.kappa * vars.k2 * (2.0 * vars.Al_k.real + vars.Cr_k.real)
        )
        vars.f11Al_k.real = -np.sqrt(vars.k2) * (
            vars.dGdAl_k.imag
            + pars.kappa * vars.k2 * (2.0 * vars.Al_k.imag + vars.Cr_k.imag)
        )
        vars.f11Al_k.imag = np.sqrt(vars.k2) * (
            vars.dGdAl_k.real
            + pars.kappa * vars.k2 * (2.0 * vars.Al_k.real + vars.Cr_k.real)
        )
        vars.f12Al_k.real = -np.sqrt(vars.k2) * (
            vars.dGdCr_k.imag
            + pars.kappa * vars.k2 * (2.0 * vars.Cr_k.imag + vars.Al_k.imag)
        )
        vars.f12Al_k.imag = np.sqrt(vars.k2) * (
            vars.dGdCr_k.real
            + pars.kappa * vars.k2 * (2.0 * vars.Cr_k.real + vars.Al_k.real)
        )
        vars.fft_plan_f11Cr()
        vars.fft_plan_f12Cr()
        vars.fft_plan_f11Al()
        vars.fft_plan_f12Al()
        vars.f2Cr_r.real = mCrCr * vars.f11Cr_r.real + mCrAl * vars.f12Cr_r.real
        vars.f2Cr_r.imag = mCrCr * vars.f11Cr_r.imag + mCrAl * vars.f12Cr_r.imag
        vars.f2Al_r.real = mAlAl * vars.f11Al_r.real + mCrAl * vars.f12Al_r.real
        vars.f2Al_r.imag = mAlAl * vars.f11Al_r.imag + mCrAl * vars.f12Al_r.imag
        vars.fft_plan_f2Cr()
        vars.fft_plan_f2Al()
        vars.out_fCr_k.real = (
            -np.sqrt(vars.k2) * vars.f2Cr_k.imag - ballistic * vars.Cr_k.real
        )
        vars.out_fCr_k.imag = (
            np.sqrt(vars.k2) * vars.f2Cr_k.real - ballistic * vars.Cr_k.imag
        )
        vars.out_fAl_k.real = (
            -np.sqrt(vars.k2) * vars.f2Al_k.imag - ballistic * vars.Al_k.real
        )
        vars.out_fAl_k.imag = (
            np.sqrt(vars.k2) * vars.f2Al_k.real - ballistic * vars.Al_k.imag
        )
        vars.fft_plan_outCr()
        vars.fft_plan_outAl()
        if pars.Cr0 > ERROR:
            Cr += dt * vars.out_fCr_r.real
        if pars.Al0 > ERROR:
            Al += dt * vars.out_fAl_r.real
        Fe, Cr, Al = conservation(pars.Cr0, pars.Al0, Cr, Al)
    return Fe, Cr, Al