from .calc_functions import *
from .precipitates import calcPrecipitate2d

R = 8.3144598
a0Al = 4.05e-10
a0Cr = 2.91e-10
a0Fe = 2.86e-10
ERROR = 1.0e-5
dt = 1.0e-2


def calc_diagram_prep(progress, xCr_values, T_values, xAl, N, K, r0):
    if xAl < 1e-5:
        xCr_values, T_values = spinodal(R)
        progress = 100
    if xAl > 1e-5:

        xCr = 0.1 + progress * 0.8 / 100
        progress += 1
        xCr_fin = 0.1 + progress * 0.8 / 100

        flag = 0
        while xCr <= xCr_fin:
            Temp = 1000.0
            while Temp > 500.0:
                pars = params()
                pars.single_graph(Temp, xCr, xAl, N, K)
                k = 0.0
                while k < math.pi:
                    l1 = lambda1(
                        k,
                        pars.kappa,
                        pars.MCrCr,
                        pars.MAlAl,
                        pars.MCrAl,
                        pars.d2fdCr2,
                        pars.d2fdCrdAl,
                        pars.d2fdAl2,
                        pars.G,
                        r0,
                    )
                    l2 = lambda1(
                        k,
                        pars.kappa,
                        pars.MCrCr,
                        pars.MAlAl,
                        pars.MCrAl,
                        pars.d2fdCr2,
                        pars.d2fdCrdAl,
                        pars.d2fdAl2,
                        pars.G,
                        r0,
                    )
                    if l1 > 0 or l2 > 0.0:
                        flag = 1
                        break
                    k += dk
                if flag == 1:
                    break
                Temp -= 1.0
            if flag == 1:
                xCr_values.append(xCr * 100)
                T_values.append(Temp)
                flag = 0
            xCr += 0.01
    return progress, xCr_values, T_values


def calc_diagram_irr(progress, K1, dK, arrays, xCr, xAl, N, r0):
    K_values_1 = arrays[0]
    T_values_1 = arrays[1]
    K_values_2 = arrays[2]
    T_values_2 = arrays[3]
    K_values_3 = arrays[4]
    T_values_3 = arrays[5]
    K_values_4 = arrays[6]
    T_values_4 = arrays[7]
    K = K1
    Kfin = K1 + dK
    dT = 1

    while K < Kfin:
        flag = 0
        Temp = 500.0
        while Temp < 1000.0:
            pars = params()
            pars.single_graph(Temp, xCr, xAl, N, K)
            l1_1k = lambda1(
                dk,
                pars.kappa,
                pars.MCrCr,
                pars.MAlAl,
                pars.MCrAl,
                pars.d2fdCr2,
                pars.d2fdCrdAl,
                pars.d2fdAl2,
                pars.G,
                r0,
            )
            l2_1k = l1_1k

            if l1_1k > 0 or l2_1k > 0:
                K_values_3.append(K)
                T_values_3.append(Temp)
                break
            if flag == 0:
                k = 0.0
                while k < math.pi:
                    l1_1k = lambda1(
                        k,
                        pars.kappa,
                        pars.MCrCr,
                        pars.MAlAl,
                        pars.MCrAl,
                        pars.d2fdCr2,
                        pars.d2fdCrdAl,
                        pars.d2fdAl2,
                        pars.G,
                        r0,
                    )
                    l1_2k = lambda1(
                        k + dk,
                        pars.kappa,
                        pars.MCrCr,
                        pars.MAlAl,
                        pars.MCrAl,
                        pars.d2fdCr2,
                        pars.d2fdCrdAl,
                        pars.d2fdAl2,
                        pars.G,
                        r0,
                    )
                    l2_1k = l1_1k
                    l2_2k = l1_2k
                    if (l1_2k > 0 and l1_1k < 0) or (l2_2k > 0 and l2_1k < 0):
                        K_values_1.append(K)
                        T_values_1.append(Temp)
                        flag = 1
                        break
                    k += dk
            Temp += dT

        flag = 0
        Temp = 1000.0
        while Temp > 500.0:
            pars = params()
            pars.single_graph(Temp, xCr, xAl, N, K)
            l1_1k = lambda1(
                k,
                pars.kappa,
                pars.MCrCr,
                pars.MAlAl,
                pars.MCrAl,
                pars.d2fdCr2,
                pars.d2fdCrdAl,
                pars.d2fdAl2,
                pars.G,
                r0,
            )
            l2_1k = l1_1k
            if l1_1k > 0 or l2_1k > 0:
                K_values_4.append(K)
                T_values_4.append(Temp)
                break
            if flag == 0:
                k = 0.0
                while k < math.pi:
                    l1_1k = lambda1(
                        k,
                        pars.kappa,
                        pars.MCrCr,
                        pars.MAlAl,
                        pars.MCrAl,
                        pars.d2fdCr2,
                        pars.d2fdCrdAl,
                        pars.d2fdAl2,
                        pars.G,
                        r0,
                    )
                    l1_2k = lambda1(
                        k + dk,
                        pars.kappa,
                        pars.MCrCr,
                        pars.MAlAl,
                        pars.MCrAl,
                        pars.d2fdCr2,
                        pars.d2fdCrdAl,
                        pars.d2fdAl2,
                        pars.G,
                        r0,
                    )
                    l2_1k = l1_1k
                    l2_2k = l1_2k
                    if (l1_2k > 0 and l1_1k < 0) or (l2_2k > 0 and l2_1k < 0):
                        K_values_2.append(K)
                        T_values_2.append(Temp)
                        flag = 1
                        break
                    k += dk
            Temp -= dT

        K += dK
        if K > 9 * dK:
            dK = dK * 10

        arrays[0] = K_values_1
        arrays[1] = T_values_1
        arrays[2] = K_values_2
        arrays[3] = T_values_2
        arrays[4] = K_values_3
        arrays[5] = T_values_3
        arrays[6] = K_values_4
        arrays[7] = T_values_4
        progress += 2.8

    return progress, K, dK, arrays


