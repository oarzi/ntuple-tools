from __future__ import division
import GeoUtils

from ROOT import TCanvas, TH2I, TGraph, TMultiGraph
from array import array


def print_hec(plane):
    mg = TMultiGraph()


def main():
    # print "reade ntuple for file ", sys.arg[1]
    # print "read geometry from file ", sys.argv[2]
    # ntuple = HGCalNtuple(sys.argv[1])
    # planes = GeoUtils.read_planes(sys.argv[2])

    # for plane in planes:
    #  print_geo(ntuple, plane)
    print "read geometry from file: ", "fullgeometry_.txt"

    print "reading planes"
    planes = GeoUtils.read_planes("fullgeometry_.txt")

    c = TCanvas()

    mg = TMultiGraph()

    cells = planes[0].cells

    for cell in cells:
        x = array("d", cell.coordinates.vertices[:, 0])
        x.append(x[0])

        y = array("d", cell.coordinates.vertices[:, 1])
        y.append(y[0])

        gi = TGraph(len(x), x, y)
        gi.SetMarkerStyle(1)

        mg.Add(gi, "AL")

    # mg.Draw("AL")
    mg.Draw("A")
    c.Draw()
    c.SaveAs("hex0.png")


if __name__ == '__main__':
    main()
