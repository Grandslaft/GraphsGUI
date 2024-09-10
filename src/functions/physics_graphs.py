import numpy as np
import matplotlib.pyplot as plt
import math

R = 8.3144598
ell = 2.86E-10
dk = math.pi/1000


def omega(k, G, r0):
    w = G*(1.0 - 1.0/(1.0 + k*k*r0*r0))
    return w


def parameters(T, xCr, xAl, N, K):
    xFe = 1 - xCr - xAl
    G_Fe_Ref = 1225.7 + 124.134*T - 23.5143*T*math.log(T) - 0.439752E-2*T*T - 0.589269E-7*T*T*T + 77358.5/T
    G_Cr_Ref = - 8856.94 + 157.48*T - 26.908*T*math.log(T) + 0.189435E-2*T*T - 0.147721E-5*T*T*T + 139250.0/T
    G_Al_Ref = - 1193.24 + 218.235446*T - 38.5844296*T*math.log(T) + 0.18531982E-1*T*T - 0.576227E-5*T*T*T + 74092.0/T
    L0_FeCr = 20500 - 9.68*T
    L0_CrAl = - 54900 + 10.0*T
    L0_FeAl = -122452.9 + 31.6455*T
    kappa = L0_FeCr/(6.0*R*T)
    DFe = 0.28E-3*math.exp(-251000/(R*T))
    DCr = 0.37E-2*math.exp(-267000/(R*T))
    DAl = 0.52E-3*math.exp(-246000/(R*T))
    MFe = DFe/DAl
    MCr = DCr/DAl
    MAl = DAl/DAl
    MCrCr = xCr*(((1.0 - xCr)*(1.0 - xCr))*MCr + xCr*xAl*MAl + xCr*xFe*MFe)
    MAlAl = xAl*(((1.0 - xAl)*(1.0 - xAl))*MAl + xCr*xAl*MCr + xAl*xFe*MFe)
    MCrAl = xCr*xAl*(xFe*MFe - (1.0 - xCr)*MCr - (1.0 - xAl)*MAl)
    d2fdCr2 = (-2.0*L0_FeCr + R*T*(1.0/(1.0 - xCr - xAl) + 1.0/xCr))/(R*T)
    d2fdCrdAl = (-L0_FeCr + L0_CrAl - L0_FeAl + R*T/(1.0 - xCr - xAl))/(R*T)
    d2fdAl2 = (-2.0*L0_FeAl + R*T*(1.0/(1.0 - xCr - xAl) + 1.0/xAl))/(R*T)
    G = N*K*ell*ell/DAl
    return kappa, MCrCr, MAlAl, MCrAl, d2fdCr2, d2fdCrdAl, d2fdAl2, G


def A11(k, kappa, MCrCr, MAlAl, MCrAl, d2fdCr2, d2fdCrdAl, d2fdAl2, G, r0):
    a = -k*k*(MCrCr*(2.0*k*k*kappa + d2fdCr2) + MCrAl*(k*k*kappa + d2fdCrdAl)) - omega(k, G, r0)
    return a


def A12(k, kappa, MCrCr, MAlAl, MCrAl, d2fdCr2, d2fdCrdAl, d2fdAl2, G, r0):
    a = -k*k*(MCrCr*(k*k*kappa + d2fdCrdAl) + MCrAl*(2.0*k*k*kappa + d2fdAl2))
    return a


def A21(k, kappa, MCrCr, MAlAl, MCrAl, d2fdCr2, d2fdCrdAl, d2fdAl2, G, r0):
    a = -k*k*(MAlAl*(k*k*kappa + d2fdCrdAl) + MCrAl*(2.0*k*k*kappa + d2fdCr2))
    return a


def A22(k, kappa, MCrCr, MAlAl, MCrAl, d2fdCr2, d2fdCrdAl, d2fdAl2, G, r0):
    a = -k*k*(MAlAl*(2.0*k*k*kappa + d2fdAl2) + MCrAl*(k*k*kappa + d2fdCrdAl)) - omega(k, G, r0)
    return a


