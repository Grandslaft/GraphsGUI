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


def calc_diagram_prep(xAl, N=0, K=0, r0=0):
    xCr_values = []
    T_values = []
    if xAl < 1E-5:
        xCr_values, T_values = spinodal(R)
    if xAl > 1E-5:
        flag = 0
        xCr = 0.1
        while xCr <= 0.9:
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
    return xCr_values, T_values


# # параметри для читання з форми
# xAl = 0.0

# # Розрахунок діанрами
# x, y = calc_diagram_prep(xAl, N=0, K=0, r0=0)

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

# # при натисканні на кнопку EXPORT треба і рисунок зберегти і дані (x, y) в текстовий файл