def FeCr_phase_graph(params):
    progress, x, y = 0.0, [], []
    while progress < 100:
        progress, x, y = calc_diagram_prep(
            progress, x, y, params["xAl"] / 100, N=0, K=0, r0=0
        )
        yield progress / 100, -1, None
    yield 1, -100, [(x, y)]


def FeCrAl_phase_graph(params):
    progress, K, dK, arrays = 0.0, 1e-8, 1e-8, [[] for _ in range(8)]
    while progress < 100:
        progress, K, dK, arrays = calc_diagram_irr(
            progress,
            K,
            dK,
            arrays,
            params["xCr"] / 100,
            params["xAl"] / 100,
            params["N"],
            params["r0"],
        )
        yield progress / 100, -1, None
    yield 1, -100, [compile_arrays(arrays)]


def FeCr_phase_model(params):
    Cr0 = params["Cr0"] / 100
    Al0 = params["Al0"] / 100
    T = params["T"]
    max_t = params["max_t"]
    Size = int(params["Size"])

    # if import path to the saved data is specified
    to_import, vtk_path, xyz_path = False, "", ""
    if params.get("vtk_path"):
        to_import = True
        vtk_path = params["vtk_path"]
    if params.get("xyz_path"):
        to_import = True
        xyz_path = params["xyz_path"]

    K, N, r0 = 0, 0, 0

    Rp_list = []
    Np_list = []
    t_list = []
    t = 0.0
    tprogress = max_t / 100
    steps = int(tprogress / dt)
    Fe0 = 1.0 - Cr0 - Al0
    TotSize = int(Size**2)
    ell = a0Al * Al0 + a0Cr * Cr0 + a0Fe * Fe0
    Fe, Cr, Al, pars, vars = initPFT(
        Cr0, Al0, T, N, K, r0, ell, Size, TotSize, to_import, vtk_path, xyz_path
    )
    scaling = pars.scaling
    progress = 0
    while t <= max_t:
        Fe, Cr, Al = calcPFT(Fe, Cr, Al, pars, vars, steps)
        Rp, Np = calcPrecipitate2d(Cr, 0.5, Size, ell)
        t_list.append(t * scaling / 3600)
        Rp_list.append(Rp)
        Np_list.append(Np)
        progress += 1

        yield progress / 100, t, [Cr, Al, (t_list, Rp_list), (t_list, Np_list)]
        t += tprogress