def lambda1(k, kappa, MCrCr, MAlAl, MCrAl, d2fdCr2, d2fdCrdAl, d2fdAl2, G, r0):
    a11 = A11(k, kappa, MCrCr, MAlAl, MCrAl, d2fdCr2, d2fdCrdAl, d2fdAl2, G, r0)
    a12 = A12(k, kappa, MCrCr, MAlAl, MCrAl, d2fdCr2, d2fdCrdAl, d2fdAl2, G, r0)
    a21 = A21(k, kappa, MCrCr, MAlAl, MCrAl, d2fdCr2, d2fdCrdAl, d2fdAl2, G, r0)
    a22 = A22(k, kappa, MCrCr, MAlAl, MCrAl, d2fdCr2, d2fdCrdAl, d2fdAl2, G, r0)
    A = 1.0
    B = - (a11 + a22)
    C = a11*a22 - a12*a21
    D = B*B - 4.0*A*C
    if D >= 0.0:
        l = (-B + math.sqrt(D))/(2.0*A)
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
    C = a11*a22 - a12*a21
    D = B*B - 4.0*A*C
    if D >= 0.0:
        l = (-B - math.sqrt(D))/(2.0*A)
    else:
        l = 0.0
    return l


def spinodal(R):
    xcr = np.linspace(10, 90, 800)
    temp = []
    x = 0.0
    for i in range(len(xcr)):
        x = xcr[i]/100
        y = -1.025000E6*x*(-1.0+x)/(-484.0*x*x+25.0*R+484.0*x)
        temp.append(y)
    return xcr, temp


def init_prep():
    xCr_values = []
    T_values = []
    progress = 0.0
    return progress, xCr_values, T_values



def calc_diagram_prep(progress, xCr_values, T_values, xAl, N, K, r0):
    if xAl < 1E-5:
        xCr_values, T_values = spinodal(R)
        progress = 100
    if xAl > 1E-5:

        xCr = 0.1 + progress * 0.8 / 100
        progress += 1
        xCr_fin = 0.1 + progress * 0.8 / 100

        flag = 0
        while xCr <= xCr_fin:
            Temp = 1000.0
            while Temp > 500.0:
                kappa, MCrCr, MAlAl, MCrAl, d2fdCr2, d2fdCrdAl, d2fdAl2, G = parameters(Temp, xCr, xAl, N, K)
                k = 0.0
                while k < math.pi:
                    l1 = lambda1(k, kappa, MCrCr, MAlAl, MCrAl, d2fdCr2, d2fdCrdAl, d2fdAl2, G, r0)
                    l2 = lambda1(k, kappa, MCrCr, MAlAl, MCrAl, d2fdCr2, d2fdCrdAl, d2fdAl2, G, r0)
                    if l1 > 0 or l2 > 0.0:
                        flag = 1
                        break
                    k += dk
                if flag == 1: break
                Temp -= 1.0
            if flag == 1:
                xCr_values.append(xCr*100)
                T_values.append(Temp)
                flag = 0
            xCr += 0.01
    return progress, xCr_values, T_values


def init_irr():
    arrays = []
    K_values_1 = []
    arrays.append(K_values_1)
    T_values_1 = []
    arrays.append(T_values_1)
    K_values_2 = []
    arrays.append(K_values_2)
    T_values_2 = []
    arrays.append(T_values_2)
    K_values_3 = []
    arrays.append(K_values_3)
    T_values_3 = []
    arrays.append(T_values_3)
    K_values_4 = []
    arrays.append(K_values_4)
    T_values_4 = []
    arrays.append(T_values_4)
    progress = 0.0
    K = 1E-8
    dK = 1E-8
    return progress, K, dK, arrays


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
            kappa, MCrCr, MAlAl, MCrAl, d2fdCr2, d2fdCrdAl, d2fdAl2, G = parameters(Temp, xCr, xAl, N, K)
            l1_1k = lambda1(dk, kappa, MCrCr, MAlAl, MCrAl, d2fdCr2, d2fdCrdAl, d2fdAl2, G, r0)
            l2_1k = lambda1(dk, kappa, MCrCr, MAlAl, MCrAl, d2fdCr2, d2fdCrdAl, d2fdAl2, G, r0)
            if l1_1k > 0 or l2_1k > 0:
                K_values_3.append(K)
                T_values_3.append(Temp)
                break
            if flag == 0:
                k = 0.0
                while k < math.pi:
                    l1_1k = lambda1(k, kappa, MCrCr, MAlAl, MCrAl, d2fdCr2, d2fdCrdAl, d2fdAl2, G, r0)
                    l1_2k = lambda1(k + dk, kappa, MCrCr, MAlAl, MCrAl, d2fdCr2, d2fdCrdAl, d2fdAl2, G, r0)
                    l2_1k = lambda1(k, kappa, MCrCr, MAlAl, MCrAl, d2fdCr2, d2fdCrdAl, d2fdAl2, G, r0)
                    l2_2k = lambda1(k + dk, kappa, MCrCr, MAlAl, MCrAl, d2fdCr2, d2fdCrdAl, d2fdAl2, G, r0)
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
            kappa, MCrCr, MAlAl, MCrAl, d2fdCr2, d2fdCrdAl, d2fdAl2, G = parameters(Temp, xCr, xAl, N, K)
            l1_1k = lambda1(dk, kappa, MCrCr, MAlAl, MCrAl, d2fdCr2, d2fdCrdAl, d2fdAl2, G, r0)
            l2_1k = lambda1(dk, kappa, MCrCr, MAlAl, MCrAl, d2fdCr2, d2fdCrdAl, d2fdAl2, G, r0)
            if l1_1k > 0 or l2_1k > 0:
                K_values_4.append(K)
                T_values_4.append(Temp)
                break
            if flag == 0:
                k = 0.0
                while k < math.pi:
                    l1_1k = lambda1(k, kappa, MCrCr, MAlAl, MCrAl, d2fdCr2, d2fdCrdAl, d2fdAl2, G, r0)
                    l1_2k = lambda1(k + dk, kappa, MCrCr, MAlAl, MCrAl, d2fdCr2, d2fdCrdAl, d2fdAl2, G, r0)
                    l2_1k = lambda1(k, kappa, MCrCr, MAlAl, MCrAl, d2fdCr2, d2fdCrdAl, d2fdAl2, G, r0)
                    l2_2k = lambda1(k + dk, kappa, MCrCr, MAlAl, MCrAl, d2fdCr2, d2fdCrdAl, d2fdAl2, G, r0)
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


