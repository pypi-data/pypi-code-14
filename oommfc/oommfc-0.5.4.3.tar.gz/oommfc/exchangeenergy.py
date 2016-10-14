import oommfc as oc
import discretisedfield as df

mesh = oc.Mesh((0, 0, 0), (100e-9, 100e-9, 10e-9), (5e-9, 5e-9, 5e-9))
system = oc.System(name="mysystem")

system.mesh = mesh
system.hamiltonian = oc.Exchange(A=1.2e-11) + oc.Zeeman(H=(1e6, 1e6, 0))
system.m = df.Field(mesh, value=(0, 0, 1), normalisedto=8e6)

md = oc.MinDriver()
md.drive(system)

print(system.hamiltonian.exchange.energy())
