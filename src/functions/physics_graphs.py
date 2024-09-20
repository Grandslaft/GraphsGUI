import os
import numpy as np
import matplotlib.pyplot as plt

from .calc_functions import *

R = 8.3144598
a0Al = 4.05E-10
a0Cr = 2.91E-10
a0Fe = 2.86E-10
ERROR = 1.0E-5
dt = 1.0E-2

def saveImageFile(fname, field, Size):
    plt.imsave(fname, field.reshape(Size, Size), cmap='coolwarm')


def write_data_to_xyz_file(fname, x, size):
    f = open(fname, "w")
    for i in range(size):
        for j in range(size):
            line = str(i) + '\t' + str(j) + '\t' + str(x.reshape(size, size)[i, j]) + '\n'
            f.write(line)
    f.close()

def write_data_to_vtk_file(fname, x, size):
    f = open(fname, "w")
    f.write('# vtk DataFile Version 2.0')
    f.write('\n')
    f.write('Structured Grid 2D Dataset')
    f.write('\n')
    f.write('ASCII')
    f.write('\n')
    f.write('DATASET STRUCTURED_GRID')
    f.write('\n')
    line = 'DIMENSIONS ' + str(size) + ' ' + str(size) + ' ' + str(1) + '\n'
    f.write(line)
    line = 'POINTS ' + str(size * size * 1) + ' float \n'
    f.write(line)
    for i in range(size):
        for j in range(size):
            line = str(i + 1) + '\t' + str(j + 1) + '\t' + str(0) + '\n'
            f.write(line)
    line = 'POINT_DATA ' + str(size *size * 1) + '\n'
    f.write(line)
    f.write('SCALARS colors float\n')
    f.write('LOOKUP_TABLE default\n')
    for i in range(size*size):
        f.write(str(x[i]))
        f.write('\n')
    f.close()


def make_file_name_prep(size, cr0, al0, T, time, ext, xname):
    fname = xname + str(size) + '_t' + str(time) + '_Cr' + str(cr0 * 100) + '%Al' + str(al0 * 100) + '%_T' + str(
        T) + '.' + ext
    return fname


def make_file_name_irr(size, cr0, al0, T, N, K, r0, time, ext, xname):
    fname = xname + str(size) + '_t' + str(time) + '_Cr' + str(cr0 * 100) + '%Al' + str(al0 * 100) + '%_T' + str(
        T) + '_K' + str(K*1E6) + 'E-6_N' + str(N) + '_r0' + str(r0) + '.' + ext
    return fname


def save_precipitates(stage, Size, Cr0, Al0, T, N, K, r0, t, r, n):
    if stage == 1:
        fname = make_file_name_prep(Size, Cr0, Al0, T, '', 'dat', 'Prec')
        colxname = 'Time [hours]'
    else:
        fname = make_file_name_irr(Size, Cr0, Al0, T, N, K, r0, '', 'dat', 'Prec')
        colxname = 'Dose [dpa]'
    f = open(fname, "w")
    line = colxname + '\t<Rp> [nm]\tNp x 1E-27 [m^3]\n'
    f.write(line)
    for i in range(len(t)):
        line = str(t[i]) + '\t' + str(r[i]) + '\t' + str(n[i]) + '\n'
        f.write(line)
    f.close()


def save_data_prep(Size, Cr0, Al0, T, twrite, Cr, Al, png, vtk, xyz):
    if png == 1:
        fname = make_file_name_prep(Size, Cr0, Al0, T, twrite, 'png', 'Cr(r)')
        saveImageFile(fname, Cr, Size)
        fname = make_file_name_prep(Size, Cr0, Al0, T, twrite, 'png', 'Al(r)')
        saveImageFile(fname, Al, Size)
    if xyz == 1:
        fname = make_file_name_prep(Size, Cr0, Al0, T, twrite, 'xyz', 'Cr(r)')
        write_data_to_xyz_file(fname, Cr, Size)
        fname = make_file_name_prep(Size, Cr0, Al0, T, twrite, 'xyz', 'Al(r)')
        write_data_to_xyz_file(fname, Al, Size)
    if vtk == 1:
        fname = make_file_name_prep(Size, Cr0, Al0, T, twrite, 'vtk', 'Cr(r)')
        write_data_to_vtk_file(fname, Cr, Size)
        fname = make_file_name_prep(Size, Cr0, Al0, T, twrite, 'vtk', 'Al(r)')
        write_data_to_vtk_file(fname, Al, Size)


