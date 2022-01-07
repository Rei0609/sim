import numpy as np
import matplotlib.pyplot as plt
import pyPLUTO as pp
import norm
import physconst as pc

nm = norm.PhysNorm(x=pc.kpc, dens=pc.amu*0.6063, v=pc.c, curr=1, temp=pc.amu*pc.c*pc.c/pc.kboltz)

def compute_ref_gradient(u, eps=0.01):
    d2 = np.diff(u, 2, prepend=u[0], append=u[-1])
    fd = np.diff(u, append=u[-1])
    bd = np.diff(u, prepend=u[0])
    ur = np.r_[u[1:], u[-1]]
    ul = np.r_[u[0], u[:-1]]
    uref = np.abs(ur) + 2*np.abs(u) + np.abs(ul)

    x = d2*d2 / (np.abs(fd)*np.abs(fd) + np.abs(bd)*np.abs(bd) + eps*uref)
    x = np.sqrt(x)
    return x


def plot_snapshot(i, data_dir):

    if data_dir[-1] != '/':
        data_dir += '/'

    data = pp.pload.pload(i, datatype='hdf5', level=4,  w_dir=data_dir)

    fig, ax1 = plt.subplots()
    ax2 = ax1.twinx()
    ax3 = ax1.twinx()
    energy_density = 0.5 * data.rho * data.vx1 * data.vx1 + 1.5 * data.prs
    xi = compute_ref_gradient(energy_density)


    ax1.plot(data.x1, data.rho, '.b-', label='density')
    ax1.plot(data.x1, data.prs, '.y-', label='pressure')
    ax1.plot(data.x1, energy_density, '.m-', label='energy density')
    ax2.plot(data.x1, data.vx1, '.r-', label='velocity')
    ax3.plot(data.x1, xi, '.k-', label='xi')

    handler1, label1 = ax1.get_legend_handles_labels()
    handler2, label2 = ax2.get_legend_handles_labels()
    handler3, label3 = ax3.get_legend_handles_labels()

    ax1.legend(handler1 + handler2 + handler3, label1 + label2 + handler3)

    ax1.set_ylim((1.e-10, 1.e2))
    ax1.set_xscale("log")
    ax1.set_yscale("log")


    ax2.set_ylim((-0.3, 0.3))
    ax2.set_xscale("log")

    ax3.set_ylim((0., 1.))
    ax3.set_xscale("log")

    ax3.spines["right"].set_position(("axes", 1.05))

    plt.xlabel('x')
    plt.ylabel('value')

    ax = plt.gca()

    plt.text(0.04, 0.93, f'{data.SimTime*nm.t/pc.kyr:>5.1f} kyr', transform=ax.transAxes)

    plt.savefig(f'{data_dir}vars-{i:0>4d}.png', dpi=100)

    plt.close(plt.gcf())

