import time
import os
import sys
import SeqPyPlotLib.DataContainer as DataContainer

from SeqPyPlotLib.DataPlotter import MainDataPlotter
from SeqPyPlotLib.DataAnalyzer import DataAnalyzer
from SeqPyPlotLib.ArgumentCollector import Args

print '\n' + '{:^68}'.format(
    '***SeqPyPlot v0.2***'), '\nA tool for helping you analyze pilot data (data without replicates).\n'

if len(sys.argv) == 0:
    print "Set options."
    sys.exit()

start = float(time.time())
print '\n\n'
# Collect args
argz = Args()
argz.make_logs()
args = argz.args


# if files aren't provided properly
if args.raw_data is None and args.plot_data is None:
    print("\nProvide either a (raw_data file) or (plot_data file)\n")
    os.system('python SeqPyPlot.py -h')
    sys.exit()

# if only raw data is supplied

if args.raw_data is not None:
    FullContainer = DataContainer.DataContainer(args)  # object containing parsed raw_data
    Analyzer = DataAnalyzer(args, FullContainer)  # object used for filtering data and writing out filtered data files

    Analyzer.seqpyfilter()  # object containing analyzed data

    DataPrinter = DataContainer.DataPrinter(args, FullContainer, Analyzer)
    DataPrinter.write_plot_data()
    DataPrinter.write_de_results()
    DataPrinter.write_filtered_data()

    if args.ercc:
        DataPrinter.write_ercc_data()

    if args.tally:
        Plot_Builder = MainDataPlotter(args, Analyzer, None)  # object used for generating plots
        if args.scatter or args.all or args.plots:
            print "Building Scatter Plots for un-flagged data...\n"
            Plot_Builder.make_scatter_plots()
            print "Building Scatter Plots for flagged data...\n"
            Plot_Builder.make_scatter_plots(flagged=True)
        if args.all or args.plots and args.num == 2:
            print "Building Bland-Altman Plots...\n"
            Plot_Builder.bland_altman_plot()
        if args.bar or args.all or args.plots:
            print "Building Bar Plots...\n"
            Plot_Builder.de_bar('black')
        if args.tally or args.all:
            print "Performing Tallys...\n"
            Plot_Builder.plot_tally()
        if args.histo or args.all or args.plots:
            print "Plotting Histograms...\n"
            Plot_Builder.plot_histograms()
            print "Building Scatter Plots for log2fold data...\n"
            Plot_Builder.collective_log_plot()
            Plot_Builder.single_log_plots()

        Analyzer.print_analyzer_results()

    print(
        "Data analyzed, select genes for plotting from {}_filtered.txt and rerun the program with plot data.".format(
            args.out))
    sys.exit()

elif args.plot_data is not None:
    if args.gene_list is not None:  # if plot data and gene list is provided

        # Create Output files
        DataContainer.PrepareOutputDirectory.make_folder(args.out)

        FullContainer = DataContainer.DataContainer(args)  # object containing parsed premade plot data
        if args.de_results is not None:  # if no results are provided, calculate them and then load them
            FullContainer.load_results()
            Analyzer = DataAnalyzer(args, FullContainer)
        else:
            Analyzer = DataAnalyzer(args, FullContainer)

        Analyzer.seqpyfilter()

        assert FullContainer.analyzed

        # Ready, get set....
        FigureList = DataContainer.MakeFigureList(args)  # object containing gene list for plotting and other attributes
        Plot_Builder = MainDataPlotter(args, Analyzer, FigureList)  # object used for generating plots
        Plot_Builder.plot_figures()

        if args.report:
            DataPrinter = DataContainer.DataPrinter(args, FullContainer, Analyzer)
            DataPrinter.write_plot_data()
            DataPrinter.write_de_results()
            DataPrinter.write_filtered_data()

        if args.scatter or args.all or args.plots:
            print "Building Scatter Plots for un-flagged data...\n"
            Plot_Builder.make_scatter_plots()
            print "Building Scatter Plots for flagged data...\n"
            Plot_Builder.make_scatter_plots(flagged=True)

        if args.all or args.plots and args.num == 2:
            print "Building Bland-Altman Plots...\n"
            Plot_Builder.bland_altman_plot()
        if args.bar or args.all or args.plots:
            print "Building Bar Plots...\n"
            Plot_Builder.de_bar('black')
        if args.tally or args.all:
            print "Performing Tallys...\n"
            Plot_Builder.plot_tally()
        if args.histo or args.all or args.plots:
            print "Plotting Histograms...\n"
            Plot_Builder.plot_histograms()
            print "Building Scatter Plots for log2fold data...\n"
            Plot_Builder.collective_log_plot()
            Plot_Builder.single_log_plots()
        print "Building Bland-Gradie Plots...\n"
        Plot_Builder.bland_gradie_plot()
        Plot_Builder.bland_gradie_plot(flagged=True)
        Analyzer.print_analyzer_results()

    else:  # IF plot data is provided without a genelist
        # perform the DE analysis using processed plot data
        FullContainer = DataContainer.DataContainer(args)
        Analyzer = DataAnalyzer(args, FullContainer)
        Analyzer.seqpyfilter()
        Plot_Builder = MainDataPlotter(args, Analyzer, None)

        DataPrinter = DataContainer.DataPrinter(args, FullContainer, Analyzer)
        DataPrinter.write_de_results()
        DataPrinter.write_filtered_data()

        Analyzer.print_analyzer_results()

        if args.scatter or args.all or args.plots:
            print "Building Scatter Plots for un-flagged data...\n"
            Plot_Builder.make_scatter_plots()
            print "Building Scatter Plots for flagged data...\n"
            Plot_Builder.make_scatter_plots(flagged=True)
        if args.all or args.plots and args.num == 2:
            print "Building Bland-Altman Plots...\n"
            Plot_Builder.bland_altman_plot()
        if args.bar or args.all or args.plots:
            print "Building Bar Plots...\n"
            Plot_Builder.de_bar('black')
        if args.tally or args.all:
            print "Performing Tallys...\n"
            Plot_Builder.plot_tally()
        if args.histo or args.all or args.plots:
            print "Plotting Histograms...\n"
            Plot_Builder.plot_histograms()
            print "Building Scatter Plots for collecticue log2fold data...\n"
            Plot_Builder.collective_log_plot()
            Plot_Builder.single_log_plots()
        if args.blandg or args.all or args.plots:
            print "Building Bland-Gradie Plots...\n"
            Plot_Builder.bland_gradie_plot()
            Plot_Builder.bland_gradie_plot(flagged=True)
        print "Finished."
        sys.exit()
else:
    os.system('python SeqPyPlot.py -h')
    sys.exit()

end = float(time.time())
print("Total Run Time: {}".format((end - start) / 60.0))