def save_data_irr(Size, Cr0, Al0, T, dose_write, N, K, r0, Cr, Al, png, vtk, xyz):
    if png == 1:
        fname = make_file_name_irr(Size, Cr0, Al0, T, N, K, r0, dose_write, 'png', 'Cr(r)')
        saveImageFile(fname, Cr, Size)
        fname = make_file_name_irr(Size, Cr0, Al0, T, N, K, r0, dose_write, 'png', 'Al(r)')
        saveImageFile(fname, Al, Size)
    if xyz == 1:
        fname = make_file_name_irr(Size, Cr0, Al0, T, N, K, r0, dose_write, 'xyz', 'Cr(r)')
        write_data_to_xyz_file(fname, Cr, Size)
        fname = make_file_name_irr(Size, Cr0, Al0, T, N, K, r0, dose_write, 'xyz', 'Al(r)')
        write_data_to_xyz_file(fname, Al, Size)
    if vtk == 1:
        fname = make_file_name_irr(Size, Cr0, Al0, T, N, K, r0, dose_write, 'vtk', 'Cr(r)')
        write_data_to_vtk_file(fname, Cr, Size)
        fname = make_file_name_irr(Size, Cr0, Al0, T, N, K, r0, dose_write, 'vtk', 'Al(r)')
        write_data_to_vtk_file(fname, Al, Size)


def getFlagFilename():
    # Якщо опромінення тпердого розчину
    flag = 0
    CrFileName = ''
    AlFileName = ''
    # Якщо опромінення відпаленого сплвіу
    flag = 1
    CrFileName = 'CrFileName.xyz'
    AlFileName = 'AlFileName.xyz'
    return flag, CrFileName, AlFileName


def mkFolderPrep(size, cr0, al0, T):
    folder = 'M' + str(size) + '_Cr' + str(cr0 * 100) + '%Al' + str(al0 * 100) + '%_T' + str(T)
    return folder

def FeCr_phase_graph(params):
    Cr0 = params['Cr0']
    Al0 = params['Al0']
    T = params['T']
    max_t = params['max_t']
    Size = int(params['Size'])
    
    K, N, r0 = 0, 0, 0
    
    Rp_list = []
    Np_list = []
    t_list = []
    t = 0.0
    tprogress = max_t / 100
    steps = int(tprogress / dt)
    Fe0 = 1.0 - Cr0 - Al0
    TotSize = int(Size ** 2)
    ell = a0Al * Al0 + a0Cr * Cr0 + a0Fe * Fe0
    Fe, Cr, Al, pars, vars = initPFT(Cr0, Al0, T, N, K, r0, ell, Size, TotSize, '', '', 0)
    scaling = pars[16]
    progress = 0
    while t <= max_t:
        Fe, Cr, Al = calcPFT(Fe, Cr, Al, pars, vars, steps)
        Rp, Np = calcPrecipitate2d(Cr, 0.5, Size, ell)
        t_list.append(t * scaling / 3600)
        Rp_list.append(Rp)
        Np_list.append(Np)
        progress += 1
        
        yield progress/100, t, [Cr, Al, (t_list, Rp_list), (t_list, Np_list)]
        t += tprogress

def FeCrAl_phase_graph(params):
    Cr0 = params['Cr0']
    Al0 = params['Al0']
    T = params['T']
    K = params['K']
    N = params['N']
    r0 = params['r0']
    max_iter = params['max_dose']
    Size = int(params['Size'])
    
    Rp_list = []
    Np_list = []
    t_list = []

    dose = 0.0
    Fe0 = 1.0 - Cr0 - Al0
    TotSize = int(Size**2)
    ell = a0Al * Al0 + a0Cr * Cr0 + a0Fe * Fe0
    Fe, Cr, Al, pars, vars = initPFT(Cr0, Al0, T, N, K, r0, ell, Size, TotSize, '', '', 0)
    scaling = pars[16]
    d_dose = dt * K * scaling
    dose_progress = max_iter / 100
    steps = int(dose_progress/d_dose)
    progress = 0
    while dose <= max_iter:
        Fe, Cr, Al = calcPFT(Fe, Cr, Al, pars, vars, steps)
        Rp, Np = calcPrecipitate2d(Cr, 0.5, Size, ell)
        t_list.append(dose)
        Rp_list.append(Rp)
        Np_list.append(Np)
        progress += 1
                
        yield progress/100, dose, [Cr, Al, (t_list, Rp_list), (t_list, Np_list)]
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