def FeCrAl_phase_model(params):
    Cr0 = params["Cr0"] / 100
    Al0 = params["Al0"] / 100
    T = params["T"]
    K = params["K"]
    N = params["N"]
    r0 = params["r0"]
    max_iter = params["max_dose"]
    Size = int(params["Size"])

    Rp_list = []
    Np_list = []
    t_list = []

    dose = 0.0
    Fe0 = 1.0 - Cr0 - Al0
    TotSize = int(Size**2)
    ell = a0Al * Al0 + a0Cr * Cr0 + a0Fe * Fe0
    Fe, Cr, Al, pars, vars = initPFT(
        Cr0, Al0, T, N, K, r0, ell, Size, TotSize, "", "", 0
    )
    scaling = pars.scaling
    d_dose = dt * K * scaling
    dose_progress = max_iter / 100
    steps = dose_progress / d_dose
    progress = 0
    while dose <= max_iter:
        Fe, Cr, Al = calcPFT(Fe, Cr, Al, pars, vars, steps)
        Rp, Np = calcPrecipitate2d(Cr, 0.5, Size, ell)
        t_list.append(dose)
        Rp_list.append(Rp)
        Np_list.append(Np)
        progress += 1

        yield progress / 100, dose, [Cr, Al, (t_list, Rp_list), (t_list, Np_list)]
        dose += dose_progress


###################### МОДЕЛЮВАННЯ РІВНОВАЖНІ УМОВИ #############################
############### input data ###########
# Cr0 = 0.3
# Al0 = 0.05
# T = 710
# tfin = 1000
# twrite = 200
# Size = 64
# png = 1
# vtk = 0
# xyz = 0
# ############### run calculation ###########
# CalcPFT_prep(Cr0, Al0, T, tfin, twrite, Size, 0, 0, 0, 0, '', '', png, vtk, xyz)
################################################################################


# ###################### МОДЕЛЮВАННЯ ОПРОМІНЕННЯ ###############################
# ############### input data ###########
# Cr0 = 0.3
# Al0 = 0.05
# T = 710
# K = 1E-6
# N = 30
# r0 = 1
# max_dose = 6
# dose_write = 1
# Size = 128
# flag, CrFileName, AlFileName = 0, '', '' # getFlagFilename()
# png = 1
# vtk = 0
# xyz = 0
############### run calculation ###########
# CalcPFT_irr(Cr0, Al0, T, max_dose, dose_write, Size, K, N, r0, flag, CrFileName, AlFileName, png, vtk, xyz)
######################################### #######################################

# Size = 128
# TotSize = Size**2
#
# fnameCr = 'Cr(r)128_t4000_Cr30.0%Al5.0%_T710.xyz'
# xyz = read_data_from_xyz_file(fnameCr, TotSize)
# Cr = xyz[:, 2]
# plt.imshow(Cr.reshape(Size, Size), cmap='coolwarm')
# plt.title('Просторовий розподіл Хрому')
# plt.colorbar()
# plt.show()
#
# fnameAl = 'Al(r)128_t4000_Cr30.0%Al5.0%_T710.xyz'
# xyz = read_data_from_xyz_file(fnameAl, TotSize)
# Al = xyz[:, 2]
# plt.imshow(Al.reshape(Size, Size), cmap='coolwarm')
# plt.title('Просторовий розподіл Алюмінію')
# plt.colorbar()
# plt.show()
#
# fnamePrec = 'Prec128_t_Cr30.0%Al5.0%_T710.dat'
# xyz = read_data_from_xyz_file(fnamePrec, 101)
# t = xyz[:, 0]
# R = xyz[:, 1]
# N = xyz[:, 2]
# title = 'Еволюція середнього розміру преципітатів Хрому'
# plt.plot(t, R)
# plt.xlabel('t [hours]')
# plt.ylabel('<Rp> [nm]')
# plt.xscale("log")
# plt.yscale("log")
# plt.title(title)
# plt.tight_layout()
# plt.show()
#
# title = 'Еволюція густини преципітатів Хрому'
# plt.plot(t, N)
# plt.xlabel('t [hours]')
# plt.ylabel('N x 10^(-27) [m^-3]')
# plt.xscale("log")
# plt.yscale("log")
# plt.title(title)
# plt.tight_layout()
# plt.show()