def write_data_to_file(fname, x, y):
    f = open(fname, "w")
    for i in range(len(x)):
        line = str(x[i]) + '\t' + str(y[i]) + '\n'
        f.write(line)
    f.close()
    
def FeCr_phase_graph(**kwargs):
    progress, x, y = init_prep()
    while progress < 100:
        progress, x, y = calc_diagram_prep(progress, x, y, kwargs['xAl'], N=0, K=0, r0=0)
        yield progress/100, 'progress'
    yield x, y

def FeCrAl_phase_graph(**kwargs):
    progress, K, dK, arrays = init_irr()
    while progress < 100:
        progress, K, dK, arrays = calc_diagram_irr(progress, K, dK, arrays, kwargs['xCr'], kwargs['xAl'], kwargs['N'],  kwargs['r0'])
        yield progress/100, 'progress'
    yield compile_arrays(arrays)
            
############################   БЛОК РІВНОВАЖНИХ УМОВ   #####################################

# # РІВНОВАЖНІ УМОВИ
# # параметри для читання з форми
# xAl = 0.0
# progress, x, y = init_prep()
# # Розрахунок діанрами
# while progress < 100:
#     progress, x, y = calc_diagram_prep(progress, x, y, xAl, N=0, K=0, r0=0)
#     return progress, x, y
# # Запис даних у файл
# fname = 'T(xCr)_Al' + str(xAl*100) + '%.dat'
# write_data_to_file(fname, x, y)
# # Виведення на екран
# if xAl < 1E-5:
#     title = 'Фазова діаграма для сплаву Fe-Cr'
# else:
#     title = 'Фазова діаграма для сплаву Fe-Cr-'+str(xAl*100)+'Al'
# plt.plot(x,y)
# plt.xlabel('xCr [%]')
# plt.ylabel('T [K]')
# plt.title(title)
# plt.show()

#############################   БЛОК ОПРОМІНЕННЯ   ###############################################

# # ОПРОМІНЕННЯ
# # параметри для читання з форми
# xCr = 0.3
# xAl = 0.05
# N = 30
# r0 = 4
# progress, K, dK, arrays = init_irr()
# # Розрахунок діанрами
# while progress < 100:
#     progress, K, dK, arrays = calc_diagram_irr(progress, K, dK, arrays, xCr, xAl, N, r0)
#     print(progress)
# x1, y1, x2, y2 = compile_arrays(arrays)
# # Запис даних у файл
# fname = 'K(T)_Cr' + str(xCr*100) + '%Al' + str(xAl*100) + '%_N' + str(N) + '_r0' + str(r0) + '_line1.dat'
# write_data_to_file(fname, x1, y1)
# fname = 'K(T)_Cr' + str(xCr*100) + '%Al' + str(xAl*100) + '%_N' + str(N) + '_r0' + str(r0) + '_line2.dat'
# write_data_to_file(fname, x2, y2)
# # Виведення на екран
# title = 'Фазова діаграма для сплаву Fe-' +str(xCr*100)+ '%Cr-'+str(xAl*100)+'%Al'
# plt.plot(x1,y1)
# plt.plot(x2,y2)
# plt.xlabel('T [K]')
# plt.ylabel('K [dpa/sec]')
# plt.yscale("log")
# plt.title(title)
# plt.show()
