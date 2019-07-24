import xraylib


#Generating the Element Tab
file = open("elements.txt","w")
file.write('Element\tEdge\tEdge Energy\n\n')

for i in range(0, 103):
    edge = 'K'
    y =  xraylib.AtomicNumberToSymbol(i)
    if (xraylib.EdgeEnergy(i, xraylib.K_SHELL) >= 4.5):
        if (xraylib.EdgeEnergy(i, xraylib.K_SHELL) <= 25):
            file.write(y + '\t' + edge + '\t'+ str(round(xraylib.EdgeEnergy(i, xraylib.K_SHELL)*1000,1)) + '\n')

    if (xraylib.EdgeEnergy(i, xraylib.L1_SHELL) >= 4.5):
        if (xraylib.EdgeEnergy(i, xraylib.L1_SHELL) <= 25):
            file.write(y + '\t' + 'L1' + '\t' + str(round(xraylib.EdgeEnergy(i, xraylib.L1_SHELL)*1000, 1)) + '\n')

    if (xraylib.EdgeEnergy(i, xraylib.L2_SHELL) >= 4.5):
        if (xraylib.EdgeEnergy(i, xraylib.L2_SHELL) <= 25):
            file.write(y + '\t' + 'L2' + '\t' + str(round(xraylib.EdgeEnergy(i, xraylib.L2_SHELL)*1000,1)) + '\n')

    if (xraylib.EdgeEnergy(i, xraylib.L3_SHELL) >= 4.5):
        if (xraylib.EdgeEnergy(i, xraylib.L3_SHELL) <= 25):
            file.write(y + '\t' + 'L3' + '\t' + str(round(xraylib.EdgeEnergy(i, xraylib.L3_SHELL)*1000,1)) + '\n')
file.close()


#Generating the Edge Tab
file = open("edges.txt","w")
file.write('Element\tEdge\tEdge Energy\n\n')

for i in range(0, 103):
    edge = 'K'
    y =  xraylib.AtomicNumberToSymbol(i)
    if (xraylib.EdgeEnergy(i, xraylib.K_SHELL) >= 4.5):
        if (xraylib.EdgeEnergy(i, xraylib.K_SHELL) <= 25):
            file.write(y + '\t' + edge + '\t'+ str(round(xraylib.EdgeEnergy(i, xraylib.K_SHELL)*1000,1)) + '\n')

for i in range(0, 103):
    y = xraylib.AtomicNumberToSymbol(i)
    if (xraylib.EdgeEnergy(i, xraylib.L1_SHELL) >= 4.5):
        if (xraylib.EdgeEnergy(i, xraylib.L1_SHELL) <= 25):
            file.write(y + '\t' + 'L1' + '\t' + str(round(xraylib.EdgeEnergy(i, xraylib.L1_SHELL)*1000, 1)) + '\n')

for i in range(0, 103):
    y = xraylib.AtomicNumberToSymbol(i)
    if (xraylib.EdgeEnergy(i, xraylib.L2_SHELL) >= 4.5):
        if (xraylib.EdgeEnergy(i, xraylib.L2_SHELL) <= 25):
            file.write(y + '\t' + 'L2' + '\t' + str(round(xraylib.EdgeEnergy(i, xraylib.L2_SHELL)*1000,1)) + '\n')

for i in range(0, 103):
    y = xraylib.AtomicNumberToSymbol(i)
    if (xraylib.EdgeEnergy(i, xraylib.L3_SHELL) >= 4.5):
        if (xraylib.EdgeEnergy(i, xraylib.L3_SHELL) <= 25):
            file.write(y + '\t' + 'L3' + '\t' + str(round(xraylib.EdgeEnergy(i, xraylib.L3_SHELL)*1000,1)) + '\n')
file.close()